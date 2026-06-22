import pytest
import json
from code_forge import load_lockfile, run_unit_tests, validate_lockfile, Dependency, Lockfile

def test_load_lockfile():
    lockfile_path = 'lockfile.json'
    with open(lockfile_path, 'w') as f:
        json.dump({'dependencies': [{'name': 'dep1', 'version': '1.0.0'}, {'name': 'dep2', 'version': '2.0.0'}]}, f)
    lockfile = load_lockfile(lockfile_path)
    assert len(lockfile.dependencies) == 2
    assert lockfile.dependencies[0].name == 'dep1'
    assert lockfile.dependencies[0].version == '1.0.0'
    assert lockfile.dependencies[1].name == 'dep2'
    assert lockfile.dependencies[1].version == '2.0.0'

def test_run_unit_tests():
    lockfile = Lockfile(dependencies=[Dependency(name='dep1', version='1.0.0'), Dependency(name='dep2', version='2.0.0')])
    assert run_unit_tests(lockfile)

def test_run_unit_tests_failure():
    lockfile = Lockfile(dependencies=[Dependency(name='dep1', version='0.0.0'), Dependency(name='dep2', version='2.0.0')])
    assert not run_unit_tests(lockfile)

def test_validate_lockfile():
    lockfile = Lockfile(dependencies=[Dependency(name='dep1', version='1.0.0'), Dependency(name='dep2', version='2.0.0')])
    expected_dependencies = [Dependency(name='dep1', version='1.0.0'), Dependency(name='dep2', version='2.0.0')]
    assert validate_lockfile(lockfile, expected_dependencies)

def test_validate_lockfile_failure():
    lockfile = Lockfile(dependencies=[Dependency(name='dep1', version='1.0.0'), Dependency(name='dep2', version='2.0.0')])
    expected_dependencies = [Dependency(name='dep1', version='1.0.0'), Dependency(name='dep3', version='3.0.0')]
    assert not validate_lockfile(lockfile, expected_dependencies)
