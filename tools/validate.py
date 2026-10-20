"""Validate registry metadata, local links and optional migration integrity.

Run: python -X utf8 tools/validate.py [--migration-source ../meowdoku-legal]
Only --migration-source permits reading a sibling repository.
Use it immediately after migration to verify the original Git snapshot.
"""
import argparse
import datetime as dt
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import hashlib
import subprocess
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
KINDS = ('privacy-policy', 'terms-of-service')
DRAFT_NOTICES = {
    'en': 'Status: Draft',
    'zh-CN': '状态：待发布草案',
    'zh-Hans': '状态：待发布草案',
    'zh-Hant': '狀態：待發布草案',
    'ja': '状態：公開に向けた草案（未発効）',
    'ko': '상태: 게시를 위한 초안(아직 효력이 없음)',
    'es': 'Estado: Borrador para publicación (todavía no vigente)',
    'pt': 'Estado: Rascunho para publicação (ainda sem vigência)',
    'ru': 'Статус: Проект для публикации (ещё не вступил в силу)',
}


def check(condition, message):
    if not condition:
        raise ValueError(message)


def inside(path):
    resolved = path.resolve()
    check(resolved.is_relative_to(ROOT), f'Path outside legal hub: {path}')
    return resolved


def date(value, label):
    check(isinstance(value, str), f'Missing date: {label}')
    check(dt.date.fromisoformat(value).isoformat() == value, f'Invalid date: {label}')


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.targets = []

    def handle_starttag(self, tag, attrs):
        self.targets.extend(value for key, value in attrs if key in ('href', 'src') and value)


def validate():
    registry = json.loads((ROOT / 'registry.json').read_text(encoding='utf-8'))
    check(registry['schema_version'] == 1, 'Unsupported schema version')
    check((ROOT / 'docs/.nojekyll').is_file(), 'Missing publishing .nojekyll')
    check((ROOT / 'docs/index.html').is_file(), 'Missing publishing index')
    check(not (ROOT / 'games').exists(), 'Obsolete games directory')
    ids = set()
    paths = set()
    count = 0
    for game in registry['games']:
        game_id = game['id']
        check(re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', game_id), f'Invalid id: {game_id}')
        check(game_id not in ids, f'Duplicate game: {game_id}')
        ids.add(game_id)
        check(bool(game['name']) and bool(game['locales']), f'Empty game: {game_id}')
        if game.get('legacy_entry'):
            check(inside(ROOT / game['legacy_entry']).is_file(), f'Missing legacy entry: {game_id}')
        for locale, policies in game['locales'].items():
            check(set(policies) == set(KINDS), f'Policy kinds missing: {game_id}/{locale}')
            for kind, policy in policies.items():
                label = f'{game_id}/{locale}/{kind}'
                status = policy['status']
                check(status in ('published', 'draft', 'missing'), f'Invalid status: {label}')
                if status == 'missing':
                    check(all(policy[key] is None for key in ('path', 'version', 'updated_date', 'effective_date')), f'Missing policy has metadata: {label}')
                    continue
                expected = f'docs/{game_id}/{locale}/{kind}.md'
                check(policy['path'] == expected, f'Unexpected path: {label}')
                path = inside(ROOT / expected)
                check(path.is_file(), f'File missing: {expected}')
                check(expected not in paths, f'Duplicate file: {expected}')
                paths.add(expected)
                text = path.read_text(encoding='utf-8')
                check(text.startswith('# ') and '{{' not in text, f'Incomplete policy: {expected}')
                check(bool(policy['version']), f'Missing version: {label}')
                date(policy['updated_date'], label)
                if status == 'published':
                    date(policy['effective_date'], label)
                    effective = dt.date.fromisoformat(policy['effective_date'])
                    en_date = f'{effective.strftime("%B")} {effective.day}, {effective.year}'
                    zh_date = f'{effective.year}年{effective.month}月{effective.day}日'
                    ko_date = f'{effective.year}년 {effective.month}월 {effective.day}일'
                    es_months = ('enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre')
                    pt_months = ('janeiro','fevereiro','março','abril','maio','junho','julho','agosto','setembro','outubro','novembro','dezembro')
                    ru_months = ('января','февраля','марта','апреля','мая','июня','июля','августа','сентября','октября','ноября','декабря')
                    ru_date = f'{effective.day} {ru_months[effective.month-1]} {effective.year} года'
                    romance_dates = tuple(f'{effective.day} de {months[effective.month-1]} de {effective.year}' for months in (es_months,pt_months))
                    check(any(value in text for value in (policy['effective_date'], en_date, zh_date, ko_date, ru_date, *romance_dates)), f'Effective date absent from text: {label}')
                else:
                    check(policy['effective_date'] is None, f'Draft has effective date: {label}')
                    check(policy['version'] in text, f'Draft version mismatch: {label}')
                    check(policy['updated_date'] in text, f'Draft date mismatch: {label}')
                    check(locale in DRAFT_NOTICES and DRAFT_NOTICES[locale] in text, f'Draft notice absent: {label}')
                count += 1
        for alias, target in game.get('language_aliases', {}).items():
            check(alias in game['locales'] and target in game['locales'], f'Invalid language alias: {game_id}')
            for kind in KINDS:
                first = game['locales'][alias][kind]
                second = game['locales'][target][kind]
                check(first['status'] == second['status'], f'Alias status mismatch: {game_id}/{kind}')
                if first['path']:
                    check((ROOT / first['path']).read_text(encoding='utf-8') == (ROOT / second['path']).read_text(encoding='utf-8'), f'Alias text mismatch: {game_id}/{kind}')
    actual = {str(path.relative_to(ROOT)).replace('\\', '/') for path in (ROOT / 'docs').glob('*/*/*.md') if path.stem in KINDS}
    check(actual == paths, f'Unregistered or absent policies: {actual ^ paths}')
    for path in (ROOT / 'docs/meowdoku').glob('*/privacy-policy.md'):
        original = ROOT / 'docs/meowdoku/privacy' / (path.parent.name + '.md')
        check(path.read_bytes() == original.read_bytes(), f'Canonical and legacy text differ: {path}')
    for path in ROOT.rglob('*'):
        if not path.is_file() or path.suffix not in ('.md', '.html') or '.git' in path.parts:
            continue
        text = path.read_text(encoding='utf-8')
        if path.suffix == '.html':
            parser = Links()
            parser.feed(text)
            targets = parser.targets
        else:
            targets = re.findall(r'\[[^\]]*\]\(([^)]+)\)', text)
        for target in targets:
            url = urlsplit(target)
            if url.scheme or url.netloc or not url.path:
                continue
            check(not url.path.startswith('/'), f'Root-relative link: {path}: {target}')
            resolved = inside(path.parent / unquote(url.path))
            check(resolved.exists(), f'Broken link: {path.relative_to(ROOT)}: {target}')
    return count


def validate_migration(source):
    source = source.resolve()
    manifest_path = ROOT / 'references/meowdoku/cocos-migration.json'
    if source.name == 'meowdoku-cocos':
        manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
        for record in manifest['files']:
            # The working tree now contains redirects; compare the pre-migration Git snapshot.
            original = subprocess.check_output(['git', '-C', str(source), 'show', manifest['source_revision'] + ':' + record['source']])
            check(hashlib.sha256(original).hexdigest() == record['sha256'], f'Source snapshot mismatch: {record["source"]}')
            for target in record['targets']:
                check(original == inside(ROOT / target).read_bytes(), f'Migration differs: {target}')
        return len(manifest['files'])
    check((source / 'privacy').is_dir(), f'Invalid migration source: {source}')
    # Original text remains unchanged; generated HTML now includes the added Russian locale.
    originals = [path for path in (source / 'privacy').glob('*.md') if path.stem != 'README']
    for path in originals:
        canonical = ROOT / 'docs/meowdoku' / path.stem / 'privacy-policy.md'
        check(canonical.is_file() and canonical.read_bytes() == path.read_bytes(), f'Locale migration differs: {path.stem}')
    return len(originals)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--migration-source', type=Path)
    args = parser.parse_args()
    try:
        count = validate()
        print(f'OK: registry, {count} policies, statuses, dates, aliases and local links')
        if args.migration_source:
            files = validate_migration(args.migration_source)
            print(f'OK: {files} original policy/template files preserved byte-for-byte')
    except (ValueError, KeyError, TypeError, OSError) as error:
        parser.exit(1, f'Validation failed: {error}\n')
