# requests for fetching html of website
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import matplotlib.pyplot as plt

# Make the GET request to a url
r = requests.get('http://www.cleveland.com/metro/index.ssf/2017/12/case_western_reserve_university_president_barbara_snyders_base_salary_and_bonus_pay_tops_among_private_colleges_in_ohio.html')
# Extract the content
c = r.content 

# Create a soup object
soup = BeautifulSoup(c, 'html.parser')

# Find the element on the webpage
main_content = soup.find('div', attrs = {'class': 'entry-content'})

# Extract the relevant information as text
content = main_content.find('ul').get_text("\n")
print("============Web Scraping Results============")
print(content,"\n \n")

# Create a pattern to match names
name_pattern = re.compile (r'^([A-Z]{1}.+?)(?:,)', flags = re.M)

# Find all occurrences of the pattern
names = name_pattern.findall(content)
print("============RegEx Results============")
print("Name:\n", names,"\n")

#print(salaries,"\n")

# Make school patttern and extract schools
school_pattern = re.compile(r'(?:,|,\s)([A-Z]{1}.*?)(?:\s\(|:|,)')
schools = school_pattern.findall(content)
print("Schools:\n", schools,"\n")

# Pattern to match the salaries
salary_pattern = re.compile(r'\$.+')
salary= salary_pattern.findall(content)
print("Salary:\n", salary,"\n")

# Convert salaries to numbers in a list comprehension 
numeric_salaries=[int(''.join(s[1:].split(','))) for s in salary]
print(numeric_salaries)

#create pandas DF
df = pd.DataFrame({'College':schools, 'President':names, 'Salary':numeric_salaries})

#sort values
df = df.sort_values('Salary', ascending=False).reset_index()

#style
plt.style.use('fivethirtyeight')
plt.rcParams['font.size'] = 6

df.plot(kind = 'barh', x = 'President', y = 'Salary')

plt.tight_layout()
plt.show()

