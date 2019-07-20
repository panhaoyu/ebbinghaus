import os
import tempfile
import pytest
from ebbinghaus import database as db


def test_create_memory_database():
    db.set_database()


def test_create_disk_database():
    with tempfile.TemporaryDirectory() as temp_dir:
        database = db.set_database(os.path.join(temp_dir, 'test.db'))
        database.close()
    with tempfile.TemporaryDirectory() as temp_dir:
        database = db.set_database(os.path.join(temp_dir, 'parent', 'children', 'test.db'))
        database.close()


def test_create_item():
    db.set_database()
    obj = db.EbbinghausModel.create(external_id=3)
    assert obj.external_id == 3


def test_item_init_stage():
    db.set_database()
    obj = db.EbbinghausModel.create(external_id=3)
    assert obj.stage == 0


def test_item_remember_1():
    db.set_database()
    obj = db.EbbinghausModel.create(external_id=3)
    obj.remember()
    assert obj.stage == 1


def test_item_remember_8():
    db.set_database()
    obj = db.EbbinghausModel.create(external_id=4)
    [obj.remember() for _ in range(8)]
    assert obj.stage == 8


def test_item_forget():
    db.set_database()
    obj = db.EbbinghausModel.create(external_id=3)
    obj.remember()
    obj.forget()
    assert obj.stage == 0


def test_item_remember_overflow():
    db.set_database()
    obj = db.EbbinghausModel.create(external_id=3)
    [obj.remember() for _ in range(8)]
    with pytest.raises(ValueError):
        obj.remember()


def test_item_forget_overflow():
    db.set_database()
    obj = db.EbbinghausModel.create(external_id=3)
    with pytest.raises(ValueError):
        obj.forget()


def test_available():
    db.set_database()
    obj = db.EbbinghausModel.create(external_id=3)
    assert obj.available
    obj.remember()
    assert not obj.available


def test_random():
    db.set_database()
    db.EbbinghausModel.create(external_id=3)
    assert db.EbbinghausModel.random(1)[0] == 3


def test_random_2():
    db.set_database()
    db.EbbinghausModel.create(external_id=3)
    db.EbbinghausModel.create(external_id=4)
    assert set(db.EbbinghausModel.random(2)) == {3, 4}


def test_random_overflow():
    db.set_database()
    db.EbbinghausModel.create(external_id=3)
    db.EbbinghausModel.create(external_id=4)
    assert set(db.EbbinghausModel.random(4)) == {3, 4}
