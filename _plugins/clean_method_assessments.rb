require "csv"
require "fileutils"

module NaviDAM
  RAW_NAME = "DetectionAttribution methods - Method Assessment.tsv"
  CLEAN_NAME = "method_assessments_clean.tsv"
  SKIP_LINES = 3

  def self.regenerate(site)
    source = site.source
    input_path = File.join(source, "_data", RAW_NAME)
    output_path = File.join(source, "_data", CLEAN_NAME)

    unless File.exist?(input_path)
      Jekyll.logger.warn "NaviDAM:", "raw assessment TSV not found: #{input_path}"
      return
    end

    begin
      lines = File.readlines(input_path, encoding: "UTF-8")
    rescue StandardError => e
      Jekyll.logger.error "NaviDAM:", "cannot read raw TSV (#{e.message})"
      return
    end

    if lines.length <= SKIP_LINES
      Jekyll.logger.error "NaviDAM:", "raw TSV has only #{lines.length} lines, expected > #{SKIP_LINES}"
      return
    end

    cleaned = lines[SKIP_LINES..].join

    # Basic sanity check: header row must contain the Method column.
    header = lines[SKIP_LINES] || ""
    unless header.include?("Method")
      Jekyll.logger.error "NaviDAM:", "raw TSV header does not contain a 'Method' column - skipping regeneration"
      return
    end

    if File.exist?(output_path)
      begin
        existing = File.read(output_path, encoding: "UTF-8")
        if existing == cleaned
          # Up to date, nothing to do (avoids triggering extra rebuild loops).
          return
        end
      rescue StandardError
        # Fall through and rewrite.
      end
    end

    File.write(output_path, cleaned, encoding: "UTF-8")
    Jekyll.logger.info "NaviDAM:", "regenerated #{CLEAN_NAME} from raw assessment TSV"

    # If site data was already loaded (e.g. incremental rebuild), refresh the
    # in-memory copy so method pages render the new values without restart.
    begin
      if site.data && File.exist?(output_path)
        rows = CSV.read(output_path, col_sep: "\t", headers: true, encoding: "UTF-8").map(&:to_h)
        site.data["method_assessments_clean"] = rows
      end
    rescue StandardError => e
      Jekyll.logger.warn "NaviDAM:", "cleaned TSV written but in-memory reload failed (#{e.message})"
    end
  end
end

# Run before `site.read` so Jekyll's DataReader picks up the fresh file...
Jekyll::Hooks.register :site, :after_init do |site|
  NaviDAM.regenerate(site)
end

Jekyll::Hooks.register :site, :after_reset do |site|
  NaviDAM.regenerate(site)
end

# ...and as a generator as a safety net for incremental rebuilds where
# data was already loaded before the file was rewritten.
module NaviDAM
  class AssessmentGenerator < Jekyll::Generator
    safe true
    priority :highest

    def generate(site)
      NaviDAM.regenerate(site)
    end
  end
end
