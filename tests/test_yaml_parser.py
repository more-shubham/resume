
import pytest
from src.services.yaml_parser import _build_skills
from src.models.resume_data import SkillCategory

def test_build_skills_basic():
    skills_list = [
        {"category": "Programming", "items": ["Python", "Java"]},
        {"category": "Web", "items": ["HTML", "CSS"]}
    ]
    result = _build_skills(skills_list)
    assert len(result) == 2
    assert isinstance(result[0], SkillCategory)
    assert result[0].category == "Programming"
    assert result[0].items == ["Python", "Java"]
    assert result[1].category == "Web"
    assert result[1].items == ["HTML", "CSS"]

def test_build_skills_empty():
    skills_list = []
    result = _build_skills(skills_list)
    assert result == []

def test_build_skills_missing_items():
    skills_list = [
        {"category": "Soft Skills"}
    ]
    result = _build_skills(skills_list)
    assert len(result) == 1
    assert result[0].category == "Soft Skills"
    assert result[0].items == []

def test_build_skills_mixed():
    skills_list = [
        {"category": "Cat1", "items": ["A"]},
        {"category": "Cat2"}
    ]
    result = _build_skills(skills_list)
    assert len(result) == 2
    assert result[0].items == ["A"]
    assert result[1].items == []
