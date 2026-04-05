from jinja2 import Environment, FileSystemLoader
from pathlib import Path

env = Environment(loader=FileSystemLoader("templates"))

def render_template(template_name, context):
    template = env.get_template(template_name)
    html = template.render(context)
    output_dir = Path("reports")
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / "report.html"
    output_path.write_text(html, encoding="utf-8")
    return output_path