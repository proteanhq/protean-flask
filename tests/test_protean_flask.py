"""Tests for Protean Flask's main method"""

from click.testing import CliRunner

from protean_flask.cli import main


def test_main():
    """Test Main method"""
    runner = CliRunner()
    result = runner.invoke(main, [])

    assert 'Utility commands for the Protean-Flask package' in result.output
    assert result.exit_code == 0
