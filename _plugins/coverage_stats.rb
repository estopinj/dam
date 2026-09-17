require "csv"
require "set"

module NaviDAM
  RAW_ASSESSMENT = "DetectionAttribution methods - Method Assessment.tsv"
  RAW_PANELS = "DetectionAttribution methods - Good practices _ Examples Panels.tsv"
  COVERAGE_SKIP_LINES = 3

  class CoverageGenerator < Jekyll::Generator
    safe true
    priority :highest

    def generate(site)
      source = site.source
      coverage = {
        "methods_total" => 0,
        "method_categories" => [],
        "method_subcategories" => [],
        "assess" => {},
        "doc" => {},
        "gp" => {},
        "ex" => {},
        "criteria_total" => 0,
        "criteria_categories" => 0
      }

      # --- Criteria: count non-index .md files under contents/criteria ---
      begin
        crit_files = Dir.glob(File.join(source, "contents", "criteria", "**", "*.md"))
          .reject { |f| File.basename(f) == "index.md" }
        coverage["criteria_total"] = crit_files.size
        cat_dirs = Dir.glob(File.join(source, "contents", "criteria", "*"))
          .select { |d| File.directory?(d) }
        coverage["criteria_categories"] = cat_dirs.size
      rescue StandardError
        coverage["criteria_total"] = 25
        coverage["criteria_categories"] = 5
      end

      # --- Method assessment TSV (positional parse: Doc status col 1, Assessment status col 5) ---
      begin
        input_path = File.join(source, "_data", RAW_ASSESSMENT)
        if File.exist?(input_path)
          lines = File.readlines(input_path, encoding: "UTF-8")
          if lines.length > COVERAGE_SKIP_LINES
            rows = CSV.parse(lines[COVERAGE_SKIP_LINES..].join, col_sep: "\t", encoding: "UTF-8")
            header = rows.shift || []
            data = rows.select { |r| r[4] && !r[4].strip.empty? }
            # pad rows
            data.each { |r| r.fill("", r.length...header.length) if r.length < header.length }

            cats = Set.new
            subcats = Set.new
            assess_complete = 0
            assess_toreview = 0
            doc_online = 0
            doc_toreview = 0
            doc_assigned = 0
            doc_invited = 0
            doc_todo = 0
            assess_review_list = []
            doc_todo_list = []
            doc_planned_list = []
            doc_review_list = []

            data.each do |r|
              doc_status = (r[1] || "").strip
              assess_status = (r[5] || "").strip
              method = (r[4] || "").strip
              (r[8] || "").split(",").each { |c| c = c.strip; cats.add(c) unless c.empty? }
              (r[9] || "").split(",").each { |c| c = c.strip; subcats.add(c) unless c.empty? }

              if assess_status == "Complete"
                assess_complete += 1
              else
                # Anything not marked Complete (To review, blank, …) still needs review
                assess_toreview += 1
                assess_review_list << method
              end

              case doc_status
              when "Online"
                doc_online += 1
              when "To review"
                doc_toreview += 1
                doc_review_list << { "method" => method, "status" => doc_status }
              when "Assigned", "Invited"
                doc_planned_list << { "method" => method, "status" => doc_status }
                if doc_status == "Assigned"
                  doc_assigned += 1
                else
                  doc_invited += 1
                end
              when "No", "To do"
                doc_todo += 1
                doc_todo_list << { "method" => method, "status" => "To do" }
              when ""
                doc_todo += 1
                doc_todo_list << { "method" => method, "status" => "To do" }
              else
                doc_todo += 1
                doc_todo_list << { "method" => method, "status" => doc_status }
              end
            end

            total = data.size
            coverage["methods_total"] = total
            coverage["method_categories"] = cats.to_a.sort
            coverage["method_subcategories"] = subcats.to_a.sort
            coverage["assess"] = {
              "complete" => assess_complete,
              "toreview" => assess_toreview,
              "total" => total,
              "review_list" => assess_review_list.sort
            }
            coverage["doc"] = {
              "online" => doc_online,
              "toreview" => doc_toreview,
              "assigned" => doc_assigned,
              "invited" => doc_invited,
              "planned" => doc_assigned + doc_invited,
              "todo" => doc_todo,
              "total" => total,
              "todo_list" => doc_todo_list.sort_by { |h| h["method"] },
              "planned_list" => doc_planned_list.sort_by { |h| h["method"] },
              "review_list" => doc_review_list.sort_by { |h| h["method"] }
            }
          end
        end
      rescue StandardError => e
        Jekyll.logger.warn "NaviDAM coverage:", "method assessment parse failed (#{e.message})"
      end

      # --- Good practices / Examples panels TSV ---
      begin
        gp_path = File.join(source, "_data", RAW_PANELS)
        if File.exist?(gp_path)
          lines = File.readlines(gp_path, encoding: "UTF-8")
          rows = CSV.parse(lines.join, col_sep: "\t", encoding: "UTF-8")
          rows.shift # title row
          rows.shift # header row
          gp_counts = Hash.new(0)
          ex_counts = Hash.new(0)
          gp_total = 0
          ex_total = 0
          rows.each do |r|
            r.fill("", r.length...10) if r.length < 10
            gp_name = (r[0] || "").strip
            gp_status = (r[2] || "").strip
            ex_name = (r[7] || "").strip
            ex_status = (r[9] || "").strip
            unless gp_name.empty?
              gp_total += 1
              gp_counts[gp_status] += 1
            end
            unless ex_name.empty?
              ex_total += 1
              ex_counts[ex_status] += 1
            end
          end
          coverage["gp"] = {
            "online" => gp_counts["Online"] || 0,
            "toreview" => gp_counts["To review"] || 0,
            "assigned" => gp_counts["Assigned"] || 0,
            "invited" => gp_counts["Invited"] || 0,
            "planned" => (gp_counts["Assigned"] || 0) + (gp_counts["Invited"] || 0),
            "todo" => gp_counts["No"] || 0,
            "total" => gp_total
          }
          coverage["ex"] = {
            "online" => ex_counts["Online"] || 0,
            "toreview" => ex_counts["To review"] || 0,
            "assigned" => ex_counts["Assigned"] || 0,
            "invited" => ex_counts["Invited"] || 0,
            "planned" => (ex_counts["Assigned"] || 0) + (ex_counts["Invited"] || 0),
            "todo" => ex_counts["No"] || 0,
            "total" => ex_total
          }
        end
      rescue StandardError => e
        Jekyll.logger.warn "NaviDAM coverage:", "panels parse failed (#{e.message})"
      end

      site.data["coverage"] = coverage
      Jekyll.logger.info "NaviDAM coverage:", "methods=#{coverage['methods_total']} criteria=#{coverage['criteria_total']} gp=#{coverage.dig('gp', 'total')} ex=#{coverage.dig('ex', 'total')}"
    end
  end
end
