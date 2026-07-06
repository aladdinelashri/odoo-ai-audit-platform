from abc import ABC, abstractmethod


class BaseAIProvider(ABC):

    @abstractmethod
    def analyze(self, prompt: str):

        pass
