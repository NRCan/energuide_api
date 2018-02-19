import enum
import typing
from energuide import element
from energuide import bilingual
from energuide.embedded import area
from energuide.embedded import distance
from energuide.embedded import insulation
from energuide.exceptions import InvalidInputDataError


class FoundationType(enum.Enum):
    BASEMENT = enum.auto()
    CRAWLSPACE = enum.auto()
    SLAB = enum.auto()
    UNKNOWN = enum.auto()


class FoundationType(enum.Enum):
    BASEMENT = enum.auto()
    CRAWLSPACE = enum.auto()
    SLAB = enum.auto()
    UNKNOWN = enum.auto()


class WallType(enum.Enum):
    INTERIOR = enum.auto()
    EXTERIOR = enum.auto()
    PONY = enum.auto()


class MaterialType(enum.Enum):
    WOOD = enum.auto()
    CONCRETE = enum.auto()
    CONCRETE_AND_WOOD = enum.auto()
    UNKNOWN = enum.auto()


class _BasementWall(typing.NamedTuple):
    wall_type: WallType
    nominal_insulation: insulation.Insulation
    effective_insulation: insulation.Insulation
    composite_percentage: float
    wall_area: area.Area


class _BasementFloor(typing.NamedTuple):
    rectangular: bool
    nominal_insulation: typing.Optional[insulation.Insulation]
    effective_insulation: typing.Optional[insulation.Insulation]
    length: typing.Optional[distance.Distance]
    width: typing.Optional[distance.Distance]
    perimeter: typing.Optional[distance.Distance]
    optional_area: typing.Optional[float]


class _BasementHeader(typing.NamedTuple):
    nominal_insulation: insulation.Insulation
    effective_insulation: insulation.Insulation
    height: distance.Distance
    perimeter: distance.Distance


class BasementHeader(_BasementHeader):

    @classmethod
    def from_data(cls, header: element.Element) -> 'BasementHeader':
        return BasementHeader(
            nominal_insulation=insulation.Insulation(float(header.xpath('Construction/Type/@nominalInsulation')[0])),
            effective_insulation=insulation.Insulation(float(header.xpath('Construction/Type/@rValue')[0])),
            height=distance.Distance(float(header.xpath('Measurements/@height')[0])),
            perimeter=distance.Distance(float(header.xpath('Measurements/@perimeter')[0])),
        )

    @property
    def _header_area(self) -> area.Area:
        return area.Area(self.perimeter.metres * self.height.metres)

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        return {
            'insulationNominalRsi': self.nominal_insulation.rsi,
            'insulationNominalR': self.nominal_insulation.r_value,
            'insulationEffectiveRsi': self.effective_insulation.rsi,
            'insulationEffectiveR': self.effective_insulation.r_value,
            'areaMetres': self._header_area.square_metres,
            'areaFeet': self._header_area.square_feet,
            'perimeterMetres': self.perimeter.metres,
            'perimeterFeet': self.perimeter.feet,
            'heightMetres': self.height.metres,
            'heightFeet': self.height.feet,
        }


class BasementFloor(_BasementFloor):

    @classmethod
    def from_data(cls, floor: element.Element) -> 'BasementFloor':
        rectangular = floor.xpath('Measurements/@isRectangular')[0] == 'true'
        length: typing.Optional[float] = None
        width: typing.Optional[float] = None
        area: typing.Optional[float] = None
        perimeter: typing.Optional[float] = None

        if rectangular:
            length = float(floor.xpath('Measurements/@length')[0])
            width = float(floor.xpath('Measurements/@width')[0])
        else:
            area = float(floor.xpath('Measurements/@area')[0])
            perimeter = float(floor.xpath('Measurements/@perimeter')[0])

        nominal_insulation = floor.xpath('Construction/AddedToSlab/@nominalInsulation')
        effective_insulation = floor.xpath('Construction/AddedToSlab/@rValue')

        return BasementFloor(
            rectangular=rectangular,
            nominal_insulation=insulation.Insulation(float(nominal_insulation[0]))
            if nominal_insulation else None,

            effective_insulation=insulation.Insulation(float(effective_insulation[0]))
            if effective_insulation else None,

            length=distance.Distance(length)
            if length is not None else None,

            width=distance.Distance(width)
            if width is not None else None,

            perimeter=distance.Distance(perimeter)
            if perimeter is not None  else None,

            optional_area=area,
        )

    @property
    def area(self):
        if self.rectangular:
            return area.Area(self.length.metres * self.width.metres)
        return area.Area(self.optional_area)

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        return {
            'insulationNominalRsi': self.nominal_insulation.rsi if self.nominal_insulation is not None else None,
            'insulationNominalR': self.nominal_insulation.r_value if self.nominal_insulation is not None else None,
            'insulationEffectiveRsi': self.effective_insulation.rsi if self.effective_insulation is not None else None,
            'insulationEffectiveR': self.effective_insulation.r_value
                                    if self.effective_insulation is not None else None,
            'areaMetres': self.area.square_metres,
            'areaFeet': self.area.square_feet,
            'perimeterMetres': self.perimeter.metres if self.perimeter is not None else None,
            'perimeterFeet': self.perimeter.feet if self.perimeter is not None else None,
            'widthMetres': self.width.metres if self.width is not None else None,
            'widthFeet': self.width.feet if self.width is not None else None,
            'lengthMetres': self.length.metres if self.length is not None else None,
            'lengthFeet': self.length.feet if self.length is not None else None,
        }


class BasementWall(_BasementWall):

    _WALL_TYPE_TRANSLATION = {
        WallType.INTERIOR: bilingual.Bilingual(
            english='Interior',
            french='Intérieur',
        ),
        WallType.EXTERIOR: bilingual.Bilingual(
            english='Exterior',
            french='Extérieur',
        ),
        WallType.PONY: bilingual.Bilingual(
            english='Pony Wall',
            french='Murs bas',
        ),
    }

    @classmethod
    def _from_data(cls, wall: element.Element, wall_perimiter: float, wall_height: float, tag: WallType):
        percentage = float(wall.attrib['percentage'])
        return BasementWall(
            wall_type=tag,
            nominal_insulation=insulation.Insulation(float(wall.attrib['nominalRsi'])),
            effective_insulation=insulation.Insulation(float(wall.attrib['rsi'])),
            composite_percentage=percentage,
            wall_area=area.Area(wall_perimiter * wall_height * (percentage / 100))
        )

    @classmethod
    def from_data(cls, wall: element.Element, wall_perimiter: float) -> typing.List['BasementWall']:
        interior_wall_sections = wall.xpath('Construction/InteriorAddedInsulation/Composite/Section')
        exterior_wall_sections = wall.xpath('Construction/ExteriorAddedInsulation/Composite/Section')
        pony_wall_sections = wall.xpath('Construction/PonyWallType/Composite/Section')

        wall_height = float(wall.xpath('Measurements/@height')[0])
        pony_height = float(wall.xpath('Measurements/@ponyWallHeight')[0])

        walls = []
        walls.extend([BasementWall._from_data(wall_section, wall_perimiter, wall_height, WallType.INTERIOR)
                      for wall_section in interior_wall_sections])

        walls.extend([BasementWall._from_data(wall_section, wall_perimiter, wall_height, WallType.EXTERIOR)
                      for wall_section in exterior_wall_sections])

        walls.extend([BasementWall._from_data(wall_section, wall_perimiter, pony_height, WallType.PONY)
                      for wall_section in pony_wall_sections])

        return walls

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        wall_type = self._WALL_TYPE_TRANSLATION[self.wall_type]
        return {
            'wallTypeEnglish': wall_type.english,
            'wallTypeFrench': wall_type.french,
            'insulationNominalRsi': self.nominal_insulation.rsi,
            'insulationNominalR': self.nominal_insulation.r_value,
            'insulationEffectiveRsi': self.effective_insulation.rsi,
            'insulationEffectiveR': self.effective_insulation.r_value,
            'percentage': self.composite_percentage,
            'areaMetres': self.wall_area.square_metres,
            'areaFeet': self.wall_area.square_feet,
        }


class _Basement(typing.NamedTuple):
    foundation_type: FoundationType
    label: str
    configuration_type: str

    walls: typing.List[BasementWall]
    floor: BasementFloor
    header: BasementHeader


class Basement(_Basement):

    _MATERIAL_TRANSLATIONS = {
        MaterialType.UNKNOWN: bilingual.Bilingual(english='', french=''),
        MaterialType.WOOD: bilingual.Bilingual(
            english='wood',
            french='bois',
        ),
        MaterialType.CONCRETE: bilingual.Bilingual(
            english='concrete',
            french='béton',
        ),
        MaterialType.CONCRETE_AND_WOOD: bilingual.Bilingual(
            english='concrete and wood',
            french='béton et bois',
        ),
    }

    _FOUNDATION_TRANSLATIONS = {
        FoundationType.BASEMENT: bilingual.Bilingual(
            english='Basement',
            french='Sous-sol',
        ),
        FoundationType.CRAWLSPACE: bilingual.Bilingual(
            english='Crawlspace',
            french='Vide Sanitaire',
        ),
        FoundationType.SLAB: bilingual.Bilingual(
            english='Slab',
            french='Dalle',
        ),
    }

    @classmethod
    def from_data(cls, basement: element.Element) -> 'Basement':
        foundation_type = cls._derive_foundation_type(basement.tag)
        if foundation_type is FoundationType.UNKNOWN:
            raise InvalidInputDataError(f'Invalid foundation type: {basement.tag}')

        floor = BasementFloor.from_data(basement.xpath('Floor')[0])

        foundation_type = cls._derive_foundation_type(basement.tag)

        if floor.rectangular:
            length = typing.cast(distance.Distance, floor.length)
            width = typing.cast(distance.Distance, floor.width)
            floor_perimeter = (2 * length.metres) + (2 * width.metres)
        else:
            perimeter = typing.cast(distance.Distance, floor.perimeter)
            floor_perimeter = typing.cast(float, perimeter.metres)

        return Basement(
            foundation_type=foundation_type,
            label=basement.get_text('Label'),
            configuration_type=basement.xpath('Configuration/@type')[0],
            walls=BasementWall.from_data(basement.xpath('Wall')[0], floor_perimeter),
            floor=floor,
            header=BasementHeader.from_data(basement.xpath('Components/FloorHeader')[0]),
        )

    @staticmethod
    def _derive_foundation_type(tag: str) -> FoundationType:
        if tag == 'Basement':
            return FoundationType.BASEMENT
        elif tag == 'Crawlspace':
            return FoundationType.CRAWLSPACE
        elif tag == 'Slab':
            return FoundationType.SLAB
        return FoundationType.UNKNOWN

    @staticmethod
    def _derive_material(configuration_type: str) -> MaterialType:
        material = configuration_type[1]
        if material == 'W':
            return MaterialType.WOOD
        elif material == 'C':
            return MaterialType.CONCRETE
        elif material == 'B':
            return MaterialType.CONCRETE_AND_WOOD
        return MaterialType.UNKNOWN

    @property
    def material(self) -> MaterialType:
        return Basement._derive_material(self.configuration_type)

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        material = self._MATERIAL_TRANSLATIONS.get(self.material)
        foundation = self._FOUNDATION_TRANSLATIONS.get(self.foundation_type)
        return {
            'foundationTypeEnglish': foundation.english if foundation else None,
            'foundationTypeFrench': foundation.french if foundation else None,
            'label': self.label,
            'configurationType': self.configuration_type,
            'materialEnglish': material.english if material else None,
            'materialFrench': material.french if material else None,
            'wall': [wall.to_dict() for wall in self.walls],
            'floor': self.floor.to_dict(),
            'header': self.header.to_dict(),
        }
