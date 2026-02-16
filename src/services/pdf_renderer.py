from __future__ import annotations

import os
from datetime import datetime
from typing import Callable

from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    HRFlowable,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

from src.core.styles import (
    BULLET_CHAR,
    CONTACT_SEPARATOR,
    CONTENT_WIDTH,
    EM_DASH,
    EN_DASH,
    ITEM_VERTICAL_GAP,
    LEFT_COLUMN_RATIO,
    LINE_RULE_WIDTH,
    PAGE_HEIGHT,
    PAGE_MARGIN,
    PAGE_WIDTH,
    RIGHT_COLUMN_RATIO,
    STYLE_BULLET,
    STYLE_CONTACT,
    STYLE_DATE_RIGHT,
    STYLE_LOCATION_LEFT,
    STYLE_NAME,
    STYLE_PROJECT_DETAIL,
    STYLE_PROJECT_NAME,
    STYLE_ROLE_LEFT,
    STYLE_SECTION_HEADER,
    STYLE_SKILLS,
    STYLE_SUMMARY,
)
from src.models.resume_data import (
    ContactInfo,
    Education,
    Experience,
    Project,
    ResumeData,
    SkillCategory,
)


def render_resume_pdf(resume_data: ResumeData, output_path: str) -> None:
    _ensure_output_directory(output_path)
    doc = _create_document(resume_data, output_path)
    flowables = _build_all_flowables(resume_data)
    doc.build(flowables)


def _create_document(resume_data: ResumeData, output_path: str) -> BaseDocTemplate:
    frame = Frame(
        PAGE_MARGIN,
        PAGE_MARGIN,
        CONTENT_WIDTH,
        PAGE_HEIGHT - (2 * PAGE_MARGIN),
        leftPadding=0,
        rightPadding=0,
        topPadding=0,
        bottomPadding=0,
    )
    keywords = _build_keywords(resume_data.skills)
    doc = BaseDocTemplate(
        output_path,
        pagesize=(PAGE_WIDTH, PAGE_HEIGHT),
        leftMargin=PAGE_MARGIN,
        rightMargin=PAGE_MARGIN,
        topMargin=PAGE_MARGIN,
        bottomMargin=PAGE_MARGIN,
        title=f"{resume_data.contact.name} - Resume",
        author=resume_data.contact.name,
        subject=resume_data.summary,
        keywords=keywords,
        creator=f"Resume Generator - {datetime.now().strftime('%Y-%m-%d %H:%M')}",
    )
    doc.addPageTemplates([PageTemplate(id="main", frames=[frame])])
    return doc


def _build_keywords(skills: list[SkillCategory]) -> str:
    all_items = []
    for skill_category in skills:
        for item in skill_category.items:
            all_items.append(item)
    return ", ".join(all_items)


def _ensure_output_directory(output_path: str) -> None:
    directory = os.path.dirname(output_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)


def _build_all_flowables(resume_data: ResumeData) -> list:
    flowables = []

    flowables.extend(_build_contact_header(resume_data.contact))

    if resume_data.summary:
        flowables.extend(_build_summary_section(resume_data.summary))

    if resume_data.skills:
        flowables.extend(_build_skills_section(resume_data.skills))

    if resume_data.experience:
        flowables.extend(_build_experience_section(resume_data.experience))

    if resume_data.projects:
        flowables.extend(_build_projects_section(resume_data.projects))

    if resume_data.education:
        flowables.extend(_build_education_section(resume_data.education))

    return flowables


def _build_contact_header(contact: ContactInfo) -> list:
    flowables = []

    flowables.append(Paragraph(contact.name, STYLE_NAME))

    contact_parts = [contact.email]
    if contact.phone:
        contact_parts.append(contact.phone)
    if contact.linkedin:
        contact_parts.append(contact.linkedin)
    if contact.github:
        contact_parts.append(contact.github)
    if contact.location:
        contact_parts.append(contact.location)

    contact_line = CONTACT_SEPARATOR.join(contact_parts)
    flowables.append(Paragraph(contact_line, STYLE_CONTACT))

    return flowables


def _build_section_header(title: str) -> list:
    flowables = []

    flowables.append(Paragraph(title.upper(), STYLE_SECTION_HEADER))

    rule = HRFlowable(
        width="100%",
        thickness=LINE_RULE_WIDTH,
        color="black",
        spaceAfter=2,
        spaceBefore=0,
    )
    flowables.append(rule)

    return flowables


def _build_two_column_row(
    left_text: str,
    left_style: ParagraphStyle,
    right_text: str,
    right_style: ParagraphStyle,
) -> Table:
    left_paragraph = Paragraph(left_text, left_style)
    right_paragraph = Paragraph(right_text, right_style)

    left_column_width = CONTENT_WIDTH * LEFT_COLUMN_RATIO
    right_column_width = CONTENT_WIDTH * RIGHT_COLUMN_RATIO

    table = Table(
        [[left_paragraph, right_paragraph]],
        colWidths=[left_column_width, right_column_width],
    )
    table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))

    return table


def _build_summary_section(summary: str) -> list:
    flowables = []
    flowables.extend(_build_section_header("Summary"))
    flowables.append(Paragraph(summary, STYLE_SUMMARY))
    return flowables


def _build_skills_section(skills: list[SkillCategory]) -> list:
    flowables = []
    flowables.extend(_build_section_header("Skills"))

    for skill_category in skills:
        items_text = ", ".join(skill_category.items)
        line = f"<b>{skill_category.category}:</b> {items_text}"
        flowables.append(Paragraph(line, STYLE_SKILLS))

    return flowables


def _build_list_section(title: str, items: list, build_single_item: Callable) -> list:
    flowables = []
    flowables.extend(_build_section_header(title))
    for index, item in enumerate(items):
        if index > 0:
            flowables.append(Spacer(1, ITEM_VERTICAL_GAP))
        flowables.extend(build_single_item(item))
    return flowables


def _build_experience_section(experiences: list[Experience]) -> list:
    return _build_list_section("Experience", experiences, _build_single_experience)


def _build_single_experience(exp: Experience) -> list:
    flowables = []

    date_range = f"{exp.start_date} {EN_DASH} {exp.end_date}"
    role_text = f"<b>{exp.company}</b> {EM_DASH} {exp.role}"

    row = _build_two_column_row(
        role_text, STYLE_ROLE_LEFT,
        date_range, STYLE_DATE_RIGHT,
    )
    flowables.append(row)

    location_row = _build_two_column_row(
        f"<i>{exp.location}</i>", STYLE_LOCATION_LEFT,
        "", STYLE_LOCATION_LEFT,
    )
    flowables.append(location_row)

    for bullet in exp.bullets:
        bullet_text = f"{BULLET_CHAR} {bullet}"
        flowables.append(Paragraph(bullet_text, STYLE_BULLET))

    return flowables


def _build_education_section(education: list[Education]) -> list:
    return _build_list_section("Education", education, _build_single_education)


def _build_single_education(edu: Education) -> list:
    flowables = []

    date_range = f"{edu.start_date} {EN_DASH} {edu.end_date}"
    degree_text = f"<b>{edu.university}</b> {EM_DASH} {edu.degree}"

    row = _build_two_column_row(
        degree_text, STYLE_ROLE_LEFT,
        date_range, STYLE_DATE_RIGHT,
    )
    flowables.append(row)

    for detail in edu.details:
        detail_text = f"{BULLET_CHAR} {detail}"
        flowables.append(Paragraph(detail_text, STYLE_BULLET))

    return flowables


def _build_projects_section(projects: list[Project]) -> list:
    return _build_list_section("Projects", projects, _build_single_project)


def _build_single_project(proj: Project) -> list:
    flowables = []

    name_text = f"<b>{proj.name}</b>"
    if proj.link:
        name_text = f"<b>{proj.name}</b> | {proj.link}"
    flowables.append(Paragraph(name_text, STYLE_PROJECT_NAME))

    if proj.description:
        flowables.append(Paragraph(proj.description, STYLE_PROJECT_DETAIL))

    for bullet in proj.bullets:
        bullet_text = f"{BULLET_CHAR} {bullet}"
        flowables.append(Paragraph(bullet_text, STYLE_BULLET))

    if proj.tech_stack:
        tech_text = f"<b>Tech:</b> {', '.join(proj.tech_stack)}"
        flowables.append(Paragraph(tech_text, STYLE_PROJECT_DETAIL))

    return flowables
