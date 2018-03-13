import typing
from extract_endpoint.endpoint_triggers import EndpointTrigger


class EndpointRunner:
    def __init__(self, triggers: typing.List[EndpointTrigger]) -> None:
        self.triggers = triggers
        return None

    def apply(self) -> None:
        for trigger in self.triggers:
            trigger.run()
            # raise error here if code is not correct
