import typing
from energuide import element


class _EnergyUpgradesSnippet(typing.NamedTuple):
    upgrades: typing.List[str]


class EnergyUpgradesSnippet(_EnergyUpgradesSnippet):

    EMPTY_SNIPPET: typing.Dict[str, typing.List[str]] = {
        'upgrades': [],
    }

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        return {
            'upgrades': self.upgrades,
        }


def snip_energy_upgrade_order(energy_upgrades: element.Element) -> EnergyUpgradesSnippet:
    upgrades = energy_upgrades.xpath('EnergyUpgrades/Settings/*')

    return EnergyUpgradesSnippet(
        upgrades=[upgrade.to_string() for upgrade in upgrades],
    )
