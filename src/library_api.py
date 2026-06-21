import json
from dataclasses import dataclass
from hashlib import sha256
from http import HTTPStatus
from typing import Dict

@dataclass
class Library:
    name: str
    version: str
    code: str

class LibraryAPI:
    def __init__(self):
        self.libraries: Dict[str, Dict[str, Library]] = {}

    def add_library(self, library: Library):
        if library.name not in self.libraries:
            self.libraries[library.name] = {}
        self.libraries[library.name][library.version] = library

    def get_library(self, name: str, version: str):
        if name not in self.libraries:
            raise ValueError(f"Library '{name}' not found")
        if version not in self.libraries[name]:
            raise ValueError(f"Version '{version}' not found for library '{name}'")
        library = self.libraries[name][version]
        return {
            "name": library.name,
            "version": library.version,
            "sha256": sha256(library.code.encode()).hexdigest(),
            "download_url": f"https://example.com/{library.name}/{library.version}.zip",
        }

    def handle_request(self, name: str, version: str):
        try:
            library = self.get_library(name, version)
            return json.dumps(library), HTTPStatus.OK
        except ValueError as e:
            return json.dumps({"error": str(e)}), HTTPStatus.NOT_FOUND
