import re
import template1

def write_resume():
    filename = "resume.tex"
    name = re.compile(r"&&NAME&&")
    phone = re.compile(r"&&PHONE&&")
    email = re.compile(r"&&EMAIL&&")
    linkedin = re.compile(r"&&LINKEDIN&&")
    github = re.compile(r"&&GITHUB&&")

    exp1_bps = ""
    for _ in range(3):
        exp1_bps += re.sub("&&BP_INFO&&", "This is a bullet point", template1.bullet_point)

    experience1 = {
        "&&EXP_TITLE&&": "Software Engineer Intern",
        "&&EXP_DATES&&": "May 2001 - May 2020",
        "&&EXP_ORG&&": "JinAntonix Inc.",
        "&&EXP_LOC&&": "The Restaurant at the End of the Universe",
        "&&EXP_BPS&&": exp1_bps
    }
    exp_inst1 = multiple_replace(experience1, template1.experience_instance)
    experience2 = {
        "&&EXP_TITLE&&": "Product Manager",
        "&&EXP_DATES&&": "May 1934 - May 3051",
        "&&EXP_ORG&&": "LaTeX Foundation",
        "&&EXP_LOC&&": "Outer Space",
        "&&EXP_BPS&&": exp1_bps
    }
    exp_inst2 = multiple_replace(experience2, template1.experience_instance)
    exp = re.sub("&&EXPERIENCE_INSTS&&", exp_inst1 + '\n' + exp_inst2, str(template1.experience))

    project1 = {
        "&&PROJ_TITLE&&": "XKCD Chatbot",
        "&&PROJ_DATES&&": "May 2001 - May 2030",
        "&&SKILLS&&": "Mojo, Word, Llama",
        "&&PROJ_BPS&&": exp1_bps
    }
    proj_inst1 = multiple_replace(project1, template1.project_instance)

    project2 = {
        "&&PROJ_TITLE&&": "Resume Generator",
        "&&PROJ_DATES&&": "Crossword season",
        "&&SKILLS&&": "Python, LaTeX, Alpaca",
        "&&PROJ_BPS&&": exp1_bps
    }
    proj_inst2 = multiple_replace(project2, template1.project_instance)
    projects = re.sub("&&PROJECT_INSTS&&", proj_inst1 + '\n' + proj_inst2, str(template1.projects))

    lang_skills = {
        "&&LIST_NAME&&": "Other skills",
        "&&SKILLS&&": "Crosswords, NYT connections, Advent of Code"
    }
    skill_list_inst1 = multiple_replace(lang_skills, template1.skills_list)
    # skills = re.sub("&&SKILL_LIST&&", skill_list_inst1, str(template1.projects))

    d = {
        "&&NAME&&": "Tux",
        "&&PHONE&&": "123-456-7890",
        "&&EMAIL&&": "tux@calpoly.edu",
        "&&LINKEDIN&&": "www.linkedin.com/in/tux",
        "&&GITHUB&&": "github.com/tux",
        "&&UNIVERSITY&&": "California Polytechnic State University",
        "&&UNIV_LOC&&": "San Luis Obispo, CA",
        "&&UNIV_DESC&&": "Bachelor of Science in Computer Science",
        "&&UNIV_DATES&&": "May 2000 - Feb 2001",
        "&&EXPERIENCE&&": exp,
        "&&PROJECTS&&": projects,
        "&&SKILL_LIST&&": skill_list_inst1
    }

    
    with open(filename, 'w') as f:
        f.write(multiple_replace(d, template1.resume))

# From stack overflow
def multiple_replace(replacements: dict, text):
    # Create a regular expression from the dictionary keys
    regex = re.compile("(%s)" % "|".join(map(re.escape, replacements.keys())))
    # For each match, look-up corresponding value in dictionary
    return regex.sub(lambda mo: replacements[mo.group()], text) 


if __name__ == "__main__":
    write_resume()