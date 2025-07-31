import os
import yaml

FOLDER = "contents"

def get_categories_from_path(filepath):
    rel_path = os.path.relpath(filepath, FOLDER)
    return rel_path.split(os.sep)[:-1]

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    if not lines or not lines[0].strip() == '---':
        return  # no front matter

    # Find where front matter ends
    try:
        end_index = lines[1:].index('---\n') + 1
    except ValueError:
        print(f"⚠️ No end to front matter in: {filepath}")
        return

    front_lines = lines[1:end_index]
    body_lines = lines[end_index + 1:]

    try:
        front_dict = yaml.safe_load(''.join(front_lines)) or {}
    except yaml.YAMLError:
        print(f"⚠️ Invalid YAML in: {filepath}")
        return

    categories = get_categories_from_path(filepath)
    if front_dict.get("categories") == categories:
        return  # already correct

    front_dict["categories"] = categories

    # Dump updated front matter
    new_front = yaml.dump(front_dict, sort_keys=False).strip()
    # new_front = yaml.dump(front_dict, sort_keys=False, default_flow_style=True).strip()
    new_lines = ['---\n'] + [new_front + '\n'] + ['---\n'] + body_lines

    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

    print(f"✅ Updated categories in: {filepath}")



# Custom YAML dumper to quote strings with spaces
def str_presenter(dumper, data):
    if isinstance(data, str) and (' ' in data or ':' in data):
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='"')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)

yaml.add_representer(str, str_presenter)



def scan_folder(folder):
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith('.md'):
                process_file(os.path.join(root, file))

if __name__ == "__main__":
    scan_folder(FOLDER)