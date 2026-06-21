import json
import hashlib
from library_api import Library, LibraryAPI

def test_add_library():
    api = LibraryAPI()
    library = Library("test", "1.0", "example code")
    api.add_library(library)
    assert library.name in api.libraries
    assert library.version in api.libraries[library.name]

def test_get_library():
    api = LibraryAPI()
    library = Library("test", "1.0", "example code")
    api.add_library(library)
    result = api.get_library("test", "1.0")
    assert result["name"] == "test"
    assert result["version"] == "1.0"
    assert result["sha256"] == hashlib.sha256("example code".encode()).hexdigest()

def test_get_library_not_found():
    api = LibraryAPI()
    try:
        api.get_library("test", "1.0")
        assert False
    except ValueError as e:
        assert str(e) == "Library 'test' not found"

def test_handle_request():
    api = LibraryAPI()
    library = Library("test", "1.0", "example code")
    api.add_library(library)
    result, status = api.handle_request("test", "1.0")
    assert status == 200
    result = json.loads(result)
    assert result["name"] == "test"
    assert result["version"] == "1.0"
    assert result["sha256"] == hashlib.sha256("example code".encode()).hexdigest()

def test_handle_request_not_found():
    api = LibraryAPI()
    result, status = api.handle_request("test", "1.0")
    assert status == 404
    result = json.loads(result)
    assert result["error"] == "Library 'test' not found"
