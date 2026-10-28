import pipecat


def test_pipecat_version_is_pinned():
    assert pipecat.__version__ == "1.14.0"
