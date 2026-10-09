#!/usr/bin/env python3
"""Regression tests for editorial portrait conditioning contract; no local model required."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from dore_speaker_editorial_quality import build_reference_profile
from dore_speaker_image_backend import generate

class EditorialPortraitTests(unittest.TestCase):
    def test_reference_required(self):
        with self.assertRaises(ValueError):
            build_reference_profile({'slug':'david-pawson'}, '/nonexistent/photo.jpg')

    def test_reference_profile_is_explicitly_not_published(self):
        with tempfile.TemporaryDirectory() as folder:
            photo=Path(folder)/'photo.png'
            photo.write_bytes(b'reference-test')
            spec=build_reference_profile({'slug':'david-pawson'},photo)
            self.assertTrue(spec['requiresReferenceConditioning'])
            self.assertFalse(spec['publishAutomatically'])
            self.assertEqual(spec['typography'],'LIVE_HTML_CSS_ONLY')

    def test_text_only_backend_rejects_reference_job_before_generation(self):
        with tempfile.TemporaryDirectory() as folder:
            directory=Path(folder)
            photo=directory/'reference.png'
            photo.write_bytes(b'example image')
            (directory/'image-prompt.txt').write_text('portrait',encoding='utf-8')
            (directory/'editorial-quality.json').write_text(json.dumps({
                'requiresReferenceConditioning':True,'referenceImage':str(photo)
            }))
            from unittest.mock import MagicMock
            health_response=MagicMock()
            health_response.__enter__.return_value.read.return_value=b'{"model_backed":true}'
            with patch('dore_speaker_image_backend.urlopen',return_value=health_response) as remote:
                with self.assertRaisesRegex(RuntimeError,'REFERENCE_CONDITIONING_UNSUPPORTED'):
                    generate(directory/'image-prompt.txt',directory/'output.png')
                self.assertFalse((directory/'output.png').exists())
                self.assertEqual(remote.call_count,1)

    def test_reference_image_is_sent_only_with_advertised_capability(self):
        with tempfile.TemporaryDirectory() as folder:
            directory=Path(folder)
            photo=directory/'reference.png'
            photo.write_bytes(b'example image')
            (directory/'image-prompt.txt').write_text('portrait',encoding='utf-8')
            (directory/'editorial-quality.json').write_text(json.dumps({
                'requiresReferenceConditioning':True,'referenceImage':str(photo)
            }))
            from unittest.mock import MagicMock
            health_response=MagicMock()
            health_response.__enter__.return_value.read.return_value=(
                b'{"model_backed":true,"capabilities":{"reference_image":true}}')
            generated=MagicMock()
            generated.__enter__.return_value.read.return_value=(
                b'{"ok":true,"model_backed":true,"reference_conditioned":false}')
            with patch('dore_speaker_image_backend.urlopen',side_effect=[health_response,generated]) as remote:
                with self.assertRaisesRegex(RuntimeError,'did not confirm reference-conditioned'):
                    generate(directory/'image-prompt.txt',directory/'output.png')
                payload=json.loads(remote.call_args_list[1].args[0].data)
                self.assertEqual(payload['mode'],'image_to_image')
                self.assertEqual(payload['reference_image']['mime_type'],'image/png')
                self.assertTrue(payload['reference_image']['data_base64'])
                self.assertFalse((directory/'output.png').exists())

if __name__=='__main__':
    unittest.main()
