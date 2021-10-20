import sys
sys.path.append('.')
from nltk import StanfordNERTagger
import nltk
from utils.helper_functions import process_text, check_for_digits
from utils.base_interface import DetectorInterface
from utils.config import MODEL_PATH, CLASS_PATH


class SerialDetector(DetectorInterface):

    def __init__(self, model_path: str = MODEL_PATH, class_path: str = CLASS_PATH):
        self.text = None
        self.split_text = None
        self.processed_text = None
        self.st = StanfordNERTagger(model_path, class_path, encoding='utf-8')
        self.results = dict()
        self.cluster = list()

    def ingest(self, inp: str):
        self.text = inp
        return self

    def process(self):
        self.processed_text = list()
        self.split_text = self.text.split('",')
        for text in self.split_text:
            text = process_text(text, replace_whitespace=True)
            text = nltk.word_tokenize(text)
            self.processed_text.append(text)
        return self

    def detect(self):
        for i, text in enumerate(self.processed_text):
            tags = map(lambda val: val[1], filter(lambda val: val[1] == 'O', self.st.tag(text)))
            if len(text) == 1 and len(list(tags)) == 1:
                # check if text contains number
                if check_for_digits(text[0]):
                    self.results[' '.join(text)] = "SERIAL"

    def update(self):
        if len(self.cluster) == 0:
            self.cluster = list(self.results.keys())
        else:
            self.cluster = list(set(self.cluster + list(self.results.keys())))


if __name__ == "__main__":
    # test_data1 = '"MARKS AND SPENCERS LTD", "LONDON", "ICNAO02312", "LONDON, GREAT BRITAIN", "TOYS", "INTEL LLC", "M&S CORPORATION Limited", "LONDON, ENGLAND", "XYZ 13423 / ILD", "ABC/ICL/20891NC"'
    # test_data2 = '"ICNAO02312", "XYZ 13423 / ILD", "ABC/ICL/20891NC"'
    # test_data3 = "123456"
    # test_data = [test_data1, test_data2, test_data3]
    # sd = SerialDetector()
    # for data in test_data:
    #     sd.ingest(data)
    #     sd.process()
    #     sd.detect()
    #     sd.update()
    #     print(sd.cluster)
    pass
