def dots(country, counterparts, start, end, freq='A', form="wide"):
    
    """
    Highly flexible function to return time series trade data between countries from the IMF Direction of Trade (DOTS) Database.
    The function sends a get request to the IMF JSON RESTful API. 

    Parameters
    ----------
    country : str (required)
        Country code for home country. 
        Use searches.country_codes() for a list of codes.
        Use searches.country_search("keyword") to search countries
    counterparts : str or list (required)
        Country code(s) for the counterpart country (or countries)
        Use searches.country_codes() for a list of codes.
        Use searches.country_search("keyword") to search countries
    start: int or float (reqiured)
        Start date of the series. 
        Years may be entered as int dtype, such as 1980
        Month start dates, such as 1980.02 (float) are acceptable.
        Numbers such as 1980.00 and 1980.14 are unacceptable.
    end: int or float (required)
        Same as start date but end of the series.
    freq: str (optional, default='A')
        Frequency of the time series (intervals)
        Default: 'A' - annual
        Alternatives: 'M' - monthly
        Note, freq "A" will override start dates entered as months, such as 1980.02
        In this case, start will be rounded down to the nearest whole year
        And end will be rounded up to the nearest whole year
    form: str (optional, default='A')
        If multiple counterparts, should the returned data be wide-form or long-form?
        Default: 'wide' (MultiIndex)
        Alternatives: 'long'

    Returns
    -------
    full_df : pandas.core.frame.DataFrame
        DataFrame with trade statistics.
        If multiple counterpart countries are selected and wide-form data is requested,
        the resulting DataFrame will be multiIndexed/hierarchical

    Examples
    --------
    >>> dots('US', 'CN', 1995, 2020)
    Returns wide-form US-China annual data between 1995 and 2020.
    
    >>> dots('MX','W00', 2010, 2020, freq='M')
    Returns wide-form Mexico-World monthly data between 2010 and 2020.
    
    >>> dots("GR", ["US", "AU", "DE"], 1998, 2018)
    Returns wide-form Greece annual data vs. the U.S., Australia and Germany 
    Between 1998 and 2018.
        
    >>> dots("XS25", ["JP", "KR"], 2000.05, 2020.09, freq="M", form="long")
    Returns long-form monthly data from Developing Asia vs. Japan and Korea
    Between May 2005 and September 2009

    """
    #validate input datatypes
    assert isinstance(country, str), "country must be a str"
    assert isinstance(counterparts, (str, list)), "counterparts must be a str or list"
    if isinstance(counterparts, list):
        assert len(counterparts) > 1, "counterparts must be a str or list of length 2 or more"
        assert country not in counterparts, "country must not be in counterparts"
    else:
        assert country != counterparts, "country and counterpart must not be the same"
    assert isinstance(start, (int,float)),"start must be a number"
    assert isinstance(end, (int,float)), "end must be a number"
    assert freq=="M" or freq=="A", "frequency must be M or A"
    assert form in ['long', 'wide'], "form must be long or wide"
    assert start > 1800 and start < 2200, "start must be a reasonable date"
    assert end > 1800 and end < 2200, "end must be a reasonable date"
    assert end >= start, "end must be after start"
    
    #transform mismatchedfrequency and start/end dates, if applicable
    if freq=="A" and isinstance(start, float):
        start = int(start)
    if freq=="A" and isinstance(end, float):
        end = int(end)+1
    
    #import libraries and define base URL for API
    import requests, dateutil.parser
    import pandas as pd
    start_url = "http://dataservices.imf.org/REST/SDMX_JSON.svc/"
    
    #Specify all available series for trade (exports, imports and trade balance)
    series = 'TBG_USD+TXG_FOB_USD+TMG_CIF_USD' 
    
    #define subfunction to handle single requests
    def retrieve(counterpart):
        
        request = f'{start_url}CompactData/DOT/{freq}.{country}.{series}.{counterpart}?startPeriod={start}&endPeriod={end}'

        #Send the get request to the API
        r = requests.get(request)
        print(r)
        
        #assert the response was 200 (OK)
        assert r.status_code==200, "Error - HTTP Request unsuccessful. Please try again."
            
        #convert the data to subscriptable json 
        data_json = r.json()
        
        try:
            #extract exports, imports and trade balance portions of the JSON (they are lists)
            exports = data_json['CompactData']['DataSet']['Series'][0]['Obs']
            imports = data_json['CompactData']['DataSet']['Series'][1]['Obs']
            tbal = data_json['CompactData']['DataSet']['Series'][2]['Obs']
            
        #if series is not found, throw an error.    
        except KeyError:
            raise AssertionError("One or more series not found. Please try again.")

        #Make sure all series are the same length
        assert len(exports)==len(imports), "Error - data not available. Try a different time period or frequency."
    
        #Parse time periods and values for each series
        periods = [dateutil.parser.parse(obs['@TIME_PERIOD']) for obs in exports]
        values_exports = [float(obs['@OBS_VALUE']) for obs in exports]
        values_imports = [float(obs['@OBS_VALUE']) for obs in imports]
        values_tbal = [float(obs['@OBS_VALUE']) for obs in tbal]
  
        #Convert to a pandas dataframe
        compile_df = pd.DataFrame({'Period':periods,
                                'Exports':values_exports, 
                                'Imports':values_imports, 
                                'Trade Balance':values_tbal})
        
        #Inlucde a column for two-way trade (exports + imports)
        compile_df['Twoway Trade']=compile_df['Exports']+compile_df['Imports']
    
        #Return the dataframe
        return compile_df
    
    #subfunction to format date correctly based on user input frequency
    def format_date(full_df):
        if freq=="A":
            full_df['Period'] = full_df['Period'].apply('{:%Y}'.format)
        else:
            full_df['Period'] = full_df['Period'].apply('{:%Y-%m}'.format)  
        return full_df
    
    #if counterparts is a list of countries, send a request for each country
    #append it to a master dataframe in long form
    #pivot to wide and return
    if isinstance(counterparts, list):
        
        full_df = pd.DataFrame()
        for counterpart in counterparts:
            retrieved = retrieve(counterpart)
            retrieved.insert(1,"Counterpart",counterpart)
            full_df = full_df.append(retrieved) #if long-form data requested, stop here
        
        #format dates correctly based on the user-specified frequency
        full_df = format_date(full_df)
        
        if(form=="wide"): #otherwise, pivot to wide form data
            full_df.insert(1,"Country",country)
            full_df = full_df.pivot(index="Period",
                    columns='Counterpart', 
                    values=['Exports', 'Imports', 'Trade Balance', 'Twoway Trade'])
            full_df.insert(0,"Country",country)
        else:
            full_df.insert(1,"Country",country) #if long-form data, insert country at position 1
        
    #if counterparts is a single country, create columns for country, counterpart
    #and return the result of that single request
    else:
        full_df = retrieve(counterparts)
        full_df.insert(1,'Country',country)
        full_df.insert(2,'Counterpart',counterparts)
        
        #format dates correctly based on the user-specified frequency
        full_df = format_date(full_df)
        
    return full_df