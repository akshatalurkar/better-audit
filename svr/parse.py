from bs4 import BeautifulSoup
from bs4.element import Tag
import os
import re

#Prerequisite Dictionary
prereqs = {
    # MATH lower division
    "MATH 3C": ["MATH 3B"],
    "MATH 4C": [["MATH 3C"], "Math Placement Exam", "ACT Math 25+", "AP Calc AB 2"],
    "MATH 10A": [["MATH 3C", "MATH 4C"], "Math Placement Exam", "AP Calc AB 2"],
    "MATH 10B": [["MATH 10A", "MATH 20A"]],
    "MATH 10C": [["MATH 10B", "MATH 20B"]],
    "MATH 11": [["MATH 10B", "MATH 20B", "AP Calc BC 3+"]],
    "MATH 15A": [["CSE 8B", "CSE 11"]],
    "MATH 18": [["MATH 4C", "MATH 10A", "MATH 20A"], "Math Placement Exam", "AP Calc AB 3", "SAT Math Level 2 650+"],
    "MATH 20A": [["MATH 4C", "MATH 10A"], "Math Placement Exam", "AP Calc AB 3", "SAT Math 650+"],
    "MATH 20B": [["MATH 20A", "MATH 10B", "MATH 10C", "AP Calc BC 3+"], "AP Calc AB 4+"],
    "MATH 20C": [["MATH 20B", "AP Calc BC 4+"]],
    "MATH 20D": ["MATH 20C", ["MATH 18", "MATH 31AH"]],
    "MATH 20E": [["MATH 18", "MATH 20F", "MATH 31AH"], ["MATH 20C", "MATH 21C", "MATH 31BH"]],
    "MATH 31AH": ["AP Calc BC 5", "Instructor consent"],
    "MATH 31BH": ["MATH 31AH", "Instructor consent"],
    "MATH 31CH": ["MATH 31BH", "Instructor consent"],

    # MATH upper division
    "MATH 100A": [["MATH 31CH", "MATH 109", "Instructor consent"]],
    "MATH 100B": ["MATH 100A"],
    "MATH 100C": ["MATH 100B"],
    "MATH 102": [["MATH 18", "MATH 20F", "MATH 31AH"], "MATH 20C"],
    "MATH 103A": [["MATH 31CH", "MATH 109", "Instructor consent"]],
    "MATH 103B": [["MATH 103A", "MATH 100A", "Instructor consent"]],
    "MATH 104A": [["MATH 100B", "MATH 103B", "Instructor consent"]],
    "MATH 104B": [["MATH 104A", "Instructor consent"]],
    "MATH 105": [["MATH 31CH", "MATH 109", "Instructor consent"]],
    "MATH 106": [["MATH 100B", "MATH 103B", "Instructor consent"]],
    "MATH 109": [["MATH 18", "MATH 20F", "MATH 31AH"], "MATH 20C"],
    "MATH 110": [["MATH 18", "MATH 20F", "MATH 31AH"], "MATH 20D", ["MATH 20E", "MATH 31CH"]],
    "MATH 111A": ["MATH 20D", ["MATH 18", "MATH 20F", "MATH 31AH"], ["MATH 109", "MATH 31CH"]],
    "MATH 111B": ["MATH 111A"],
    "MATH 112A": [["MATH 11", "MATH 180A", "MATH 183", "MATH 186"], ["MATH 18", "MATH 31AH"], "MATH 20D", "BILD 1"],
    "MATH 112B": ["MATH 112A", "MATH 110", "MATH 180A"],
    "MATH 114": ["MATH 180A"],
    "MATH 120A": [["MATH 20E", "MATH 31CH"]],
    "MATH 120B": ["MATH 120A"],
    "MATH 121A": [["EDS 30", "MATH 95"], ["MATH 31CH", "MATH 109"]],
    "MATH 121B": ["MATH 121A"],
    "MATH 130": [["MATH 18", "MATH 20F", "MATH 31AH"], "MATH 20D"],
    "MATH 140A": [["MATH 31CH", "MATH 109"]],
    "MATH 140B": ["MATH 140A"],
    "MATH 140C": ["MATH 140B"],
    "MATH 142A": [["MATH 31CH", "MATH 109"]],
    "MATH 142B": [["MATH 142A", "MATH 140A"]],
    "MATH 144": [["MATH 140B", "MATH 142B"]],
    "MATH 146": [["MATH 140B", "MATH 142B"]],
    "MATH 148": [["MATH 140B", "MATH 142B"]],
    "MATH 150A": [["MATH 20E", "MATH 31CH"], ["MATH 18", "MATH 20F", "MATH 31AH"]],
    "MATH 150B": ["MATH 150A"],
    "MATH 152": ["MATH 20D", ["MATH 18", "MATH 20F", "MATH 31AH"]],
    "MATH 153": [["MATH 109", "MATH 31CH"]],
    "MATH 154": [["MATH 31CH", "MATH 109"]],
    "MATH 155A": [["MATH 18", "MATH 20F", "MATH 31AH"], "MATH 20C"],
    "MATH 155B": ["MATH 155A"],
    "MATH 157": [["MATH 18", "MATH 20F", "MATH 31AH"], ["BILD 62", "COGS 18", "CSE 5A", "CSE 6R", "CSE 8A", "CSE 11", "DSC 10", "ECE 15", "ECE 143", "MATH 189"]],
    "MATH 158": [["MATH 31CH", "MATH 109"]],
    "MATH 160A": [["MATH 100A", "MATH 103A", "MATH 140A"]],
    "MATH 160B": ["MATH 160A"],
    "MATH 163": [["MATH 20B", "Instructor consent"]],
    "MATH 168A": [["MATH 18", "MATH 20F", "MATH 31AH"], "MATH 20C"],
    "MATH 170A": [["MATH 18", "MATH 31AH"], ["MATH 20C", "MATH 31BH"], ["CSE 20", "MATH 15A", "MATH 31CH", "MATH 109"]],
    "MATH 170B": ["MATH 170A"],
    "MATH 170C": [["MATH 20D", "MATH 21D"], "MATH 170B"],
    "MATH 171A": [["MATH 18", "MATH 20F", "MATH 31AH"], "MATH 20C"],
    "MATH 171B": [["MATH 20C", "MATH 31BH"], "MATH 171A"],
    "MATH 173A": [["MATH 20C", "MATH 31BH"], ["MATH 18", "MATH 20F", "MATH 31AH"]],
    "MATH 173B": ["MATH 173A"],
    "MATH 174": [["MATH 20D", "MATH 21D"], ["MATH 20F", "MATH 31AH"]],
    "MATH 175": [["MATH 174"]],
    "MATH 179": [["MATH 174"]],
    "MATH 180A": [["MATH 20C", "MATH 31BH"]],
    "MATH 180B": ["MATH 20D", ["MATH 18", "MATH 20F", "MATH 31AH"], ["MATH 109", "MATH 31CH"], "MATH 180A"],
    "MATH 180C": ["MATH 180B"],
    "MATH 181A": ["MATH 180A", ["MATH 18", "MATH 20F", "MATH 31AH"], ["MATH 20C", "MATH 31BH"]],
    "MATH 181B": ["MATH 181A"],
    "MATH 181C": ["MATH 181B"],
    "MATH 181D": [["ECE 109", "ECON 120A", "MAE 108", "MATH 181A", "MATH 183", "MATH 186", "MATH 189"]],
    "MATH 181E": ["MATH 181B"],
    "MATH 181F": [["ECE 109", "ECON 120A", "MAE 108", "MATH 11", "MATH 181A", "MATH 183", "MATH 186", "MATH 189"]],
    "MATH 182": ["MATH 180A", ["MATH 18", "MATH 31AH"]],
    "MATH 183": [["MATH 20C", "MATH 31BH"]],
    "MATH 184": [["MATH 31CH", "MATH 109"]],
    "MATH 185": ["MATH 181A", ["MATH 18", "MATH 20F", "MATH 31AH"], ["MATH 20C", "MATH 31BH"]],
    "MATH 186": [["MATH 20C", "MATH 31BH"]],
    "MATH 187A": [["MATH 10A", "MATH 20A"]],
    "MATH 187B": ["MATH 187A", ["MATH 18", "MATH 20F", "MATH 31AH"]],
    "MATH 188": [["MATH 31CH", "MATH 109"], ["MATH 18", "MATH 31AH"], ["MATH 100A", "MATH 103A"]],
    "MATH 189": [["MATH 18", "MATH 20F", "MATH 31AH"], "MATH 20C", ["BENG 134", "COGS 118D", "CSE 103", "ECE 109", "ECON 120A", "MAE 108", "MATH 180A", "MATH 183", "MATH 186", "SE 125"]],
    "MATH 190A": [["MATH 31CH", "MATH 140A", "MATH 142A"]],
    "MATH 190B": ["MATH 190A"],
    "MATH 191": [["MATH 190A", "Instructor consent"]],
    "MATH 193A": [["MATH 180A", "MATH 183"]],
    "MATH 193B": ["MATH 193A"],
    "MATH 194": ["MATH 20D", ["MATH 18", "MATH 20F", "MATH 31AH"], "MATH 180A"],

    #CSE Lower Division
    "CSE 3": [],
    "CSE 4GS": [["MATH 10A", "MATH 20A"], "Department approval", "Corequisite: CSE 6GS"],
    "CSE 6GS": [["MATH 10A", "MATH 20A"], "Department approval", "Corequisite: CSE 4GS"],
    "CSE 6R": [],
    "CSE 8A": [],
    "CSE 8B": ["CSE 8A"],
    "CSE 11": [],
    "CSE 12": [["CSE 8B", "CSE 11"]],
    "CSE 15L": [["CSE 8B", "CSE 11", "CSE 12", "DSC 30"]],
    "CSE 20": [["CSE 11", "CSE 6R", "CSE 8A", "CSE 8B", "ECE 15"]],
    "CSE 21": [["CSE 20", "MATH 15A", "MATH 31CH"]],
    "CSE 25": [["COGS 18", "CSE 11", "CSE 6R", "CSE 8A", "CSE 8B", "DSC 20"]],
    "CSE 29": [["CSE 11", "CSE 8B", "ECE 15"]],
    "CSE 30": [["CSE 15L", "CSE 29", "ECE 15"]],
    "CSE 42": ["Instructor approval"],
    "CSE 55": ["CSE 12", "CSE 25", ["CSE 15L", "CSE 29"], ["MATH 18", "MATH 31AH"], ["MATH 20C", "MATH 31BH"]],
    "CSE 86": [["CSE 12", "Instructor consent"]],
    "CSE 87": [],
    "CSE 89": [],
    "CSE 90": [],
    "CSE 91": ["Majors only"],
    "CSE 95": ["Concurrent tutor appointment"],
    "CSE 99": ["Lower-division standing", "30 units completed at UCSD", "UCSD GPA ≥ 3.0", "Department approval", "Instructor consent"],

    #CSE Upper Division
    "CSE 100": [["CSE 21", "MATH 154", "MATH 158", "MATH 184", "MATH 188"], "CSE 12", ["CSE 15L", "CSE 29", "ECE 15"]],
    "CSE 100R": [["CSE 21", "MATH 154", "MATH 158", "MATH 184", "MATH 188"], "CSE 12", ["CSE 15L", "CSE 29", "ECE 15"]],
    "CSE 101": [["CSE 21", "MATH 154", "MATH 158", "MATH 184", "MATH 188"], ["CSE 12", "DSC 30"]],
    "CSE 103": ["MATH 20B", ["CSE 21", "MATH 154", "MATH 158", "MATH 184", "MATH 188"]],
    "CSE 105": ["CSE 12", ["CSE 20", "MATH 109", "MATH 15A", "MATH 31CH"], ["CSE 21", "MATH 100A", "MATH 103A", "MATH 154", "MATH 158", "MATH 184", "MATH 188"]],
    "CSE 106": [["MATH 18", "MATH 31AH"], ["MATH 20C", "MATH 31BH"], ["CSE 21", "DSC 40B", "MATH 154", "MATH 158", "MATH 184", "MATH 188"]],
    "CSE 107": [["CSE 21", "MATH 154", "MATH 158", "MATH 184", "MATH 188"], "CSE 101", "CSE 105"],
    "CSE 109": [["CSE 15L", "CSE 29", "Instructor consent"]],
    "CSE 110": [["CSE 100", "CSE 100R"]],
    "CSE 112": ["CSE 110"],
    "CSE 118": [["COGS 102C", "COGS 121", "COGS 184", "COGS 184GS", "CSE 131", "CSE 132B", "ECE 111", "ECE 118", "ECE 191", "ECE 192"]],
    "CSE 120": [["CSE 15L", "CSE 29"], "CSE 30", ["CSE 100", "CSE 100R"], "CSE 101"],
    "CSE 121": ["CSE 120"],
    "CSE 122": [["CSE 30", "ECE 30"], ["CSE 101", "ECE 141A"], ["CSE 110", "ECE 141B"]],
    "CSE 123": [["CSE 15L", "CSE 29"], "CSE 101", "CSE 110"],
    "CSE 124": [["CSE 15L", "CSE 29"], "CSE 101", "CSE 110"],
    "CSE 125": ["Senior standing", "Substantial programming experience", "Instructor consent"],
    "CSE 127": [["CSE 21", "MATH 154", "MATH 158", "MATH 184", "MATH 188"], ["CSE 120", "CSE 123", "CSE 124", "ECE 158A", "ECE 158B"]],
    "CSE 130": ["CSE 12", ["CSE 100", "CSE 100R"], "CSE 105"],
    "CSE 131": ["CSE 30", ["CSE 100", "CSE 100R"], "CSE 105", "CSE 130"],
    "CSE 132A": [["CSE 100", "CSE 100R"]],
    "CSE 132B": ["CSE 132A"],
    "CSE 132C": [["CSE 132A", "DSC 102"]],
    "CSE 134B": [["CSE 100", "CSE 100R"]],
    "CSE 135": [["CSE 100", "CSE 100R"]],
    "CSE 136": ["CSE 135"],
    "CSE 140": [["CSE 30", "ECE 30"]],
    "CSE 140L": ["CSE 30"],
    "CSE 141": [["CSE 30", "ECE 30"], "CSE 140"],
    "CSE 141L": [["CSE 30", "ECE 30"], "CSE 140"],
    "CSE 142": [["CSE 30", "ECE 30"], ["CSE 100", "CSE 100R"]],
    "CSE 142L": [["CSE 30", "ECE 30"], ["CSE 100", "CSE 100R"]],
    "CSE 143": ["CSE 140"],
    "CSE 145": ["Instructor approval"],
    "CSE 147": ["CSE 30"],
    "CSE 148": ["CSE 141", "CSE 141L"],
    "CSE 150A": [["CSE 12", "DSC 40B"], ["CSE 15L", "CSE 29", "DSC 80"], ["COGS 118D", "CSE 103", "ECE 109", "ECON 120A", "MAE 108", "MATH 180A", "MATH 180B", "MATH 181A", "MATH 183", "MATH 186"], "MATH 20A", ["MATH 18", "MATH 31AH"]],
    "CSE 150B": [["CSE 12", "DSC 40B"], ["CSE 15L", "CSE 29", "DSC 80"], ["COGS 118D", "CSE 103", "ECE 109", "ECON 120A", "MAE 108", "MATH 180A", "MATH 180B", "MATH 181A", "MATH 183", "MATH 186"], ["CSE 100", "CSE 100R"]],
    "CSE 151A": [["CSE 12", "DSC 40B"], ["CSE 15L", "CSE 29", "DSC 80"], ["COGS 118D", "CSE 103", "ECE 109", "ECON 120A", "MAE 108", "MATH 180A", "MATH 180B", "MATH 181A", "MATH 183", "MATH 186"], ["MATH 18", "MATH 31AH"], ["MATH 20C", "MATH 31BH"]],
    "CSE 151B": [["MATH 20C", "MATH 31BH"], ["BENG 134", "COGS 118D", "CSE 103", "ECE 109", "ECON 120A", "MAE 108", "MATH 180A", "MATH 180B", "MATH 181A", "MATH 183", "MATH 186", "SE 125"], ["COGS 118A", "COGS 118B", "COGS 188", "CSE 151A", "ECE 175A"]],
    "CSE 152A": [["MATH 18", "MATH 31AH"], ["CSE 12", "DSC 30"], ["CSE 15L", "CSE 29", "DSC 80"]],
    "CSE 152B": [["CSE 152A", "CSE 152", "CSE 166"]],
    "CSE 153": [["CSE 12", "DSC 40B"], ["CSE 15L", "CSE 29", "DSC 80"], ["BENG 100", "BENG 134", "COGS 118D", "CSE 103", "ECE 109", "ECON 120A", "MAE 108", "MATH 180A", "MATH 180B", "MATH 181A", "MATH 183", "MATH 186"]],
    "CSE 153R": [["CSE 12", "DSC 40B"], ["CSE 15L", "CSE 29", "DSC 80"], ["BENG 100", "BENG 134", "COGS 118D", "CSE 103", "ECE 109", "ECON 120A", "MAE 108", "MATH 180A", "MATH 180B", "MATH 181A", "MATH 183", "MATH 186"]],
    "CSE 156": [["CSE 12", "DSC 40B"], ["CSE 15L", "CSE 29", "DSC 80"], ["BENG 134", "COGS 118D", "CSE 103", "ECE 109", "ECON 120A", "MAE 108", "MATH 180A", "MATH 180B", "MATH 181A", "MATH 183", "MATH 186"]],
    "CSE 158": [["CSE 12", "DSC 40B"], ["CSE 15L", "CSE 29", "DSC 80"], ["BENG 100", "BENG 134", "COGS 118D", "CSE 103", "ECE 109", "ECON 120A", "MAE 108", "MATH 180A", "MATH 180B", "MATH 181A", "MATH 183", "MATH 186"]],
    "CSE 158R": [["CSE 12", "DSC 40B"], ["CSE 15L", "CSE 29", "DSC 80"], ["BENG 100", "BENG 134", "COGS 118D", "CSE 103", "ECE 109", "ECON 120A", "MAE 108", "MATH 180A", "MATH 180B", "MATH 181A", "MATH 183", "MATH 186"]],
    "CSE 160": [["CSE 100", "CSE 100R"]],
    "CSE 163": ["CSE 167"],
    "CSE 165": [["CSE 167", "CSE 167R", "MATH 155A"]],
    "CSE 166": [["DSC 40B", "MATH 18", "MATH 31AH"], ["CSE 100", "CSE 100R", "DSC 80"]],
    "CSE 167": [["CSE 100", "CSE 100R"]],
    "CSE 167R": [["CSE 100", "CSE 100R"]],
    "CSE 168": [["CSE 167", "CSE 167R", "MATH 155A"]],
    "CSE 168R": [["CSE 167", "CSE 167R", "MATH 155A"]],
    "CSE 169": ["CSE 167"],
    "CSE 170": [["COGS 108", "CSE 12", "DSC 30"], ["COGS 1", "COGS 10", "DSGN 1", "ENG 100D"]],
    "CSE 175": ["Instructor approval"],
    "CSE 176A": [["CSE 110", "CSE 170", "COGS 120"]],
    "CSE 176E": ["Junior or senior standing", "Instructor approval"],
    "CSE 180": [["BILD 1", "BILD 4", "CSE 11", "CSE 3", "CSE 8A", "CSE 8B"]],
    "CSE 180R": [["BILD 1", "BILD 4", "CSE 11", "CSE 3", "CSE 8A", "CSE 8B"]],
    "CSE 181": [["CSE 100", "CSE 100R"], "CSE 101", ["BIMM 100", "CHEM 114C"]],
    "CSE 181R": [["CSE 100", "CSE 100R"], "CSE 101", ["BIMM 100", "CHEM 114C"]],
    "CSE 182": [["CSE 100", "CSE 100R"]],
    "CSE 184": [["BIMM 181", "BENG 181", "CSE 181"], ["BENG 182", "BIMM 182", "CSE 182", "CHEM 182"]],
    "CSE 185": [["CSE 11", "CSE 8B"], "CSE 12", ["MATH 20C", "MATH 31BH"], "BILD 1", ["BIEB 123", "BILD 4", "BIMM 101", "CHEM 109"]],
    "CSE 190": ["Instructor consent"],
    "CSE 191": ["Instructor consent"],
    "CSE 192": ["Upper-division standing", "Instructor consent"],
    "CSE 193": ["Department chair consent"],
    "CSE 194": [["AAS 10", "CSE 12", "ECE 35", "ETHN 3", "HILD 7A", "LTEN 27"], ["CAT 125", "CAT 125R", "CAT 3", "DOC 3", "HUM 2", "MCWP 125", "MCWP 125R", "MCWP 50", "MCWP 50R", "MMW 121", "MMW 121R", "MMW 122", "MMW 13", "SYN 2", "WCWP 100", "WCWP 10B"]],
    "CSE 197": ["Instructor consent", "Department approval"],
    "CSE 197C": ["Department approval"],
    "CSE 198": ["Instructor consent"],
    "CSE 199": ["Instructor consent"],
    "CSE 199H": ["CSE Honors Program admission", "Instructor consent"],
}

def parse_course_line(line):
    tokens = [t.strip() for t in line.split(',')]
    parsed_courses = []
    current_department = None

    #Handling interchangeable courses (honors/non-honors)
    for token in tokens:
        token = token.strip(", ")

        if "OR" in token:
            or_parts = [part.strip() for part in token.split("OR")]
            or_courses = []
            for part in or_parts:
                match = re.match(r"([A-Z]+)\s+(\d+\w*)", part)
                if match:
                    department, id = match.groups()
                    department = department.strip(", ")
                    id = id.strip(", ")
                    current_department = department
                    or_courses.append(f"{department} {id}")
                else:
                    match_number = re.match(r"(\d+\w*)", part)
                    if match_number and current_department:
                        id = match_number.group(1).strip(", ")
                        or_courses.append(f"{current_department} {id}")
            if or_courses:
                parsed_courses.append(", ".join(or_courses))
        else:
            match = re.match(r"([A-Z]+)\s+(\d+\w*)", token)
            if match:
                department, id = match.groups()
                department = department.strip(", ")
                id = id.strip(", ")
                current_department = department
                parsed_courses.append(f"{department} {id}")
            else:
                match_number = re.match(r"(\d+\w*)", token)
                if match_number and current_department:
                    id = match_number.group(1).strip(", ")
                    parsed_courses.append(f"{current_department} {id}")

    return parsed_courses

def can_take_course(course, taken_courses, prereqs_dict, special_keywords):
    if course not in prereqs_dict:
        return True, False

    prereq_options = prereqs_dict[course]

    satisfied = False

    for prereq in prereq_options:
        if isinstance(prereq, str):
            if prereq in taken_courses:
                satisfied = True
        elif isinstance(prereq, list):
            group_satisfied = False
            for option in prereq:
                if option in taken_courses:
                    group_satisfied = True
            if group_satisfied:
                satisfied = True

    has_any_special = False
    for prereq in prereq_options:
        if isinstance(prereq, str):
            if prereq in special_keywords:
                has_any_special = True
        elif isinstance(prereq, list):
            if any(opt in special_keywords for opt in prereq):
                has_any_special = True

    if satisfied:
        return True, has_any_special
    else:
        return False, has_any_special

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
        if len(cells) >= 4:
            quarter = cells[0].text.strip()
            course = cells[1].text.strip()
            letter_grade = cells[3].text.strip()

            #Fixing the detection of WIP credit elements
            prefix = quarter[:2]
            year_str = quarter[2:]
            if prefix in quarter_order and year_str.isdigit():
                if (quarter, course) not in seen_courses:
                    seen_courses.add((quarter, course))
                    year = int(year_str)
                    order = quarter_order[prefix]
                    formatted = f"{quarter} {course} {letter_grade}"
                    classes_list.append((year, order, formatted))

    classes_list.sort()
    for _, _, formatted in classes_list:
        output_lines.append(formatted)

    output_lines.append("")
    output_lines.append("Needs:")
    needs_courses = []

    needs_tables = soup.find_all('table', class_='selectcourses')
    for table in needs_tables:
        if isinstance(table, Tag):
            from_list = table.find('td', class_='fromcourselist')
            if from_list:
                raw_text = from_list.get_text(separator=" ", strip = True)
                lines = raw_text.split('\n')
                for line in lines:
                    parsed_courses = parse_course_line(line)
                    for course in parsed_courses:
                        output_lines.append(course)
                        needs_courses.append(course)

    output_lines.append("")

    taken_courses = set()
    for _, _, formatted in classes_list:
        parts = formatted.split()
        if len(parts) >= 3:
            course_code = f"{parts[1]} {parts[2]}"
            taken_courses.add(course_code)

    can_take_list = []
    cannot_take_list = []
    special_list = []

    special_keywords = {"Instructor consent", "Instructor approval", "Department approval", "Majors only", "Concurrent tutor appointment"}
    for course in needs_courses:
        if course in prereqs:
            can_take_flag, has_any_special = can_take_course(course, taken_courses, prereqs, special_keywords)
            if can_take_flag:
                can_take_list.append(course)
            elif has_any_special:
                special_list.append(course)
            else:
                cannot_take_list.append(course)
    
    output_lines.append("Can take:")
    output_lines.extend(can_take_list)
    output_lines.append("")
    output_lines.append("Cannot take:")
    output_lines.extend(cannot_take_list)
    output_lines.append("")
    output_lines.append("Special:")
    output_lines.extend(special_list)
    output_lines.append("")

    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output.txt")
    with open(output_path, "w") as f:
        f.write("\n".join(output_lines))

    return output_path
