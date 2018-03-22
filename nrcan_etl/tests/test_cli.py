from click import testing
from energuide import cli

def test_nothing() -> None:
    runner = testing.CliRunner()
    result = runner.invoke(cli.main)

    assert result.exit_code == 0
