import pandas as pd
import random

def main():

    df_jobs = pd.read_csv("alumniJobs.csv")
    df_locations = pd.read_csv("alumniLocation.csv")
    df_companies = pd.read_csv("alumniCompanies.csv")
    df_skills = pd.read_csv('alumniSkills.csv')
    df_years = pd.read_csv('2022Enrollment.csv')
    df_courses = pd.read_csv('CSCEnrollment.csv')

    prompt = str(input("Enter prompt: "))
    output = []
    if prompt == 'company':
        num = int(input("How many years of experience? "))
        while len(output) < num:
            curGen = random.choices(list(df_companies['Company'].values), weights=list(df_companies['Number'].values))[0]
            if curGen not in output:
                output.append(curGen)
        print(', '.join(output))
    elif prompt == 'skills':
        num = int(input("How many skills? "))
        while len(output) < num:
            curGen = random.choices(list(df_skills['Skill'].values), weights=list(df_skills['Number'].values))[0]
            if curGen not in output:
                output.append(curGen)
        print(', '.join(output))
    elif prompt == 'job':
        num = int(input("How many jobs? "))
        while len(output) < num:
            curGen = random.choices(list(df_jobs['Job'].values), weights=list(df_jobs['Number'].values))[0]
            if curGen not in output:
                output.append(curGen)
        print(', '.join(output))
    elif prompt == 'location':
        curGen = random.choices(list(df_locations['Location'].values), weights=list(df_locations['Number'].values))[0]
        print(curGen)
    elif prompt == 'year':
        curGen = random.choices(list(df_years['Year'].values), weights=list(df_years['Number'].values))[0]
        print(curGen)
    else:
        print('Enter one of the following: company, skills, job, location, year')


if __name__ == '__main__':
    while True:
        main()