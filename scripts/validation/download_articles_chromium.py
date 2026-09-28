#!/usr/bin/env python3
"""
Bulk-download article PDFs listed in a CSV, using Chromium (Playwright).

Why Chromium: the browser keeps your cookies, so if you are logged in through your
institution (or the site has accepted its cookie/consent/bot checks), paywalled PDFs
become reachable too.

Per article (stops at the first real PDF):
    1. Unpaywall (open-access copies by DOI)
    2. 'Source Linkout' from the CSV
    3. https://doi.org/<DOI>
  Each URL is first fetched with the browser's cookies; if that fails, the page is
  opened in Chromium itself (JS, redirects, downloads) and the PDF link is extracted.

On success the PDF is saved as 'Expected PDF Filename' in the output folder and the
row's 'Uploaded' column is set to 'Yes' (the CSV is rewritten after every success,
so an interruption loses nothing).

Setup:
    pip install playwright pandas
    # uses your system Chromium; no 'playwright install' needed (see --chromium-path)

Typical use:
    # 1) one-time: open the browser and log in to your institution / publishers
    python download_articles_chromium.py --login
    # 2) run the batch
    python download_articles_chromium.py --email you@university.edu

Alternative (use your everyday Chromium session directly):
    chromium --remote-debugging-port=9222        # start it yourself, log in normally
    python download_articles_chromium.py --cdp http://localhost:9222 --email you@university.edu
"""
import argparse
import re
import shutil
import sys
import time
import tempfile
from pathlib import Path
from urllib.parse import urljoin

import pandas as pd
try:
    from playwright.sync_api import sync_playwright
except ModuleNotFoundError as exc:
    raise SystemExit(
        "Missing dependency: playwright. Install it with 'pip install playwright' (and pandas if needed), "
        "then rerun the script."
    ) from exc

DEFAULT_OUT = "/home/estopinj/POSTDOC/src/dam/scripts/validation/downloaded_pdfs"
DEFAULT_PROFILE = str(Path.home() / ".cache" / "article_dl_chromium_profile")
SCRIPT_DIR = Path(__file__).resolve().parent
DOWNLOAD_STATUS_COLUMN = "Download_Status"
DOWNLOAD_COMPLETED_STATUS = "DOWNLOADED"
DOWNLOAD_FAILED_STATUS = "DOWNLOAD_FAILED"


# ----------------------------------------------------------------- helpers
def is_pdf(body: bytes) -> bool:
    return body[:5] == b"%PDF-"


def api_get(ctx, url, referer=None, timeout=45000):
    """HTTP GET sharing the browser's cookies. Returns response or None."""
    headers = {"Accept": "application/pdf,text/html;q=0.8,*/*;q=0.5"}
    if referer:
        headers["Referer"] = referer
    try:
        r = ctx.request.get(url, headers=headers, timeout=timeout)
        return r if r.ok else None
    except Exception:
        return None


def find_pdf_link(html: str, base_url: str):
    for pat in (
        r'<meta[^>]+name=["\']citation_pdf_url["\'][^>]+content=["\']([^"\']+)',
        r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+name=["\']citation_pdf_url',
        r'href=["\']([^"\']+\.pdf(?:\?[^"\']*)?)["\']',
        r'href=["\']([^"\']*/pdf(?:direct)?/[^"\']+)["\']',
    ):
        m = re.search(pat, html, re.I)
        if m:
            return urljoin(base_url, m.group(1).replace("&amp;", "&"))
    return None


def unpaywall_urls(ctx, doi, email):
    try:
        r = ctx.request.get(f"https://api.unpaywall.org/v2/{doi}?email={email}", timeout=30000)
        if not r.ok:
            return []
        data = r.json()
    except Exception:
        return []
    locs = ([data["best_oa_location"]] if data.get("best_oa_location") else []) + (data.get("oa_locations") or [])
    urls = []
    for loc in locs:
        for k in ("url_for_pdf", "url"):
            u = loc.get(k)
            if u and u not in urls:
                urls.append(u)
    return urls


def try_via_request(ctx, url):
    """Fetch url with cookies; follow one hop to a PDF link if it returns HTML."""
    r = api_get(ctx, url)
    if r is None:
        return None
    body = r.body()
    if is_pdf(body):
        return body
    if "html" in (r.headers.get("content-type") or "").lower():
        link = find_pdf_link(r.text(), r.url)
        if link:
            r2 = api_get(ctx, link, referer=r.url)
            if r2 is not None:
                b2 = r2.body()
                if is_pdf(b2):
                    return b2
    return None


def try_via_browser(ctx, url, tmp_dir: Path):
    """Open the URL in Chromium (handles JS/redirects/downloads), then extract the PDF."""
    page = ctx.new_page()
    downloads = []
    page.on("download", lambda d: downloads.append(d))
    try:
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=45000)
        except Exception:
            pass  # a direct download aborts the navigation; handled below
        page.wait_for_timeout(2500)

        # a) the URL triggered a file download
        if downloads:
            tmp = tmp_dir / "_tmp_download.pdf"
            try:
                downloads[0].save_as(str(tmp))
                body = tmp.read_bytes()
                tmp.unlink(missing_ok=True)
                if is_pdf(body):
                    return body
            except Exception:
                pass

        # b) the page itself is a PDF shown in Chromium's viewer
        cur = page.url
        r = api_get(ctx, cur)
        if r is not None and is_pdf(r.body()):
            return r.body()

        # c) rendered landing page: read the PDF link from the live DOM
        try:
            link = page.evaluate(
                """() => {
                    const m = document.querySelector('meta[name="citation_pdf_url"]');
                    if (m) return m.content;
                    const a = [...document.querySelectorAll('a[href]')]
                        .find(x => /\\.pdf(\\?|$)|\\/pdf(direct)?\\//i.test(x.href));
                    return a ? a.href : null;
                }"""
            )
        except Exception:
            link = None
        if link:
            link = urljoin(cur, link)
            r = api_get(ctx, link, referer=cur)
            if r is not None and is_pdf(r.body()):
                return r.body()
    finally:
        page.close()
    return None


def fetch_pdf(ctx, row, email, tmp_dir, prefer_doi: bool = False):
    doi = row["DOI"].strip()
    candidates = unpaywall_urls(ctx, doi, email) if email else []
    if prefer_doi:
        ordered_sources = (f"https://doi.org/{doi}", row["Source Linkout"].strip())
    else:
        ordered_sources = (row["Source Linkout"].strip(), f"https://doi.org/{doi}")
    for u in ordered_sources:
        if u and u not in candidates:
            candidates.append(u)

    for url in candidates:                       # fast pass: cookies only
        body = try_via_request(ctx, url)
        if body:
            return body, url
    for url in candidates[-2:] + candidates[:-2]:  # slow pass: real browser
        body = try_via_browser(ctx, url, tmp_dir)
        if body:
            return body, url
    return None, None


def find_chromium(explicit):
    if explicit:
        return explicit
    for name in ("chromium", "chromium-browser", "google-chrome", "chrome"):
        p = shutil.which(name)
        if p:
            return p
    return None  # fall back to Playwright's bundled browser


def select_playwright_browser(pw, browser_name):
    if browser_name == "firefox":
        return pw.firefox
    return pw.chromium


def resolve_csv_path(csv_arg: str) -> Path:
    path = Path(csv_arg).expanduser()
    if path.is_absolute():
        return path

    script_relative = (SCRIPT_DIR / path).resolve()
    if script_relative.exists():
        return script_relative

    return path.resolve()


def save_csv_atomic(df: pd.DataFrame, path: Path) -> None:
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    df.to_csv(tmp_path, index=False)
    tmp_path.replace(path)


def resolve_profile_dir(profile_arg: str, *, prefer_persistent: bool = False) -> tuple[str, Path | None]:
    if profile_arg:
        profile_path = Path(profile_arg).expanduser().resolve()
        profile_path.mkdir(parents=True, exist_ok=True)
        return str(profile_path), None

    if prefer_persistent:
        profile_path = Path(DEFAULT_PROFILE).expanduser().resolve()
        profile_path.mkdir(parents=True, exist_ok=True)
        return str(profile_path), None

    temp_dir = tempfile.TemporaryDirectory(prefix="article_dl_chromium_profile_")
    return temp_dir.name, temp_dir


def ensure_download_status_column(df: pd.DataFrame) -> pd.DataFrame:
    if DOWNLOAD_STATUS_COLUMN not in df.columns:
        df[DOWNLOAD_STATUS_COLUMN] = ""
    else:
        df[DOWNLOAD_STATUS_COLUMN] = df[DOWNLOAD_STATUS_COLUMN].fillna("")
    return df


# -------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--csv",
        default=str(SCRIPT_DIR / "articles_to_download.csv"),
        help="CSV file listing articles to download. Relative paths are resolved from the script directory first.",
    )
    ap.add_argument("--out", default=DEFAULT_OUT, help="Folder for the PDFs")
    ap.add_argument("--email", default="", help="Enables Unpaywall lookups (recommended)")
    ap.add_argument("--login", action="store_true",
                    help="Open Chromium so you can log in to your institution, then exit")
    ap.add_argument("--cdp", default="", help="Attach to a running Chromium, e.g. http://localhost:9222")
    ap.add_argument(
        "--browser",
        choices=("chromium", "firefox"),
        default="chromium",
        help="Browser engine to launch locally. CDP attach only works with Chromium.",
    )
    ap.add_argument(
        "--profile",
        default="",
        help="Optional browser profile dir. Use this if you want cookies to persist across runs.",
    )
    ap.add_argument("--chromium-path", default="", help="Path to the Chromium executable")
    ap.add_argument("--firefox-path", default="", help="Path to the Firefox executable")
    ap.add_argument("--headless", action="store_true", help="Run without a window (more likely to be blocked)")
    ap.add_argument("--include-uploaded", action="store_true",
                    help="Also process rows already marked Uploaded=Yes")
    ap.add_argument(
        "--retry-failed",
        action="store_true",
        help="Retry rows previously marked as DOWNLOAD_FAILED instead of skipping them.",
    )
    ap.add_argument(
        "--prefer-doi",
        action="store_true",
        help="Try https://doi.org/<DOI> before the Source Linkout URL.",
    )
    ap.add_argument(
        "--start-row",
        type=int,
        default=1,
        help="1-based row number to start from after applying skip rules.",
    )
    ap.add_argument("--delay", type=float, default=2.0, help="Seconds between articles")
    args = ap.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as pw:
        browser = None
        attached_via_cdp = False
        profile_guard = None
        if args.cdp:
            if args.browser != "chromium":
                raise SystemExit("--cdp is only supported with --browser chromium.")
            browser = pw.chromium.connect_over_cdp(args.cdp)
            ctx = browser.contexts[0]
            attached_via_cdp = True
        else:
            browser_type = select_playwright_browser(pw, args.browser)
            profile_dir, profile_guard = resolve_profile_dir(args.profile, prefer_persistent=args.login)
            if args.browser == "chromium":
                ctx = browser_type.launch_persistent_context(
                    profile_dir,
                    executable_path=find_chromium(args.chromium_path),
                    headless=args.headless,
                    accept_downloads=True,
                    args=["--disable-blink-features=AutomationControlled"],
                    viewport=None,
                )
            else:
                ctx = browser_type.launch_persistent_context(
                    profile_dir,
                    executable_path=args.firefox_path or None,
                    headless=args.headless,
                    accept_downloads=True,
                    viewport=None,
                )

        if args.login:
            page = ctx.new_page()
            page.goto("https://doi.org/")
            input("Log in to your institution / publishers in the browser window, "
                  "then press Enter here to save the session and exit... ")
            ctx.close()
            return

        csv_path = resolve_csv_path(args.csv)
        df = pd.read_csv(csv_path, dtype=str, keep_default_na=False)
        df = ensure_download_status_column(df)
        backup = csv_path.with_suffix(".csv.bak")
        if not backup.exists():
            shutil.copy(csv_path, backup)

        ok = skipped = 0
        try:
            for i, row in df.iterrows():
                if i + 1 < max(1, args.start_row):
                    continue
                fname = row["Expected PDF Filename"].strip()
                target = out / fname
                label = f"[{i + 1}/{len(df)}]"

                # already on disk -> just make sure the CSV says so
                if target.exists() and target.stat().st_size > 1000:
                    if row["Uploaded"] != "Yes":
                        df.at[i, "Uploaded"] = "Yes"
                        df.at[i, DOWNLOAD_STATUS_COLUMN] = DOWNLOAD_COMPLETED_STATUS
                        save_csv_atomic(df, csv_path)
                    skipped += 1
                    continue
                if row["Uploaded"] == "Yes" and not args.include_uploaded:
                    skipped += 1
                    continue
                if str(row.get(DOWNLOAD_STATUS_COLUMN, "")).strip() == DOWNLOAD_FAILED_STATUS and not args.retry_failed:
                    skipped += 1
                    continue

                body, used = fetch_pdf(ctx, row, args.email, out, prefer_doi=args.prefer_doi)
                if body:
                    tmp = target.with_suffix(".part")
                    tmp.write_bytes(body)
                    tmp.rename(target)
                    df.at[i, "Uploaded"] = "Yes"
                    df.at[i, DOWNLOAD_STATUS_COLUMN] = DOWNLOAD_COMPLETED_STATUS
                    save_csv_atomic(df, csv_path)   # save progress immediately
                    ok += 1
                    print(f"{label} OK      {fname}  <- {used}")
                else:
                    df.at[i, DOWNLOAD_STATUS_COLUMN] = DOWNLOAD_FAILED_STATUS
                    save_csv_atomic(df, csv_path)
                    print(f"{label} FAILED  {row['DOI']}")
                time.sleep(args.delay)
        except KeyboardInterrupt:
            print("\nInterrupted - progress so far is saved in the CSV.")
        finally:
            print(f"\nDownloaded: {ok} | skipped: {skipped}")
            if browser and attached_via_cdp:
                ctx.close()
            elif browser:
                browser.close()
            else:
                ctx.close()
            if profile_guard is not None:
                profile_guard.cleanup()


if __name__ == "__main__":
    sys.exit(main())
