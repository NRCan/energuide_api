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
    heated_floor_area: str
    heating_cooling: str
    ventilation: typing.List[str]
    water_heating: str


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


def snip_house(house: element.Element) -> HouseSnippet:
    ceilings = house.xpath('Components/Ceiling')
    floors = house.xpath('Components/Floor')
    walls = house.xpath('Components/Wall')
    doors = house.xpath('Components//Components/Door')
    windows = house.xpath('Components//Components/Window')
    heated_floor_area = house.xpath('Specifications/HeatedFloorArea')
    heating_cooling = house.xpath('HeatingCooling')
    heating_cooling_string = heating_cooling[0].to_string() if heating_cooling else None
    ventilation = house.xpath('Ventilation/WholeHouseVentilatorList/Hrv')
    ventilation_strings = [hrv.to_string() for hrv in ventilation]

    water_heating = house.xpath('Components/HotWater')
    water_heating_string = water_heating[0].to_string() if water_heating else None

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
    )


def snip_codes(codes: element.Element) -> Codes:
    wall_codes = codes.xpath('Wall/*/Code')
    window_codes = codes.xpath('Window/*/Code')

    return Codes(
        wall=[node.to_string() for node in wall_codes],
        window=[node.to_string() for node in window_codes],
    )
