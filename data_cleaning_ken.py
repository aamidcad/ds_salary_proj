# -*- coding: utf-8 -*-
"""
Created on Thu May  4 15:45:30 2023

@author: LENOVO
"""

import pandas as pd

df = pd.read_csv('glassdoor_jobs.csv')


def function

df['hourly'] = df['Salary'].apply(lamda x: 1 if 'per hour' in x,lower() else 0)
df['employer_provided'] = df['Salary'].apply(lamda x: 1 if 'employer provided salary:' in x,lower() else 0)

df = df[df['Salary Estimate not'] != '-1']
salary = df['Salary Estimate'].apply(lambda x: x.split('(')[0]))
minus_Kd = salary.apply(lamda x: x.replace('K','').replace('$',''))

min_hr = minus_Kd.apply(lambda x: x.lower().replace('per hour','').replace('employer provider salary',''))

df['min_salary'] = min_hr.apply(lamda x: int(x.split('-')[0]))
df['max_salary'] = min_hr.apply(lamda x: int(x.split('-')[1]))
df['avg_salary'] = (df.min_salary+df.max_salary)/2


#company name text only
df['company_txt'] = df.apply(lamda x: x['Company Nmae'] if x['Rating'] <0 els x['company Name'][:-1], axis =1)

#state field
df['job_state'] = df['Location'].apply(lambda x: x.split(',')[1])
df.job_state.value_counts()

df['same_state'] = df.apply(lambda x: x.Location == x.Headquarters else 0, axis =1)

#age of company
df['age'] = df.Founded.apply(lambda x: x if x <1 else 2020 -x)


#Job description(python,etc)
df['python_yn'] = df['Job Description'].apply(lamda x: 1 if 'puthon' inx.lower() or 'r studion' in x.lower() else 0)
df.R_yn.valu_counts()

#spark
df['spark'] = df['Job Description'].apply(lamda x: 1 if 'spark' in x.lower() else 0)
df.spark_value_counts()

#aws
df['aws'] = df['Job Description'].apply(lamda x: 1 if 'aws' in x.lower() else 0)
df.spark_value_counts()

#excel
df['excel'] = df['Job Description'].apply(lamda x: 1 if 'excel' in x.lower() else 0)
df.spark_value_counts()

df.columns

df.drop(['Unnamed: 0'],axis =1)

df_out.to_csv('salary_data_cleaned.csv',index = False)


