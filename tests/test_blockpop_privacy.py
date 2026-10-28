"""Verify BlockPop's four draft policies, generated pages and registry states."""
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('blockpop_policy_builder', ROOT / 'tools/build-blockpop-privacy.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)

class BlockPopPolicyTests(unittest.TestCase):
    def test_generated_pages_match_canonical_text(self):
        self.assertEqual(builder.build(check=True), 6)

    def test_arabic_is_rtl_and_pages_do_not_load_tracking_code(self):
        for locale in builder.LOCALES:
            text = (ROOT / 'docs/blockpop' / locale / 'privacy-policy.html').read_text(encoding='utf-8')
            self.assertIn('lang="' + locale + '"', text)
            self.assertIn('dir="' + ('rtl' if locale == 'ar' else 'ltr') + '"', text)
            self.assertNotIn('<script', text)
            self.assertNotIn('<iframe', text)
            self.assertNotIn('<nav', text)
            self.assertNotIn('<footer', text)

    def test_registry_has_drafts_and_no_invented_terms(self):
        registry = json.loads((ROOT / 'registry.json').read_text(encoding='utf-8'))
        games = [g for g in registry['games'] if g['id'] == 'blockpop']
        self.assertEqual(len(games), 1)
        self.assertEqual(set(games[0]['locales']), set(builder.LOCALES))
        for locale, policies in games[0]['locales'].items():
            privacy = policies['privacy-policy']
            self.assertEqual(privacy['status'], 'draft')
            self.assertIsNone(privacy['effective_date'])
            self.assertEqual(privacy['path'], 'docs/blockpop/' + locale + '/privacy-policy.md')
            self.assertEqual(policies['terms-of-service']['status'], 'missing')
            for field in ['path', 'version', 'effective_date', 'updated_date']:
                self.assertIsNone(policies['terms-of-service'][field])

if __name__ == '__main__':
    unittest.main()
