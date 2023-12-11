import re
import template1

def write_resume(d):
    filename = "resume.tex"


    tex_d = {
        "&&NAME&&": d['name'],
        "&&PHONE&&": d['phone'],
        "&&EMAIL&&": d['email'],
        "&&LINKEDIN&&": d['linkedin'],
        "&&GITHUB&&": d['github'],

        "&&CONTENT&&": None,
    }

    content_dict = {
        "&&EDUCATION&&": None,
        "&&EXPERIENCE&&": [],
        "&&PROJECTS&&": [],
        "&&SKILLS&&": None,
    }

    edu_dict = {
        "&&UNIVERSITY&&": d['university'],
        "&&UNIV_LOC&&": d['uni_loc'],
        "&&UNIV_DESC&&": d['uni_desc'],
        "&&UNIV_DATES&&": d['uni_dates'],
    }
    content_dict['&&EDUCATION&&'] = multiple_replace(edu_dict, template1.education)
    
    for exp in d['experiences']:
        exp_dict = {
            "&&EXP_TITLE&&": exp['exp_title'],
            "&&EXP_DATES&&": exp['exp_dates'],
            "&&EXP_ORG&&": exp['exp_org'],
            "&&EXP_LOC&&": exp['exp_loc'],
            "&&EXP_BPS&&": ""
        }
        for bp in exp['exp_bps']:
            exp_dict['&&EXP_BPS&&'] += re.sub("&&BP_INFO&&", bp, template1.bullet_point)

        exp_str = multiple_replace(exp_dict, template1.experience_instance)

        content_dict["&&EXPERIENCE&&"].append(exp_str)

    content_dict["&&EXPERIENCE&&"] = re.sub("&&EXPERIENCE_INSTS&&", '\n'.join(content_dict["&&EXPERIENCE&&"]), \
                                     str(template1.experience))
    

    for proj in d['projects']:
        proj_dict = {
            "&&PROJ_TITLE&&": proj['proj_title'],
            "&&PROJ_DATES&&": proj['proj_date'],
            "&&SKILLS&&": proj['proj_skills'],
            "&&PROJ_BPS&&": ""
        }
        for bp in proj['proj_bps']:
            proj_dict['&&PROJ_BPS&&'] += re.sub("&&BP_INFO&&", bp, template1.bullet_point)

        proj_str = multiple_replace(proj_dict, template1.project_instance)

        content_dict["&&PROJECTS&&"].append(proj_str)

    content_dict["&&PROJECTS&&"] = re.sub("&&PROJECT_INSTS&&", '\n'.join(content_dict["&&PROJECTS&&"]), \
                                     str(template1.projects))
    
    content_dict["&&SKILLS&&"] = re.sub("&&SKILL_LIST&&", d['skills'], \
                                     str(template1.skills))
    

    print(content_dict.keys())

    if len(d['experiences']) == 0:
        content_dict['&&EXPERIENCE&&'] = ''
    if len(d['projects']) == 0:
        content_dict['&&PROJECTS&&'] = ''
    
    tex_d['&&CONTENT&&'] = multiple_replace(content_dict, template1.content)
    
    

    # name = re.compile(r"&&NAME&&")
    # phone = re.compile(r"&&PHONE&&")
    # email = re.compile(r"&&EMAIL&&")
    # linkedin = re.compile(r"&&LINKEDIN&&")
    # github = re.compile(r"&&GITHUB&&")



    # exp1_bps = ""
    # for _ in range(3):
    #     exp1_bps += re.sub("&&BP_INFO&&", "This is a bullet point", template1.bullet_point)

    # experience1 = {
    #     "&&EXP_TITLE&&": "Software Engineer Intern",
    #     "&&EXP_DATES&&": "May 2001 - May 2020",
    #     "&&EXP_ORG&&": "JinAntonix Inc.",
    #     "&&EXP_LOC&&": "The Restaurant at the End of the Universe",
    #     "&&EXP_BPS&&": exp1_bps
    # }
    # exp_inst1 = multiple_replace(experience1, template1.experience_instance)
    # experience2 = {
    #     "&&EXP_TITLE&&": "Product Manager",
    #     "&&EXP_DATES&&": "May 1934 - May 3051",
    #     "&&EXP_ORG&&": "LaTeX Foundation",
    #     "&&EXP_LOC&&": "Outer Space",
    #     "&&EXP_BPS&&": exp1_bps
    # }
    # exp_inst2 = multiple_replace(experience2, template1.experience_instance)
    # exp = re.sub("&&EXPERIENCE_INSTS&&", exp_inst1 + '\n' + exp_inst2, str(template1.experience))

    # project1 = {
    #     "&&PROJ_TITLE&&": "XKCD Chatbot",
    #     "&&PROJ_DATES&&": "May 2001 - May 2030",
    #     "&&SKILLS&&": "Mojo, Word, Llama",
    #     "&&PROJ_BPS&&": exp1_bps
    # }
    # proj_inst1 = multiple_replace(project1, template1.project_instance)

    # project2 = {
    #     "&&PROJ_TITLE&&": "Resume Generator",
    #     "&&PROJ_DATES&&": "Crossword season",
    #     "&&SKILLS&&": "Python, LaTeX, Alpaca",
    #     "&&PROJ_BPS&&": exp1_bps
    # }
    # proj_inst2 = multiple_replace(project2, template1.project_instance)
    # projects = re.sub("&&PROJECT_INSTS&&", proj_inst1 + '\n' + proj_inst2, str(template1.projects))

    # lang_skills = {
    #     "&&LIST_NAME&&": "Other skills",
    #     "&&SKILLS&&": "Crosswords, NYT connections, Advent of Code"
    # }
    # skill_list_inst1 = multiple_replace(lang_skills, template1.skills_list)
    # # skills = re.sub("&&SKILL_LIST&&", skill_list_inst1, str(template1.projects))

    # d = {
    #     "&&NAME&&": "Tux",
    #     "&&PHONE&&": "123-456-7890",
    #     "&&EMAIL&&": "tux@calpoly.edu",
    #     "&&LINKEDIN&&": "www.linkedin.com/in/tux",
    #     "&&GITHUB&&": "github.com/tux",
    #     "&&UNIVERSITY&&": "California Polytechnic State University",
    #     "&&UNIV_LOC&&": "San Luis Obispo, CA",
    #     "&&UNIV_DESC&&": "Bachelor of Science in Computer Science",
    #     "&&UNIV_DATES&&": "May 2000 - Feb 2001",
    #     "&&EXPERIENCE&&": exp,
    #     "&&PROJECTS&&": projects,
    #     "&&SKILL_LIST&&": skill_list_inst1
    # }

    
    with open(filename, 'w') as f:
        f.write(multiple_replace(tex_d, template1.resume))

# From stack overflow
def multiple_replace(replacements: dict, text):
    # Create a regular expression from the dictionary keys
    regex = re.compile("(%s)" % "|".join(map(re.escape, replacements.keys())))
    # For each match, look-up corresponding value in dictionary
    return regex.sub(lambda mo: replacements[mo.group()], text) 


if __name__ == "__main__":
    write_resume()