import sys
sys.path.append('.')
from nltk import StanfordNERTagger
import nltk
from utils.helper_functions import process_text
from utils.base_interface import DetectorInterface
from utils.config import MODEL_PATH, CLASS_PATH
from collections import Counter
from geopy.geocoders import Nominatim
import geopy.distance
import time


class LOCDetector(DetectorInterface):

    def __init__(self, model_path: str = MODEL_PATH, class_path: str = CLASS_PATH):
        self.text = None
        self.split_text = None
        self.processed_text = None
        self.st = StanfordNERTagger(model_path, class_path, encoding='utf-8')
        self.results = dict()
        self.cluster = list()
        self.geo_locator = Nominatim(user_agent='anewmyapplication')

    def ingest(self, inp: str):
        self.text = inp
        return self

    def process(self):
        self.processed_text = list()
        self.split_text = self.text.split('",')
        for text in self.split_text:
            text = process_text(text)
            text = nltk.word_tokenize(text)
            self.processed_text.append(text)
        return self

    def detect(self):
        for i, text in enumerate(self.processed_text):
            tags = map(lambda val: val[1], filter(lambda val: val[1] == 'LOCATION', self.st.tag(text)))
            tags = set(list(tags))
            if bool(tags):
                tag = list(tags)[0]
                self.results[' '.join(text)] = tag
        return self

    def update(self):
        d = dict()
        alloted = []
        cordinates = dict()
        for k in self.results:
            cordinates[k] = self.geo_locator.geocode(k, timeout=15)[1]

        if len(self.cluster) == 0:
            input_list = list(set(list(self.results.keys())))
            print(input_list)
        else:
            input_list = list(set([item for sublist in self.cluster for item in sublist] + list(self.results.keys())))
            print(input_list)
            self.cluster = list()

        for i in input_list:
            if i not in d:
                d[i] = list()
            for j in input_list:
                if i != j and j not in alloted and j not in d:
                    w1 = cordinates[i]
                    w2 = cordinates[j]
                    if geopy.distance.distance(w1, w2).km < 1000:
                        alloted.append(j)
                        d[i].append(j)

        d = dict(sorted(d.items(), key=lambda x: x[1], reverse=True))

        for k, v in d.items():
            if bool(v):
                self.cluster.append([k] + v)
            else:
                if not bool(self.cluster):
                    self.cluster.append([k])
                else:
                    for cl in self.cluster:
                        if k in cl:
                            break
                        else:
                            self.cluster.append([k])
                            break
        return self

if __name__ == "__main__":
    pass
    # test_data = '"MARKS AND SPENCERS LTD", "LONDON", "ICNAO02312", "LONDON, GREAT BRITAIN", "TOYS", "INTEL LLC", "M&S CORPORATION Limited", "LONDON, ENGLAND",  "LONDON", "HONG KONG", "ASIA"'
    # locd = LOCDetector()
    # locd.ingest(test_data)
    # locd.process()
    # locd.detect()
    # locd.update()
    # print(locd.results)
    # print(locd.cluster)
