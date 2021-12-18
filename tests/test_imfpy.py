import pytest, time
import pandas as pd
from imfpy.retrievals import dots
from imfpy import searches

#need to wait between tests or else the json decoder will break down
@pytest.fixture(autouse=True)
def slow_down_tests():
    """ Enforcing wait period between tests to allow the json decoder to reset """
    yield
    time.sleep(10)

def test_dots_simple():
    """ Testing if retrievals.dots works on a simple case """
    actual = dots("CN", "MX", 1990, 2015)
    assert isinstance(actual, pd.DataFrame), "Fails to return dataframe"
    assert actual.Country.unique()[0]=="CN", "Incorrect country"
    assert actual.Counterpart.unique()[0]=="MX", "Incorrect counterpart"

#test a series of bad inputs that we should be expecting
@pytest.mark.parametrize("country, counterparts, start, end, freq, form", [
    (5,5,5,5,5,5), #all int inputs
    ("huh","this","isn't","going","to","work"), #all str inputs
    ("CN","MX", 1000, 2020, "A", "wide"), #bad start year
    ("CN","CN", 1980, 2020, "A", "wide"), #country==counterparts
    ("CN",["MX"], 1980, 2020, "A", "wide"), #counterparts is a list length 1
    ("CN",["MX","CN"], 1980, 2020, "A", "something else"), #country in counterparts
    (["CN","MX"],"MX", 1980, 2020, "A", "wide"), #country is a list
    ("CN","MX", 2020, 2018, "A", "wide"), #start > end
    ("CN",["MX","ZZ"], 2000, 2018, "A", "wide"), #invalid country
    ("CN","MX", 2020.12, 2020.01, "M", "wide"), #start >end, month
    ("CN",["MX",True], 2020.15, 2018, "M", "long"), #invalid counterparts list
    ("CN","MX", 2020.15, 2018, "M", "long"), #invalid month
    ("CN","MX", 2020.2, 2018, "A", "long"), #invalid month format
    ("CN","MX", 1950.05, 2018, "M", "long") #missing data
])

def test_dots_bad_inputs(country, counterparts, start, end, freq, form):
    """ Testing if retrievals.dots expects and handles bad inputs """
    with pytest.raises(AssertionError):
        dots(country, counterparts, start, end, freq, form)
        
#test a series of good inputs that should give non-empty pd.DataFrame output
@pytest.mark.parametrize("country, counterparts, start, end, freq, form", [
    ("US","MX", 2000, 2020, "A", "wide"),
    ("AU","A10", 1990, 2011, "M", "wide"),
    ("AU",["W00","BR"], 2015, 2016, "M", "long"),
    ("KR",["FR","IT"], 2010.05, 2010.11, "M", "wide"),
    ("KR",["FR","IT","IN"], 2010.05, 2010.11, "A", "long"),
    ("NZ",["AU","IS"], 1980.05, 1980.6, "A", "wide"),
    ("RO",["AU","RU","GB","CN"], 2001.05, 2010, "M", "long")
    
])
    
def test_dots_good_inputs(country, counterparts, start, end, freq, form):
    """ Testing if retrievals.dots expects and handles valid, complex inputs """
    d = dots(country, counterparts, start, end, freq, form)
    assert isinstance(d, pd.core.frame.DataFrame)
    assert not d.empty

def test_country_searches():
    """ Testing if searches.country_searches behaves correctly """
    assert searches.country_codes().shape==(247,2)
    assert searches.country_search("Br").shape==(3, 2)
    assert searches.country_search("^A.*a$",regex=True).size==24

def test_database_searches():
    """ Testing if searches.database_searches behaves correctly """
    assert searches.database_codes().shape == (260,2)
    assert searches.database_search("BOP").size==112
    assert searches.database_search("BOPS").empty
    
def test_database_dimensions():
    """ Testing if searches.database_dimensions behaves correctly """
    assert searches.database_dimensions('BOP').iloc[2,3]=='CL_INDICATOR_BOP'
    with pytest.raises(AssertionError):
        searches.database_dimensions('BOPS')

def test_indicator_dimensions():
    """ Testing if searches.indicator_dimensions behaves correctly """
    assert searches.indicator_dimensions('CL_INDICATOR_FAS').shape==(205,3)
    with pytest.raises(AssertionError):
        searches.indicator_dimensions('christmas')
        
def test_integration():
     """ Integration tests on simple chained procedure """
     c = searches.country_search("Bah").reset_index(drop=True)
     c = list(c['Country Code'])
     d = dots("IT", c, 1990, 2000, "M", "long")
     assert isinstance(d, pd.DataFrame)