import src.utils as utils

class TestUtils:
    def test_get_formatted_title_success(self):
        result = utils.get_formatted_title("Coldplay Viva La Vida Official Video")
        assert result == "Coldplay_Viva_La_Vida_Official_Video"
    
    def test_get_formatted_title_truncate(self):
        result = utils.get_formatted_title("A Man Without Love LYRICS Video Engelbert Humperdinck 1968 🌙 Moon Knight Episode 1")
        assert result == "A_Man_Without_Love_LYRICS_Video_Engelbert_Humperdinck_1968_M"