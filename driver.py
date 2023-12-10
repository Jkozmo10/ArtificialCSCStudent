import pandas as pd
import random
import utils

df_jobs = pd.read_csv("data/alumniJobs.csv")
df_locations = pd.read_csv("data/alumniLocation.csv")
df_companies = pd.read_csv("data/alumniCompanies.csv")
df_skills = pd.read_csv('data/alumniSkills.csv')
df_years = pd.read_csv('data/2022Enrollment.csv')
df_courses = pd.read_csv('data/CSCEnrollmentInfo.csv')

def main(year=None):
    if year == None:
        year = get_year()

    first_name = "Tux"
    last_name = "Linux"
    d = {}
    d['name'] = f'{first_name} {last_name}' # Generate name function?
    d['phone'] = "123-456-7890"
    d['email'] = f'{get_calpoly_username(first_name, last_name)}@calpoly.edu'
    d['linkedin'] = f'www.linkedin.com/in/{first_name.lower()}-{last_name.lower()}'
    d['university'] = "California Polytechnic State University"
    d['uni_loc'] = "San Luis Obispo"
    d['uni_desc'] = "Bachelor of Science in Computer Science"
    d['uni_dates'] = 'NONE'
    d['skills'] = get_skills(utils.get_num_skills(year))
    d['courses'] = get_relevant_coursework(year, utils.get_num_courses(year))

    d['experiences'] = []
    d['projects'] = []

    nums_dict = utils.get_distribution(year)


    companies_positions = get_companies_positions(sum(nums_dict['experiences']))
    for idx, num_bp in enumerate(nums_dict['experiences']):
        exp = {}
        exp['exp_title'] = companies_positions[idx][1]
        exp['exp_org'] = companies_positions[idx][0]
        for b in range(num_bp):
            l += "This is a bullet point"
        d['experiences'].append(l)
    for proj in nums_dict['projects']:
        pass






def get_calpoly_username(first_name, last_name):
    return f'{first_name.lower()[0]}{last_name}'[:7]

def get_companies_positions(numPositions):
    companies = []
    result = []
    df_companies = df_companies.set_index('Company')
    while len(companies) < numPositions:
        curGen = random.choices(list(df_companies.index.values), weights=list(df_companies['Number'].values))[0]
        if curGen not in companies:
            companies.append(curGen)
    result = [(company, df_companies.loc[company, 'Location']) for company in companies]
    
    return result

def get_skills(numSkills):
    """
    
    """
    output = []
    while len(output) < numSkills:
        curGen = random.choices(list(df_skills['Skill'].values), weights=list(df_skills['Number'].values))[0]
        if curGen not in output:
            output.append(curGen)
    
    return ', '.join(output)

def get_relevant_coursework(year, numCourses):
    # df_courses.set_index('Course', inplace=True)
    df_filtered = df_courses[(df_courses['Year'] == year) | (df_courses['Year'] == year - 1)]

    output = []
    while len(output) < numCourses:
        curGen = random.choices(list(df_filtered['Description'].values), weights=list(df_filtered['2023Enroll'].values))[0]
        if curGen not in output:
            output.append(curGen)
    
    return ', '.join(output)

    

def get_year():
    return random.choices(list(df_years['Year'].values), weights=list(df_years['Number'].values))[0]

"""
User clicks button, selects year
Year feeds into util function, determines how many projects + experiences
Determine dates of each project + experience
Query data to determine companies worked for (experiences) + job title, user skills, coursework
Feed into LLM:
    Company + title => Experience bullet points
    Year + course => Project bullet points
Put all info in dictionary, feed into resume.py
Run latex on generated resume, serve back to user
"""

if __name__ == "__main__":
    main()