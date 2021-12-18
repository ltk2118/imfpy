# -*- coding: utf-8 -*-

#initialize a (very) simple caching mechanism for search results
import pandas as pd, requests

country_cache = pd.DataFrame()
''' Cache for countries data '''
database_cache = pd.DataFrame()
''' Cache for databases data '''

def country_search(keyword, regex = False):
    
    """
    Function to identify country codes and names from a keyword seach.
    It also returns codes from aggregated spatial units.
    The function returns a pandas dataframe of country codes and countries matching the search,
    which can be done by normal string methods (the default) or a regular expression 
    The search operates on cached data or calls country_codes if the cache is empty.
    
    Parameters
    ----------
    keyword : str or regular expression
        The keyword or regular expression to search. Not case-sensitive.
    regex : bool (optional), default=False
        Whether the keyword should be searched as a regular expression.
        Defaults to False, in which case normal string matching is used.
        
    Returns
    -------
    match : pandas.core.frame.DataFrame
        A DataFrame of matched results, including country code and country.
    
    Examples
    --------
    >>> searches.country_search("germany")
    Returns keyword matches for simple string search "germany"
    
    >>> searches.country_search("^B.*a$", regex=True)
    Returns matches for countries starting with B and ending in a
    """

    #Input data types and values- validation
    assert isinstance(keyword, str),"Invalid inputs, please try again."
    
    global country_cache
    
    if country_cache.empty:
       #get full list of countries if cache is empty
       codes = country_codes()   
    else: 
       #otherwise just access the cached countries
        codes = country_cache
    
    #give the user the option to use regex to search if desired
    if regex == False:
        keyword = keyword.lower()
        match = codes[codes['Country'].str.lower().str.contains(keyword, regex = False)]
    else: 
        match = codes[codes['Country'].str.contains(keyword, regex = True)]

    return match

def country_codes():

   """
   Function returns a dataframe of all IMF countries and codes for which data can be accessed through the JSON API. 
   The resulting dataframe is cached to the local environment using a simple technique.
   
   Parameters
   ----------
   None
       
   Returns
   -------
   database_cache : pandas.core.frame.DataFrame
       A DataFrame of all country names and codes, cached to local environment.
   
   Examples
   --------
   >>> searches.country_codes()
   Returns country codes and caches to local environment.
   
   """
   
    
   #only request data if it hasn't been cached
   global country_cache
  
   if country_cache.empty:
      
      #import libraries and define base URL for API
      start_url = "http://dataservices.imf.org/REST/SDMX_JSON.svc/"
      
      # send the get request, use the DOTS database as the database_id
      database_id = 'DOT' 
      r = requests.get(f'{start_url}DataStructure/{database_id}')
      print(r)
      
      # assert the response was 200 (OK)
      assert r.status_code==200, "Error - HTTP request was unsuccessful."
    
      #convert the data to subscriptable json 
      data_json = r.json()
    
      #get codelist (which contains countries)
      country_codelist = data_json['Structure']['CodeLists']['CodeList'][2]['Code']
    
      #get list of countries and codes with a list comprehension
      codes = [country['@value'] for country in country_codelist]
      countries = [country['Description']['#text'] for country in country_codelist]
      
      #cache the result to avoid running it again
      country_cache = pd.DataFrame({"Country Code": codes, "Country": countries})
  
   return country_cache

def database_codes():
    
    """
    Function returns a dataframe of all IMF databases from which data can be accessed through the JSON API. 
    The resulting dataframe is cached to the local environment using a simple technique.
    
    Parameters
    ----------
    None
        
    Returns
    -------
    database_cache : pandas.core.frame.DataFrame
        A DataFrame of all Database names and codes, cached to local environment.
    
    Examples
    --------
    >>> searches.database_codes()
    Returns database codes and caches to local environment.
    
    """
    
    #only request data if it hasn't been cached
    global database_cache
    
    if database_cache.empty:
    
        #define IMF data services API start point 
        start_url = "http://dataservices.imf.org/REST/SDMX_JSON.svc"
        
        #requests.get the full list of databases, convert to json
        import requests
        r = requests.get(f'{start_url}/Dataflow')
        print(r)
        
        #assert the response was 200 (OK)
        assert r.status_code==200, "Error - HTTP request was unsuccessful."
        
        #convert the data to subscriptable json 
        data_json = r.json()
        
        #convert results to dataframe
        df_temp = pd.DataFrame(data_json['Structure']['Dataflows']['Dataflow']) 
        
        #parse out columns that themselves contain multiple cols of data
        parsed_Name = pd.DataFrame([database['Name'] for database in data_json['Structure']['Dataflows']['Dataflow']])
        parsed_KeyFamilyRef = pd.DataFrame([database['KeyFamilyRef'] for database in data_json['Structure']['Dataflows']['Dataflow']])
        
        #clean up dataframe columns
        df_temp = df_temp.join(parsed_Name).join(parsed_KeyFamilyRef)[['@id', '#text']]
        df_temp = df_temp.rename(columns={'@id': 'Database ID', '#text': 'Description'})
        df_temp['Database ID'] = df_temp['Database ID'].str.replace("DS-","")
        
        #store clean dataframe to global cache
        database_cache = df_temp.sort_values('Database ID').reset_index(drop=True)
        
    #return cache
    return database_cache 

def database_search(keyword, regex = False):
    
    """
    Function to identify database codes and names from a keyword seach.
    The function returns a pandas dataframe of database codes and databases matching the search,
    which can be done by normal string methods (the default) or a regular expression 
    The search operates on cached data or calls database_codes if the cache is empty.
    
    Parameters
    ----------
    keyword : str or regular expression
        The keyword or regular expression to search. Not case-sensitive.
    regex : bool (optional), default=False
        Whether the keyword should be searched as a regular expression.
        Defaults to False, in which case normal string matching is used.
        
    Returns
    -------
    match : pandas.core.frame.DataFrame
        A DataFrame of matched results, including database code and database.
    
    Examples
    --------
    >>> searches.database_search("development")
    Returns keyword matches for simple string search "development"
    
    >>> searches.database_search("^Financial.*", regex=True)
    Returns matches for databases that start with "Financial"
    """
    
    #Input data types and values- validation
    assert isinstance(keyword, str),"Invalid inputs, please try again."
    
    global database_cache
    
    if database_cache.empty:
       #get full list of countries if cache is empty
       codes = database_codes()  
    else: 
       #otherwise just access the cached countries
        codes = database_cache
    
    #give the user the option to use regex to search if desired
    if regex == False:
        keyword = keyword.lower()
        match = codes[codes['Description'].str.lower().str.contains(keyword, regex = False)]
    else: 
        match = codes[codes['Description'].str.contains(keyword, regex = True)]

    return match

def database_info(database_id):
    
    """
    Returns the high-level information on a particular user-specified database.
    
    Parameters
    ----------
    database_id : str
        The database ID of the database of interest.
        Checks against database cache to validate input.
        
    Returns
    -------
    info : pandas.core.frame.DataFrame
        A DataFrame of information (update time, name, definition, methodology, etc.)
        about the specified database.
    
    Examples
    --------
    >>> searches.database_info('FSI')
    Returns information about the database 'FSI' (Financial Soundness Indicators)
    
    """
    
    global database_cache
    
    if database_cache.empty:
       #get full list of countries if cache is empty
       codes = database_codes()  
    else: 
       #otherwise just access the cached countries
        codes = database_cache
        
    #check the database ID is valid before sending a request
    assert codes['Database ID'].str.fullmatch(database_id).any(), "Invalid database. Please try again."
    
    #define IMF data services API start point 
    start_url = "http://dataservices.imf.org/REST/SDMX_JSON.svc"
        
    #send the get request
    import requests
    r = requests.get(f'{start_url}/DataStructure/{database_id}')
    print(r)
    
    #assert the response was 200 (OK)
    assert r.status_code==200, "Error - HTTP request was unsuccessful."
    
    #convert the data to subscriptable json 
    data_json = r.json()
    
    #get info from annotations
    annotations_json = data_json['Structure']['KeyFamilies']['KeyFamily']['Annotations']['Annotation']
    
    #parse two columns: title and text
    titles = [annotation['AnnotationTitle'] for annotation in annotations_json]
    text_raw = [annotation['AnnotationText']['#text'] for annotation in annotations_json]
    
    #clean html tags out of the text if they exist
    import re
    text_clean = [re.sub(r'<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});','',text) for text in text_raw]
    #return neat dataframe of database info
    info = pd.DataFrame({'Variable':titles, 'Value':text_clean})
    
    return info

def database_dimensions(database_id):
    
    """
    This function returns the dimensions of a particular user-specified database.
    Database dimensions are effectively indicator collections indexed by an indicator_id.
    
    Parameters
    ----------
    database_id : str
        The database ID of the database of interest.
        Checks against database cache to validate input.
        
    Returns
    -------
    dimensions : pandas.core.frame.DataFrame
        A DataFrame of dimensions (typically frequencies, spatial units and indicators)
        that can be accessed through the specified database
    
    Examples
    --------
    >>> searches.database_dimensions('FSI')
    Returns dimensions of the database 'FSI' (Financial Soundness Indicators)
    
    """
    
    global database_cache
    
    if database_cache.empty:
       #get full list of countries if cache is empty
       codes = database_codes()  
    else: 
       #otherwise just access the cached countries
        codes = database_cache
        
    #check the database ID is valid before sending a request
    assert codes['Database ID'].str.fullmatch(database_id).any(), "Invalid database. Please try again."
    
    #define IMF data services API start point 
    start_url = "http://dataservices.imf.org/REST/SDMX_JSON.svc"
        
    #send the get request
    r = requests.get(f'{start_url}/DataStructure/{database_id}')
    print(r)
    
    #assert the response was 200 (OK)
    assert r.status_code==200, "Error - HTTP request was unsuccessful."
    
    #convert the data to subscriptable json 
    data_json = r.json()
    
    #get info from KeyFamilies --> Components
    dimensions_temp = data_json['Structure']['KeyFamilies']['KeyFamily']['Components']['Dimension']
    
    #return neat dataframe of database dimensions, dropping redundant columns
    dimensions_temp = pd.DataFrame(dimensions_temp)[['@conceptRef', '@conceptSchemeRef','@codelist']]
    dimensions = dimensions_temp.rename(columns={'@conceptRef': 'Concept', 
                                                       '@conceptSchemeRef': 'Scheme',
                                                       '@codelist': 'Indicator ID'})
    
    #have a column for Database ID so user can keep track of search
    dimensions.insert(0, "Database ID", database_id)
    
    return dimensions

def indicator_dimensions(indicator_id):
    
    """
    Function returns a dataframe of indicator dimensions and series IDs 
    (i.e. the most granular unit of data apart from individual values) 
    for a given user-specified indicator ID. 
    Indicator dimensions are single time series.
    
    Parameters
    ----------
    indicator_id : str
        The indicator ID of the indicator of interest.
        
    Returns
    -------
    indicator_dimensions : pandas.core.frame.DataFrame
        A DataFrame of indicator dimensions or series that can be accessed via a particular indicator_id
    
    Examples
    --------
    >>> searches.indicator_dimensions('CL_INDICATOR_FSI')
    Returns indicators dimensions and series for the indicator ID 'CL_INDICATOR_FSI'
    
    """
    
    #define IMF data services API start point 
    start_url = "http://dataservices.imf.org/REST/SDMX_JSON.svc"
    
    # pull the data 
    r = requests.get(f'{start_url}/CodeList/{indicator_id}')
    print(r)
    
    #assert the response was 200 (OK)
    assert r.status_code==200, "Error - HTTP request was unsuccessful."
    
    #convert the data to subscriptable json 
    data_json = r.json()

    #get codelist for that indicator
    codelist = data_json['Structure']['CodeLists']['CodeList']['Code']
    
    #get list of codes and descriptions with a list comprehension
    codes = [code['@value'] for code in codelist]
    descriptions = [code['Description']['#text'] for code in codelist]
    
    #return neat dataframe of codes and descriptions
    #have a column for Indicator ID so user can keep track of search
    indicator_dimensions = pd.DataFrame({'Indicator ID':indicator_id, 
                         'Series ID':codes, 
                         'Description':descriptions})
    return indicator_dimensions

