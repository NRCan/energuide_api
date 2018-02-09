import typing
from lxml import etree


class _Codes(typing.NamedTuple):
    wall: typing.List[str]
    window: typing.List[str]


class Codes(_Codes):

    def to_dict(self) -> typing.Dict[str, typing.Dict[str, typing.List[str]]]:
        return {
            'codes': {
                'wall': self.wall,
                'window': self.window,
            }
        }


class _HouseSnippet(typing.NamedTuple):
    ceilings: typing.List[str]
    floors: typing.List[str]
    walls: typing.List[str]
    doors: typing.List[str]
    windows: typing.List[str]
    heated_floor_area: str
    heating_cooling: str
    ventilation: typing.List[str]
    water_heating: typing.List[str]


class HouseSnippet(_HouseSnippet):

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        return {
            'ceilings': self.ceilings,
            'floors': self.floors,
            'walls': self.walls,
            'doors': self.doors,
            'windows': self.windows,
            'heatedFloorArea': self.heated_floor_area,
            'heating_cooling': self.heating_cooling,
            'ventilations': self.ventilation,
            'waterHeatings': self.water_heating,
        }


def _extract_values(node: etree._Element,
                    xpath_mapping: typing.Dict[str, str]) -> typing.Dict[str, typing.Optional[str]]:
    output = {key: node.xpath(value) for key, value in xpath_mapping.items()}
    return {key: value[0] if value else None for key, value in output.items()}


def snip_house(house: etree._Element) -> HouseSnippet:
    ceilings = house.xpath('Components/Ceiling')
    floors = house.xpath('Components/Floor')
    walls = house.xpath('Components/Wall')
    doors = house.xpath('Components//Components/Door')
    windows = house.xpath('Components//Components/Window')
    heated_floor_area = house.xpath('Specifications/HeatedFloorArea')
    heating_cooling = house.xpath('HeatingCooling')
    heating_cooling_string = (
        etree.tostring(heating_cooling[0], encoding='unicode') if heating_cooling else None
    )
    ventilation = house.xpath('Ventilation/WholeHouseVentilatorList/Hrv')
    ventilation_strings = [etree.tostring(hrv, encoding='unicode') for hrv in ventilation]

    water_heating = house.xpath('Components/HotWater')
    water_heating_string = (
        etree.tostring(water_heating[0], encoding='unicode') if water_heating else None
    )


    return HouseSnippet(
        ceilings=[etree.tostring(node, encoding='unicode') for node in ceilings],
        floors=[etree.tostring(node, encoding='unicode') for node in floors],
        walls=[etree.tostring(node, encoding='unicode') for node in walls],
        doors=[etree.tostring(node, encoding='unicode') for node in doors],
        windows=[etree.tostring(node, encoding='unicode') for node in windows],
        heated_floor_area=etree.tostring(heated_floor_area[0], encoding='unicode') if heated_floor_area else None,
        heating_cooling=heating_cooling_string,
        ventilation=ventilation_strings,
        water_heating=water_heating_string,
    )



def snip_codes(codes: etree._Element
              ) -> Codes:
    wall_codes = codes.xpath('Wall/*/Code')
    window_codes = codes.xpath('Window/*/Code')

    return Codes(
        wall=[etree.tostring(node, encoding='unicode') for node in wall_codes],
        window=[etree.tostring(node, encoding='unicode') for node in window_codes],
    )
