import typing
from energuide import element
from energuide.exceptions import InvalidEmbeddedDataTypeError


class _Upgrade(typing.NamedTuple):
    upgrade_type: str
    cost: int
    priority: int


class Upgrade(_Upgrade):

    @classmethod
    def from_data(cls, setting: element.Element) -> 'Upgrade':
        return Upgrade(
            upgrade_type=setting.tag,
            cost=int(setting.attrib['cost']),
            priority=int(setting.attrib['priority'])
        )

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        return {
            'upgradeType': self.upgrade_type,
            'cost': self.cost,
            'priority': self.priority,
        }