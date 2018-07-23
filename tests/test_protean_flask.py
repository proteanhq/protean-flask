"""Tests for Protean Flask's main method"""

from click.testing import CliRunner

from protean_flask.cli import main


def test_main():
    """Test Main method"""
    runner = CliRunner()
    result = runner.invoke(main, [])

    assert result.output == '()\n'
    assert result.exit_code == 0
