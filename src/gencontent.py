import os

from markdown_blocks import markdown_to_html_node


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("No title found")


def generate_page(from_path, template_path, dest_path):
    print(f" * {from_path} {template_path} -> {dest_path}")
    
    with open(from_path, 'r') as f:
        markdown = f.read()
    
    with open(template_path, 'r') as f:
        template = f.read()
    
    content = markdown_to_html_node(markdown, "div").to_html()
    title = extract_title(markdown)

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", content)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, 'w') as f:
        f.write(template)
