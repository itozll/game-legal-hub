const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const { test } = require('node:test');
const source = fs.readFileSync(path.join(__dirname, '../docs/meowdoku/privacy/entry.js'), 'utf8');

function route(search = '', languages = ['en'], language = 'en') {
    let destination;
    vm.runInNewContext(source, {
        URL, URLSearchParams,
        document: { currentScript: { src: 'https://example.test/game-legal-hub/meowdoku/privacy/entry.js' } },
        navigator: { languages, language },
        window: { location: { search, replace: value => { destination = value; } } },
    });
    return destination;
}

test('explicit game language wins over browser language for all supported locales', () => {
    for (const locale of ['en', 'zh-Hans', 'zh-Hant', 'ja', 'ko', 'es', 'pt', 'ru']) {
        assert.equal(route('?lang=' + locale, ['de', 'fr']), `https://example.test/game-legal-hub/meowdoku/privacy/${locale}.html`);
    }
});

test('browser regional and script variants select the matching policy', () => {
    for (const [input, expected] of [
        ['en-GB', 'en'], ['zh-CN', 'zh-Hans'], ['zh-SG', 'zh-Hans'],
        ['zh-TW', 'zh-Hant'], ['zh-HK', 'zh-Hant'], ['zh-MO', 'zh-Hant'],
        ['zh-Hans-HK', 'zh-Hans'], ['zh-Hant-CN', 'zh-Hant'],
        ['JA_jp', 'ja'], ['ko-KR', 'ko'], ['es-MX', 'es'], ['pt-BR', 'pt'], ['pt-PT', 'pt'], ['ru-RU', 'ru'], ['ru-BY', 'ru'], ['RU_ru', 'ru'],
    ]) assert.equal(route('', [input]).split('/').pop(), expected + '.html');
});

test('uses the first supported browser preference and falls back to English', () => {
    assert.equal(route('', ['fr-FR', 'ja-JP', 'en-US']).split('/').pop(), 'ja.html');
    assert.equal(route('', ['fr-FR', 'de-DE']).split('/').pop(), 'en.html');
    assert.equal(route('', [], 'ko-KR').split('/').pop(), 'ko.html');
    assert.equal(route('', null, 'es-ES').split('/').pop(), 'es.html');
});

test('blank language uses browser preference; invalid explicit language is safe', () => {
    assert.equal(route('?lang=', ['pt-BR']).split('/').pop(), 'pt.html');
    assert.equal(route('?lang=%20%20', ['ja']).split('/').pop(), 'ja.html');
    assert.equal(route('?lang=fr', ['ja']).split('/').pop(), 'en.html');
    assert.equal(route('?lang=https%3A%2F%2Fevil.example%2F', ['ja']).split('/').pop(), 'en.html');
    assert.equal(route('?lang=zhfoo', ['ja']).split('/').pop(), 'en.html');
});

test('manual selection does not redirect even with an explicit language', () => {
    assert.equal(route('?select=1&lang=ko', ['ja']), undefined);
});

test('all registered privacy locales have a routable page and source', () => {
    const registry = JSON.parse(fs.readFileSync(path.join(__dirname, '../registry.json'), 'utf8'));
    const game = registry.games.find(game => game.id === 'meowdoku');
    for (const [locale, policies] of Object.entries(game.locales)) {
        if (policies['privacy-policy'].status === 'missing') continue;
        const canonical = locale === 'zh-CN' ? 'zh-Hans' : locale;
        assert.equal(route('?lang=' + locale).split('/').pop(), canonical + '.html');
        for (const extension of ['md', 'html']) {
            assert.ok(fs.existsSync(path.join(__dirname, '../docs/meowdoku/privacy', locale + '.' + extension)), 'Missing policy: ' + locale + '.' + extension);
        }
    }
});
