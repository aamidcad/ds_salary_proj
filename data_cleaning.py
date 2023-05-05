
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

#Importing uncleaned Data

#uncleaned=pd.read_csv('/kaggle/input/data-science-job-posting-on-glassdoor/Uncleaned_DS_jobs.csv',low_memory=False)
uncleaned=pd.read_csv('C:/Users/LENOVO/Documents/ds_salary_proj/Data set/Uncleaned_DS_jobs.csv',low_memory=False)
#uncleaned.head(5)

## In the cleaned version the columns explanation are as follows,
'''
Job Title: Title of the job posting
Salary Estimation: Salary range for that particular job
Job Description: This contains the full description of that job
Rating: Rating of that post
Company: Name of company
Location: Location of the company
Headquarter: Location of the headquater
Size: Total employee in that company
Type of ownership: Describes the company type i.e non-profit/public/private farm etc
Industry, Sector: Field applicant will work in
Revenue: Total revenue of the company
min_salary,max_salary,avg_salary: Refers to the minimum, maximum and average salary for that post
job_state: State where the applicant will work
same_state: Same state as headquarter or not(Boolean)
company_age: Age of company
python,excel,hadoop,spark,aws,tableau,big_data: Some most appeared skills in boolean columns form
job_simp: Job type
seniority: if job type is senior or not (Boolean)
'''
uncleaned.drop('index',axis=1,inplace=True)
uncleaned.head()
uncleaned.shape
uncleaned.dtypes

#check for duplicate rows and drop duplicate rows except 1st row
print(uncleaned[uncleaned.duplicated()].shape)
uncleaned[uncleaned.duplicated()]

uncleaned.drop_duplicates(inplace=True)

uncleaned.reset_index(inplace=True)
uncleaned.shape

#Remove numbers from Company Name
uncleaned['Company Name']=uncleaned['Company Name'].apply(lambda x:x.split("\n")[0])

uncleaned['Salary Estimate'].value_counts()

'''
Here values are present in 2 formats:

79K−
 131K (Glassdoor est.)
145K−
 225K(Employer est.)
To convert from this format to 79-131,145-225

Calculate min_salary,max_salary,avg_salary
'''
len(uncleaned)

uncleaned['min_salary']=0
uncleaned['max_salary']=0
uncleaned['avg_salary']=0
for i in range(len(uncleaned)):
    try:
        uncleaned.loc[i,"min_salary"]=int(uncleaned['Salary Estimate'][i].split(" ")[0].split("-")[0].replace("$","").replace("K",""))
        uncleaned.loc[i,"max_salary"]=int(uncleaned['Salary Estimate'][i].split(" ")[0].split("-")[1].replace("$","").replace("K",""))
    except:
        uncleaned.loc[i,"min_salary"]=int(uncleaned['Salary Estimate'][i].split("(E")[0].split("-")[0].replace("$","").replace("K",""))
        uncleaned.loc[i,"max_salary"]=int(uncleaned['Salary Estimate'][i].split("(E")[0].split("-")[1].replace("$","").replace("K",""))
    finally:
        uncleaned.loc[i,"Salary Estimate"]=str(uncleaned.loc[i,"min_salary"])+"-"+str(uncleaned.loc[i,"max_salary"])
        uncleaned.loc[i,"avg_salary"]=np.mean([uncleaned.loc[i,"min_salary"],uncleaned.loc[i,"max_salary"]])
        
        
uncleaned.head()

#Extracting job_state from Location Column and replacing Full Names with appropriate state code and for Remote and Utah deleting the rows

uncleaned['Location'].apply(lambda x: x.split(",")[-1]).value_counts()

uncleaned['job_state']=uncleaned['Location'].apply(lambda x: x.split(",")[-1].strip())
uncleaned['job_state'].replace(['United States','Texas','California','New Jersey','Remote','Utah'],["US","TX","CA","NJ",np.nan,np.nan],inplace=True)
uncleaned.dropna(axis=0,inplace=True)
uncleaned.reset_index(inplace=True)

uncleaned['job_state'].value_counts()

uncleaned.head()

#Comparing job_state and Headquaerters location

uncleaned['Headquarters1']=uncleaned['Headquarters'].apply(lambda x:x.split(",")[-1].strip())
uncleaned['same_state']=np.where(uncleaned['Headquarters1']==uncleaned['job_state'],1,0)
uncleaned.drop('Headquarters1',axis=1,inplace=True)

uncleaned.head()

#Calculating company Age from Founded Year

uncleaned['Founded']=np.where(uncleaned['Founded']==-1,0,uncleaned['Founded'])
uncleaned['company_age']=2021-uncleaned['Founded']

uncleaned.head()

uncleaned.Rating = np.where(uncleaned.Rating==-1.0,0,uncleaned.Rating)
uncleaned.sort_values(by='Rating', ascending=True)
uncleaned.head()

#extracting key skills mentioned in the job description

uncleaned['Job Description'][0].split("\n\n")

uncleaned['python']=uncleaned['Job Description'].apply(lambda x: 1 if "python" in x.lower() else 0)
uncleaned['excel']=uncleaned['Job Description'].apply(lambda x: 1 if "excel" in x.lower() else 0)
uncleaned['hadoop']=uncleaned['Job Description'].apply(lambda x: 1 if "hadoop" in x.lower() else 0)
uncleaned['spark']=uncleaned['Job Description'].apply(lambda x: 1 if "spark" in x.lower() else 0)
uncleaned['aws']=uncleaned['Job Description'].apply(lambda x: 1 if "aws" in x.lower() else 0)
uncleaned['tableau']=uncleaned['Job Description'].apply(lambda x: 1 if "tableau" in x.lower() else 0)
uncleaned['big_data']=uncleaned['Job Description'].apply(lambda x: 1 if "big_data" in x.lower() else 0)

uncleaned.head()

#Simplifying Job Title
uncleaned['Job Title'].value_counts()[:100]

def seniority(job_title):
    job_title=job_title.lower()
    snr=['sr','senior','lead','principal','vp','vice president','director']
    for i in snr:
        if i in job_title:
            return "senior"
    if "jr" in job_title:
        return "junior"
    return "na"

uncleaned['Seniority']=uncleaned['Job Title'].apply(seniority)

uncleaned[uncleaned['Job Title']=='Vice President, Biometrics and Clinical Data Management']

#Simplifying Job Title

def title_simplifier(title):
    if 'data scientist' in title.lower():
        return 'data scientist'
    elif 'data engineer' in title.lower():
        return 'data engineer'
    elif 'analyst' in title.lower():
        return 'analyst'
    elif 'machine learning' in title.lower():
        return 'mle'
    elif 'manager' in title.lower():
        return 'manager'
    elif 'director' in title.lower():
        return 'director'
    elif 'vice president' in title.lower():
        return 'vp'
    else:
        return 'na'
uncleaned['job_simp']=uncleaned['Job Title'].apply(title_simplifier)

uncleaned.head()

#dropping columns like index, level_0, Founded, Competitors

uncleaned.drop(['level_0','index','Founded','Competitors'],axis=1,inplace=True)

uncleaned.head()

uncleaned.columns

#Export cleaned data to csv

file_path = 'C:/Users/LENOVO/Documents/ds_salary_proj/Data set/Cleaned_DS_Jobs.csv'

uncleaned.to_csv(file_path, index=False)




