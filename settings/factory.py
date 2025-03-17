from .loader import ConfigLoader, LocalConfigLoader, ApiConfigLoader
from enums import LoadSource


class ConfigLoaderFactory:
    @staticmethod
    def create_loader(source: LoadSource, location: str) -> ConfigLoader:
        if isinstance(source, LoadSource):
            source_type = {
                LoadSource.LOCAL: LocalConfigLoader(location),
                LoadSource.API: ApiConfigLoader(location)
            }
            return source_type[source]
        else:
            raise ValueError("Unknown config source type")
