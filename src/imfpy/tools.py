# -*- coding: utf-8 -*-

def dotsplot(dots_dataframe, subset=['Exports', 'Imports', 'Trade Balance']):
    
    """ 
    A flexible function for plotting a time series of returned dots data 
    I plan to expand this functionality later to handle wide-form data.
    
    Parameters
    ----------
    dots_dataframe : pandas.core.frame.DataFrame (required)
        A long-form DataFrame output from retrievals.dots 
        Or a wide-from DataFrame output with a single counterpart country
    subset : list (optional), default=['Exports', 'Imports', 'Trade Balance']
        A list containing the variables the user wishes to plot.
        Combinations of 'Exports', 'Imports', 'Twoway Trade' and 'Trade Balance' are allowed.
   
   Returns 
   -------
   Grouped plot: list of Line2D (matplotlib)
   Time series plots of trade data.
   
   Examples
   --------
   >>> d = dots('US', 'CN', 1995, 2020)
   dotsplot(d)
   Plots annnual time series data of US-China trade from 1995 to 2020 
   For the default variables Exports, Imports and Trade Balance
   
   >>> d = dots('MX','W00', 2010, 2020, freq='M')
   dotsplot(d, subset=['Imports'])
   Plots monthly time series data of Mexico-Worldwide imports from 2010 to 2020
   
   >>> dotsplot(dots("GR", ["US", "AU", "DE"], 1998, 2018, "M", "long"))
   Chained method, plots monthly time series data of Greece-U.S., Greece-Australia
   and Greece-Germany trade from 1998 to 2018 for the default variables
   Note: here three separate plots will be generated, one for each country-counterpart pair.

   """
    
    #check the user has entered possible inputs
    import pandas as pd
    assert isinstance(dots_dataframe, pd.DataFrame), "dots_dataframe must be a DataFrame"
    assert isinstance(subset, list), "Subset must be a list"
    possible = {'Exports', 'Imports', 'Trade Balance', 'Twoway Trade'}
    assert set(subset).intersection(possible) == set(subset), "Subset has invalid inputs. Only 'Exports', 'Imports', 'Twoway Trade' and 'Trade Balance' are allowed." 
    
    try: 
        dots_dataframe['Counterpart'] == dots_dataframe['Counterpart']
    except KeyError:
        raise AssertionError("Wrong data form. Please ensure you enter long form data.")
    country = dots_dataframe.Country.unique()[0]
    assert len([country])==1, "Non-unique origin countries detected"
    
    #group by counterpart country and subsetted variables
    dots_dataframe.index = dots_dataframe.Period
    grouped = dots_dataframe.groupby('Counterpart')[subset]
    
    titles = list(grouped.groups.keys())
    
    from matplotlib import pyplot as plt
    axes = grouped.plot(
                sharex=True,
                sharey=False,
                legend=True,
                linewidth=0.8)
    
    count=0
    for ax in axes:
        ax.set_title(f'Home: {country}, Foreign: {titles[count]}')
        count+=1
    plt.show()
