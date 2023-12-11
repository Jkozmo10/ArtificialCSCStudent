import re
import random
import template1

def write_resume(d):
    filename = "resume.tex"

    sections = ["&&EDUCATION&&", "&&EXPERIENCE&&", "&&PROJECTS&&", "&&SKILLS&&"]
    # Randomly determine the order of sections
    random.shuffle(sections)
    content = "\n\n".join(sections)


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
    
    content_dict["&&SKILLS&&"] = re.sub("&&SKILL_LIST&&", ', '.join(d['skills']), \
                                     str(template1.skills))
    

    # print(content_dict.keys())

    if len(d['experiences']) == 0:
        content_dict['&&EXPERIENCE&&'] = ''
    if len(d['projects']) == 0:
        content_dict['&&PROJECTS&&'] = ''
    
    tex_d['&&CONTENT&&'] = multiple_replace(content_dict, content)


    
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