from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

FONT_NAME = "Helvetica"
FONT_NAME_BOLD = "Helvetica-Bold"
FONT_NAME_ITALIC = "Helvetica-Oblique"

NAME_FONT_SIZE = 16
CONTACT_FONT_SIZE = 9
SECTION_HEADER_FONT_SIZE = 10.5
COMPANY_ROLE_FONT_SIZE = 10
DATE_LOCATION_FONT_SIZE = 9
BULLET_FONT_SIZE = 9
SKILLS_FONT_SIZE = 9

PAGE_WIDTH, PAGE_HEIGHT = letter
PAGE_MARGIN = 36
CONTENT_WIDTH = PAGE_WIDTH - (2 * PAGE_MARGIN)

SECTION_SPACING = 4
BULLET_SPACING = 1
LINE_RULE_WIDTH = 0.5

LEFT_COLUMN_RATIO = 0.72
RIGHT_COLUMN_RATIO = 0.28
ITEM_VERTICAL_GAP = 3

EN_DASH = "\u2013"
EM_DASH = "\u2014"
BULLET_CHAR = "\u2022"
CONTACT_SEPARATOR = " | "

STYLE_NAME = ParagraphStyle(
    name="ResumeName",
    fontName=FONT_NAME_BOLD,
    fontSize=NAME_FONT_SIZE,
    alignment=TA_CENTER,
    spaceAfter=1,
    leading=NAME_FONT_SIZE + 2,
)

STYLE_CONTACT = ParagraphStyle(
    name="ContactInfo",
    fontName=FONT_NAME,
    fontSize=CONTACT_FONT_SIZE,
    alignment=TA_CENTER,
    spaceAfter=2,
    leading=CONTACT_FONT_SIZE + 2,
)

STYLE_SECTION_HEADER = ParagraphStyle(
    name="SectionHeader",
    fontName=FONT_NAME_BOLD,
    fontSize=SECTION_HEADER_FONT_SIZE,
    alignment=TA_LEFT,
    spaceBefore=SECTION_SPACING,
    spaceAfter=0,
    leading=SECTION_HEADER_FONT_SIZE + 2,
)

STYLE_ROLE_LEFT = ParagraphStyle(
    name="RoleLeft",
    fontName=FONT_NAME_BOLD,
    fontSize=COMPANY_ROLE_FONT_SIZE,
    alignment=TA_LEFT,
    spaceBefore=0,
    spaceAfter=0,
    leading=COMPANY_ROLE_FONT_SIZE + 2,
)

STYLE_DATE_RIGHT = ParagraphStyle(
    name="DateRight",
    fontName=FONT_NAME,
    fontSize=COMPANY_ROLE_FONT_SIZE,
    alignment=TA_RIGHT,
    spaceBefore=0,
    spaceAfter=0,
    leading=COMPANY_ROLE_FONT_SIZE + 2,
)

STYLE_LOCATION_LEFT = ParagraphStyle(
    name="LocationLeft",
    fontName=FONT_NAME_ITALIC,
    fontSize=DATE_LOCATION_FONT_SIZE,
    alignment=TA_LEFT,
    spaceBefore=0,
    spaceAfter=0,
    leading=DATE_LOCATION_FONT_SIZE + 2,
)

STYLE_BULLET = ParagraphStyle(
    name="BulletText",
    fontName=FONT_NAME,
    fontSize=BULLET_FONT_SIZE,
    alignment=TA_LEFT,
    spaceBefore=BULLET_SPACING,
    spaceAfter=0,
    leading=BULLET_FONT_SIZE + 2,
    leftIndent=6,
    firstLineIndent=-6,
)

STYLE_SKILLS = ParagraphStyle(
    name="SkillsText",
    fontName=FONT_NAME,
    fontSize=SKILLS_FONT_SIZE,
    alignment=TA_LEFT,
    spaceBefore=0,
    spaceAfter=0,
    leading=SKILLS_FONT_SIZE + 2,
)

STYLE_SUMMARY = ParagraphStyle(
    name="Summary",
    fontName=FONT_NAME,
    fontSize=BULLET_FONT_SIZE,
    alignment=TA_LEFT,
    spaceBefore=0,
    spaceAfter=0,
    leading=BULLET_FONT_SIZE + 2,
)

STYLE_PROJECT_NAME = ParagraphStyle(
    name="ProjectName",
    fontName=FONT_NAME_BOLD,
    fontSize=COMPANY_ROLE_FONT_SIZE,
    alignment=TA_LEFT,
    spaceBefore=0,
    spaceAfter=0,
    leading=COMPANY_ROLE_FONT_SIZE + 2,
)

STYLE_PROJECT_DETAIL = ParagraphStyle(
    name="ProjectDetail",
    fontName=FONT_NAME,
    fontSize=BULLET_FONT_SIZE,
    alignment=TA_LEFT,
    spaceBefore=0,
    spaceAfter=0,
    leading=BULLET_FONT_SIZE + 2,
)
