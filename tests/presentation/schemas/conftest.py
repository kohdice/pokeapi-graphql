from dataclasses import dataclass

import pytest
from injector import Injector
from starlette.responses import Response


class MockRequest:
    pass


@dataclass
class MockInfo:
    context: dict


@pytest.fixture(scope="module")
def mock_info(container: Injector) -> MockInfo:
    return MockInfo(
        context={
            "container": container,
            "request": MockRequest(),
            "response": Response(),
        }
    )
