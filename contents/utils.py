import bleach
from bleach_allowlist import markdown_attrs, markdown_tags
from markdownx.utils import markdownify


def markdown_to_content(markdown_text):
    raw_html = markdownify(markdown_text)
    tags = markdown_tags
    tags += ["table", "thead", "tr", "th", "td", "tbody"]
    markdown_attrs["*"] = ["class", "id"]
    markdown_attrs["img"] = ["src", "alt", "title", "width", "height"]
    return bleach.clean(raw_html, tags=tags, attributes=markdown_attrs)
