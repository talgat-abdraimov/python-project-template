"""Sanity check ensuring pytest collects at least one test in fresh repositories."""

import src


def test_sanity():
    """Verify the src package is importable."""
    assert src is not None
