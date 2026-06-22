import json
import zipfile
from dataclasses import dataclass
from typing import Dict
from io import BytesIO

@dataclass
class LibraryMetadata:
    name: str
    version: str
    description: str

class Library:
    def __init__(self, name: str, version: str, metadata: Dict):
        self.name = name
        self.version = version
        self.metadata = metadata

    @classmethod
    def from_zip(cls, zip_file: bytes, metadata: Dict) -> 'Library':
        zip_buffer = BytesIO(zip_file)
        with zipfile.ZipFile(zip_buffer, 'r') as zip_ref:
            manifest_file = zip_ref.open('manifest.json')
            manifest_data = json.load(manifest_file)
            required_fields = ['name', 'version', 'description']
            if not all(field in manifest_data for field in required_fields):
                raise ValueError("Manifest is missing required fields")
            return cls(manifest_data['name'], manifest_data['version'], metadata)

    def to_dict(self) -> Dict:
        return {
            'name': self.name,
            'version': self.version,
            'metadata': self.metadata
        }
