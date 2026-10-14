(() => {
    'use strict';
    const supported = ['en', 'zh-Hans', 'zh-Hant', 'ja', 'ko', 'es', 'pt'];
    function matchLocale(value) {
        const tag = String(value || '').trim().toLowerCase().replace(/_/g, '-');
        if (/^zh(?:-|$)/.test(tag)) {
            const parts = tag.split('-');
            // An explicit script takes precedence over the regional default.
            if (parts.includes('hant')) return 'zh-Hant';
            if (parts.includes('hans')) return 'zh-Hans';
            return parts.some(part => ['tw', 'hk', 'mo'].includes(part)) ? 'zh-Hant' : 'zh-Hans';
        }
        return supported.find(locale => tag === locale || tag.startsWith(locale + '-'));
    }
    const parameters = new URLSearchParams(window.location.search);
    // Keep an accessible manual selector, including when JavaScript is disabled.
    if (parameters.get('select') === '1') return;
    let locale;
    if (parameters.has('lang') && parameters.get('lang').trim()) {
        locale = matchLocale(parameters.get('lang')) || 'en';
    } else {
        const languages = navigator.languages && navigator.languages.length
            ? navigator.languages : [navigator.language];
        locale = Array.from(languages, matchLocale).find(Boolean) || 'en';
    }
    // Resolve from the script URL so both entry points work under a project subpath.
    const script = document.currentScript;
    if (!script) return;
    const target = new URL(locale + '.html', script.src);
    window.location.replace(target.href);
})();
