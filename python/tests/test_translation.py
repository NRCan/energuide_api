from energuide import bilingual


def test_translation() -> None:
    output = bilingual.Bilingual(english='english text', french='french text')
    assert output.english == 'english text'
    assert output.french == 'french text'
