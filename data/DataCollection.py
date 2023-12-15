# %%
import pandas as pd
from bs4 import BeautifulSoup
import requests
import time
import io

# %%
quarters = ['Fall 2023',
         'Summer 2023',
         'Spring 2023',
         'Winter 2023',
         'Fall 2022',
         'Summer 2022',
         'Winter 2022',
         'Fall 2021',
         'Summer 2021',
         'Spring 2021',
         'Winter 2021',
         'Fall 2020',
         'Summer 2020',
         'Spring 2020',
         'Winter 2020',
         'Fall 2019',
         'Summer 2019',
         'Spring 2019',
         'Winter 2019',
         'Fall 2018',
         'Summer 2018',
         'Spring 2018',
         'Winter 2018']
CPEquarters = ['CPE Fall 2023',
         'CPE Summer 2023',
         'CPE Spring 2023',
         'CPE Winter 2023',
         'CPE Fall 2022',
         'CPE Summer 2022',
         'CPE Winter 2022',
         'CPE Fall 2021',
         'CPE Summer 2021',
         'CPE Spring 2021',
         'CPE Winter 2021',
         'CPE Fall 2020',
         'CPE Summer 2020',
         'CPE Spring 2020',
         'CPE Winter 2020',
         'CPE Fall 2019',
         'CPE Summer 2019',
         'CPE Spring 2019',
         'CPE Winter 2019',
         'CPE Fall 2018',
         'CPE Summer 2018',
         'CPE Spring 2018',
         'CPE Winter 2018'
         ]

# %%
df_csc_courses = pd.DataFrame()

for quarter in quarters:
  with open(f"html/{quarter.replace(' ', '')}.html", "r", encoding="utf-8") as file:
    html_content = file.read()

  soup = BeautifulSoup(html_content, "html.parser")

  table = soup.find_all('table', attrs={'id' : 'listing'})

  df_current = pd.read_html(io.StringIO(str(table)))[0]
  df_current = df_current[(df_current['Type'].str.lower() == 'lec') & (df_current['Course'].str[:7].str.match('^\w\w\w \d\d\d$'))]# | (df_current['Type'].str.lower() == 'ind')]
  df_current = df_current[['Course', 'Enrl']]
  df_current['Course'] = df_current['Course'].str[:7].str.strip()
  df_current.set_index('Course', inplace=True)

  df_csc_courses = df_csc_courses.merge(df_current, left_index=True, right_index=True,how='outer', suffixes=('', f"_{quarter.replace(' ', '')}"))



# %%
df_csc_courses = df_csc_courses.fillna(0)
df_csc_courses

# %%
df_cpe_courses = pd.DataFrame()

for quarter in CPEquarters:
  with open(f"html/{quarter.replace(' ', '')}.html", "r", encoding="utf-8") as file:
    html_content = file.read()

  soup = BeautifulSoup(html_content, "html.parser")

  table = soup.find_all('table', attrs={'id' : 'listing'})

  df_current = pd.read_html(io.StringIO(str(table)))[0]
  df_current = df_current[(df_current['Type'].str.lower() == 'lec') & (df_current['Course'].str[:7].str.match('^\w\w\w \d\d\d$'))] # | (df_current['Type'].str.lower() == 'ind')]
  df_current = df_current[['Course', 'Enrl']]
  df_current['Course'] = df_current['Course'].str[:7].str.replace('CPE', 'CSC')
  df_current.set_index('Course', inplace=True)

  df_cpe_courses = df_cpe_courses.merge(df_current, left_index=True, right_index=True,how='outer', suffixes=('', f"_{quarter[3:].replace(' ', '')}"))



# %%
df_cpe_courses = df_cpe_courses.fillna(0)
df_cpe_courses


# %%
df_combined = pd.DataFrame()
for index in df_csc_courses.index.to_list():
  if index in df_cpe_courses.index:
    curRow = (df_csc_courses.loc[index] + df_cpe_courses.loc[index]).to_frame().T
  else:
    try:
      curRow = df_csc_courses.loc[index].to_frame().T
    except:
      curRow = df_csc_courses.loc[index]
  df_combined = pd.concat([df_combined, curRow])



# %%
df_combined.rename(columns={'Enrl' : 'Fall2023', 'Enrl_Summer2023' : 'Summer2023', 'Enrl_Spring2023' : 'Spring2023', 'Enrl_Winter2023' : 'Winter2023',
       'Enrl_Fall2022' : "Fall2022", 'Enrl_Summer2022' : 'Summer2022', 'Enrl_Winter2022' : 'Winter2022', 'Enrl_Fall2021' : 'Fall2021',
       'Enrl_Summer2021' : 'Summer2021', 'Enrl_Spring2021' : 'Spring2021', 'Enrl_Winter2021' : 'Winter2021',
       'Enrl_Fall2020' : 'Fall2020', 'Enrl_Summer2020' : 'Summer2020', 'Enrl_Spring2020' : 'Spring2020',
       'Enrl_Winter2020' : 'Winter2020', 'Enrl_Fall2019' : 'Fall2019', 'Enrl_Summer2019' : 'Summer2019',
       'Enrl_Spring2019' : 'Spring2019', 'Enrl_Winter2019' : 'Winter2019', 'Enrl_Fall2018' : 'Fall2018',
       'Enrl_Summer2018' : 'Summer2018', 'Enrl_Spring2018' : 'Spring2018', 'Enrl_Winter2018' : 'Winter2018'}, inplace=True)

df_combined.index.name = 'Course'

df_combined = df_combined.astype(int)

# %%
df_courses = df_combined.copy()

# %% [markdown]
# This section gets the titles for all of the course numbers. This is useful for generating the relevant coursework section of the resumes.

# %%
response = requests.get('https://catalog.calpoly.edu/coursesaz/csc/')
soup = BeautifulSoup(response.content, "html.parser")

# %%
courses = soup.find('div', attrs={'class' : 'sc_sccoursedescs'})

courses = courses.find_all('div', attrs={'class' : 'courseblock'})

courseDict = {}

for course in courses:
    title = course.find('p').strong.get_text(strip=True)
    curList = title.split('.')
    cleanLst = [cur.replace('\xa0', ' ').strip() for cur in curList]
    courseDict[cleanLst[0]] = cleanLst[1]

# %%
# df_courses.set_index('Course', inplace=True)
df_courses['Description'] = ""
for id in df_courses.index:
    try:
        df_courses.loc[id, 'Description'] = str(courseDict[id])
    except:
        df_courses.loc[id, 'Description'] = None

# %% [markdown]
# This section adds summary statistics and the year to each class, which will be useful later.

# %%
import re 

def get_year(c):
    if re.match(r'CSC 5', c):
        return 5
    elif re.match(r'CSC 4', c):
        return 4
    elif re.match(r'CSC 3', c):
        return 3
    elif re.match(r'CSC 2', c):
        return 2
    else:
        return 1

df_courses["Year"] = df_courses.index.to_series().map(get_year)

# %%
df_courses['2023Enroll'] = df_courses['Fall2023'] + df_courses['Spring2023'] + df_courses['Winter2023'] + df_courses['Fall2022'] +  df_courses['Winter2022']

# %%
df_courses.to_csv('CSCEnrollmentInfo.csv')


