"""Custom exceptions for yt_downloader."""


class YtDownloaderError(Exception):
    """Base exception for all yt_downloader errors."""

    pass


class InvalidURLError(YtDownloaderError):
    """Raised when URL validation fails (scheme, netloc, or path)."""

    pass


class DownloadError(YtDownloaderError):
    """Raised when download fails (no streams, download failure)."""

    pass


class ConversionError(YtDownloaderError):
    """Raised when audio conversion fails."""

    pass
