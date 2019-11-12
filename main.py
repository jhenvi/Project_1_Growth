#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
get_ipython().run_line_magic('matplotlib', 'notebook')
fpath = "main_table.csv"
df = pd.read_csv(fpath)
df.head()


# In[3]:


##INSERT COMMENTS HERE 


# In[4]:


df2 = df.loc[df["REF_DATE"] >= 1988]
df2.head()


# In[5]:


##INSERT COMMENTS HERE 


# In[6]:


df3 =df2[["REF_DATE","GEO","Labour force characteristics","Sex", "Age group",
          "North American Industry Classification System (NAICS)","VALUE"
]]
df3.reset_index(drop=True).head()


# In[7]:


## INSERT COMMENTS HERE


# In[8]:


df3["North American Industry Classification System (NAICS)"].value_counts().head()


# In[9]:


##INSERT COMMENTS HERE


# In[10]:


df3 = df3.replace(
    {"Finance, insurance, real estate, rental and leasing [52, 53]": "Finance and insurance",
     "Wholesale and retail trade [41, 44-45]":"Wholesale trade [41]", "Retail trade [44-45]":"Wholesale trade [41]"})
df3["North American Industry Classification System (NAICS)"].value_counts().head()


# ### SORT CLEANED DATA FRAME FOR 1988 VALUES 

# In[11]:


df5 = df3.loc[df3["REF_DATE"]==1988]
df5.head()


# ### SORT CLEANED DATA FRAME FOR 2018 VALUES 

# In[12]:


df6 = df3.loc[df3["REF_DATE"]==2018]
df6.head()


# ### CENTRALIZE SINGLE DATA FRAME VIEW FOR OVERALL LABOUR FORCE 1988 - 2018 

# In[13]:


test_df = pd.merge(df5,df6, on = ["GEO", "Labour force characteristics", "Sex","Age group","North American Industry Classification System (NAICS)" ], suffixes = ("_1988", "_2018"))
test_df.head()


# In[14]:


#percentage_change = ((total_2018 - total_1988)/total_2018)*100
#percentage_change.sort_values(ascending = True)


# In[15]:


#percentage_change.sort_values(ascending=False)


# ### FIND TOTAL FEMALES EMPLOYED IN CANADA - NAICS 54, 1988 - 2018

# In[16]:


# Pull only data needed for calcualtions: NAICS: [54], Sex: Females, Labour Force: Employment, Geo: Canada
df_NAICS_54_females = df3.loc[(df3["North American Industry Classification System (NAICS)"] == "Professional, scientific and technical services [54]") & (df3["Sex"] == 'Females')& (df3["Labour force characteristics"] == 'Employment') & (df3["GEO"] == 'Canada')]
df_NAICS_54_females.dropna().head()


# In[17]:


# Group by years to show Total Females Employed in Canada within NAICS [54] each year, 1988 - 2018
df_NAICS_54_1988_2019_females = df_NAICS_54_females.groupby(["REF_DATE"]).sum()["VALUE"].round()
df_NAICS_54_1988_2019_females.head()


# ### FIND TOTAL MALES EMPLOYED IN CANADA - NAICS 54, 1988 - 2018

# In[18]:


# Pull only data needed for calcualtions: NAICS: [54], Sex: Males, Labour Force: Employment, Geo: Canada
df_NAICS_54_males = df3[(df3["North American Industry Classification System (NAICS)"] == "Professional, scientific and technical services [54]") & (df3["Sex"] == 'Males')& (df3["Labour force characteristics"] == 'Employment') & (df3["GEO"] == 'Canada')]
df_NAICS_54_males.dropna().head()


# In[19]:


# Group by years to show Total Males Employed within NAICS [54] each year, 1988 - 2018
df_NAICS_54_1988_2019_males = df_NAICS_54_males.groupby(["REF_DATE"]).sum()["VALUE"].round()
df_NAICS_54_1988_2019_males.head()


# In[20]:


# Create Data Frame to hold new values 
Yearly_Employment_NAICS54_1988_2018_bySex = pd.DataFrame({
    "Males Employed": df_NAICS_54_1988_2019_males,
    "Females Employed": df_NAICS_54_1988_2019_females
})
Yearly_Employment_NAICS54_1988_2018_bySex.head()


# In[21]:


#Find percentage change YoY
Yearly_Employment_NAICS54_1988_2018_bySex.pct_change().fillna(0).head()


# In[22]:


#Find Max Change & Find Corresponding Years
Yearly_Employment_NAICS54_1988_2018_bySex.pct_change().max()


# ### CREATE GRAPH TO SHOW GROWTH IN EMPLOYMENT RATE BY GENDER

# In[26]:


# Plot data into bar graph and label 
Yearly_Employment_NAICS54_1988_2018_bySex.plot(kind='line', figsize=(10,10))
plt.title("MALE & FEMALE EMPLOYMENT GROWTH, NAICS [54], CANADA, 1988  - 2018")
plt.xlabel("YEARS")
plt.ylabel("NUMBER EMPLOYED")
plt.xticks(np.arange(1988, 2020, 5)) 
plt.yticks(np.arange(300, 2000, 300)) 
plt.show()


# ### FIND TOTAL EMPLOYED BY PROVINCE - NAICS 54, 1988 - 2018

# In[21]:


# Pull only data needed for calcualtions: NAICS: [54], Both Sexes, Labour Force: Employment, Geo: All provinces
df_NAICS_54_GEO = df3.loc[(df3["North American Industry Classification System (NAICS)"] == "Professional, scientific and technical services [54]") & (df3["Sex"] == 'Both sexes')& (df3["Labour force characteristics"] == 'Employment') & (df3["GEO"] != 'Canada')]
df_NAICS_54_GEO.dropna().head()


# In[22]:


# Group by years and GEO to show Total Employed within NAICS [54] each year, 1988 - 2018
df_NAICS_54_1988_2019_GEO = df_NAICS_54_GEO.groupby(["REF_DATE","GEO"]).sum()["VALUE"].round()
Yearly_Employment_NAICS54_1988_2018_byProvinces = pd.DataFrame(df_NAICS_54_1988_2019_GEO)
Yearly_Employment_NAICS54_1988_2018_byProvinces.head()


# In[23]:


# Create and label graph
pltGEO = Yearly_Employment_NAICS54_1988_2018_byProvinces["VALUE"].unstack().plot(kind='line', figsize=(10,10))
plt.title("PROVINCIAL LABOUR GROWTH, NAICS [54], CANADA, 1988  - 2018")
plt.xlabel("YEARS")
plt.ylabel("NUMBER EMPLOYED")
plt.xticks(np.arange(1988, 2020, 5)) 
plt.yticks(np.arange(-20, 1300, 300)) 
plt.show()


# ### FIND TOTAL EMPLOYED BY AGE GROUP - NAICS 54, 1988 - 2018

# In[24]:


# Pull only data needed for calcualtions: NAICS: [54], Both Sexes, Labour Force: Employment, Geo: Canada
df_NAICS_54_AGE = df3.loc[(df3["North American Industry Classification System (NAICS)"] == "Professional, scientific and technical services [54]") & (df3["Sex"] == 'Both sexes')& (df3["Labour force characteristics"] == 'Employment') & (df3["Age group"] != "15 years and over") & (df3["GEO"] == 'Canada')]
df_NAICS_54_GEO.dropna().head()


# In[25]:


# Group by years and AGE to show Total Employers within NAICS [54] each year, 1988 - 2018
df_NAICS_54_1988_2019_AGE = df_NAICS_54_AGE.groupby(["REF_DATE","Age group"]).sum()["VALUE"].round()
Yearly_Employment_NAICS54_1988_2018_byAGE = pd.DataFrame(df_NAICS_54_1988_2019_AGE)
Yearly_Employment_NAICS54_1988_2018_byAGE.head()


# In[26]:


# Create & label graph
pltAGE = Yearly_Employment_NAICS54_1988_2018_byAGE["VALUE"].unstack().plot(kind='bar',stacked=True, figsize=(10,10))
plt.title("AGE GROUP GROWTH, NAICS [54], CANADA, 1988  - 2018")
plt.xlabel("YEARS")
plt.ylabel("EMPLOYED")
plt.show()


# ### FURTHER GENDER ANALYSIS FOR NAICS [54] 1988 - 2018 

# In[27]:


#Find total NAICS [54] employed from 1988 - 2018 
total_employed_NAICS_54_1988_2018 = df_NAICS_54_1988_2019_males + df_NAICS_54_1988_2019_females
total_employed_NAICS_54_1988_2018.head()


# In[28]:


# Find the percent of males employed in NAICS [54] fom 1988 - 2018
percent_male_employed_NAICS_54_1988_2018 = (df_NAICS_54_1988_2019_males/total_employed_NAICS_54_1988_2018)*100
percent_male_employed_NAICS_54_1988_2018.round().head()


# In[29]:


# Format for percentages of males employed in NAICS [54] 1988 - 2018
percent_male_employed_NAICS_54_1988_2018.map("{0:,.2f}%".format).head()


# In[30]:


# Find the average percentage of Males Employed within NAICS [54] from 1988 - 2018
percent_male_employed_NAICS_54_1988_2018.mean()


# In[31]:


# Find the percent of females employed in NAICS [54] fom 1988 - 2018
percent_female_employed_NAICS_54_1988_2018 = (df_NAICS_54_1988_2019_females/total_employed_NAICS_54_1988_2018)*100
percent_female_employed_NAICS_54_1988_2018.round().head()


# In[32]:


# Format for percentages of females employed in NAICS [54] 1988 - 2018
percent_female_employed_NAICS_54_1988_2018.map("{0:,.2f}%".format).head()


# In[33]:


# Find the average percentage of Females Employed within NAICS [54] from 1988 - 2018
percent_female_employed_NAICS_54_1988_2018.mean()


# In[48]:


# Create data frame to hold values
gender_percentage_breakdown_NAICS_1988_2018 = pd.DataFrame({
    "Males Employed": df_NAICS_54_1988_2019_males,
    "Females Employed": df_NAICS_54_1988_2019_females,
    "% Males Employed": percent_male_employed_NAICS_54_1988_2018,
    "% Females Employed": percent_female_employed_NAICS_54_1988_2018
})
gender_percentage_breakdown_NAICS_1988_2018.head()


# In[49]:


# Format for percentage
gender_percentage_breakdown_NAICS_1988_2018["% Males Employed"] = gender_percentage_breakdown_NAICS_1988_2018["% Males Employed"].map("{0:,.2f}%".format)
gender_percentage_breakdown_NAICS_1988_2018["% Females Employed"] = gender_percentage_breakdown_NAICS_1988_2018["% Females Employed"].map("{0:,.2f}%".format)
gender_percentage_breakdown_NAICS_1988_2018.head()


# In[ ]:




