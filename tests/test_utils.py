import yt_downloader.utils as utils
import os

class TestUtils:
    def test_remove_video_file_success(self):
        with open("temp_video.mp4", "w") as video_file:
            video_file.write("dummy data")
        utils.remove_video_file(video_file.name)
        assert not os.path.exists("temp_video.mp4")

    def test_get_formatted_title_success(self):
        result = utils.get_formatted_title("Coldplay Viva La Vida Official Video")
        assert result == "Coldplay_Viva_La_Vida_Official_Video"
    
    def test_get_formatted_title_truncate(self):
        result = utils.get_formatted_title("A Man Without Love LYRICS Video Engelbert Humperdinck 1968 🌙 Moon Knight Episode 1")
        assert result == "A_Man_Without_Love_LYRICS_Video_Engelbert_Humperdinck_1968_M"