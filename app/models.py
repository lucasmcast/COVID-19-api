from . import db
from flask import url_for

class GeneralsDatas(db.Model):
    
    __tablename__ = 'generals_datas'
    id = db.Column(db.Integer, primary_key=True)
    total_cases = db.Column(db.String(20))
    total_deaths = db.Column(db.String(20))
    total_recovered = db.Column(db.String(20))
    date_data = db.Column(db.String(20))
    hour_data = db.Column(db.String(5))

    def __repr__(self):
        return "<GeneralsDatas(total_cases='{}',\
            total_deaths='{}',total_recovered='{}', date_data='{}', hour_data='{}')>".format(self.total_cases,
            self.total_deaths, self.total_recovered, self.date_data, self.hour_data)
    
    def to_json(self):
        json_generaldata = {
            'url' : url_for('api.all_cases'),
            'total_cases' : self.total_cases,
            'total_deaths' : self.total_deaths,
            'total_recovered' : self.total_recovered,
            'date_data' : self.date_data,
            'hour_data' : self.hour_data
        }

        return json_generaldata
    

    def to_json_noturl(self, has_url):
        json_generaldata = {
            'total_cases' : self.total_cases,
            'total_deaths' : self.total_deaths,
            'total_recovered' : self.total_recovered,
            'date_data' : self.date_data,
            'hour_data' : self.hour_data
        }
        return json_generaldata

class CountryCases(db.Model):

    __tablename__ = 'country_cases'
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(20))
    url_country = db.Column(db.String(50))
    total_cases = db.Column(db.String(20))
    new_cases = db.Column(db.String(20))
    deaths_cases = db.Column(db.String(20))
    new_deaths = db.Column(db.String(20))
    total_recovered = db.Column(db.String(20))
    active_cases = db.Column(db.String(20))
    serious_critical = db.Column(db.String(20))
    date_data = db.Column(db.String(20))
    hour_data = db.Column(db.String(5))

    def __repr__(self):
        return "<CountryCases(country='{}', url_country='{}',\
            total_cases='{}', new_cases='{}',deaths_cases='{}',\
                new_deaths='{}', total_recovered='{}', actice_cases='{}',\
                    serious_critical='{}', date_data='{}', hour_data='{}')>".format(self.country,
                    self.url_country, self.total_cases,
                    self.new_cases, self.deaths_cases, self.new_deaths,
                    self.total_recovered, self.active_cases, self.serious_critical,
                    self.date_data, self.hour_data)

    def to_json(self):
        data_json = {
            'url' : url_for('api.all_countries'),
            'country' : self.country,
            'url_country' : self.url_country,
            'total_cases' : self.total_cases,
            'new_cases' : self.new_cases,
            'deaths_cases' : self.deaths_cases,
            'new_deaths' : self.new_deaths,
            'total_recovered' : self.total_recovered,
            'active_cases' : self.active_cases,
            'serious_critical' : self.serious_critical,
            'date_data' : self.date_data,
            'hour_data' : self.hour_data
        }
        return data_json

    def to_json_noturl(self):

        data_json = {
            'country' : self.country,
            'url_country' : self.url_country,
            'total_cases' : self.total_cases,
            'new_cases' : self.new_cases,
            'deaths_cases' : self.deaths_cases,
            'new_deaths' : self.new_deaths,
            'total_recovered' : self.total_recovered,
            'active_cases' : self.active_cases,
            'serious_critical' : self.serious_critical,
            'date_data' : self.date_data,
            'hour_data' : self.hour_data
        }

        return data_json

class ListCountryCases:

    def __init__(self):
        self._list_country_cases = []

    def set_list_countries(self, list_countries):
        self._list_country_cases = list_countries

    def get_list_countries(self):
        return self._list_country_cases

class ListGeneralsDatas:

    def __init__(self):
        self._list_generals_datas = []

    def set_general_datals(self, list_generals_datas):
        self._list_generals_datas = list_generals_datas
    
    def get_generals_datals(self):
        return self._list_generals_datas