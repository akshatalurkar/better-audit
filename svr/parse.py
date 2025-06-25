from bs4 import BeautifulSoup
from bs4.element import Tag
import os

def extract_from_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    output_lines = []

    # Find the element containing GPA
    gpa_elem = soup.find(string=lambda text: isinstance(text, str) and "GPA:" in text)
    if gpa_elem is not None:
        gpa_text = str(gpa_elem)
        gpa = gpa_text.split("GPA:")[-1].strip()
        output_lines.append(f"GPA: {gpa}\n")
    else:
        output_lines.append("GPA: Not found\n")

    output_lines.append("Classes Taken:")
    table_rows = soup.find_all('tr')
    for row in table_rows:
        # Ensure row is a Tag before calling find_all
        if not isinstance(row, Tag):
            continue
        cells = row.find_all('td')
        if len(cells) >= 3:
            quarter = cells[0].text.strip()
            course = cells[1].text.strip()
            if course and any(q in quarter for q in ["FA", "WI", "SP", "S1", "S2"]):
                output_lines.append(f"{quarter} {course}")
    output_lines.append("")

    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output.txt")
    with open(output_path, "w") as f:
        f.write("\n".join(output_lines))

    return output_path
