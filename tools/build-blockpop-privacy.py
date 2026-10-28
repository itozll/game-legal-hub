"""Build BlockPop policy reading pages from canonical Markdown; no external packages."""
import argparse
import html
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'docs/blockpop'
LOCALES = ('zh-CN', 'en', 'ru', 'ar')
STYLE = ':root{color-scheme:light}*{box-sizing:border-box}body{margin:0;background:#f5f7f4;color:#203d48;font:17px/1.8 system-ui,sans-serif}main{max-width:820px;margin:32px auto;padding:32px;background:white;border:1px solid #dce5df;border-radius:18px}a{color:#176d70;text-underline-offset:3px}a:focus-visible{outline:3px solid #e0a933;outline-offset:4px}h1{font-size:2rem;line-height:1.3}h2{margin-top:2rem;font-size:1.25rem;line-height:1.5}p,li{overflow-wrap:anywhere}html[dir=rtl] article{text-align:start}@media(max-width:600px){main{margin:0;padding:24px 20px;border:0;border-radius:0}h1{font-size:1.7rem}}'

def inline(text):
    escaped = html.escape(text)
    return re.sub(r'\[([^\]]+)\]\(([^\s)]+)\)', r'<a href="\2">\1</a>', escaped)

def markdown(text):
    output = []
    for block in text.strip().split('\n\n'):
        lines = block.splitlines()
        if all(line.startswith('- ') for line in lines):
            output.append('<ul>' + ''.join('<li>' + inline(line[2:]) + '</li>' for line in lines) + '</ul>')
        elif block.startswith('## '):
            output.append('<h2>' + inline(block[3:]) + '</h2>')
        elif block.startswith('# '):
            output.append('<h1>' + inline(block[2:]) + '</h1>')
        else:
            output.append('<p>' + '<br>'.join(map(inline, lines)) + '</p>')
    return '\n'.join(output)

def page(locale, title, content):
    direction = 'rtl' if locale == 'ar' else 'ltr'
    return ('<!doctype html>\n<html lang="' + locale + '" dir="' + direction + '">\n<head>\n'
            '<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            '<meta name="referrer" content="no-referrer">\n<title>' + html.escape(title) + '</title>\n'
            '<style>' + STYLE + '</style>\n</head>\n<body><main><article>\n' + content +
            '\n</article></main></body>\n</html>\n')

def outputs():
    files = {}
    for locale in LOCALES:
        source = SITE / locale / 'privacy-policy.md'
        text = source.read_text(encoding='utf-8')
        files[source.with_suffix('.html')] = page(locale, text.splitlines()[0][2:], markdown(text))
    notes = (SITE / 'README.md').read_text(encoding='utf-8')
    files[SITE / 'publication-notes.html'] = page('zh-CN', 'BlockPop 发布核对说明', markdown(notes))
    content = ('<h1>BlockPop / 方块泡泡 / بلوك بوب</h1>\n'
               '<p>Draft privacy policies — not yet effective.<br>四语隐私政策草案，尚未生效。</p>\n'
               '<ul><li><a href="zh-CN/privacy-policy.html" lang="zh-CN">简体中文 · 隐私政策</a></li>'
               '<li><a href="en/privacy-policy.html" lang="en">English · Privacy Policy</a></li>'
               '<li><a href="ru/privacy-policy.html" lang="ru">Русский · Политика конфиденциальности</a></li>'
               '<li><a href="ar/privacy-policy.html" lang="ar" dir="rtl">العربية · سياسة الخصوصية</a></li></ul>\n'
               '<p><a href="publication-notes.html">发布核对说明 / Publication checklist</a></p>')
    files[SITE / 'index.html'] = page('en', 'BlockPop · Privacy policy drafts', content)
    return files

def build(check=False):
    generated = outputs()
    for target, content in generated.items():
        if check:
            if not target.is_file() or target.read_text(encoding='utf-8') != content:
                raise ValueError('Outdated generated page: ' + str(target.relative_to(ROOT)))
        else:
            target.write_text(content, encoding='utf-8', newline='\n')
    return len(generated)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    print('OK:', build(args.check), 'BlockPop generated pages' + (' verified' if args.check else ' written'))
