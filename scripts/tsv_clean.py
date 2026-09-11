def clean_tsv(input_file, output_file, skip_lines=3):
    """Strip the leading metadata rows from a raw exported TSV and write the rest to output_file.

    Validates that the first kept line (the header) contains a 'Method'
    column, so a malformed upload fails fast instead of silently producing
    empty assessment tables. Raises ValueError on invalid input.
    """
    with open(input_file, newline='', encoding='utf-8') as infile:
        lines = infile.readlines()
    if len(lines) <= skip_lines:
        raise ValueError(
            f"Raw TSV has only {len(lines)} line(s), expected more than {skip_lines} "
            f"(metadata rows + header + data). Did the export go wrong?"
        )
    header = lines[skip_lines]
    if "Method" not in header:
        raise ValueError(
            "Raw TSV header does not contain a 'Method' column. "
            "Make sure the uploaded file is the method-assessment export "
            f"with {skip_lines} leading metadata rows."
        )
    with open(output_file, "w", newline='', encoding='utf-8') as outfile:
        outfile.writelines(lines[skip_lines:])
