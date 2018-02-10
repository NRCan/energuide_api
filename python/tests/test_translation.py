import pytest
from energuide import translation


def test_translation() -> None:
    data = translation.Translation({
        translation.Language.ENGLISH: 'english text',
        translation.Language.FRENCH: 'french text',
    })

    assert data.to_string(translation.Language.ENGLISH) == 'english text'
    assert data.to_string(translation.Language.FRENCH) == 'french text'


def test_translation_can_underspecify_languages() -> None:
    data = translation.Translation({
        translation.Language.ENGLISH: 'english text',
    })

    with pytest.raises(translation.TranslationNotFoundError) as ex:
        data.to_string(translation.Language.FRENCH)

    assert translation.Language.FRENCH.name in ex.exconly()


def test_translation_equality() -> None:
    data = {
        translation.Language.ENGLISH: 'english text',
        translation.Language.FRENCH: 'french text',
    }
    version1 = translation.Translation(data)
    version2 = translation.Translation(data)
    assert version1 == version2
