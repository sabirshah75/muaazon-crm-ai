import importlib.util
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

HERE = Path(__file__).resolve().parents[1] / 'tools' / 'brand_runtime.py'
spec = importlib.util.spec_from_file_location('brand_runtime', HERE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class BrandingOverlayTests(unittest.TestCase):
    def test_compile_only_patch_preserves_js_asset(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            base = root / 'base'
            out = root / 'out'
            base.mkdir()
            original = '''<html><head><title>Twenty</title><meta name="theme-color" content="#000000" />
<meta name="description" content="A modern open-source CRM" />
<meta property="og:title" content="Twenty" />
<meta name="twitter:title" content="Twenty" />
<script type="module" src="/assets/index-TEST.js"></script></head></html>'''
            (base / 'index.html').write_text(original)
            (base / 'manifest.json').write_text(json.dumps({'name':'Twenty','icons':[{'src':'a.png'}]}))
            mod.apply_branding(base, out)
            html = (out / 'index.html').read_text()
            manifest = json.loads((out / 'manifest.json').read_text())
            self.assertIn('<title>Muaazon CRM AI</title>', html)
            self.assertIn('/assets/index-TEST.js', html)
            self.assertEqual(manifest['name'], 'Muaazon CRM AI')
            self.assertEqual(manifest['icons'], [{'src': 'a.png'}])
            self.assertEqual((base / 'index.html').read_text(), original)
    def test_refuse_uncompiled_index(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'index.html').write_text('<title>Twenty</title><script src="/src/index.tsx"></script>')
            (root / 'manifest.json').write_text('{}')
            with self.assertRaisesRegex(ValueError, 'compiled'):
                mod.apply_branding(root, root / 'out')

if __name__ == '__main__':
    unittest.main()
