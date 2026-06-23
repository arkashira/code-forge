import pytest
from code_forge import CodeForge, Skill

@pytest.fixture
def code_forge():
    code_forge = CodeForge()
    skill1 = Skill("Skill 1", "print('Hello World')", "https://example.com/ci-badge", "https://example.com/docs", version="1")
    skill2 = Skill("Skill 2", "print('Hello World 2')", "https://example.com/ci-badge-2", "https://example.com/docs-2", version="2")
    code_forge.add_skill(skill1)
    code_forge.add_skill(skill2)
    return code_forge

def test_search_skills(code_forge):
    results = code_forge.search_skills(keyword="Skill")
    assert len(results) == 2

def test_search_skills_with_tag(code_forge):
    results = code_forge.search_skills(tag="Skill")
    assert len(results) == 2

def test_search_skills_with_version(code_forge):
    results = code_forge.search_skills(version="1")
    assert len(results) == 1

def test_insert_code_snippet(code_forge):
    skill = code_forge.skills[0]
    code_snippet = code_forge.insert_code_snippet(skill, 0)
    assert code_snippet == "print('Hello World')"

def test_get_ci_badge(code_forge):
    skill = code_forge.skills[0]
    ci_badge = code_forge.get_ci_badge(skill)
    assert ci_badge == "https://example.com/ci-badge"

def test_get_documentation_link(code_forge):
    skill = code_forge.skills[0]
    documentation_link = code_forge.get_documentation_link(skill)
    assert documentation_link == "https://example.com/docs"

def test_handle_api_error(code_forge):
    error = "API Error"
    code_forge.handle_api_error(error)
    # No assertion, just checking that it runs without error
