from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ContactInfo:
    name: str
    email: str
    phone: str | None = None
    linkedin: str | None = None
    github: str | None = None
    location: str | None = None


@dataclass
class SkillCategory:
    category: str
    items: list[str] = field(default_factory=list)


@dataclass
class Experience:
    company: str
    role: str
    location: str
    start_date: str
    end_date: str
    bullets: list[str] = field(default_factory=list)


@dataclass
class Education:
    degree: str
    university: str
    start_date: str
    end_date: str
    details: list[str] = field(default_factory=list)


@dataclass
class Project:
    name: str
    description: str = ""
    tech_stack: list[str] = field(default_factory=list)
    link: str | None = None
    bullets: list[str] = field(default_factory=list)


@dataclass
class ResumeData:
    contact: ContactInfo
    summary: str
    skills: list[SkillCategory] = field(default_factory=list)
    experience: list[Experience] = field(default_factory=list)
    education: list[Education] = field(default_factory=list)
    projects: list[Project] = field(default_factory=list)
