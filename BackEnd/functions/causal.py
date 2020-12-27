import datetime
import logging
import re
import warnings
import numpy as np
import pandas as pd

from pathlib import Path
from collections import namedtuple
from dowhy import CausalModel
from pytrends.request import TrendReq

import matplotlib
import requests
import yfinance as yf
import plotly.graph_objects as go

warnings.simplefilter(action='ignore', category=FutureWarning)
logging.disable(logging.CRITICAL)


class Causal:

    def __init__(self):
        pass

    def gauge(self, title: str, val: int = -1):

        threshold = 210

        if val < 0:
            colour = 'white'
            causal = 'Data Unavailable'
            val = None
        elif val < threshold:
            colour = 'rgb(51, 51, 51)'
            causal = 'Causal Test Failed'
        else:
            colour = 'rgb(47, 79, 255)'
            causal = 'Causal Test Passed'

        fig = go.Figure(go.Indicator(
            domain={'x': [0, 1], 'y': [0, 1]},
            value=val,
            mode="gauge+number",
            title={"text": title + "<br><span style='font-size:16;color:rgb(51, 51, 51)'>" + causal,
                   'font': {'size': 30}},
            number={'suffix': "/300<br>Tests Passed", 'font': {'size': 30}},
            gauge={'axis': {'range': [None, 300], 'tickfont_size': 19.2, 'tickwidth': 1},
                   'bar': {'color': colour},
                   'steps': [
                       {'range': [0, 300], 'color': 'rgb(235, 235, 235)'}, ],
                   'threshold': {'line': {'color': "black", 'width': 8}, 'thickness': 1, 'value': threshold}}))

        fig.update_layout(font={'color': "rgb(51, 51, 51)", 'family': 'Poppins'})

        return fig

    def bar(self, title: str, values: [int] = [0, 0, 0, 0, 0]):

        tests = ['Estimate', 'Random', 'Unobserved', 'Placebo', 'Subset']

        colours = ['rgb(47, 79, 255)', ] * 5
        colours[3] = 'rgb(51, 51, 51)'

        fig = go.Figure([go.Bar(x=tests, y=values, marker_color=colours)])
        fig.update_layout(title=dict(text=title + ' Causal Test Results', font_size=24, font_color='black'),
                          yaxis=dict(title='Estimate Value', titlefont_size=19.2, tickfont_size=19.2, color='black'),
                          xaxis=dict(tickfont_size=19.2, color='black'),
                          plot_bgcolor='rgb(235, 235, 235)',
                          font={'family': 'Poppins'})

        return fig

    def get_keyword_trends(self, keywords: [str], country: str = 'GB'):
        pytrend = TrendReq()

        for i in range(len(keywords)):
            try:
                pytrend.build_payload(kw_list=[keywords[i]], geo=country)
                if i == 0:
                    df = pytrend.interest_over_time()
                else:
                    resp = pytrend.interest_over_time()
                    df[keywords[i]] = resp[keywords[i]].values

            except:
                print("Warning: Couldn't connect to Google Trends")
                return

        if 'isPartial' in df.columns:
            df = df.drop('isPartial', axis=1)
        df['metric'] = df.mean(axis=1)

        trend_data = self.dates(df, 'trend', 'metric')

        return trend_data

    def get_economic_data(self, country: str = 'GB', timeframe: str = '5y'):
        tickers = {
            "GB": "^FTSE", "FR": "^FCHI", "CA": "^GSPTSE", "DE": "^GDAXI", "US": "^DJI", "JP": "^N225",
            "HK": "^HSI", "CN": "399001.SZ", "AU": "^AXJO", "CH": "^STOXX50E", "BE": "BFX", "RU": "IMOEX.ME",
            "SG": "^STI", "ZA": "^JN0U.JO", "IN": "^BSESN", "ID": "^JKSE", "MY": "^KLSE", "NZ": "^NZ50",
            "KR": "^KS11", "TW": "^TWII", "BR": "^BVSP", "MX": "^MXX", "CL": "^IPSA", "AR": "^MERV",
            "IT": "^TA125.TA", "EG": "^CASE30"
        }

        if country not in tickers.keys():
            print("Error: No ticker available for", country)
            return

        ticker = tickers[country]
        try:
            YF = yf.Ticker(ticker)
            df = YF.history(period=timeframe, interval='1d')
        except:
            print("Warning: Couldn't connect to Yahoo Finance")
            return

        df = df.resample('W').mean()

        econ_data = self.dates(df, 'econ', 'Close')

        return econ_data

    def get_health_data(self, country: str):

        health_keywords = ['depression', 'anxiety', 'doctor', 'drugs', 'medication']
        health_data = self.get_keyword_trends(health_keywords, country)
        health_data.rename(columns={'trend': 'health'}, inplace=True)

        return health_data

    def get_political_data(self, country: str):
        urls = {'GB': 'https://yougov.co.uk/_pubapis/v5/uk/trackers/government-approval/download/',
                'US': 'https://today.yougov.com/_pubapis/v5/us/trackers/us-congress-approval-rating/download/'}

        if country not in urls:
            print("Error: No politics data available for", country)
            return

        url = urls[country]

        try:
            r = requests.get(url, allow_redirects=True)
        except:
            print("Warning: Couldn't connect to YouGov")
            return

        df = pd.read_excel(r.content, engine='openpyxl')
        df.columns.values[0] = ''
        df = df.set_index('')

        for val in df.index:
            if val not in ['Approve', 'Somewhat approve', 'Strongly approve']:
                df.drop(val, inplace=True)

        df = df.transpose()

        months = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06',
                  'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
        dates = []
        for date in df.index:
            data = date.split()
            day = re.search(r'\d+', data[0]).group()
            month = months[data[1]]
            year = data[2][-2:]
            final = day + '/' + month + '/' + year
            temp = datetime.datetime.strptime(final, '%d/%m/%y')
            dates.append(temp)

        df['date'] = dates
        df = df.set_index('date')

        column_length = len(df.columns)

        for i in range(column_length):
            temp = []
            for val in df[df.columns.values[i]]:
                num = re.search(r'\d+', str(val)).group()
                num = int(num)
                temp.append(num)
            df[str(i)] = temp
            df = df.drop([df.columns.values[i]], axis=1)

        politics = pd.DataFrame(df.mean(axis=1))
        politics.columns = ['politics']
        politics = politics.resample('W').mean()

        politics_data = self.dates(politics, 'politics', 'politics')

        return politics_data

    def dates(self, df, target: str, source: str):

        date = []
        for i in range(len(df)):
            year = str(df.index[i].year)
            week = str(df.index[i].week)
            temp = week + ', ' + year
            date.append(temp)
        data = pd.DataFrame(date, columns=['date'])
        data[target] = list(df[source])

        return data

    def scale(self, data):

        return_list = []
        for val in data:
            scaled = (val - data.min()) / (data.max() - data.min())
            return_list.append(scaled)

        return return_list

    def dowhy(self, data, indicator: str):
        flag = 0
        runtime = 300  # Adjust if slow
        np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)

        esti_total = 0
        rand_total = 0
        unob_total = 0
        plac_total = 0
        subs_total = 0

        for i in range(runtime):
            treatment_name = ['trend']  # v0
            outcome_name = indicator  # y
            common_causes_names = []  # W0, W1, W2
            effect_modifier_names = []  # X0
            instrument_names = []  # Z0

            model = CausalModel(
                data=data,
                treatment=treatment_name,
                outcome=outcome_name,
                common_causes=common_causes_names,
                effect_modifiers=effect_modifier_names,
                instruments=instrument_names)

            identified_estimand = model.identify_effect(proceed_when_unidentifiable=True)
            estimate = model.estimate_effect(identified_estimand, method_name="backdoor.linear_regression")
            res_random = model.refute_estimate(identified_estimand, estimate, method_name="random_common_cause")
            res_unobserved = model.refute_estimate(identified_estimand, estimate,
                                                   method_name="add_unobserved_common_cause",
                                                   confounders_effect_on_treatment="linear",
                                                   confounders_effect_on_outcome="linear",
                                                   effect_strength_on_treatment=0.01, effect_strength_on_outcome=0.02)
            res_placebo = model.refute_estimate(identified_estimand, estimate,
                                                method_name="placebo_treatment_refuter", placebo_type="permute")
            res_subset = model.refute_estimate(identified_estimand, estimate,
                                               method_name="data_subset_refuter", subset_fraction=0.9)

            esti = estimate.value
            rand = res_random.new_effect
            unob = res_unobserved.new_effect
            plac = res_placebo.new_effect
            subs = res_subset.new_effect

            if type(esti) == tuple:
                esti = esti.item()
            if type(rand) == tuple:
                rand = rand[0].item()
            if type(unob) == tuple:
                unob = unob[0].item()
            if type(plac) == tuple:
                plac = plac[0].item()
            if type(subs) == tuple:
                subs = subs[0].item()

            five_percent = (esti / 100) * 5
            ten_percent = five_percent * 2
            fifteen_percent = five_percent * 3
            twenty_percent = five_percent * 4

            if (esti - five_percent <= rand <= esti + five_percent) or (
                    esti - five_percent >= rand >= esti + five_percent):
                if (esti - ten_percent <= unob <= esti + ten_percent) or (
                        esti - ten_percent >= unob >= esti + ten_percent):
                    if (-fifteen_percent <= plac <= fifteen_percent) or (-fifteen_percent >= plac >= fifteen_percent):
                        if (esti - twenty_percent <= subs <= esti + twenty_percent) or (
                                esti - twenty_percent >= subs >= esti + twenty_percent):
                            flag += 1

            esti_total += esti
            rand_total += rand
            unob_total += unob
            plac_total += plac
            subs_total += subs

        esti_mean = esti_total / runtime
        rand_mean = rand_total / runtime
        unob_mean = unob_total / runtime
        plac_mean = plac_total / runtime
        subs_mean = subs_total / runtime

        bar_vals = [esti_mean, rand_mean, unob_mean, plac_mean, subs_mean]
        value = round(flag / (runtime / 100), 2)

        if flag >= (runtime / 100) * 70:
            print('Treatment is causal - ' + str(value) + '% confidence')
            return flag, bar_vals
        else:
            print('Treatment is not causal')
            print('Test failed', (runtime - flag), 'out of', runtime, 'times')
            return flag, bar_vals

        return 0, bar_vals

    def analyse(self, keywords: [str], country: str = 'United Kingdom'):
        matplotlib.use('TkAgg')
        print('Country:', country)
        countries = pd.read_csv(Path(__file__).parent.parent.parent / 'Data' / 'countries.csv')
        ans = countries[countries == country].stack().index.tolist()
        
        CausalValues = namedtuple('CausalValues', 'value estimate random unobserved placebo subset')

        try:
            country_key = countries.code[ans[0][0]].upper()
        except:
            print('Error: Country unavailable')
            return CausalValues(-1, 0, 0, 0, 0, 0), CausalValues(-1, 0, 0, 0, 0, 0), CausalValues(-1, 0, 0, 0, 0, 0)

        print('----- Collecting Data -----')
        trends = self.get_keyword_trends(keywords, country_key)
        if not isinstance(trends, pd.DataFrame):
            return CausalValues(-1, 0, 0, 0, 0, 0), CausalValues(-1, 0, 0, 0, 0, 0), CausalValues(-1, 0, 0, 0, 0, 0)

        trends['trend'] = self.scale(trends['trend'])

        econ = self.get_economic_data(country_key)
        health = self.get_health_data(country_key)
        politics = self.get_political_data(country_key)

        econ_result = 0
        health_result = 0
        politics_result = 0

        if isinstance(econ, pd.DataFrame):
            econ = pd.merge(trends, econ, on='date', sort=False).dropna()
            econ['econ'] = self.scale(econ['econ'])
            econ['trend'] = self.scale(econ['trend'])
            print('----- Economics Causal Test -----')
            econ_result, econ_vals = self.dowhy(econ, 'econ')
            econ_values = CausalValues(econ_result, econ_vals[0], econ_vals[1], econ_vals[2], econ_vals[3],
                                 econ_vals[4])
        else:
            econ_values = CausalValues(-1, 0, 0, 0, 0, 0)

        if isinstance(health, pd.DataFrame):
            health = pd.merge(trends, health, on='date', sort=False).dropna()
            health['health'] = self.scale(health['health'])
            health['trend'] = self.scale(health['trend'])
            print('----- Health Causal Test -----')
            health_result, health_vals = self.dowhy(health, 'health')
            health_values = CausalValues(health_result, health_vals[0], health_vals[1], health_vals[2],
                                   health_vals[3], health_vals[4])
        else:
            health_values = CausalValues(-1, 0, 0, 0, 0, 0)

        if isinstance(politics, pd.DataFrame):
            politics = pd.merge(trends, politics, on='date', sort=False).dropna()
            politics['politics'] = self.scale(politics['politics'])
            politics['trend'] = self.scale(politics['trend'])
            print('----- Politics Causal Test -----')
            politics_result, politics_vals = self.dowhy(politics, 'politics')
            politics_values = CausalValues(politics_result, politics_vals[0], politics_vals[1],
                                     politics_vals[2], politics_vals[3], politics_vals[4])
        else:
            politics_values = CausalValues(-1, 0, 0, 0, 0, 0)

        matplotlib.rcParams.update(matplotlib.rcParamsDefault)

        return econ_values, health_values, politics_values


class TrendMap:

    def __init__(self):
        pass

    def map_maker(self, keywords: [str]):
        pytrend = TrendReq()
        for i in range(len(keywords)):
            try:
                pytrend.build_payload(kw_list=[keywords[i]])
                if i == 0:
                    df = pytrend.interest_by_region()
                else:
                    resp = pytrend.interest_by_region()
                    df[keywords[i]] = resp[keywords[i]].values
            
            except:
                print("Warning: Couldn't connect to Google Trends")
                return 0

        df['metric'] = df.mean(axis=1)
        countries = pd.read_csv(Path(__file__).parent.parent.parent / 'Data' / 'countries.csv')

        index = df.index
        vals = {}
        country = []
        trend = []
        for code in index:
            if (countries['Title'] == code).any():
                temp = int(df.loc[[code]].metric)
                ans = countries[countries == code].stack().index.tolist()
                key = countries.code3[ans[0][0]]
                if temp != 0:
                    vals[key] = temp
                    country.append(key)
                    trend.append(temp)

        # vals = pd.DataFrame(country, columns=['country'])
        # vals['trend'] = trend

        # fig = go.Figure(data=go.Choropleth(
        #     locations=vals['country'],
        #     z=vals['trend'],
        #     colorscale=[[0, 'rgb(229,236,246)'], [1.0, 'rgb(47, 79, 255)']],
        #     autocolorscale=False,
        #     marker_line_color='rgb(51, 51, 51)',
        #     marker_line_width=0.02,
        #     colorbar_title='Trend<br>Value', ))
        #
        # fig.update_layout(
        #     title=dict(text='Manifesto Trend Map', font_size=24, font_color='black'),
        #     geo=dict(
        #         showframe=False,
        #         showcoastlines=False,
        #         projection_type='equirectangular'
        #     ),
        #     font={'color': "rgb(51, 51, 51)", 'family': 'Poppins', 'size': 19.2})

        MapValues = namedtuple('MapValues', 'countries trends')
        Map = MapValues(country, trend)
        return Map


if __name__ == "__main__":
    c = Causal()
    test_keywords = ['Vaccine', 'Vaccination', 'Control', 'Government', 'MicroChip']
    country = 'United Kingdom'
    econ, health, politics = c.analyse(test_keywords, country)
    print(econ)
    print(health)
    print(politics)
    t = TrendMap()
    test_map = t.map_maker(test_keywords)
    print(test_map)


