from __future__ import annotations

import yaml

from src.models.resume_data import (
    ContactInfo,
    Education,
    Experience,
    Project,
    ResumeData,
    SkillCategory,
)
from src.utils.validators import ResumeValidationError, validate_resume_data


class ResumeParseError(Exception):
    pass


def parse_resume_file(filepath: str) -> ResumeData:
    raw_dict = _load_yaml_file(filepath)
    _run_validation(raw_dict)
    return _build_resume_data(raw_dict)


def _load_yaml_file(filepath: str) -> dict:
    try:
        with open(filepath, "r") as file:
            data = yaml.safe_load(file)
    except FileNotFoundError:
        raise ResumeParseError(f"File not found: {filepath}")
    except yaml.YAMLError as exc:
        raise ResumeParseError(f"Invalid YAML syntax: {exc}")

    if data is None:
        raise ResumeParseError("YAML file is empty")

    return data


def _run_validation(raw_dict: dict) -> None:
    errors = validate_resume_data(raw_dict)
    if errors:
        raise ResumeValidationError(errors)


def _build_resume_data(raw_dict: dict) -> ResumeData:
    contact = _build_contact(raw_dict["contact"])
    summary = raw_dict["summary"]
    skills = _build_skills(raw_dict.get("skills", []))
    experience = _build_experience(raw_dict.get("experience", []))
    education = _build_education(raw_dict.get("education", []))
    projects = _build_projects(raw_dict.get("projects", []))

    return ResumeData(
        contact=contact,
        summary=summary,
        skills=skills,
        experience=experience,
        education=education,
        projects=projects,
    )


def _build_contact(contact_dict: dict) -> ContactInfo:
    return ContactInfo(
        name=contact_dict["name"],
        email=contact_dict["email"],
        phone=contact_dict.get("phone"),
        linkedin=contact_dict.get("linkedin"),
        github=contact_dict.get("github"),
        leetcode=contact_dict.get("leetcode"),
        location=contact_dict.get("location"),
    )


def _build_skills(skills_list: list[dict]) -> list[SkillCategory]:
    return [
        SkillCategory(
            category=entry["category"],
            items=entry.get("items", []),
        )
        for entry in skills_list
    ]


def _build_experience(experience_list: list[dict]) -> list[Experience]:
    return [
        Experience(
            company=entry["company"],
            role=entry["role"],
            location=entry["location"],
            start_date=str(entry["start_date"]),
            end_date=str(entry["end_date"]),
            bullets=entry.get("bullets", []),
        )
        for entry in experience_list
    ]


def _build_education(education_list: list[dict]) -> list[Education]:
    result = []
    for entry in education_list:
        edu = Education(
            degree=entry["degree"],
            university=entry["university"],
            start_date=str(entry["start_date"]),
            end_date=str(entry["end_date"]),
            details=entry.get("details", []),
        )
        result.append(edu)
    return result


def _build_projects(projects_list: list[dict]) -> list[Project]:
    result = []
    for entry in projects_list:
        proj = Project(
            name=entry["name"],
            description=entry.get("description", ""),
            tech_stack=entry.get("tech_stack", []),
            link=entry.get("link"),
            bullets=entry.get("bullets", []),
        )
        result.append(proj)
    return result
