from .textprocessing import TextProcessor
from dbmanager import DbManager


# class for the data visualisation
class DataVisualiser:
    db_manager = None

    def __init__(self):
        self.db_manager = DbManager()

    # Returns a list of 20 common words that appeared throughout the texts
    def word_cloud(self, uid: str):
        # Get all keywords from mongodb (big big string) need UID
        # use TextProcessor method get_all_keywords_with_textrank we want approx 25 words
        text = self.db_manager.get_all_main_texts(uid)
        keywords_with_values = TextProcessor.calculate_keywords_with_text_rank(text, 25)
        return dict(keywords_with_values)
