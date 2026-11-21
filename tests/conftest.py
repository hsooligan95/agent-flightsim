import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
# The agent under test must run on its offline stub composer.
os.environ.pop("OPENAI_API_KEY", None)

import pytest  # noqa: E402

from flightsim.engine import Engine  # noqa: E402


@pytest.fixture(scope="module")
def engine(tmp_path_factory) -> Engine:
    return Engine(workdir=tmp_path_factory.mktemp("flightsim"))
