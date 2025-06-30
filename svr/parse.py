from bs4 import BeautifulSoup
from bs4.element import Tag
import os

def extract_from_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    output_lines = []

    #Getting GPA value from the HTML file here
    gpa_value = None
    for label_td in soup.find_all('td', class_='gpalabel'):
        if 'GPA' in label_td.get_text():
            gpa_td = label_td.find_previous_sibling('td', class_='gpa number')
            if gpa_td:
                gpa_value = gpa_td.get_text(strip=True)
                break
    if gpa_value:
        output_lines.append(f"GPA: {gpa_value}\n")
    else:
        output_lines.append("GPA: Not found\n")

    #Getting classes taken from the HTML file here
    output_lines.append("Classes Taken:")

    #Setting up ordering logic
    classes_list = []
    quarter_order = {
        "WI": 1,
        "SP": 2,
        "S1": 3,
        "S2": 4,
        "FA": 5
    }

    #Setting up duplicate removal logic
    seen_courses = set()

    table_rows = soup.find_all('tr')
    for row in table_rows:
        if not isinstance(row, Tag):
            continue
        cells = row.find_all('td')
        if len(cells) >= 3:
            quarter = cells[0].text.strip()
            course = cells[1].text.strip()

            #Fixing the detection of WIP credit elements
            prefix = quarter[:2]
            year_str = quarter[2:]
            if prefix in quarter_order and year_str.isdigit():
                if (quarter, course) not in seen_courses:
                    seen_courses.add((quarter, course))
                    year = int(year_str)
                    order = quarter_order[prefix]
                    formatted = f"{quarter} {course}"
                    classes_list.append((year, order, formatted))

    classes_list.sort()

    for _, _, formatted in classes_list:
        output_lines.append(formatted)

    output_lines.append("")

    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output.txt")
    with open(output_path, "w") as f:
        f.write("\n".join(output_lines))

    return output_path
