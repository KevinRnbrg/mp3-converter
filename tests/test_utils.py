"""Tests for yt_downloader.utils."""

import os
import pytest
import yt_downloader.utils as utils


class TestRemoveVideoFile:
    def test_remove_video_file_success(self, tmp_path: pytest.TempPathFactory) -> None:
        video_file = tmp_path / "temp_video.mp4"
        video_file.write_text("dummy data")
        assert video_file.exists()
        utils.remove_video_file(str(video_file))
        assert not video_file.exists()

    def test_remove_video_file_none_does_nothing(self) -> None:
        utils.remove_video_file(None)

    def test_remove_video_file_nonexistent_does_not_raise(self) -> None:
        """Nonexistent path is a no-op (only removes if file exists)."""
        utils.remove_video_file("/nonexistent/path/video.mp4")


class TestGetFormattedTitle:
    def test_get_formatted_title_success(self) -> None:
        result = utils.get_formatted_title("Coldplay Viva La Vida Official Video")
        assert result == "Coldplay_Viva_La_Vida_Official_Video"

    def test_get_formatted_title_truncate(self) -> None:
        result = utils.get_formatted_title(
            "A Man Without Love LYRICS Video Engelbert Humperdinck 1968 🌙 Moon Knight Episode 1"
        )
        assert result == "A_Man_Without_Love_LYRICS_Video_Engelbert_Humperdinck_1968_M"
