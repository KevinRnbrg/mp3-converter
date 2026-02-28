"""Shared pytest fixtures for yt_downloader tests."""

import pytest


@pytest.fixture
def valid_youtube_url() -> str:
    return "https://www.youtube.com/watch?v=dvgZkm1xWPE&ab_channel=Coldplay"


@pytest.fixture
def invalid_scheme_url() -> str:
    return "http://www.youtube.com/watch?v=dvgZkm1xWPE&ab_channel=Coldplay"


@pytest.fixture
def invalid_netloc_url() -> str:
    return "https://www.youtube.net/watch?v=dvgZkm1xWPE&ab_channel=Coldplay"


@pytest.fixture
def invalid_path_url() -> str:
    return "https://www.youtube.com/video?v=dvgZkm1xWPE&ab_channel=Coldplay"


@pytest.fixture
def invalid_path_watch_url() -> str:
    return "https://www.youtube.com/wat?v=dvgZkm1xWPE&ab_channel=Coldplay"
