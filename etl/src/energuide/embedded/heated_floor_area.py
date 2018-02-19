import typing
from energuide import element
from energuide.embedded import area
from energuide.exceptions import InvalidEmbeddedDataTypeException


class _HeatedFloorArea(typing.NamedTuple):
    area_above_grade: area.Area
    area_below_grade: area.Area


class HeatedFloorArea(_HeatedFloorArea):

    @classmethod
    def from_data(cls, heated_floor_area: element.Element) -> 'HeatedFloorArea':
        try:
            return HeatedFloorArea(
                area_above_grade=area.Area(float(heated_floor_area.attrib['aboveGrade'])),
                area_below_grade=area.Area(float(heated_floor_area.attrib['belowGrade'])),
            )
        except (KeyError, ValueError) as exc:
            raise InvalidEmbeddedDataTypeException(HeatedFloorArea) from exc

    def to_dict(self) -> typing.Dict[str, typing.Optional[float]]:
        return {
            'areaAboveGradeMetres': self.area_above_grade.square_metres,
            'areaAboveGradeFeet': self.area_above_grade.square_feet,
            'areaBelowGradeMetres': self.area_below_grade.square_metres,
            'areaBelowGradeFeet': self.area_below_grade.square_feet,
        }
