import typing
from lxml import etree


class Element:

    def __init__(self, node: etree._Element) -> None:
        self.__node = node

    @classmethod
    def from_string(cls, data: str) -> 'Element':
        output = etree.fromstring(data)
        return cls(output)

    def findtext(self, *args, **kwargs) -> typing.Optional[str]:
        return self.__node.findtext(*args, **kwargs)

    @property
    def attrib(self) -> typing.Dict[str, typing.Any]:
        return self.__node.attrib

    def xpath(self, *args, **kwargs) -> typing.List[typing.Any]:
        output = self.__node.xpath(*args, **kwargs)
        return [Element(node) if isinstance(node, etree._Element) else node for node in output]
