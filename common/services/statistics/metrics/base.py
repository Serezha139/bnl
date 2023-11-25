from abc import ABC, abstractmethod


class BaseMetric(ABC):
    def __init__(self, name, description):
        self.name = name
        self.description = description

    @abstractmethod
    def get_data(self):
        return []

    @abstractmethod
    def format_result(self, raw_data):
        return []

    @abstractmethod
    def calculate(self, data):
        return []

    def result(self, data):
        raw_result = self.calculate(data)
        return self.format_result(raw_result)