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
    exp = multiple_replace(experience1, template1.experience)
    # print(exp)

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
        "&&EXPERIENCE&&": exp
    }

    
    with open(filename, 'w') as f:
        f.write(multiple_replace(d, template1.resume))

# From stack overflow, don't ask me how it works
def multiple_replace(replacements: dict, text):
    # Create a regular expression from the dictionary keys
    regex = re.compile("(%s)" % "|".join(map(re.escape, replacements.keys())))
    # For each match, look-up corresponding value in dictionary
    return regex.sub(lambda mo: replacements[mo.group()], text) 


if __name__ == "__main__":
    write_resume()