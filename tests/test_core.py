"""Tests for yt_downloader.core."""

import os
import pytest
from unittest.mock import patch, MagicMock
import yt_downloader.core as core
from yt_downloader.exceptions import InvalidURLError, DownloadError


class TestValidateUrl:
    def test_validate_url_success(self, valid_youtube_url: str) -> None:
        core.validate_url(valid_youtube_url)

    def test_validate_url_exception_scheme(self, invalid_scheme_url: str) -> None:
        with pytest.raises(InvalidURLError):
            core.validate_url(invalid_scheme_url)

    def test_validate_url_exception_netloc(self, invalid_netloc_url: str) -> None:
        with pytest.raises(InvalidURLError):
            core.validate_url(invalid_netloc_url)

    def test_validate_url_exception_path(self, invalid_path_url: str) -> None:
        with pytest.raises(InvalidURLError):
            core.validate_url(invalid_path_url)

    def test_validate_url_exception_path_watch(self, invalid_path_watch_url: str) -> None:
        with pytest.raises(InvalidURLError):
            core.validate_url(invalid_path_watch_url)


class TestCreateYoutubeObject:
    def test_create_youtube_object_success(self, valid_youtube_url: str) -> None:
        with patch("yt_downloader.core.YouTube") as mock_yt:
            mock_instance = MagicMock()
            mock_yt.return_value = mock_instance
            result = core.create_youtube_object(valid_youtube_url)
            mock_yt.assert_called_once_with(valid_youtube_url)
            assert result is mock_instance

    def test_create_youtube_object_fail(self, invalid_path_watch_url: str) -> None:
        with pytest.raises(InvalidURLError):
            core.create_youtube_object(invalid_path_watch_url)


class TestDownloadHighestBitrateVideo:
    def test_download_highest_bitrate_video_success(self) -> None:
        mock_stream = MagicMock()
        mock_stream.abr = "128kbps"
        mock_stream.download.return_value = "/path/to/temp_video.mp4"
        mock_streams = MagicMock()
        mock_streams.filter.return_value = [mock_stream]
        mock_yt = MagicMock()
        mock_yt.streams = mock_streams

        result = core.download_highest_bitrate_video(mock_yt)
        assert result == "/path/to/temp_video.mp4"
        mock_stream.download.assert_called_once_with(filename="temp_video.mp4")

    def test_download_highest_bitrate_video_no_audio_streams(self) -> None:
        mock_streams = MagicMock()
        mock_streams.filter.return_value = []
        mock_yt = MagicMock()
        mock_yt.streams = mock_streams
        with pytest.raises(DownloadError, match="No audio streams found"):
            core.download_highest_bitrate_video(mock_yt)


class TestCreateMp3File:
    @patch("yt_downloader.core.utils.remove_video_file")
    @patch("yt_downloader.core.write_audio_file_from_video")
    @patch("yt_downloader.core.os.path.exists")
    @patch("yt_downloader.core.os.mkdir")
    def test_create_mp3_file_creates_dir_and_calls_writer(
        self,
        mock_mkdir: MagicMock,
        mock_exists: MagicMock,
        mock_write: MagicMock,
        mock_remove: MagicMock,
    ) -> None:
        mock_exists.return_value = False
        core.create_mp3_file("/tmp/video.mp4", "Test Title")
        mock_mkdir.assert_called_once()
        mock_write.assert_called_once_with("/tmp/video.mp4", "Test Title")
        mock_remove.assert_called_once_with("/tmp/video.mp4")

    @patch("yt_downloader.core.utils.remove_video_file")
    @patch("yt_downloader.core.write_audio_file_from_video")
    @patch("yt_downloader.core.os.path.exists")
    def test_create_mp3_file_always_removes_video_on_error(
        self,
        mock_exists: MagicMock,
        mock_write: MagicMock,
        mock_remove: MagicMock,
    ) -> None:
        mock_exists.return_value = True
        mock_write.side_effect = OSError("write failed")
        with pytest.raises(OSError):
            core.create_mp3_file("/tmp/video.mp4", "Test Title")
        mock_remove.assert_called_once_with("/tmp/video.mp4")


class TestWriteAudioFileFromVideo:
    @patch("yt_downloader.core.AudioFileClip")
    @patch("yt_downloader.core.utils.get_formatted_title")
    def test_write_audio_file_from_video(
        self,
        mock_get_formatted_title: MagicMock,
        mock_audio_clip_class: MagicMock,
    ) -> None:
        mock_get_formatted_title.return_value = "Test_Title"
        mock_audio = MagicMock()
        mock_audio_clip_class.return_value.__enter__.return_value = mock_audio
        with patch("yt_downloader.core.config") as mock_config:
            mock_config.AUDIO_DIR = "/audio"
            core.write_audio_file_from_video("/tmp/video.mp4", "Test Title")
        mock_get_formatted_title.assert_called_once_with("Test Title")
        expected_path = os.path.join("/audio", "Test_Title.mp3")
        mock_audio.write_audiofile.assert_called_once_with(expected_path)


class TestProcessUrl:
    @patch("yt_downloader.core.create_mp3_file")
    @patch("yt_downloader.core.download_highest_bitrate_video")
    @patch("yt_downloader.core.create_youtube_object")
    def test_process_url_success(
        self,
        mock_create_yt: MagicMock,
        mock_download: MagicMock,
        mock_create_mp3: MagicMock,
        valid_youtube_url: str,
    ) -> None:
        mock_yt = MagicMock()
        mock_yt.title = "My Video"
        mock_create_yt.return_value = mock_yt
        mock_download.return_value = "/tmp/temp_video.mp4"
        core.process_url(valid_youtube_url)
        mock_create_yt.assert_called_once_with(valid_youtube_url)
        mock_download.assert_called_once_with(mock_yt)
        mock_create_mp3.assert_called_once_with("/tmp/temp_video.mp4", "My Video")

    @patch("yt_downloader.core.create_youtube_object")
    def test_process_url_invalid_url_raises_download_error(
        self,
        mock_create_yt: MagicMock,
        valid_youtube_url: str,
    ) -> None:
        mock_create_yt.return_value = None
        with pytest.raises(DownloadError, match="Invalid or unavailable video"):
            core.process_url(valid_youtube_url)

    @patch("yt_downloader.core.create_mp3_file")
    @patch("yt_downloader.core.download_highest_bitrate_video")
    @patch("yt_downloader.core.create_youtube_object")
    def test_process_url_download_returns_none_raises_download_error(
        self,
        mock_create_yt: MagicMock,
        mock_download: MagicMock,
        mock_create_mp3: MagicMock,
        valid_youtube_url: str,
    ) -> None:
        mock_yt = MagicMock()
        mock_yt.title = "My Video"
        mock_create_yt.return_value = mock_yt
        mock_download.return_value = None
        with pytest.raises(DownloadError, match="Could not find video to process"):
            core.process_url(valid_youtube_url)

    @patch("yt_downloader.core.create_youtube_object")
    def test_process_url_invalid_url_raises_invalid_url_error(
        self,
        mock_create_yt: MagicMock,
    ) -> None:
        mock_create_yt.side_effect = InvalidURLError("Invalid path for URL")
        with pytest.raises(InvalidURLError):
            core.process_url("https://www.youtube.com/bad")
