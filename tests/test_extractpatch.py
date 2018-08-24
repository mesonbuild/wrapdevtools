import pytest
from pathlib import Path
import py
import shutil
import os
from wrapdevtools import extractpatch

DATADIR: Path = Path(__file__).parent / 'data'


@pytest.fixture(scope="session")
def simple_project(tmpdir_factory):
    result = Path(tmpdir_factory.mktemp("simple project"))
    data_source_dir = DATADIR / 'simple project'
    for file in data_source_dir.iterdir():
        shutil.copytree(file, result / file.name)
    return result


@pytest.fixture(scope="session")
def simple_project_extracted(tmpdir_factory):
    result = Path(tmpdir_factory.mktemp("simple project extracted"))
    data_source_dir = DATADIR / 'simple project extracted'
    for file in data_source_dir.iterdir():
        shutil.copytree(str(file), str(result / file.name))
    return result

def test_no_changes(simple_project_extracted, tmpdir):
    wrapfile = simple_project_extracted / 'subprojects' / 'simple.wrap'
    output = tmpdir.mkdir('output')
    print(str(output))
    args = [
        '--output', str(output),
        str(wrapfile)
    ]
    extractpatch.main(args)
    assert (output / 'upstream.wrap').exists()
    assert (output / 'upstream.wrap').isfile()


