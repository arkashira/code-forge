import json
from dataclasses import dataclass
from typing import List

@dataclass
class Dependency:
    name: str
    version: str

@dataclass
class Lockfile:
    dependencies: List[Dependency]

def load_lockfile(path: str) -> Lockfile:
    with open(path, 'r') as f:
        data = json.load(f)
    dependencies = [Dependency(name=dep['name'], version=dep['version']) for dep in data['dependencies']]
    return Lockfile(dependencies=dependencies)

def run_unit_tests(lockfile: Lockfile) -> bool:
    # Simulate running unit tests
    # For demonstration purposes, assume all tests pass if the lockfile is valid
    return all(dep.version != '0.0.0' for dep in lockfile.dependencies)

def validate_lockfile(lockfile: Lockfile, expected_dependencies: List[Dependency]) -> bool:
    # Simulate validating the lockfile
    # For demonstration purposes, assume the lockfile is valid if it contains all expected dependencies
    return all(any(dep.name == expected_dep.name and dep.version == expected_dep.version for dep in lockfile.dependencies) for expected_dep in expected_dependencies)
