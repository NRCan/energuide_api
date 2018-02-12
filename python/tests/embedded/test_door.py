import pytest
# from energuide import bilingual
from energuide import element
from energuide import extracted_datatypes


@pytest.fixture
def sample_raw() -> element.Element:
    doc = """
    <Door>
        <Label>Front door</Label>
        <Construction>
            <Type value='0.39'>
                <English>Solid wood</English>
                <French>Bois massif</French>
            </Type>
        </Construction>
        <Measurements height='1.9799' width='0.8499' />
    </Door>
    """
    return element.Element.from_string(doc)


@pytest.fixture
def sample() -> extracted_datatypes.Door:
    return extracted_datatypes.Door(
        label='Front door',
        type_english='Solid wood',
        type_french='Bois massif',
        rsi=0.39,
        height=1.9799,
        width=0.8499,
    )


def test_from_data(sample_raw: element.Element, sample: extracted_datatypes.Door) -> None:
    output = extracted_datatypes.Door.from_data(sample_raw)
    assert output == sample


def test_to_dict(sample: extracted_datatypes.Door) -> None:
    output = sample.to_dict()
    assert output == {
        'typeEnglish': 'Solid wood',
        'typeFrench': 'Bois massif',
        'rsi': 0.39,
        'rValue': 2.21452270143,
        'uFactor': 2.564102564102564,
        'uFactorImperial': 0.45156457387149956,
        'areaMetres': 1.68271701,
        'areaFeet': 18.112616311521026,
    }


def test_properties(sample_raw: element.Element) -> None:
    output = extracted_datatypes.Door.from_data(sample_raw)
    assert output.r_value == 2.21452270143
    assert output.u_factor == 2.564102564102564
    assert output.u_factor_imperial == 0.45156457387149956
    assert output.area_metres == 1.68271701
    assert output.area_feet == 18.112616311521027
