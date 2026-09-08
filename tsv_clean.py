def clean_tsv(input_file, output_file, skip_lines=3):
    """Strip the leading metadata rows from a raw exported TSV and write the rest to output_file."""
    with open(input_file, newline='', encoding='utf-8') as infile, \
         open(output_file, "w", newline='', encoding='utf-8') as outfile:
        lines = infile.readlines()[skip_lines:]
        outfile.writelines(lines)
