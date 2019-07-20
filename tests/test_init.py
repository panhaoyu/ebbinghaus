import pytest
import ebbinghaus as eb
from ebbinghaus import exceptions


def test_register():
    eb.set_database()
    eb.register(123)


def test_exists():
    eb.set_database()
    assert not eb.exists(123)
    eb.register(123)
    assert eb.exists(123)


def test_register_repeat():
    eb.set_database()
    eb.register(123)
    with pytest.raises(exceptions.ExternalKeyExistsError):
        eb.register(123)


def test_get_not_exists():
    eb.set_database()
    with pytest.raises(exceptions.ExternalKeyNotExistsError):
        eb.get_stage(123)
