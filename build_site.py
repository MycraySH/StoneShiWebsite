"""Export the Python portfolio for GitHub Pages without a running server."""

from html import escape
from html.parser import HTMLParser
from pathlib import Path
import shutil
from urllib.parse import urlsplit, urlunsplit

import app


OUTPUT = Path(__file__).resolve().parent / "docs"
BASE_PATH = "/StoneShiWebsite"


class PagesHTML(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.parts = []

    def handle_starttag(self, tag, attrs):
        rewritten = []
        for name, value in attrs:
            if name in {"href", "src", "data"} and value and value.startswith("/") and not value.startswith("//"):
                url = urlsplit(value)
                path = url.path
                if not path.startswith("/static/") and not path.endswith("/"):
                    path += "/"
                value = urlunsplit(("", "", BASE_PATH + path, url.query, url.fragment))
            rewritten.append(name if value is None else f'{name}="{escape(value, quote=True)}"')
        self.parts.append("<" + tag + (" " + " ".join(rewritten) if rewritten else "") + ">")

    def handle_endtag(self, tag):
        self.parts.append(f"</{tag}>")

    def handle_data(self, data):
        self.parts.append(data)

    def handle_decl(self, decl):
        self.parts.append(f"<!{decl}>")

    def handle_comment(self, data):
        self.parts.append(f"<!--{data}-->")

    def handle_entityref(self, name):
        self.parts.append(f"&{name};")

    def handle_charref(self, name):
        self.parts.append(f"&#{name};")


def build():
    pages = {
        "index.html": app.home_page(),
        "cv/index.html": app.cv_page(),
        "cover-letter/index.html": app.cover_letter_page(),
        "research-proposal/index.html": app.research_proposal_page(),
        "404.html": app.base("Page not found", '<h1>Page not found</h1><a href="/">Back to CV</a>'),
    }
    for sample in app.WORK_SAMPLES:
        pages[f"work/{sample['slug']}/index.html"] = app.work_page(sample["slug"])
    for path, html in pages.items():
        parser = PagesHTML()
        parser.feed(html)
        parser.close()
        target = OUTPUT / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("".join(parser.parts), encoding="utf-8")
    shutil.copytree(app.STATIC_ROOT, OUTPUT / "static", dirs_exist_ok=True)
    (OUTPUT / ".nojekyll").touch()
    print(f"Built {len(pages)} pages in {OUTPUT}")


if __name__ == "__main__":
    build()
