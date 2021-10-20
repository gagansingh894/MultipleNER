import copy
from loc_detector.core.detector import LOCDetector
from org_detector.core.detector import ORGDetector
from serial_detector.core.detector import SerialDetector
from product_detector.core.detector import ProductDetector


class DetectorSystem(object):

    def __init__(self):
        self.text = None
        self.__loc_detector = LOCDetector()
        self.__org_detector = ORGDetector()
        self.__ser_detector = SerialDetector()
        self.__prod_detector = ProductDetector()
        self.clusters = {
            'LOC': None,
            'ORG': None,
            'SERIAL': None,
            'PRODUCT': None
        }

    def ingest_text(self, inp:str):
        self.text = inp

    def run(self):
        self._detect_loc()
        self._detect_org()
        self._detect_serial()
        self._detect_product()

    def _detect_loc(self):
        text = copy.deepcopy(self.text)
        self.__loc_detector.ingest(text).process().detect().update()
        self.clusters['LOC'] = self.__loc_detector.cluster

    def _detect_org(self):
        text = copy.deepcopy(self.text)
        self.__org_detector.ingest(text).process().detect().update()
        self.clusters['ORG'] = self.__org_detector.cluster

    def _detect_serial(self):
        text = copy.deepcopy(self.text)
        self.__ser_detector.ingest(text).process().detect().update()
        self.clusters['SERIAL'] = self.__ser_detector.cluster

    def _detect_product(self):
        text = copy.deepcopy(self.text)
        self.__prod_detector.ingest(text).process().detect().update()
        self.clusters['ORG'] = self.__prod_detector.cluster
