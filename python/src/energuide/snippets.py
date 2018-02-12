import typing
from energuide import element


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
    heated_floor_area: typing.Optional[str]
    heating_cooling: typing.Optional[str]
    ventilation: typing.List[str]
    water_heating: typing.Optional[str]
    basements: typing.List[str]


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
            'basements': self.basements
        }


def _extract_nodes(node: element.Element, path: str) -> typing.List[element.Element]:
    return node.xpath(path)


def snip_house(house: element.Element) -> HouseSnippet:
    ceilings = _extract_nodes(house, 'Components/Ceiling')
    floors = _extract_nodes(house, 'Components/Floor')
    walls = _extract_nodes(house, 'Components/Wall')
    doors = _extract_nodes(house, 'Components//Components/Door')
    windows = _extract_nodes(house, 'Components//Components/Window')
    heated_floor_area = _extract_nodes(house, 'Specifications/HeatedFloorArea')
    heating_cooling = _extract_nodes(house, 'HeatingCooling')
    heating_cooling_string = heating_cooling[0].to_string() if heating_cooling else None
    ventilation = _extract_nodes(house, 'Ventilation/WholeHouseVentilatorList/Hrv')
    ventilation_strings = [hrv.to_string() for hrv in ventilation]

    water_heating = _extract_nodes(house, 'Components/HotWater')
    water_heating_string = water_heating[0].to_string() if water_heating else None

    basements = _extract_nodes(house, 'Components/Basement')

    return HouseSnippet(
        ceilings=[node.to_string() for node in ceilings],
        floors=[node.to_string() for node in floors],
        walls=[node.to_string() for node in walls],
        doors=[node.to_string() for node in doors],
        windows=[node.to_string() for node in windows],
        heated_floor_area=heated_floor_area[0].to_string() if heated_floor_area else None,
        heating_cooling=heating_cooling_string,
        ventilation=ventilation_strings,
        water_heating=water_heating_string,
        basements=[node.to_string() for node in basements],
    )


def snip_codes(codes: element.Element) -> Codes:
    wall_codes = codes.xpath('Wall/*/Code')
    window_codes = codes.xpath('Window/*/Code')

    return Codes(
        wall=[node.to_string() for node in wall_codes],
        window=[node.to_string() for node in window_codes],
    )
