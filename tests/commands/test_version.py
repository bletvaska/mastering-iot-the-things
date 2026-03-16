import pytest
from commands.version import Version


@pytest.fixture
def cmd(mocker):
    context = mocker.MagicMock()
    return Version(context)


class TestVersion:
    def test_name(self, cmd):
        assert cmd.name == 'version'

    def test_description(self, cmd):
        assert cmd.description == 'Show version'

    def test_prints_version(self, cmd, mocker, capsys):
        mocker.patch('commands.version.VERSION', '1.2.3')
        cmd([])
        captured = capsys.readouterr()
        assert 'Version: 1.2.3' in captured.out
