# mp3-converter
Convert YouTube videos to MP3 files by providing video URLs.

## Prerequisites
- Python 3.8 or higher
- (Recommended) [virtual environment](https://docs.python.org/3/library/venv.html)

## Setup

1. Clone this repository
2. Create a virtual environment with `python -m venv venv` and activate it with `venv\Scripts\activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run `pip install -e .`

## Usage

- **Single download:**
```Powershell
python yt_downloader --single "https://www.youtube.com/watch?v=YOUR_VIDEO_ID"
```
- **Multiple download:**
1. Add YouTube URLs (one per line) to `youtube_urls.txt` in the project root.
2. Run:
```Powershell
python yt_downloader --multiple
```
- For help:
```Powershell
python yt_downloader --help
```
**Downloaded `.mp3` files will be saved in the `audio` directory.**

## Testing

To run unit tests run `pytest` in the on the command line.

## Troubleshooting

- If a download fails, check that the URL is correct and the video is available.
- See log messages in the terminal for more details.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
