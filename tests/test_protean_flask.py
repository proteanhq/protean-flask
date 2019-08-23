"""Tests for Protean Flask's main method"""

from click.testing import CliRunner

from protean_flask.cli import main

from .support.sample_app import app


def test_main():
    """Test Main method"""
    runner = CliRunner()
    result = runner.invoke(main, [])

    assert 'Utility commands for the Protean-Flask package' in result.output
    assert result.exit_code == 0


def test_protean_context():
    """ Test that the protean context value gets set"""
    client = app.test_client()
    rv = client.get('/current-context')
    assert rv.status_code == 200
    assert rv.json == {
        'host_url': 'http://localhost/',
        'remote_addr': '127.0.0.1',
        'tenant_id': 'localhost',
        'url': 'http://localhost/current-context',
        'user_agent': 'werkzeug/0.15.5',
        'user_agent_hash': '4065e0471cee81c2f0845a4e59c834bae3351b96c84ddf6b1f8d6f803ec1dba4'
    }
