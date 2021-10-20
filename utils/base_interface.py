from abc import ABC, abstractmethod


class DetectorInterface(object):

    @abstractmethod
    def ingest(self,  inp: str):
        pass

    @abstractmethod
    def process(self):
        pass

    @abstractmethod
    def detect(self):
        pass

    @abstractmethod
    def update(self):
        pass
