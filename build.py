"""Builds the Scoop docs site.

Each file in pages/ is one page: first line is the title, the rest is HTML.
Run: python3 build.py   ->  writes site/
"""
import pathlib, re, shutil

ROOT = pathlib.Path(__file__).parent
NAV = [
    ('index', 'Start here'),
    ('setup', 'Set up your store'),
    ('products', 'Add your products'),
    ('product-page', 'Product page'),
    ('sections', 'Sections'),
    ('settings', 'Theme settings'),
    ('faq', 'FAQ'),
    ('support', 'Get help'),
]

TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · Scoop theme docs</title>
<meta name="description" content="{desc}">
<link rel="stylesheet" href="style.css">
</head>
<body>
<header class="top">
  <a class="brand" href="index.html">SCOOP <span>docs</span></a>
  <button class="menu" aria-expanded="false" aria-controls="nav">Menu</button>
</header>
<div class="wrap">
  <nav id="nav" class="nav" aria-label="Docs">
    <ul>{nav}</ul>
  </nav>
  <main class="main">
    <h1>{title}</h1>
    {body}
    <footer class="pager">{pager}</footer>
  </main>
</div>
<script>
  const b = document.querySelector('.menu'), n = document.getElementById('nav');
  b.addEventListener('click', () => {{ const o = n.classList.toggle('open'); b.setAttribute('aria-expanded', o); }});
</script>
</body>
</html>
"""


def main():
    out = ROOT / 'site'
    out.mkdir(exist_ok=True)
    shutil.copy(ROOT / 'style.css', out / 'style.css')
    for i, (slug, label) in enumerate(NAV):
        raw = (ROOT / 'pages' / f'{slug}.html').read_text()
        title, body = raw.split('\n', 1)
        first_p = re.search(r'<p[^>]*>(.*?)</p>', body, re.S)
        desc = re.sub(r'<[^>]+>', '', first_p.group(1)).strip() if first_p else title
        nav = ''.join(
            f'<li><a href="{s}.html"{" aria-current=\"page\"" if s == slug else ""}>{l}</a></li>'
            for s, l in NAV
        )
        pager = ''
        if i > 0:
            pager += f'<a class="prev" href="{NAV[i-1][0]}.html">← {NAV[i-1][1]}</a>'
        if i < len(NAV) - 1:
            pager += f'<a class="next" href="{NAV[i+1][0]}.html">{NAV[i+1][1]} →</a>'
        (out / f'{slug}.html').write_text(
            TEMPLATE.format(title=title.strip(), desc=desc.replace('"', '&quot;'), nav=nav, body=body, pager=pager)
        )
    print('Built', len(NAV), 'pages into', out)


if __name__ == '__main__':
    main()
