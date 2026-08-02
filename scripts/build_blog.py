#!/usr/bin/env python3
"""Build Casey's Space static blog from Markdown and Word files in /blog."""

from __future__ import annotations

import html
import re
import shutil
from datetime import date, datetime
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
BLOG = ROOT / "blog"
ARTICLES = BLOG / "articles"
EXCLUDED_DIRS = {"articles", "assets"}
EXCLUDED_FILES = {"README.md"}


def parse_front_matter(text: str) -> tuple[dict[str, str], str]:
    meta: dict[str, str] = {}
    if not text.startswith("---\n"):
        return meta, text
    closing = text.find("\n---\n", 4)
    if closing == -1:
        return meta, text
    for line in text[4:closing].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        meta[key.strip().lower()] = value.strip().strip('"\'')
    return meta, text[closing + 5 :]


def inline_markdown(value: str) -> str:
    value = html.escape(value, quote=False)
    value = re.sub(r"!\[([^]]*)\]\((https?://[^ )]+)\)", r'<img src="\2" alt="\1" loading="lazy">', value)
    value = re.sub(r"\[([^]]+)\]\((https?://[^ )]+|/[^ )]+)\)", r'<a href="\2">\1</a>', value)
    value = re.sub(r"`([^`]+)`", r"<code>\1</code>", value)
    value = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", value)
    value = re.sub(r"__([^_]+)__", r"<strong>\1</strong>", value)
    value = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", value)
    return value


def markdown_to_html(markdown: str) -> str:
    lines = markdown.replace("\r\n", "\n").split("\n")
    output: list[str] = []
    paragraph: list[str] = []
    list_type: str | None = None
    in_code = False
    code_lines: list[str] = []

    def flush_paragraph() -> None:
        if paragraph:
            output.append(f"<p>{inline_markdown(' '.join(paragraph).strip())}</p>")
            paragraph.clear()

    def close_list() -> None:
        nonlocal list_type
        if list_type:
            output.append(f"</{list_type}>")
            list_type = None

    for raw in lines:
        line = raw.rstrip()
        if line.startswith("```"):
            flush_paragraph()
            close_list()
            if in_code:
                output.append("<pre><code>" + html.escape("\n".join(code_lines)) + "</code></pre>")
                code_lines.clear()
                in_code = False
            else:
                in_code = True
            continue
        if in_code:
            code_lines.append(raw)
            continue
        if not line.strip():
            flush_paragraph()
            close_list()
            continue
        heading = re.match(r"^(#{1,3})\s+(.+)$", line)
        if heading:
            flush_paragraph()
            close_list()
            level = len(heading.group(1))
            output.append(f"<h{level}>{inline_markdown(heading.group(2))}</h{level}>")
            continue
        quote_match = re.match(r"^>\s?(.*)$", line)
        if quote_match:
            flush_paragraph()
            close_list()
            output.append(f"<blockquote>{inline_markdown(quote_match.group(1))}</blockquote>")
            continue
        unordered = re.match(r"^\s*[-*+]\s+(.+)$", line)
        ordered = re.match(r"^\s*\d+[.)]\s+(.+)$", line)
        if unordered or ordered:
            flush_paragraph()
            wanted = "ul" if unordered else "ol"
            if list_type != wanted:
                close_list()
                list_type = wanted
                output.append(f"<{wanted}>")
            match = unordered or ordered
            output.append(f"<li>{inline_markdown(match.group(1))}</li>")
            continue
        paragraph.append(line.strip())

    flush_paragraph()
    close_list()
    if in_code:
        output.append("<pre><code>" + html.escape("\n".join(code_lines)) + "</code></pre>")
    return "\n".join(output)


def slugify(value: str) -> str:
    value = value.lower().replace("&", " and ")
    return re.sub(r"[^a-z0-9]+", "-", value).strip("-") or "article"


def nice_date(value: str) -> str:
    try:
        return datetime.strptime(value[:10], "%Y-%m-%d").strftime("%B %-d, %Y")
    except (ValueError, TypeError):
        return value or "Undated"


def discover_sources() -> list[Path]:
    files: list[Path] = []
    for path in BLOG.rglob("*"):
        if not path.is_file() or any(part in EXCLUDED_DIRS for part in path.relative_to(BLOG).parts):
            continue
        if path.name in EXCLUDED_FILES:
            continue
        if path.suffix.lower() in {".md", ".markdown", ".doc", ".docx"}:
            files.append(path)
    return files


def shared_header(title: str, description: str, canonical: str) -> str:
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(description, quote=True)}">
  <link rel="canonical" href="{html.escape(canonical, quote=True)}">
  <meta property="og:title" content="{html.escape(title, quote=True)}">
  <meta property="og:description" content="{html.escape(description, quote=True)}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="{html.escape(canonical, quote=True)}">
  <meta property="og:image" content="https://caseykeown.com/ck-logo.png">
  <link rel="stylesheet" href="/blog/assets/blog.css">
</head>
<body>
<header class="site-header">
  <div class="site-shell header-top">
    <a class="brand" href="/" aria-label="Casey's Space home"><img src="/caseyspace.png" alt="Casey's Space"></a>
    <div class="utility-links"><a href="mailto:me@caseykeown.com">Mail</a><span>|</span><a href="/leads">Request a Quote</a></div>
  </div>
  <div class="search-strip"><span>Search Casey's Blog:</span><input id="site-search" type="search" placeholder="Search articles..." aria-label="Search articles"><button type="button" id="search-button">Search</button></div>
  <nav class="main-nav" aria-label="Main navigation"><a href="/">Home</a><a href="/blog/" aria-current="page">Blog</a><a href="/#services">Services</a><a href="/#projects">Projects</a><a href="/leads">Request a Quote</a><a href="mailto:me@caseykeown.com">Contact</a></nav>
</header>'''


def sidebar() -> str:
    return '''<aside class="blog-sidebar">
  <h2 class="profile-name">Casey</h2>
  <div class="profile-card"><img src="/drummer.png" alt="Casey Keown playing drums"><p><strong>Casey's Blog</strong></p><p class="online">Online Now!</p><p>Kentucky web developer writing about websites, SEO, and useful technology.</p></div>
  <section class="sidebar-box"><h2 class="box-title">Contacting Casey</h2><ul><li><a href="mailto:me@caseykeown.com">Send Message</a></li><li><a href="/leads">Request a Quote</a></li><li><a href="/">View Profile</a></li><li><a href="/blog/feed.xml">Subscribe via RSS</a></li></ul></section>
</aside>'''


def footer() -> str:
    return '''<footer class="site-footer"><p><a href="/">Home</a> | <a href="/blog/">Blog</a> | <a href="/leads">Request a Quote</a> | <a href="mailto:me@caseykeown.com">Contact</a></p><p>© 2026 CASEY KEOWN | Custom Web Architecture. All Rights Reserved.</p><p>Best viewed with a modern browser and a deeply unreasonable amount of nostalgia.</p></footer>'''


def build() -> None:
    if ARTICLES.exists():
        shutil.rmtree(ARTICLES)
    ARTICLES.mkdir(parents=True, exist_ok=True)
    posts: list[dict[str, str]] = []
    downloads: list[dict[str, str]] = []

    for source in discover_sources():
        relative = source.relative_to(BLOG).as_posix()
        if source.suffix.lower() in {".doc", ".docx"}:
            downloads.append({"title": source.stem.replace("-", " ").title(), "url": "/blog/" + quote(relative), "type": source.suffix[1:]})
            continue
        meta, markdown = parse_front_matter(source.read_text(encoding="utf-8"))
        first_heading = re.search(r"^#\s+(.+)$", markdown, re.MULTILINE)
        title = meta.get("title") or (first_heading.group(1) if first_heading else source.stem.replace("-", " ").title())
        slug = slugify(meta.get("slug") or re.sub(r"^\d{4}-\d{2}-\d{2}-", "", source.stem))
        published = meta.get("date") or (re.match(r"^(\d{4}-\d{2}-\d{2})", source.name).group(1) if re.match(r"^(\d{4}-\d{2}-\d{2})", source.name) else date.today().isoformat())
        description = meta.get("meta_description") or meta.get("description") or "Practical website development and SEO advice from Custom Web Architecture."
        seo_title = meta.get("meta_title") or title
        article_url = f"https://caseykeown.com/blog/articles/{slug}/"
        body = markdown_to_html(markdown)
        if body.startswith("<h1>"):
            body = re.sub(r"^<h1>.*?</h1>\s*", "", body, count=1, flags=re.DOTALL)
        article_html = shared_header(seo_title, description, article_url) + f'''
<div class="site-shell blog-layout">
  {sidebar()}
  <main><div class="network-banner">Casey is in your extended network — <strong>and your search results.</strong></div><section class="content-box article-shell"><p class="back-link">&laquo; <a href="/blog/">Back to Casey's Blog</a></p><header class="article-header"><h1>{html.escape(title)}</h1><p class="post-meta">Posted {html.escape(nice_date(published))} · Custom Web Architecture</p><p class="article-description">{html.escape(description)}</p></header><article class="article-body">{body}</article></section></main>
</div>{footer()}</body></html>'''
        output_dir = ARTICLES / slug
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / "index.html").write_text(article_html, encoding="utf-8")
        posts.append({"title": title, "slug": slug, "date": published, "description": description, "url": f"/blog/articles/{slug}/"})

    posts.sort(key=lambda item: item["date"], reverse=True)
    list_items = "\n".join(f'''<li data-search="{html.escape((post['title'] + ' ' + post['description']).lower(), quote=True)}"><h2><a href="{post['url']}">{html.escape(post['title'])}</a></h2><div class="post-meta">{html.escape(nice_date(post['date']))} · Casey Keown</div><p class="post-excerpt">{html.escape(post['description'])}</p></li>''' for post in posts)
    list_items += "\n".join(f'''<li data-search="{html.escape(item['title'].lower(), quote=True)}"><h2><a href="{item['url']}">{html.escape(item['title'])}<span class="file-badge">{item['type']}</span></a></h2><div class="post-meta">Downloadable Word document</div></li>''' for item in downloads)
    if not list_items:
        list_items = '<li class="empty-state">Casey is writing the first post now. Check back soon—or hit refresh like it’s 2006.</li>'

    index_description = "Website development, SEO, and small-business technology articles from Casey Keown of Custom Web Architecture in Kentucky."
    index_html = shared_header("Casey's Blog | Web Design & SEO Articles", index_description, "https://caseykeown.com/blog/") + f'''
<div class="site-shell blog-layout">
  {sidebar()}
  <main><div class="network-banner">Casey is in your extended network — <strong>and your search results.</strong></div><section class="content-box"><div class="blog-intro"><h1>Casey's Blog</h1><p><strong>Web development and SEO without the mystery tech talk.</strong></p><p>Practical answers for Kentucky small businesses, nonprofits, and people who want their websites to do real work.</p></div><div class="blog-toolbar"><input id="post-filter" type="search" placeholder="Filter Casey's blog entries..." aria-label="Filter blog posts"><span class="post-count">{len(posts)} article{'s' if len(posts) != 1 else ''}</span></div><ul class="post-list" id="post-list">{list_items}</ul></section></main>
</div>{footer()}
<script>
(function(){{
  var filter = document.getElementById('post-filter');
  var topSearch = document.getElementById('site-search');
  function run(value) {{
    var query = value.trim().toLowerCase();
    document.querySelectorAll('#post-list > li').forEach(function(item) {{ item.hidden = query && !(item.dataset.search || item.textContent.toLowerCase()).includes(query); }});
  }}
  if (filter) filter.addEventListener('input', function() {{ run(filter.value); }});
  document.getElementById('search-button').addEventListener('click', function() {{ if (filter) filter.value = topSearch.value; run(topSearch.value); }});
  topSearch.addEventListener('keydown', function(event) {{ if (event.key === 'Enter') {{ event.preventDefault(); if (filter) filter.value = topSearch.value; run(topSearch.value); }} }});
}})();
</script></body></html>'''
    (BLOG / "index.html").write_text(index_html, encoding="utf-8")

    rss_items = "\n".join(f'''<item><title>{html.escape(post['title'])}</title><link>https://caseykeown.com{post['url']}</link><guid>https://caseykeown.com{post['url']}</guid><pubDate>{html.escape(post['date'])}</pubDate><description>{html.escape(post['description'])}</description></item>''' for post in posts[:20])
    (BLOG / "feed.xml").write_text(f'''<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>Casey's Blog</title><link>https://caseykeown.com/blog/</link><description>{html.escape(index_description)}</description>{rss_items}</channel></rss>''', encoding="utf-8")

    urls = ["https://caseykeown.com/", "https://caseykeown.com/leads", "https://caseykeown.com/blog/"] + ["https://caseykeown.com" + post["url"] for post in posts]
    (ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(f"  <url><loc>{html.escape(url)}</loc></url>" for url in urls) + "\n</urlset>\n", encoding="utf-8")
    print(f"Built {len(posts)} article(s) and {len(downloads)} Word download(s).")


if __name__ == "__main__":
    build()
