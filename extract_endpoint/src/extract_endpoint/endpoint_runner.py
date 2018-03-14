import typing
from http import HTTPStatus
from extract_endpoint.endpoint_triggers import EndpointTrigger


class EndpointRunner:
    def __init__(self, triggers: typing.List[EndpointTrigger]) -> None:
        self.triggers = triggers

    def apply(self) -> int:
        for trigger in self.triggers:
            result = trigger.run()
            if result != HTTPStatus.CREATED:
                return result
        return HTTPStatus.CREATED
