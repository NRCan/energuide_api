import typing
from extract_endpoint.endpoint_triggers import EndpointTrigger

# class EndpointRunner:
#     def __init__(self, stream: typing.IO[bytes], timestamp: str, url: str) -> None:
#         self.stream = stream
#         self.timestamp = timestamp
#         self.url = url
#
#     def apply(self, stream: typing.IO[bytes]) -> None:
#         this_is_a_test()


class EndpointRunner:
    def __init__(self, triggers: typing.List[EndpointTrigger]) -> None:
        self.triggers = triggers
        return None

    def apply(self) -> None:
        this_is_a_test()
        for trigger in self.triggers:
            trigger.run()


def this_is_a_test() -> None:
    print("Starting tests")
