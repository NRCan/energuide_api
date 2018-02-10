import enum
import typing


@enum.unique
class Language(enum.Enum):
    ENGLISH = enum.auto()
    FRENCH = enum.auto()


class TranslationNotFoundError(Exception):

    def __init__(self, language: Language) -> None:
        super().__init__(f"Requested unspecified language {language.name}")


class Translation:
    def __init__(self, versions: typing.Dict[Language, str]) -> None:
        self._versions = versions

    def to_string(self, language: Language) -> str:
        if language in self._versions:
            return self._versions[language]
        raise TranslationNotFoundError(language)

    def __eq__(self, other):
        if isinstance(other, Translation):
            return self._versions == other._versions
        return False
