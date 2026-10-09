"""Wrap build/guide.html as a standalone page and inline every screenshot as a data URI, so the
encrypted payload is the ONLY place client data exists on the public site (no stray image files).
Output: build/index.plain.html (git-ignored; never commit it)."""
import base64, pathlib, re
B = pathlib.Path(__file__).parent
src = (B / 'guide.html').read_text()
def inline(m):
    data = base64.b64encode((B / m.group(1)).read_bytes()).decode()
    return f'src="data:image/png;base64,{data}"'
src, n = re.subn(r'src="(img/[^"]+\.png)"', inline, src)
# <title>, font links and <style> belong in <head>; the rest is the body
head_end = src.index('</style>') + len('</style>')
head, body = src[:head_end], src[head_end:]
page = ('<!doctype html>\n<html lang="en-GB">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
        '<meta name="robots" content="noindex,nofollow,noarchive,nosnippet">\n'
        '<link rel="icon" href="assets/marker.png">\n' + head + '\n</head>\n<body>\n' + body + '\n</body>\n</html>\n')
(B / 'index.plain.html').write_text(page)
print(f'inlined {n} screenshots -> build/index.plain.html ({len(page):,} bytes)')
