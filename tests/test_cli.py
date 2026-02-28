"""Tests for yt_downloader.cli."""

import sys
import pytest
from unittest.mock import patch, MagicMock
import yt_downloader.cli as cli
from yt_downloader.exceptions import InvalidURLError, DownloadError


class TestMain:
    def test_main_no_args_prints_help(self, capsys: pytest.CaptureFixture[str]) -> None:
        with patch.object(sys, "argv", ["yt_downloader"]):
            cli.main()
        out, _ = capsys.readouterr()
        assert "single" in out or "multiple" in out or "usage" in out.lower()

    @patch("yt_downloader.cli.process_single_url")
    def test_main_single_calls_process_single_url_with_stripped_url(
        self,
        mock_process_single: MagicMock,
    ) -> None:
        with patch.object(sys, "argv", ["yt_downloader", "-s", "  https://youtube.com/watch?v=1  "]):
            with patch("yt_downloader.cli.config") as mock_config:
                cli.main()
        mock_process_single.assert_called_once_with("  https://youtube.com/watch?v=1  ")

    @patch("yt_downloader.cli._log_completion")
    @patch("yt_downloader.cli.process_single_url")
    def test_main_single_logs_completion(
        self,
        mock_process_single: MagicMock,
        mock_log_completion: MagicMock,
    ) -> None:
        with patch.object(sys, "argv", ["yt_downloader", "-s", "https://youtube.com/watch?v=1"]):
            cli.main()
        mock_log_completion.assert_called_once_with(single=True)

    @patch("yt_downloader.cli._log_completion")
    @patch("yt_downloader.cli.process_multiple_urls")
    def test_main_multiple_calls_process_multiple_urls_and_logs(
        self,
        mock_process_multiple: MagicMock,
        mock_log_completion: MagicMock,
    ) -> None:
        with patch.object(sys, "argv", ["yt_downloader", "-m"]):
            with patch("yt_downloader.cli.config") as mock_config:
                mock_config.YT_URLS_FILE = "/path/to/urls.txt"
                cli.main()
        mock_process_multiple.assert_called_once_with("/path/to/urls.txt")
        mock_log_completion.assert_called_once_with(single=False)


class TestProcessSingleUrl:
    @patch("yt_downloader.cli.core.process_url")
    def test_process_single_url_calls_core_with_stripped_url(
        self,
        mock_process_url: MagicMock,
    ) -> None:
        cli.process_single_url("  https://youtube.com/watch?v=1  ")
        mock_process_url.assert_called_once_with("https://youtube.com/watch?v=1")

    @patch("yt_downloader.cli.core.process_url")
    def test_process_single_url_catches_invalid_url_error_and_logs(
        self,
        mock_process_url: MagicMock,
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        mock_process_url.side_effect = InvalidURLError("Invalid scheme for URL")
        cli.process_single_url("http://youtube.com/watch?v=1")
        assert "Invalid scheme" in caplog.text or "Invalid" in caplog.text

    @patch("yt_downloader.cli.core.process_url")
    def test_process_single_url_catches_download_error_and_logs(
        self,
        mock_process_url: MagicMock,
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        mock_process_url.side_effect = DownloadError("No audio streams found")
        cli.process_single_url("https://youtube.com/watch?v=1")
        assert "No audio streams" in caplog.text or "Download" in caplog.text


class TestProcessMultipleUrls:
    @patch("yt_downloader.cli.process_single_url")
    def test_process_multiple_urls_reads_file_and_calls_process_single_per_line(
        self,
        mock_process_single: MagicMock,
        tmp_path: pytest.TempPathFactory,
    ) -> None:
        url_file = tmp_path / "urls.txt"
        url_file.write_text("https://youtube.com/watch?v=1\nhttps://youtube.com/watch?v=2\n", encoding="utf-8")
        cli.process_multiple_urls(str(url_file))
        assert mock_process_single.call_count == 2
        mock_process_single.assert_any_call("https://youtube.com/watch?v=1")
        mock_process_single.assert_any_call("https://youtube.com/watch?v=2")

    def test_process_multiple_urls_missing_file_logs_error(
        self,
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        cli.process_multiple_urls("/nonexistent/youtube_urls.txt")
        assert "not found" in caplog.text.lower() or "nonexistent" in caplog.text.lower()
