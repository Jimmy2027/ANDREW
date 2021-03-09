# -*- coding: utf-8 -*-

import unittest


class TestNorby(unittest.TestCase):
    """Tests for norby package."""

    def test_import(self):
        """Tests the import from the norby package."""
        import norby
        from norby import utils
        from norby import send_msg
