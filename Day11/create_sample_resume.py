"""
create_sample_resume.py - Build the sample_resume.pdf used all session

TEACHES : Nothing - this is a setup script. Run it once before class so
          every laptop has the same one-page resume PDF to extract from.
SLIDE   : none (it builds the file slides 13, 17 and 18 all refer to)
RUN     : python create_sample_resume.py

EXPECTED OUTPUT IN THE TERMINAL
        Wrote sample_resume.pdf (reportlab)
        Check: PdfReader sees 1 page
        Check: first non-empty line is 'Aarav Sharma'
        Check: email  found -> aarav.sharma@example.com
        Check: phone  found -> +91 98765 43210
    All four checks must say OK. If any fails, the exercise in files 09
    and 10 will not find what it is looking for.

TWO WAYS TO WRITE THE PDF
    1. reportlab, if it is installed - the normal path.
         pip install reportlab
    2. A tiny built-in writer, if it is not. PDF is a text format, so a
       readable one-page document is about 40 lines of string building
       and no dependencies at all. The output is plainer, but PyPDF2
       extracts exactly the same text from it - which is all today needs.

    Either way you end up with sample_resume.pdf in this folder.
"""

from pathlib import Path

PDF_FILE = Path(__file__).with_name("sample_resume.pdf")

# The resume, one line per line of the page. The ORDER MATTERS: PyPDF2
# extracts text in the order it was written, and the exercise takes the
# first non-empty line as the name - so "Aarav Sharma" has to be first.
RESUME_LINES: list[str] = [
    "Aarav Sharma",
    "Software Engineer",
    "aarav.sharma@example.com | +91 98765 43210",
    "Amritsar, Punjab 143001",
    "",
    "EDUCATION",
    "BCA, Hindu College Amritsar (2024 - 2027)",
    "Semester III, CGPA 8.4",
    "",
    "SKILLS",
    "Python, SQL, HTML, CSS, JavaScript",
    "Streamlit, pandas, Git, SQLite",
    "",
    "EXPERIENCE",
    "Web Development Intern, Zlaark (2026-06-01 to 2026-07-31)",
    "Built a Streamlit dashboard backed by SQLite",
    "Wrote Python scripts to clean and load CSV data",
    "",
    "PROJECTS",
    "Expense Tracker - Streamlit + SQLite, 2026-08-04",
    "Portfolio - https://aarav.example.com",
]

# Lines drawn in bold, at a larger size, when reportlab is available. Only
# cosmetic - the extracted text is identical either way.
HEADINGS = {"EDUCATION", "SKILLS", "EXPERIENCE", "PROJECTS"}


def write_with_reportlab(path: Path) -> None:
    """Draw the resume with reportlab. Raises ImportError if not installed."""
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas

    page = canvas.Canvas(str(path), pagesize=A4)
    _page_width, page_height = A4

    # Start near the top and walk down. PDF coordinates start at the
    # BOTTOM-left corner, so "down the page" means decreasing y.
    y = page_height - 60

    for index, line in enumerate(RESUME_LINES):
        if index == 0:
            page.setFont("Helvetica-Bold", 20)  # the name
        elif line in HEADINGS:
            page.setFont("Helvetica-Bold", 12)
        else:
            page.setFont("Helvetica", 11)

        page.drawString(50, y, line)
        y -= 22 if index == 0 else 16

    page.showPage()
    page.save()


def escape_pdf_text(text: str) -> str:
    """Escape the three characters that are special inside a PDF string."""
    # A PDF string is wrapped in ( ), so a literal bracket or backslash
    # inside it has to be escaped or the file will not parse.
    return text.replace("\\", r"\\").replace("(", r"\(").replace(")", r"\)")


def write_minimal_pdf(path: Path) -> None:
    """Write a valid one-page PDF by hand, with no third-party library."""
    # A PDF is five numbered objects: a catalog, a page list, the page, the
    # text to draw, and a font. The tricky part is the xref table at the
    # end, which records the byte offset of every object - so the objects
    # are built first and measured as they go.

    # The text-drawing instructions. BT/ET open and close a text block,
    # Tf picks the font and size, Td sets the start position, TL the line
    # spacing, Tj draws a string, and T* moves to the next line.
    instructions = ["BT", "/F1 11 Tf", "50 780 Td", "16 TL"]
    for line in RESUME_LINES:
        instructions.append(f"({escape_pdf_text(line)}) Tj")
        instructions.append("T*")
    instructions.append("ET")
    content = "\n".join(instructions).encode("latin-1")

    objects: list[bytes] = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] "
        b"/Resources << /Font << /F1 5 0 R >> >> /Contents 4 0 R >>",
        b"<< /Length " + str(len(content)).encode() + b" >>\nstream\n" + content + b"\nendstream",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>",
    ]

    out = bytearray(b"%PDF-1.4\n")
    offsets: list[int] = []
    for number, body in enumerate(objects, start=1):
        offsets.append(len(out))  # where this object starts, in bytes
        out += f"{number} 0 obj\n".encode() + body + b"\nendobj\n"

    # The cross-reference table: one fixed-width 20-byte line per object,
    # so a reader can jump straight to any object without scanning.
    xref_start = len(out)
    out += f"xref\n0 {len(objects) + 1}\n".encode()
    out += b"0000000000 65535 f \n"
    for offset in offsets:
        out += f"{offset:010d} 00000 n \n".encode()

    out += f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\n".encode()
    out += f"startxref\n{xref_start}\n%%EOF\n".encode()

    path.write_bytes(bytes(out))


def verify(path: Path) -> bool:
    """Read the PDF back and confirm the exercise will find what it needs."""
    try:
        from PyPDF2 import PdfReader
    except ImportError:
        # PyPDF2 3.x was renamed to pypdf. Same API, same author - so
        # either import gives the same PdfReader.
        from pypdf import PdfReader

    reader = PdfReader(str(path))
    full_text = ""
    for page in reader.pages:
        full_text += (page.extract_text() or "") + "\n"

    lines = [line.strip() for line in full_text.split("\n") if line.strip()]
    first_line = lines[0] if lines else ""

    checks = [
        (f"PdfReader sees {len(reader.pages)} page", len(reader.pages) == 1),
        (f"first non-empty line is {first_line!r}", first_line == "Aarav Sharma"),
        ("email  found -> aarav.sharma@example.com", "aarav.sharma@example.com" in full_text),
        ("phone  found -> +91 98765 43210", "+91 98765 43210" in full_text),
    ]

    all_passed = True
    for label, passed in checks:
        print(f"Check: {label} ... {'OK' if passed else 'FAILED'}")
        all_passed = all_passed and passed
    return all_passed


try:
    write_with_reportlab(PDF_FILE)
    print(f"Wrote {PDF_FILE.name} (reportlab)")
except ImportError:
    write_minimal_pdf(PDF_FILE)
    print(f"Wrote {PDF_FILE.name} (built-in writer - reportlab is not installed)")
    print("For a nicer-looking PDF: pip install reportlab, then run this again.")

if not verify(PDF_FILE):
    print("\nThe PDF was written but does not contain what the exercise expects.")
    print("Files 09 and 10 will not work until this is fixed.")
