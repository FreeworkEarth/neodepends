#!/usr/bin/env python3
"""Unit tests for resolve_shadow_imports.py.

Tests the two core functions:
  1. _project_shadow_targets — census of project files that shadow stdlib names
  2. _source_has_qualified_import — AST check for qualified vs bare imports

No careship-specific literals — all tests use synthetic file/module names.
"""

import sys
import unittest
from pathlib import Path

# Add tools/ to path so we can import the module under test.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

from resolve_shadow_imports import (
    _project_shadow_targets,
    _source_has_qualified_import,
    _stdlib_module_names,
)

STDLIB = _stdlib_module_names()


class TestProjectShadowTargets(unittest.TestCase):
    """Test _project_shadow_targets census logic."""

    def test_nested_shadow_detected(self):
        """A nested file whose name matches stdlib IS a shadow target."""
        files = ["myapp/logging.py", "myapp/main.py", "myapp/utils.py"]
        result = _project_shadow_targets(files, None, STDLIB)
        self.assertIn("myapp/logging.py", result)
        self.assertEqual(result["myapp/logging.py"], "logging")

    def test_top_level_flat_shadow_skipped(self):
        """A top-level file (no package nesting) is NOT a shadow target.
        This is real Python shadowing (the classic beginner bug)."""
        files = ["logging.py", "main.py"]
        result = _project_shadow_targets(files, None, STDLIB)
        self.assertNotIn("logging.py", result)

    def test_init_py_skipped(self):
        """__init__.py files are never shadow targets."""
        files = ["myapp/__init__.py", "myapp/logging/__init__.py"]
        result = _project_shadow_targets(files, None, STDLIB)
        self.assertEqual(result, {})

    def test_non_stdlib_name_skipped(self):
        """A nested file with a non-stdlib name is not a target."""
        files = ["myapp/service.py", "myapp/models.py"]
        result = _project_shadow_targets(files, None, STDLIB)
        self.assertEqual(result, {})

    def test_multiple_shadows(self):
        """Multiple stdlib-named files all detected."""
        files = ["pkg/logging.py", "pkg/json.py", "pkg/email.py", "pkg/app.py"]
        result = _project_shadow_targets(files, None, STDLIB)
        self.assertEqual(len(result), 3)
        self.assertEqual(result["pkg/logging.py"], "logging")
        self.assertEqual(result["pkg/json.py"], "json")
        self.assertEqual(result["pkg/email.py"], "email")

    def test_deeply_nested_shadow(self):
        """Shadow detection works for deeply nested files."""
        files = ["pkg/sub/deep/logging.py"]
        result = _project_shadow_targets(files, None, STDLIB)
        self.assertIn("pkg/sub/deep/logging.py", result)


class TestSourceHasQualifiedImport(unittest.TestCase):
    """Test _source_has_qualified_import AST analysis."""

    def test_bare_import_is_not_qualified(self):
        """import logging → bare stdlib, NOT qualified."""
        src = "import logging\nlogger = logging.getLogger(__name__)"
        self.assertFalse(_source_has_qualified_import(src, "logging", "myapp/logging.py"))

    def test_bare_import_submodule_is_not_qualified(self):
        """import logging.handlers → still stdlib, NOT qualified."""
        src = "import logging.handlers"
        self.assertFalse(_source_has_qualified_import(src, "logging", "myapp/logging.py"))

    def test_from_stdlib_import_is_not_qualified(self):
        """from logging import getLogger → bare stdlib."""
        src = "from logging import getLogger"
        self.assertFalse(_source_has_qualified_import(src, "logging", "myapp/logging.py"))

    def test_from_stdlib_submodule_is_not_qualified(self):
        """from logging.handlers import RotatingFileHandler → stdlib submodule."""
        src = "from logging.handlers import RotatingFileHandler"
        self.assertFalse(_source_has_qualified_import(src, "logging", "myapp/logging.py"))

    def test_qualified_dotted_import(self):
        """import myapp.logging → qualified (first component != target)."""
        src = "import myapp.logging"
        self.assertTrue(_source_has_qualified_import(src, "logging", "myapp/logging.py"))

    def test_qualified_from_package_import(self):
        """from myapp import logging → qualified."""
        src = "from myapp import logging"
        self.assertTrue(_source_has_qualified_import(src, "logging", "myapp/logging.py"))

    def test_qualified_from_package_dot_module(self):
        """from myapp.logging import setup → qualified."""
        src = "from myapp.logging import setup"
        self.assertTrue(_source_has_qualified_import(src, "logging", "myapp/logging.py"))

    def test_relative_import_dot(self):
        """from . import logging → relative, genuine."""
        src = "from . import logging"
        self.assertTrue(_source_has_qualified_import(src, "logging", "myapp/logging.py"))

    def test_relative_import_dotmodule(self):
        """from .logging import setup → relative, genuine."""
        src = "from .logging import setup"
        self.assertTrue(_source_has_qualified_import(src, "logging", "myapp/logging.py"))

    def test_relative_import_parent(self):
        """from .. import logging → relative, genuine."""
        src = "from .. import logging"
        self.assertTrue(_source_has_qualified_import(src, "logging", "myapp/logging.py"))

    def test_syntax_error_treated_as_phantom(self):
        """Unparseable source → conservative: not qualified (phantom)."""
        src = "def ("
        self.assertFalse(_source_has_qualified_import(src, "logging", "myapp/logging.py"))

    def test_no_import_at_all(self):
        """File that doesn't import the module at all → not qualified."""
        src = "x = 1\nprint(x)"
        self.assertFalse(_source_has_qualified_import(src, "logging", "myapp/logging.py"))

    def test_mixed_bare_and_qualified(self):
        """File with BOTH bare and qualified import → qualified wins (genuine edge)."""
        src = "import logging\nfrom myapp import logging as app_logging"
        self.assertTrue(_source_has_qualified_import(src, "logging", "myapp/logging.py"))


if __name__ == "__main__":
    unittest.main()
