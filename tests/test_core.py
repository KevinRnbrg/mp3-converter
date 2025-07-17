import yt_downloader.core as core
import pytest
from pytubefix import YouTube

valid_url = "https://www.youtube.com/watch?v=dvgZkm1xWPE&ab_channel=Coldplay"

class TestCore:
    def test_validate_url_success(self):
        core.validate_url(valid_url)
    
    def test_validate_url_exception_scheme(self):
        with pytest.raises(Exception):
            url = "http://www.youtube.com/watch?v=dvgZkm1xWPE&ab_channel=Coldplay"
            core.validate_url(url)
            
    def test_validate_url_exception_netloc(self):
        with pytest.raises(Exception):
            url = "http://www.youtube.net/watch?v=dvgZkm1xWPE&ab_channel=Coldplay"
            core.validate_url(url)

    def test_validate_url_exception_path(self):
        with pytest.raises(Exception):
            url = "http://www.youtube.com/video?v=dvgZkm1xWPE&ab_channel=Coldplay"
            core.validate_url(url)
            
    def test_create_youtube_object_success(self):
        result = core.create_youtube_object(valid_url)
        assert type(result) is YouTube

    def test_create_youtube_object_fail(self):
        with pytest.raises(Exception):
            url = "https://www.youtube.com/wat?v=dvgZkm1xWPE&ab_channel=Coldplay"
            result = core.create_youtube_object(url)
            assert type(result) is None

    # def test_write_audio_file_from_video(self):
    #     core.write_audio_file_from_video()