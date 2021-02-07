# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import seaborn as sns

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
data = pd.read_csv('./COVID_NET/valid_df.csv')
cdr_df = pd.read_csv('./COVID_NET/merged_data.csv')
cdr_df = cdr_df[['catchment', 'date', 'Confirmed', 'Deaths', 'Recovered']]
population_df = pd.read_csv('./US_Census/nst-est2020.csv')

# filter for all the valid rows for states (exclude 'Entire Network')
valid_df = data[pd.notnull(data['weekly_rate'])]
valid_df = valid_df.loc[valid_df['catchment'] != 'Entire Network']

# filter for all overall rows for states exclude entire network)
overall_df = valid_df.loc[(valid_df['age_category'] == 'Overall') &
                          (valid_df['sex'] == 'Overall') &
                          (valid_df['race'] == 'Overall')]

# filter based on sex for states
sex_df = valid_df.loc[(valid_df['age_category'] == 'Overall') &
                          (valid_df['sex'] != 'Overall') &
                          (valid_df['race'] == 'Overall')]


# filter based on race for states
race_df = valid_df.loc[(valid_df['age_category'] == 'Overall') &
                          (valid_df['sex'] == 'Overall') &
                          (valid_df['race'] != 'Overall')]


# filter based on age
age_df = valid_df.loc[(valid_df['age_category'] != 'Overall') &
                          (valid_df['sex'] == 'Overall') &
                          (valid_df['race'] == 'Overall')]


# generalize to five age group as it's shown on the website
age_df = age_df.loc[(age_df['age_category'] == '0-4 yr') |
                    (age_df['age_category'] == '5-17 yr') |
                    (age_df['age_category'] == '18-49 yr') |
                    (age_df['age_category'] == '50-64 yr') |
                    (age_df['age_category'] == '65+ yr')]

overallWeekly = px.line(overall_df, x="date", y="weekly_rate", color="catchment")
overallCumulative = px.line(overall_df, x="date", y="cumulative_rate", color="catchment")

weeklyBySex = px.box(sex_df, x="date", y="weekly_rate", color="sex")
cumulativeBySex = px.box(sex_df, x="date", y="cumulative_rate", color="sex")

weeklyByRace = px.box(race_df, x="date", y="weekly_rate", color="race")
cumulativeByRace = px.box(race_df, x="date", y="cumulative_rate", color="race")

weeklyByAge = px.box(age_df, x="date", y="weekly_rate", color="age_category")
cumulativeByAge = px.box(age_df, x="date", y="cumulative_rate", color="age_category")



population_df = population_df[['state', 'name', 'popestimate2020']]
hosp_states = ["Tennessee","Utah","California","Colorado","Connecticut","Georgia","Iowa","Maryland","Michigan","Minnesota","New Mexico","New York","Ohio","Oregon"]

state_pop_df = population_df.loc[population_df['name'].isin(hosp_states)]
state_pop_df.head()

# Left join (using merger)
overall_df = overall_df.merge(state_pop_df, left_on='catchment', right_on='name')

# Then drop useless columns
overall_df = overall_df.drop(labels=['network', 'name', 'state'], axis=1)

overall_df = overall_df.assign(cumuhos_count = np.ceil(overall_df['popestimate2020']/1e6 * overall_df['cumulative_rate']).astype(int))
overall_df = overall_df.assign(weeklyhos_count = np.ceil(overall_df['popestimate2020']/1e6 * overall_df['weekly_rate']).astype(int))
overall_df = pd.merge(overall_df, cdr_df, on=['catchment', 'date'], how='left')
overall_df = joined.drop_duplicates()
overall_df = overall_df.assign(hoscount_per_confirmed = overall_df['cumuhos_count']/overall_df['Confirmed'])
overall_df = overall_df.assign(recovery_per_confirmed = overall_df['Recovered']/overall_df['Confirmed'])
overall_df = overall_df.assign(infecting_ratio = overall_df['Confirmed']/overall_df['popestimate2020'])


app.layout = html.Div(children=[
    html.Div([
    	html.H1(children='COVID-19 Hospitalization'),
    	
    	html.Div(children='''
    	    By Yixin Tian, Harris Zheng, Ron Hu
    	'''),
    ]),
    # All elements from the top of the page
     html.Div([
        html.Div([
            html.H1(children='Overall weekly rate trends for all states'),

            dcc.Graph(
                id='graph1',
                figure=overallWeekly
            ),  
        ], className='six columns'),
        html.Div([
            html.H1(children='Overall cumulative rate trends for all states'),
            
            dcc.Graph(
                id='graph2',
                figure=overallCumulative
            ),  
        ], className='six columns'),
    ], className='row'),
    
    
     html.Div([
        html.Div([
            html.H1(children='Overall weekly rate (based on gender) trends for all states'),

            dcc.Graph(
                id='graph3',
                figure=weeklyBySex
            ),  
        ], className='six columns'),
        html.Div([
            html.H1(children='Overall cumulative rate (based on gender) trends for all states'),
            
            dcc.Graph(
                id='graph4',
                figure=cumulativeBySex
            ),  
        ], className='six columns'),
    ], className='row'),

     html.Div([
        html.Div([
            html.H1(children='Overall weekly rate (based on race) trends for all states'),

            dcc.Graph(
                id='graph5',
                figure=weeklyByRace
            ),  
        ], className='six columns'),
        html.Div([
            html.H1(children='Overall cumulative rate (based on race) trends for all states'),
            
            dcc.Graph(
                id='graph6',
                figure=cumulativeByRace
            ),  
        ], className='six columns'),
    ], className='row'),
    
        
])

if __name__ == '__main__':
    app.run_server(debug=True)
