from __future__ import annotations

VALID_MONTH_ABBREVIATIONS = [
    "jan", "feb", "mar", "apr", "may", "jun",
    "jul", "aug", "sep", "oct", "nov", "dec",
]


class ResumeValidationError(Exception):
    def __init__(self, errors: list[str]) -> None:
        self.errors = errors
        super().__init__(f"Validation failed: {'; '.join(errors)}")


def _is_valid_email(value: str) -> bool:
    if not value or " " in value:
        return False

    parts = value.split("@")
    if len(parts) != 2:
        return False

    local_part = parts[0]
    domain_part = parts[1]

    if not local_part or not domain_part:
        return False

    if "." not in domain_part:
        return False

    return True


def _is_valid_url(value: str) -> bool:
    if not value or " " in value:
        return False

    url = value
    if url.startswith("https://"):
        url = url[len("https://"):]
    elif url.startswith("http://"):
        url = url[len("http://"):]

    if not url:
        return False

    domain = url.split("/")[0]

    if "." not in domain:
        return False

    return True


def _is_valid_date(value: str) -> bool:
    if not value:
        return False

    normalized = value.strip().lower()

    if normalized == "present":
        return True

    if normalized.isdigit() and len(normalized) == 4:
        return True

    parts = normalized.split()
    if len(parts) != 2:
        return False

    month_part = parts[0]
    year_part = parts[1]

    if month_part not in VALID_MONTH_ABBREVIATIONS:
        return False

    return year_part.isdigit() and len(year_part) == 4


def validate_required_fields(data: dict, required_keys: list[str]) -> list[str]:
    errors = []
    for key in required_keys:
        if key not in data or data[key] is None:
            errors.append(f"Missing required field: '{key}'")
        elif isinstance(data[key], str) and data[key].strip() == "":
            errors.append(f"Field '{key}' cannot be empty")
    return errors


def _validate_single_entry(
    entry: dict,
    required_keys: list[str],
    list_fields: list[str],
    date_fields: list[str],
) -> list[str]:
    errors = validate_required_fields(entry, required_keys)
    for field_name in list_fields:
        if field_name in entry and not isinstance(entry[field_name], list):
            errors.append(f"'{field_name}' must be a list")
    for field_name in date_fields:
        field_value = entry.get(field_name)
        if field_value and not _is_valid_date(str(field_value)):
            errors.append(f"Invalid {field_name} format: '{field_value}'")
    return errors


def _validate_entry_list(
    entries: list,
    label: str,
    required_keys: list[str],
    list_fields: list[str] = (),
    date_fields: list[str] = (),
) -> list[str]:
    if not isinstance(entries, list):
        return [f"'{label.lower()}' must be a list"]
    errors = []
    for index, entry in enumerate(entries):
        entry_label = f"{label} entry {index + 1}"
        if not isinstance(entry, dict):
            errors.append(f"{entry_label} must be a dictionary")
            continue
        entry_errors = _validate_single_entry(entry, required_keys, list_fields, date_fields)
        for error in entry_errors:
            errors.append(f"{entry_label}: {error}")
    return errors


def validate_contact_info(contact_dict: dict) -> list[str]:
    if not isinstance(contact_dict, dict):
        return ["'contact' must be a dictionary"]

    errors = validate_required_fields(contact_dict, ["name", "email"])

    email = contact_dict.get("email")
    if email and not _is_valid_email(email):
        errors.append(f"Invalid email format: '{email}'")

    linkedin = contact_dict.get("linkedin")
    if linkedin and not _is_valid_url(linkedin):
        errors.append(f"Invalid URL format for linkedin: '{linkedin}'")

    github = contact_dict.get("github")
    if github and not _is_valid_url(github):
        errors.append(f"Invalid URL format for github: '{github}'")

    return errors


def validate_experience_entries(entries: list) -> list[str]:
    required_keys = ["company", "role", "location", "start_date", "end_date", "bullets"]
    return _validate_entry_list(
        entries, "Experience", required_keys,
        list_fields=["bullets"],
        date_fields=["start_date", "end_date"],
    )


def validate_education_entries(entries: list) -> list[str]:
    required_keys = ["degree", "university", "start_date", "end_date"]
    return _validate_entry_list(
        entries, "Education", required_keys,
        date_fields=["start_date", "end_date"],
    )


def validate_skills_entries(entries: list) -> list[str]:
    if not isinstance(entries, list):
        return ["'skills' must be a list"]

    errors = []
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            errors.append(f"Skills entry {index + 1} must be a dictionary")
            continue

        if "category" not in entry or not entry["category"]:
            errors.append(f"Skills entry {index + 1}: Missing required field: 'category'")

        if "items" not in entry or not isinstance(entry["items"], list):
            errors.append(f"Skills entry {index + 1}: 'items' must be a list")

    return errors


def validate_project_entries(entries: list) -> list[str]:
    return _validate_entry_list(
        entries, "Project", ["name"],
        list_fields=["bullets"],
    )


def validate_resume_data(raw_dict: dict) -> list[str]:
    if not isinstance(raw_dict, dict):
        return ["Resume data must be a dictionary"]

    errors = []

    top_level_errors = validate_required_fields(raw_dict, ["contact", "summary"])
    errors.extend(top_level_errors)

    if "contact" in raw_dict:
        errors.extend(validate_contact_info(raw_dict["contact"]))

    if "experience" in raw_dict:
        errors.extend(validate_experience_entries(raw_dict["experience"]))

    if "education" in raw_dict:
        errors.extend(validate_education_entries(raw_dict["education"]))

    if "skills" in raw_dict:
        errors.extend(validate_skills_entries(raw_dict["skills"]))

    if "projects" in raw_dict:
        errors.extend(validate_project_entries(raw_dict["projects"]))

    return errors
