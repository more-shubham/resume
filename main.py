import argparse
import sys

from src.core.settings import DEFAULT_INPUT_PATH, DEFAULT_OUTPUT_PATH
from src.services.pdf_renderer import render_resume_pdf
from src.services.yaml_parser import ResumeParseError, parse_resume_file
from src.utils.validators import ResumeValidationError


def main() -> None:
    args = parse_arguments()

    try:
        resume_data = parse_resume_file(args.input)
        render_resume_pdf(resume_data, args.output)
        sys.exit(0)
    except ResumeParseError as parse_error:
        sys.stderr.write(f"Parse error: {parse_error}\n")
        sys.exit(1)
    except ResumeValidationError as validation_error:
        sys.stderr.write(f"Validation error: {validation_error}\n")
        sys.exit(1)
    except Exception as unexpected_error:
        sys.stderr.write(f"Unexpected error: {unexpected_error}\n")
        sys.exit(1)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a professional PDF resume from YAML data"
    )
    parser.add_argument(
        "--input",
        default=DEFAULT_INPUT_PATH,
        help=f"Path to YAML resume file (default: {DEFAULT_INPUT_PATH})",
    )
    parser.add_argument(
        "--output",
        default=DEFAULT_OUTPUT_PATH,
        help=f"Path for output PDF (default: {DEFAULT_OUTPUT_PATH})",
    )
    return parser.parse_args()


if __name__ == "__main__":
    main()
