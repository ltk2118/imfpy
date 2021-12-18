#!/usr/bin/env python
# coding: utf-8

# # `imfpy`

# # User Guide

# `imfpy` is a python package for searching, retrieving and visualizing International Monetary Fund (IMF) Data
# 
# This package interacts with the IMF's JSON RESTful API. Documentation on the API is available here: https://datahelp.imf.org/knowledgebase/articles/667681-using-json-restful-web-service. A huge amount of macroeconomic and financial data are available from this IMF's API, inlcuding (but not limited to):
# 
# - Trade (DOTS) data
# - Balance of Payments (BOP) data
# - Inflation (CPI) data
# - International Financial Statistics (IFS) data
# - Many more!
# 
# **At the moment, retrieval and visualization capacity is limited to the IMF Direction of Trade Statistics (DOTS) database. I plan to add more functionality for some other core databases (BOP, IFS, etc.) in due course.**
# 
# The base URL is http://dataservices.imf.org/REST/SDMX_JSON.svc/
# 
# No API key is required (there used to be a requirement but not anymore). However, the following rate limits apply - no more than:
# 
# - 10 requests in 5 second window from one user (IP)
# - 50 requests per second overall on the application

# ## Installation
# 
# `imfpy` has the following dependencies: 
# - python 3.7 and above
# - pandas 1.1.3 and above
# - requests 2.19.0 and above
# - matplotlib 3.2.2. and above

# Installation can be accomplished easily via a pip install.

# In[1]:


get_ipython().system('pip install -i https://test.pypi.org/simple/ imfpy==0.1.17')


# ## Submodule 1: `imfpy.searches`

# The searches submodule allows the user to search through the available databases which can be accessed through the API. It uses a simple caching mechanism to store search data efficiently. The intention is that I will build further submodules to retrieve data on the basis of user searches. In the meantime, the searches submodule is still useful for assessing what information is available.

# In[2]:


from imfpy import searches


# ### `searches.country_codes()`
# This function returns a dataframe of all IMF databases from which data can be accessed through the JSON API.
# The resulting dataframe is cached to the local environment.

# In[3]:


searches.country_codes()


# ### `searches.country_search(keyword, regex = False)`
# This function enables the user to search the country codes data for particular countries. The function returns a pandas dataframe of country codes and countries matching the search, which can be done by normal string methods (the default) or a regular expression (if the user wishes to specify). The search operates on cached data or calls `country_codes` if the cache is empty.

# In[4]:


searches.country_search("germany")


# In[5]:


searches.country_search("^B.*a$", regex=True)


# ### `searches.database_codes()`
# This function is similar to `country_codes` but instead returns a pandas dataframe of all accessible databases and database codes. The result is cached to the local environment.

# In[6]:


searches.database_codes()


# ### `searches.database_search(keyword, regex = False)`
# This function enables the user to search the database codes data for particular databases. The function returns a pandas dataframe of database codes and databases matching the search, which can be done by normal string methods (the default) or a regular expression (if the user wishes to specify). The search operates on cached data or calls `database_codes` if the cache is empty.

# In[7]:


searches.database_search("development")


# In[8]:


searches.database_search("^Financial.*", regex=True)


# ### `searches.database_info(database_id)`
# This function returns the high-level information on a particular user-specified database. The idea is that the user should first search for a database using database_search(). If the user wishes to obtain more information about that database they can use database_info() on the desired database code.

# In[9]:


searches.database_info('FSI')


# ### `searches.database_dimensions(database_id)`
# This function returns the dimensions of a particular user-specified database. The idea is that the user should first search for a database using database_search(). If the user wants to access data from that database later, it will be useful to know the dimensions of that particular database (i.e. fields that can be used as API queries). In the example below, `CL_FREQ` denotes available data frequencies; while `CL_INDICATOR_FSI` denotes the indicator variables contained in the *FSI* database.

# In[10]:


searches.database_dimensions('FSI')


# ### `searches.indicator_dimensions(indicator_id)`
# This function returns a dataframe of all indicators and series IDs (i.e. the most granular unit of data apart from individual values) for a given user-specified indicator ID. IMF data is organized hierarchically - the highest (most aggregated) unit is the database; followed by dimensions, followed by indicators, followed by values (the lowest, most disaggregated unit).

# In[11]:


searches.indicator_dimensions('CL_INDICATOR_FSI').head(6)


# ## Submodule 2: `imfpy.retrievals`

# The retrievals submodule so far only contains one function: `dots` - a highly flexible function to return time series goods trade data between countries from the IMF Direction of Trade (DOTS) Database. Over time the retrievals module will be populated with other functions designed to interact with other key databases. Since I am particularly interested in trade policy, I have focused on trade statistics and designed a lot of functionality around that (and what would be useful to practitioners in the trade policy area). 
# 
# `dots()` returns a pandas dataframe of time series trade data to fit the user's exact specifications. The data is clean and ready for econometric analysis/visualization/presentation as the user requires. `dots()` is also robust to bad inputs and will throw errors if the user enters invalid or non-requestable parameters.

# In[12]:


from imfpy.retrievals import dots


# #### **1. Return a dataframe of U.S.-China annual trade data from 1995 to 2020.**
# 
# Note: here, wide and long form data are equivalent since there is one country and one counterpart.

# In[13]:


d = dots('US', 'CN', 1995, 2020)
d.head(6)


# #### **2. Return a dataframe of Mexico-World monthly trade data from 2010 to 2020.**

# In[14]:


d = dots('MX','W00', 2010, 2020, freq='M')
d.head(6)


# #### **3. Return a wide-form dataframe of Greece-U.S. and Greece-Germany annual trade data from 2000 to 2019.**
# Note that the resulting dataframe is organized as a multilevel (hierarchical) pandas dataframe. This may feel unfamiliar to some users but all of the normal functionality of pandas is retained. Note that the wide-form data is indexed by Period, while the long-form data is indexed numerically.

# In[15]:


d = dots("GR", ["US", "DE"], 2000, 2019)
d.round(decimals=1).head(6)


# #### **4. Return a long-form dataframe of Morocco-U.S., Morocco-Algeria, and Morocco-Mozambique annual trade data from 2002 to 2003.**
# Note that the resulting dataframe is organized as a multilevel (hierarchical) pandas dataframe. This may feel unfamiliar to some users but all of the normal functionality of pandas is retained. Note that the wide-form data is indexed by Period, while the long-form data is indexed numerically.

# In[16]:


d = dots("MA", ["DZ", "MZ"], 2002, 2004, form="long")
d.head(6)


# #### **5. Return long-form monthly trade data from Developing Asia vs. Japan and Korea between July 2000 and September 2000**
# 
# As can be seen, `dots()` can handle complex queries requesting data from countries and country groups with precisely defined start and end dates.

# In[16]:


d = dots("XS25", ["JP", "KR"], 2000.07, 2000.09, freq="M", form="long")
d.head(6)


# **`dots()` is robust to a wide variety of inputs, and will warn the user of invalid inputs before sending bad requests to the API.**
# All of the following requests will trigger an `AssertionError` warning the user of how to correct their input in order to build a valid request.

# In[ ]:


dots("CN","MX", 1000, 2020, "A", "wide"), #bad start year
dots("CN","CN", 1980, 2020, "A", "wide"), #country==counterparts
dots("CN",["MX"], 1980, 2020, "A", "wide"), #counterparts is a list length 1
dots("CN",["MX","CN"], 1980, 2020, "A", "something else"), #country in counterparts
dots(["CN","MX"],"MX", 1980, 2020, "A", "wide"), #country is a list
dots("CN","MX", 2020, 2018, "A", "wide"), #start > end
dots("CN",["MX","ZZ"], 2000, 2018, "A", "wide"), #invalid country
dots("CN","MX", 2020.12, 2020.01, "M", "wide"), #start >end, month
dots("CN",["MX",True], 2020.15, 2018, "M", "long"), #invalid counterparts list
dots("CN","MX", 2020.15, 2018, "M", "long"), #invalid month
dots("CN","MX", 2020.2, 2018, "A", "long"), #invalid month format
dots("CN","MX", 1950.05, 2018, "M", "long") #missing data


# ## Submodule 3: `imfpy.tools`
# 
# Over time my idea is to include more tools in this submodule that help to conduct rudimentary analysis on the returned data. For now, I have a single function `dotsplot()` that takes in a *long-form* pandas DataFrame (of the type returned by `retrievals.dots()`, or else it will throw an error) and returns plots of variables selected by the user.

# In[2]:


from imfpy.tools import dotsplot


# ### `dotsplot(dots_dataframe, subset=['Exports', 'Imports', 'Trade Balance'])`
# `dotsplot()` takes an arbitrary dots_dataframe (pandas DataFrame returned by `retrievals.dots()`) in long-form, and plots time series charts of variables selected by the user. These variables are entered as a list in the optional argument `subset`. Options are *'Exports'*, *'Imports'*, *'Trade Balance'* and *'Twoway Trade'* - all the variables contained in the DOTS database. The default option is `['Exports', 'Imports', 'Trade Balance']`. 
# 
# This function can handle the results of multi-counterpart, complex dots queries and graph them easily. It is also robust to invalid inputs and will warn the user if they try to supply incorrect/badly formatted data or invalid subset parameters.

# #### **1. Plot annnual time series data of US-China trade from 1995 to 2020 for the default variables Exports, Imports and Trade Balance** 
# Note, we do not need to specifiy `form="long"` in the original `dots()` query for `dotsplot()` to work, since long and wide form data are equivalent for this query.

# In[5]:


d = dots('US', 'CN', 1995, 2020)
dotsplot(d)


# #### **2. Plot annnual time series data of Australia-US and Australia-China trade from 2000 to 2020 on the variables *Trade Balance* and *Two-way Trade***

# In[7]:


d = dots('AU',['US','CN'], 2000, 2020, freq='A', form="long")
dotsplot(d, subset=['Trade Balance', 'Twoway Trade'])


# #### **2. Plot monthly time series data of Denmark-US and Denmark-New Zealand, Denmark-Germany and Denmark-Italy trade from 2000 to 2020 on the default variables**
# 
# The `dots()` and `dotsplots()` methods can be chained together naturally.

# In[7]:


dotsplot(dots("DK", ["US", "NZ", "DE", "IT"], 1998, 2018, "M", "long"))

