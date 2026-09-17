require "csv"

module NaviDAM
  RAW_ASSESSMENT_META = "DetectionAttribution methods - Method Assessment.tsv"
  RAW_RESOURCES = "DA_usedressources.tsv"
  META_SKIP_LINES = 3

  # Exposes per-method display metadata that the cleaned assessment table
  # cannot (duplicate/renamed status columns, AI flag, confidence) plus the
  # list of resources used for AI-assisted assessments:
  #   site.data["method_meta"][method_name] => {
  #     "assessor", "doc_status", "assess_status", "ai_assisted", "ai_flag", "confidence" }
  #   site.data["used_resources"][method_name] => [
  #     { "type", "resource", "url", "use" }, ... ]
  class MethodMetaGenerator < Jekyll::Generator
    safe true
    priority :high

    def generate(site)
      source = site.source
      meta = {}
      resources = {}

      begin
        input_path = File.join(source, "_data", RAW_ASSESSMENT_META)
        if File.exist?(input_path)
          lines = File.readlines(input_path, encoding: "UTF-8")
          if lines.length > META_SKIP_LINES
            rows = CSV.parse(lines[META_SKIP_LINES..].join, col_sep: "\t", encoding: "UTF-8")
            rows.shift # header
            rows.each do |r|
              r.fill("", r.length...36) if r.length < 36
              method = (r[4] || "").strip
              next if method.empty?

              doc_status = (r[1] || "").strip
              doc_status = "To do" if doc_status == "No" || doc_status.empty?
              assess_status = (r[5] || "").strip
              assess_status = "To review" if assess_status.empty?

              meta[method] = {
                "assessor" => (r[3] || "").strip,
                "doc_status" => doc_status,
                "assess_status" => assess_status,
                "ai_assisted" => (r[6] || "").strip,
                "ai_flag" => (r[7] || "").strip,
                "confidence" => (r[35] || "").strip
              }
            end
          end
        end
      rescue StandardError => e
        Jekyll.logger.warn "NaviDAM meta:", "assessment parse failed (#{e.message})"
      end

      begin
        res_path = File.join(source, "_data", RAW_RESOURCES)
        if File.exist?(res_path)
          rows = CSV.read(res_path, col_sep: "\t", headers: true, encoding: "UTF-8")
          rows.each do |row|
            h = row.to_h
            method = (h["Method"] || "").strip
            next if method.empty?

            resources[method] ||= []
            resources[method] << {
              "type" => (h["Resource type"] || "").strip,
              "resource" => (h["Resource"] || "").strip,
              "url" => (h["URL"] || "").strip,
              "use" => (h["Use"] || "").strip
            }
          end
        end
      rescue StandardError => e
        Jekyll.logger.warn "NaviDAM meta:", "resources parse failed (#{e.message})"
      end

      site.data["method_meta"] = meta
      site.data["used_resources"] = resources
      Jekyll.logger.info "NaviDAM meta:", "methods=#{meta.size} resources=#{resources.size}"
    end
  end
end
