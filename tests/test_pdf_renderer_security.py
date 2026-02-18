
import os
import pytest
from src.models.resume_data import (
    ResumeData,
    ContactInfo,
    SkillCategory,
    Experience,
    Education,
    Project,
)
from src.services.pdf_renderer import render_resume_pdf

def test_render_pdf_with_malicious_input(tmp_path):
    """
    Test that PDF generation handles malicious input (HTML tags, special chars)
    without crashing or raising XML parsing errors.
    """
    malicious_string = "User <Input> & 'Quotes' \"DoubleQuotes\" <script>alert(1)</script>"

    contact = ContactInfo(
        name=malicious_string,
        email="test@example.com",
        phone="123-456-7890",
        linkedin="linkedin.com/in/test",
        github="github.com/test",
        leetcode="leetcode.com/test",
        location=malicious_string,
    )

    skills = [
        SkillCategory(category=malicious_string, items=[malicious_string, "Python"]),
    ]

    experience = [
        Experience(
            company=malicious_string,
            role=malicious_string,
            location=malicious_string,
            start_date=malicious_string,
            end_date=malicious_string,
            bullets=[malicious_string],
        )
    ]

    education = [
        Education(
            degree=malicious_string,
            university=malicious_string,
            start_date=malicious_string,
            end_date=malicious_string,
            details=[malicious_string],
        )
    ]

    projects = [
        Project(
            name=malicious_string,
            description=malicious_string,
            tech_stack=[malicious_string],
            link=malicious_string,
            bullets=[malicious_string],
        )
    ]

    resume_data = ResumeData(
        contact=contact,
        summary=malicious_string,
        skills=skills,
        experience=experience,
        education=education,
        projects=projects,
    )

    output_path = tmp_path / "secure_resume.pdf"

    # Should not raise exception
    render_resume_pdf(resume_data, str(output_path))

    assert output_path.exists()
    assert output_path.stat().st_size > 0
