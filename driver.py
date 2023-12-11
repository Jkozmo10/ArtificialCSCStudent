import pandas as pd
import random
import utils
import resume
import calendar

df_jobs = pd.read_csv("data/alumniJobs.csv")
df_locations = pd.read_csv("data/alumniLocation.csv")
df_companies_g = pd.read_csv("data/alumniCompanies.csv")
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
    d['github'] = f'github.com/{get_calpoly_username(first_name, last_name)}'
    d['university'] = "California Polytechnic State University"
    d['uni_loc'] = "San Luis Obispo"
    d['uni_desc'] = "Bachelor of Science in Computer Science"
    d['uni_dates'] = get_uni_dates(year)
    d['skills'] = get_skills(utils.get_num_skills(year))
    d['courses'] = get_relevant_coursework(year, utils.get_num_courses(year))

    d['experiences'] = []
    d['projects'] = []

    nums_dict = utils.get_distribution(year)


    companies_positions = get_companies_locations_positions(sum(nums_dict['experiences']))
    for idx, num_bp in enumerate(nums_dict['experiences']):
        exp = {}
        bps = []
        exp['exp_title'] = companies_positions[idx][1]
        exp['exp_org'] = companies_positions[idx][0]
        exp['exp_loc'] = companies_positions[idx][2]
        exp['exp_dates'] = get_exp_dates(idx)
        for b in range(num_bp):
            bps.append("This is a bullet point") # TODO LLM
        exp['exp_bps'] = bps
        d['experiences'].append(exp)

    dates = get_project_dates(len(nums_dict['projects']))[::-1]

    for idx, num_bp in enumerate(nums_dict['projects']):
        proj = {}
        bps = []
        proj['proj_title'] = 'Title' # TODO LLM
        proj['proj_skills'] = ', '.join(random.sample(d['skills'], random.randrange(1, 4)))
        proj['proj_date'] = dates[idx]
        for b in range(num_bp):
            bps.append("This is a bullet point") # TODO LLM
        proj['proj_bps'] = bps
        d['projects'].append(proj)

    # print(d)
    resume.write_resume(d)


def get_project_dates(numProjects):
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    years = ['2020', '2021', '2022']

    dates = []
    for i in range(numProjects):
        curStr = f"{random.choice(months)} {random.choices(years, weights=[0.1, 0.2, 0.7])[0]}"
        dates.append(curStr)
    
    sorted_dates = sorted(dates, key=month_and_year)

    output = []
    for pair in sorted_dates: # the abbreviations were not used earlier for sorting purposes
        ind = pair.split()
        output.append(f'{calendar.month_abbr[list(calendar.month_name).index(ind[0])]}. {ind[1]}')

    return output

def month_and_year(month_year):
    month_name, year = month_year.split()
    return (int(year), list(calendar.month_name).index(month_name))


def get_uni_dates(year):
    if year == 1:
        return 'Sep. 2023 - June 2027'
    elif year == 2:
        return 'Sep. 2022 - June 2026'
    elif year == 3:
        return 'Sep. 2021 - June 2025'
    else:
        return 'Sep. 2020 - June 2024'

def get_exp_dates(idx):
    return f'June {2023 - idx} - Sep. {2023 - idx}'

    
def get_calpoly_username(first_name, last_name):
    return f'{first_name.lower()[0]}{last_name.lower()}'[:7]

def get_companies_locations_positions(numPositions):
    # Returns list of (company, position, location)
    companies = []
    df_companies = df_companies_g.set_index('Company')
    while len(companies) < numPositions:
        curGen = random.choices(list(df_companies.index.values), weights=list(df_companies['Number'].values))[0]
        companies.append(curGen)
    return [(company,
            random.choices(list(df_jobs['Job'].values), weights=list(df_jobs['Number'].values))[0],
            df_companies.loc[company, 'Location']) for company in companies]

def get_skills(numSkills):
    output = []
    while len(output) < numSkills:
        curGen = random.choices(list(df_skills['Skill'].values), weights=list(df_skills['Number'].values))[0]
        if curGen not in output:
            output.append(curGen)
    
    return output # returns list

def get_relevant_coursework(year, numCourses):
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
Year feeds into util function, determines how many projects + experiences - DONE
Determine dates of each project + experience - Done
Query data to determine companies worked for (experiences) + job title, user skills, coursework - DONE
Feed into LLM:
    Company + title => Experience bullet points
    Year + course => Project bullet points
Put all info in dictionary, feed into resume.py
Run latex on generated resume, serve back to user
"""

if __name__ == "__main__":
    main()