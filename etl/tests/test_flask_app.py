from http import HTTPStatus
import hashlib
import typing
import _pytest
import pymongo
import pytest
from flask import testing
from energuide import flask_app


flask_app.App.testing = True


@pytest.fixture
def sample_salt() -> str:
    return 'sample salt'


@pytest.fixture
def sample_secret_key(monkeypatch: _pytest.monkeypatch.MonkeyPatch) -> str:
    monkeypatch.setitem(flask_app.App.config, 'SECRET_KEY', 'sample secret key')
    return flask_app.App.config['SECRET_KEY']


@pytest.fixture
def sample_signature(sample_salt: str, sample_secret_key: str) -> str:
    hasher = hashlib.new('sha3_256')
    hasher.update((sample_salt + sample_secret_key).encode())
    return hasher.hexdigest()


@pytest.fixture()
def test_client(monkeypatch: _pytest.monkeypatch.MonkeyPatch, database_name: str) -> testing.FlaskClient:
    monkeypatch.setattr(flask_app, 'DATABASE_NAME', database_name)
    return flask_app.App.test_client()


@pytest.fixture()
def thread_runner() -> typing.Generator:
    yield flask_app.ThreadRunner
    flask_app.ThreadRunner.join()


def test_threadrunner(thread_runner: flask_app.ThreadRunner) -> None:
    stay_asleep = True

    def sleeper() -> None:
        while stay_asleep:
            pass

    thread_runner.start_new_thread(sleeper)
    assert thread_runner.is_thread_running()
    stay_asleep = False
    thread_runner.join()
    assert not thread_runner.is_thread_running()


def test_frontend(test_client: testing.FlaskClient) -> None:
    assert test_client.get('/').status_code == HTTPStatus.OK


def test_alive(test_client: testing.FlaskClient) -> None:
    get_return = test_client.get('/test_alive')
    assert b'Alive' in get_return.data


def test_robots(test_client: testing.FlaskClient) -> None:
    get_return = test_client.get('/robots933456.txt')
    assert get_return.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.timeout(10)
@pytest.mark.usefixtures('populated_azure_emulator')
def test_run_tl(test_client: testing.FlaskClient,
                thread_runner: flask_app.ThreadRunner,
                mongo_client: pymongo.MongoClient,
                database_name: str,
                collection: str,
                sample_salt: str,
                sample_signature: str) -> None:

    post_return = test_client.post('/run_tl', data=dict(salt=sample_salt, signature=sample_signature))
    assert post_return.status_code == HTTPStatus.OK
    thread_runner.join()
    assert mongo_client[database_name][collection].count() == 7


@pytest.mark.timeout(10)
@pytest.mark.usefixtures('populated_azure_emulator', 'thread_runner')
def test_run_tl_busy(test_client: testing.FlaskClient,
                     sample_salt: str,
                     sample_signature: str) -> None:

    test_client.post('/run_tl', data=dict(salt=sample_salt, signature=sample_signature))
    post_return = test_client.post('/run_tl', data=dict(salt=sample_salt, signature=sample_signature))
    assert post_return.status_code == HTTPStatus.TOO_MANY_REQUESTS


def test_run_tl_no_salt(test_client: testing.FlaskClient, energuide_zip_fixture: str, sample_signature: str) -> None:
    post_return = test_client.post('/run_tl', data=dict(filename=energuide_zip_fixture, signature=sample_signature))
    assert post_return.status_code == HTTPStatus.BAD_REQUEST
    assert b'no salt' in post_return.data


def test_run_tl_no_signature(test_client: testing.FlaskClient, energuide_zip_fixture: str, sample_salt: str) -> None:
    post_return = test_client.post('/run_tl', data=dict(filename=energuide_zip_fixture, salt=sample_salt))
    assert post_return.status_code == HTTPStatus.BAD_REQUEST
    assert b'no signature' in post_return.data


def test_run_tl_bad_signature(test_client: testing.FlaskClient, energuide_zip_fixture: str, sample_salt: str) -> None:
    post_return = test_client.post('/run_tl',
                                   data=dict(filename=energuide_zip_fixture,
                                             salt=sample_salt,
                                             signature='bad signature'))
    assert post_return.status_code == HTTPStatus.BAD_REQUEST
    assert b'bad signature' in post_return.data
