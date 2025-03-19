import json
from abc import ABC, abstractmethod
from typing import Dict, Any


class ConfigLoader(ABC):
    @abstractmethod
    def load(self) -> Dict[str, Any]:
        pass


class LocalConfigLoader(ConfigLoader):
    def __init__(self, filename: str):
        self.filename = filename

    def load(self) -> Dict[str, Any]:
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise ValueError(f"Error loading local config: {str(e)}") from e


class ApiConfigLoader(ConfigLoader):
    def __init__(self, endpoint: str):
        self.endpoint = endpoint

    def load(self) -> Dict[str, Any]:
        raise NotImplementedError("API config loading is not implemented yet")
