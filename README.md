# YouTube MP3 Downloader
Convert YouTube videos to MP3 files by providing video URLs.

## Prerequisites
- Python 3.8 or higher
- (Recommended) [virtual environment](https://docs.python.org/3/library/venv.html)
- FFmpeg may be required for audio conversion (used by moviepy); ensure it is installed if conversion fails.

## Setup

1. Clone this repository
2. Create a virtual environment with `python -m venv venv` and activate it: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (macOS/Linux).
3. Install dependencies: `pip install -r requirements.txt`
4. Run `pip install -e .`

## Usage

- **Single download:**
```Powershell
yt_downloader --single "https://www.youtube.com/watch?v=YOUR_VIDEO_ID"
```
- **Multiple download:**
1. Add YouTube URLs (one per line) to `youtube_urls.txt` in the project root.
2. Run:
```Powershell
yt_downloader --multiple
```
- For help:
```Powershell
yt_downloader --help
```

From the project root without installing: `python -m yt_downloader --single "..."` (and similarly for `--multiple` or `--help`).

**Downloaded `.mp3` files will be saved in the `audio` directory.**

## Testing

From the project root, run: `pytest`.
To skip integration tests: `pytest -m 'not integration'`.

## Troubleshooting

- If a download fails, check that the URL is correct and the video is available.
- See log messages in the terminal for more details.

## Contributing

Contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
