import json
from dataclasses import dataclass
from typing import List

@dataclass
class Skill:
    name: str
    code_snippet: str
    ci_badge: str
    documentation_link: str
    version: str = None  # Added version attribute

class CodeForge:
    def __init__(self):
        self.skills = []

    def add_skill(self, skill: Skill):
        self.skills.append(skill)

    def search_skills(self, keyword: str = None, tag: str = None, version: str = None) -> List[Skill]:
        results = []
        for skill in self.skills:
            if (keyword and keyword not in skill.name) or (tag and tag not in skill.name) or (version and version != skill.version):
                continue
            results.append(skill)
            if len(results) >= 20:
                break
        return results

    def insert_code_snippet(self, skill: Skill, cursor_location: int) -> str:
        indentation = ''
        lines = skill.code_snippet.split('\n')
        indented_lines = [indentation + line for line in lines]
        code_snippet = '\n'.join(indented_lines)
        return code_snippet

    def get_ci_badge(self, skill: Skill) -> str:
        return skill.ci_badge

    def get_documentation_link(self, skill: Skill) -> str:
        return skill.documentation_link

    def handle_api_error(self, error: str) -> None:
        print(f"Error: {error}")
