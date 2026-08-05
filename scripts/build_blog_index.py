#!/usr/bin/env python3
"""Keep /blog/index.html aligned with the main Custom Web Architecture theme.

Run this after scripts/build_blog.py. Pass a saved copy of the branded blog index
as the first argument; the workflow preserves that copy before the main builder
regenerates the rest of the blog.
"""

from __future__ import annotations

import html
import json
import re
import sys
from datetime import date, datetime, timezone
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
BLOG = ROOT / "blog"
OUTPUT = BLOG / "index.html"
SITE_URL = "https://caseykeown.com"
SITE_NAME = "Custom Web Architecture"
OG_IMAGE = "https://raw.githubusercontent.com/caseykeown/web-dev/refs/heads/main/blog-social-image.jpg"
EXCLUDED_DIRS = {"articles", "assets"}
EXCLUDED_FILES = {"README.md"}


def parse_front_matter(text: str) -> tuple[dict[str, str], str]:
    metadata: dict[str, str] = {}
    normalized = text.replace("\r\n", "\n")
    if not normalized.startswith("---\n"):
        return metadata, normalized
    closing = normalized.find("\n---\n", 4)
    if closing == -1:
        return metadata, normalized
    for line in normalized[4:closing].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip().lower()] = value.strip().strip('"\'')
    return metadata, normalized[closing + 5 :]


def slugify(value: str) -> str:
    normalized = value.lower().replace("&", " and ")
    return re.sub(r"[^a-z0-9]+", "-", normalized).strip("-") or "article"


def parse_date(value: str) -> datetime:
    try:
        parsed = datetime.strptime(value[:10], "%Y-%m-%d")
    except (TypeError, ValueError):
        parsed = datetime.combine(date.today(), datetime.min.time())
    return parsed.replace(tzinfo=timezone.utc)


def nice_date(value: str) -> str:
    parsed = parse_date(value)
    return f"{parsed.strftime('%B')} {parsed.day}, {parsed.year}"


def discover_content() -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    posts: list[dict[str, str]] = []
    downloads: list[dict[str, str]] = []

    for path in sorted(BLOG.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(BLOG)
        if any(part in EXCLUDED_DIRS for part in relative.parts) or path.name in EXCLUDED_FILES:
            continue

        suffix = path.suffix.lower()
        if suffix in {".doc", ".docx"}:
            downloads.append(
                {
                    "title": path.stem.replace("-", " ").replace("_", " ").title(),
                    "url": "/blog/" + quote(relative.as_posix()),
                    "type": suffix[1:].upper(),
                }
            )
            continue
        if suffix not in {".md", ".markdown"}:
            continue

        metadata, body = parse_front_matter(path.read_text(encoding="utf-8"))
        if metadata.get("draft", "false").lower() in {"true", "yes", "1"}:
            continue

        first_heading = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
        title = metadata.get("title") or (
            first_heading.group(1).strip()
            if first_heading
            else path.stem.replace("-", " ").replace("_", " ").title()
        )
        filename_date = re.match(r"^(\d{4}-\d{2}-\d{2})", path.name)
        published = metadata.get("date") or (
            filename_date.group(1) if filename_date else date.today().isoformat()
        )
        slug_source = metadata.get("slug") or re.sub(r"^\d{4}-\d{2}-\d{2}-", "", path.stem)
        description = (
            metadata.get("meta_description")
            or metadata.get("description")
            or "Practical website development and SEO guidance from Custom Web Architecture."
        )
        posts.append(
            {
                "title": title,
                "date": published,
                "description": description,
                "url": f"/blog/articles/{slugify(slug_source)}/",
            }
        )

    posts.sort(key=lambda post: parse_date(post["date"]), reverse=True)
    return posts, downloads


def article_card(post: dict[str, str]) -> str:
    title = html.escape(post["title"])
    description = html.escape(post["description"])
    url = html.escape(post["url"], quote=True)
    search_text = html.escape(f"{post['title']} {post['description']}".lower(), quote=True)
    return f'''          <article class="article-card" role="listitem" data-search="{search_text}">
            <div>
              <p class="article-meta"><time datetime="{html.escape(post['date'], quote=True)}">{html.escape(nice_date(post['date']))}</time> &middot; Casey Keown</p>
              <h2><a href="{url}">{title}</a></h2>
              <p class="article-excerpt">{description}</p>
            </div>
            <a class="btn btn-quiet article-link" href="{url}" aria-label="Read {html.escape(post['title'], quote=True)}">Read article &rarr;</a>
          </article>'''


def download_card(item: dict[str, str]) -> str:
    title = html.escape(item["title"])
    url = html.escape(item["url"], quote=True)
    file_type = html.escape(item["type"])
    search_text = html.escape(f"{item['title']} {item['type']} download".lower(), quote=True)
    return f'''          <article class="article-card" role="listitem" data-search="{search_text}">
            <div>
              <p class="article-meta">Downloadable {file_type} document</p>
              <h2><a href="{url}">{title}</a></h2>
              <p class="article-excerpt">Download this resource directly from the blog.</p>
            </div>
            <a class="btn btn-quiet article-link" href="{url}" aria-label="Download {html.escape(item['title'], quote=True)}">Download &rarr;</a>
          </article>'''


def schema_json(posts: list[dict[str, str]]) -> str:
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Organization",
                "@id": f"{SITE_URL}/#business",
                "name": SITE_NAME,
                "url": f"{SITE_URL}/",
                "logo": f"{SITE_URL}/assets/cwa-monogram-transparent-black.png",
                "image": OG_IMAGE,
                "email": "mailto:me@caseykeown.com",
                "founder": {"@id": f"{SITE_URL}/#casey"},
                "areaServed": "Kentucky",
                "sameAs": ["https://www.facebook.com/profile.php?id=61590846744430"],
            },
            {
                "@type": "Person",
                "@id": f"{SITE_URL}/#casey",
                "name": "Casey Keown",
                "url": f"{SITE_URL}/about.html",
                "image": f"{SITE_URL}/assets/headshot-640.webp",
                "jobTitle": "Web Developer",
                "worksFor": {"@id": f"{SITE_URL}/#business"},
            },
            {
                "@type": "Blog",
                "@id": f"{SITE_URL}/blog/#blog",
                "url": f"{SITE_URL}/blog/",
                "name": f"{SITE_NAME} Blog",
                "description": "Practical website development, SEO, and small-business technology articles from Casey Keown.",
                "publisher": {"@id": f"{SITE_URL}/#business"},
                "author": {"@id": f"{SITE_URL}/#casey"},
                "blogPost": [{"@id": f"{SITE_URL}{post['url']}#article"} for post in posts],
                "inLanguage": "en-US",
            },
        ],
    }
    return json.dumps(schema, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


def replace_once(pattern: str, replacement: str, source: str, label: str, flags: int = 0) -> str:
    updated, count = re.subn(pattern, replacement, source, count=1, flags=flags)
    if count != 1:
        raise RuntimeError(f"Could not update {label} in the blog index template.")
    return updated


def render(template_path: Path) -> None:
    if not template_path.exists():
        raise FileNotFoundError(f"Blog index template not found: {template_path}")

    posts, downloads = discover_content()
    cards = [article_card(post) for post in posts]
    cards.extend(download_card(item) for item in downloads)
    if not cards:
        cards.append(
            '''          <article class="article-card" role="listitem" data-search="articles coming soon">
            <div>
              <p class="article-meta">Custom Web Architecture</p>
              <h2>Articles are coming soon.</h2>
              <p class="article-excerpt">Check back for practical website and SEO guidance.</p>
            </div>
          </article>'''
        )

    rendered = template_path.read_text(encoding="utf-8")

    token_updates = {
        "var(--color-surface)": "var(--color-cream-soft)",
        "var(--color-border)": "var(--color-gray)",
        "var(--radius-md)": "var(--radius)",
        "var(--color-text-muted)": "#5f5b55",
        "var(--color-text)": "var(--color-charcoal)",
        "var(--color-focus)": "var(--color-orange)",
        "var(--transition)": ".16s ease",
        "var(--shadow-md)": "var(--shadow)",
    }
    for old, new in token_updates.items():
        rendered = rendered.replace(old, new)
    rendered = rendered.replace('id="nav-toggle"', "data-nav-toggle")
    rendered = rendered.replace('<span class="sr-only">Menu</span>', '<span class="sr-only">Open menu</span>')
    rendered = rendered.replace(
        'id="nav-links" data-open="false">',
        'id="nav-links" data-open="false" data-nav-links>',
    )
    rendered = rendered.replace('<script src="/scripts/site.js"></script>', '<script src="/scripts/site.js" defer></script>')

    total = len(posts) + len(downloads)
    rendered = replace_once(
        r'<span class="post-count" id="post-count" aria-live="polite">.*?</span>',
        f'<span class="post-count" id="post-count" aria-live="polite">{total} {"article" if total == 1 else "articles"}</span>',
        rendered,
        "article count",
        re.DOTALL,
    )
    rendered = replace_once(
        r'        <div class="article-grid" id="post-list" role="list">.*?        </div>\n\n        <p class="blog-empty"',
        '        <div class="article-grid" id="post-list" role="list">\n'
        + "\n\n".join(cards)
        + '\n        </div>\n\n        <p class="blog-empty"',
        rendered,
        "article cards",
        re.DOTALL,
    )
    rendered = replace_once(
        r'  <script type="application/ld\+json">.*?</script>',
        f'  <script type="application/ld+json">{schema_json(posts)}</script>',
        rendered,
        "structured data",
        re.DOTALL,
    )
    rendered = re.sub(
        r'<span(?: id="year"| data-current-year)>\d{4}</span>',
        f'<span data-current-year>{date.today().year}</span>',
        rendered,
        count=1,
    )

    OUTPUT.write_text(rendered, encoding="utf-8")
    print(f"Rendered {OUTPUT.relative_to(ROOT)} with {total} item(s).")


if __name__ == "__main__":
    source = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else OUTPUT
    render(source)
