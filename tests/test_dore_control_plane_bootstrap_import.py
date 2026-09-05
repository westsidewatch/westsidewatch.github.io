import unittest

from dore_core.control_plane.bootstrap import build_local_design_control_plane


class ResidentBootstrapImportTests(unittest.TestCase):
    def test_bootstrap_imports_without_package_level_runtime_exports(self):
        self.assertTrue(callable(build_local_design_control_plane))


if __name__ == "__main__":
    unittest.main()
