from abc import ABC, abstractmethod


class BaseLLM(ABC):
    @abstractmethod
    def _generate_messages(self, *args, **kwargs) -> str | None:
        pass

    @abstractmethod
    def make_response(self, *args, **kwargs) -> str:
        pass
