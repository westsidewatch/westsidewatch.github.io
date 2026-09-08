from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from dore_core.substrates import longmemory, qmd


class ManagedSubstrateRuntimeTests(unittest.TestCase):
    def test_qmd_managed_wrapper_is_found_without_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            wrapper = Path(tmp) / "qmd"
            wrapper.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
            with patch.object(qmd, "_MANAGED_BIN", wrapper), \
                 patch.dict(qmd.os.environ, {}, clear=True), \
                 patch.object(qmd.shutil, "which", return_value=None):
                self.assertTrue(qmd.available())
                self.assertEqual(qmd.resolve_binary(), str(wrapper))

    def test_longmemory_managed_wrapper_is_found_without_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            wrapper = Path(tmp) / "longmemory"
            wrapper.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
            with patch.object(longmemory, "_MANAGED_BIN", wrapper), \
                 patch.dict(longmemory.os.environ, {}, clear=True), \
                 patch.object(longmemory.shutil, "which", return_value=None):
                self.assertTrue(longmemory.available())
                self.assertEqual(longmemory.resolve_binary(), str(wrapper))

    def test_explicit_env_binary_precedes_managed_wrapper(self):
        with tempfile.TemporaryDirectory() as tmp:
            configured = Path(tmp) / "configured-qmd"
            managed = Path(tmp) / "managed-qmd"
            configured.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
            managed.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
            with patch.object(qmd, "_MANAGED_BIN", managed), \
                 patch.dict(qmd.os.environ, {"DORE_QMD_BIN": str(configured)}, clear=True):
                self.assertEqual(qmd.resolve_binary(), str(configured))


if __name__ == "__main__":
    unittest.main()
