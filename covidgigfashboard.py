# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
import pandas as pd
import seaborn as sns
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
data = pd.read_csv('./COVID_NET/valid_df.csv')


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
