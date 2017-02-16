import os
from uuid import uuid4

import pytest
from click.testing import CliRunner

from todoman import model


@pytest.fixture
def default_database(tmpdir):
    return model.Database(
        [tmpdir.mkdir('default')],
        tmpdir.mkdir(uuid4().hex).join('cache.sqlite3'),
    )


@pytest.fixture
def config(tmpdir, default_database):
    path = tmpdir.join('config')
    path.write('[main]\n'
               'path = {}/*\n'
               'date_format = %Y-%m-%d\n'
               'cache_path = {}\n'
               .format(str(tmpdir), str(tmpdir.join('cache.sqlite3'))))
    return path


@pytest.fixture
def runner(config):
    return CliRunner(env={
        'TODOMAN_CONFIG': str(config)
    })


@pytest.fixture
def create(tmpdir):
    def inner(name, content, list_name='default'):
        tmpdir.ensure_dir(list_name).join(name).write(
            'BEGIN:VCALENDAR\n'
            'BEGIN:VTODO\n' +
            content +
            'END:VTODO\n'
            'END:VCALENDAR'
        )

    return inner
