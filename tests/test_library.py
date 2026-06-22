import pytest
from library import Library, LibraryMetadata
import json
import zipfile
from io import BytesIO

def test_library_from_zip():
    metadata = {'description': 'Test library'}
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_ref:
        manifest_data = {'name': 'test-library', 'version': '1.0', 'description': 'Test library'}
        zip_ref.writestr('manifest.json', json.dumps(manifest_data))
    library = Library.from_zip(zip_buffer.getvalue(), metadata)
    assert library.name == 'test-library'
    assert library.version == '1.0'
    assert library.metadata == metadata

def test_library_from_zip_missing_manifest_fields():
    metadata = {'description': 'Test library'}
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_ref:
        manifest_data = {'name': 'test-library'}
        zip_ref.writestr('manifest.json', json.dumps(manifest_data))
    with pytest.raises(ValueError):
        Library.from_zip(zip_buffer.getvalue(), metadata)

def test_library_to_dict():
    library = Library('test-library', '1.0', {'description': 'Test library'})
    library_dict = library.to_dict()
    assert library_dict['name'] == 'test-library'
    assert library_dict['version'] == '1.0'
    assert library_dict['metadata'] == {'description': 'Test library'}
