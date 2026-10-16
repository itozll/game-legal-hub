from pathlib import Path
import html
import re

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'docs/meowdoku'
POLICY = SITE / 'privacy'
# Policy locales include every game locale plus additional translations.
LOCALES = [
    ('en', 'English', 'Meow Garden Privacy Policy', 'Home', 'Language', 'Skip to content'),
    ('zh-Hans', '简体中文', 'Meow Garden 隐私保护指引', '首页', '语言', '跳至正文'),
    ('zh-Hant', '繁體中文', 'Meow Garden 隱私保護指引', '首頁', '語言', '跳至正文'),
    ('ja', '日本語', 'Meow Garden プライバシーポリシー', 'ホーム', '言語', '本文へ移動'),
    ('ko', '한국어', 'Meow Garden 개인정보 처리방침', '홈', '언어', '본문으로 이동'),
    ('es', 'Español', 'Política de privacidad de Meow Garden', 'Inicio', 'Idioma', 'Ir al contenido'),
    ('pt', 'Português', 'Política de Privacidade do Meow Garden', 'Início', 'Idioma', 'Ir para o conteúdo'),
    ('ru', 'Русский', 'Политика конфиденциальности Meow Garden', 'Главная', 'Язык', 'Перейти к содержимому'),
]


def inline(text):
    text = html.escape(text)
    return re.sub(r'\[([^\]]+)\]\((https://[^\s)]+)\)', r'<a href="\2" rel="noreferrer">\1</a>', text)


def markdown(text):
    output, listing = [], False
    for line in text.splitlines():
        if listing and not line.startswith('- '):
            output.append('</ul>')
            listing = False
        if not line.strip():
            continue
        if line.startswith('- '):
            if not listing:
                output.append('<ul>')
                listing = True
            output.append('<li>' + inline(line[2:]) + '</li>')
        elif line.startswith('## '):
            output.append('<h2>' + inline(line[3:]) + '</h2>')
        elif line.startswith('# '):
            output.append('<h1>' + inline(line[2:]) + '</h1>')
        else:
            output.append('<p>' + inline(line) + '</p>')
    if listing:
        output.append('</ul>')
    return '\n'.join(output)


def language_links(prefix='', current=None):
    return ''.join(
        f'<a href="{prefix}{code}.html" lang="{code}" hreflang="{code}"'
        + (' aria-current="page"' if code == current else '')
        + f'>{name}</a>' for code, name, *_ in LOCALES
    )


def page(lang, title, content, navigation, stylesheet, skip, head=''):
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="referrer" content="no-referrer">
<title>{html.escape(title)}</title>
<link rel="stylesheet" href="{stylesheet}">
{head}
</head>
<body>
<a class="skip" href="#content">{skip}</a>
<header><span class="brand">Meow Garden</span>{navigation}</header>
<main id="content">{content}</main>
<footer>Meow Garden · Privacy</footer>
</body>
</html>
'''


def build():
    for code, name, title, home_label, language_label, skip in LOCALES:
        canonical = SITE / ('zh-CN' if code == 'zh-Hans' else code) / 'privacy-policy.md'
        source = canonical.read_text(encoding='utf-8-sig')
        (POLICY / f'{code}.md').write_bytes(canonical.read_bytes())
        if code == 'zh-Hans':
            (SITE / 'zh-Hans/privacy-policy.md').write_bytes(canonical.read_bytes())
        navigation = f'<div class="navigation"><a href="index.html?select=1">{home_label}</a><details class="language-menu"><summary>{language_label} · {name}</summary><nav aria-label="{language_label}">{language_links(current=code)}</nav></details></div>'
        head = ''.join(f'<link rel="alternate" hreflang="{other}" href="{other}.html">' for other, *_ in LOCALES)
        rendered = page(code, title, markdown(source), navigation, 'style.css', skip, head)
        (POLICY / f'{code}.html').write_text(rendered, encoding='utf-8', newline='\n')
        if code == 'zh-Hans':
            # Preserve links delivered before the canonical game locale was used.
            (POLICY / 'zh-CN.md').write_bytes(canonical.read_bytes())
            (POLICY / 'zh-CN.html').write_text(rendered, encoding='utf-8', newline='\n')
    for directory, prefix in [(SITE, 'privacy/'), (POLICY, '')]:
        choices = ''.join(f'<a href="{prefix}{code}.html" lang="{code}" hreflang="{code}">{name}</a>' for code, name, *_ in LOCALES)
        content = f'''<h1>Meow Garden 隐私协议</h1>
<p class="subtitle" lang="en">Privacy Policy</p>
<p>正在根据语言打开对应协议。你也可以手动选择语言。</p>
<p lang="en">Opening the policy in your language. You can also choose a language below.</p>
<div class="languages">{choices}</div>
<noscript><p>请选择语言查看协议。JavaScript is disabled; choose a language above.</p></noscript>'''
        head = f'<script src="{prefix}entry.js" defer></script>'
        navigation = '<a href="?select=1">选择语言 · Choose language</a>'
        (directory / 'index.html').write_text(page('zh-Hans', 'Meow Garden Privacy Policy', content, navigation, prefix + 'style.css', '跳至正文 / Skip to content', head), encoding='utf-8', newline='\n')
    (ROOT / 'docs/.nojekyll').write_text('', encoding='utf-8', newline='\n')


if __name__ == '__main__':
    build()
