# mp3-converter
Convert YouTube videos to MP3 files by providing video URLs.

## Prerequisites
- Python 3.8 or higher
- (Recommended) [virtual environment](https://docs.python.org/3/library/venv.html)

## Setup

1. Clone this repository
2. (Optional) Create and activate a virtual environment: `venv\Scripts\activate`.
3. Install dependencies: `pip install`.

## Usage

- **Single download:**
```Powershell
python --single "https://www.youtube.com/watch?v=YOUR_VIDEO_ID"
```
- **Multiple download:**
1. Add YouTube URLs (one per line) to `youtube_urls.txt` in the project root.
2. Run:
```Powershell
python cli.py --multiple
```
- For help:
```Powershell
python cli.py --help
```
**Downloaded `.mp3` files will be saved in the `audio` directory.**

## Troubleshooting

- If a download fails, check that the URL is correct and the video is available.
- See log messages in the terminal for more details.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.