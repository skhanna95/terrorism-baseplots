import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from django.conf.urls import include, url
from dash.dependencies import Input, Output
import json
import dash_daq as daq
import locale
import numpy as np
import os
############################################################################
locale.setlocale(locale.LC_ALL, '')
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#df_Terror_By_Year = pd.read_csv('C:/Users/Veekesh/Terrorism_By_Year.csv')
############################################################################
#df_Terror_By_Region = pd.read_csv('terrorism_final.csv')
# region_list = df_Terror_By_Region['Region'].tolist()
# count_list = df_Terror_By_Region['Count'].tolist()

#df_Terror_By_Region_Sorted = df_Terror_By_Region.sort_values(by='Count', ascending=False)
############################################################################
#df_Casualty_By_Region = pd.read_csv('C:/Users/Veekesh/Casualty_By_Region.csv')
############################################################################
#df_Sunburst = pd.read_csv('C:/Users/Veekesh/sunburst.csv')
############################################################################
df_terror = pd.read_csv('terrorism_final.csv')

############################################################################
def update_pie_year(df):
    df_Terror_By_Region = df[['Region','EventId']]
    df_Terror_By_Region = df_Terror_By_Region.groupby(['Region']).count()
    df_Terror_By_Region = df_Terror_By_Region.reset_index()
    df_Terror_By_Region= df_Terror_By_Region.rename(columns={'EventId':'Count'})
    region_list = df_Terror_By_Region['Region'].tolist()
    count_list = df_Terror_By_Region['Count'].tolist()
    return [region_list,count_list]

###########################################################################
pie_data = update_pie_year(df_terror)[0]
pie_count = update_pie_year(df_terror)[1]
###########################################################################

def update_country(df):
    df_Terror_By_Year = df[['Year','EventId']]
    df_Terror_By_Year = df_Terror_By_Year.groupby(['Year']).count()
    df_Terror_By_Year = df_Terror_By_Year.reset_index()
    df_Terror_By_Year= df_Terror_By_Year.rename(columns={'EventId':'Count'})
    return df_Terror_By_Year

df_Terror_By_Year = update_country(df_terror)
###########################################################################

# Create a list of dictionary items for distinct countries
country_list = [dict({'label':'Select Country', 'value':'Select Country'})]
for i in df_terror['Country'].unique().tolist():
    country_list.append(dict({'label':i, 'value':i}))

# print(country_list)

##########################################################################
# Table 1 ################################################################

df_table = df_terror[['Year','Month','Day','Country','City','Group','AttackType','Killed','Wounded']].head(20)

##########################################################################
# TOP 5 Terrorist Groups By Year - Based on Number of Terrorist Attacks

def top5_group(df):
    df_Top5_Group = df[['Group','EventId']]
    df_Top5_Group = df_Top5_Group.groupby(['Group']).count()
    df_Top5_Group = df_Top5_Group.reset_index()
    df_Top5_Group= df_Top5_Group.rename(columns={'EventId':'Count'})
    df_Top5_Group= df_Top5_Group.sort_values('Count',ascending = False).head(5)
    return df_Top5_Group

df_Top5_Group = top5_group(df_terror)

print(df_Top5_Group['Group'].tolist())
print(df_Top5_Group['Count'].tolist())
## hEADLINES ###########################################################
killed_count_1 = int(df_terror[['Killed']].sum())
killed_count= f'{killed_count_1:n}' 

wounded_count_1 = int(df_terror[['Wounded']].sum())
wounded_count= f'{wounded_count_1:n}' 

avg_yearly_casualty = (int(killed_count_1) + int(wounded_count_1))//18
avg_yearly_casualty = f'{avg_yearly_casualty:n}'
##########################################################################

##########################################################################

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server=app.server
server.secret_key = os.environ.get('secret_key', 'secret')

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}



app.layout = html.Div([

	#################################################################





    ################################################################
#    html.Div('',style={'display': 'block'}),

    #######################################################################
#    html.Div([
 #   html.Div('killed'),
  #  ], className="people_killed",style={'display': 'inline-block'}),
#
 #   html.Div([
  #  html.Div('wounded'),
   # ], className="people_wounded",style={'display': 'inline-block'}),

    # html.Div([
    # html.Div('AVG Yearly Casualty'),
    # ], className="casualty",style={'display': 'inline-block'}),


    #######################################################################


    ##################################################################

    html.Div([

        # graph 1
        # ************************************************************
        html.Div([
            html.H5(''),
            dcc.Graph(
                id='g1',
                figure={
                        'data': [ { 'x': df_Terror_By_Year['Year'],'y': df_Terror_By_Year['Count'],  'type': 'bar', 'name': 'Terrorism'} ],
                        'layout': {'title': 'Terrorism Count By Year'}
                        },
                config={
                        'displayModeBar': False
                        },
                    ),
            html.Pre(id='click-data'),
        ], style={'width': '43%','height':'80%', 'display': 'inline-block'}, className="class_g1"),


        # html.Div(className='row', children=[
        #  html.Div([
           
        #     html.Pre(id='click-data'),
        # ], className='three columns')

        #  ]),
        # *************************************************************
   
        html.Div([
            html.H5(''),
            dcc.Graph(
                id='g2',
                figure={
                        'data': [ { 'x': df_Terror_By_Year['Year'],'y': df_Terror_By_Year['Count'],  'type': 'line', 'name': 'Terrorism1' } ],
                        'layout': {'title': 'Global Terrorism Trend'}
                        },
                config={
                        'displayModeBar': False
                        },
                     ),
        ], style={'width': '43%', 'display': 'inline-block'}, className="class_g2"),


        # *********************************************************************

        html.Div([
            html.H5(style={"textAlign": "center"}),
            dcc.Graph(
                id='g3',
                figure=go.Figure(
                    data=[go.Pie(labels=pie_data,
                                values=pie_count)],
                                layout=go.Layout(
                                title='Terrorism By Region',
                                margin=dict(l=30, r=0, t=100, b=0) )
                                ),
                    config={
                            'displayModeBar': False
                            },

                    )
        ], style={'width': '43%', 'display': 'inline-block','margin-top':'35px','margin-left':'68px'}, className="class_g3"),     

    # *************************************************************************


        html.Div([
            html.H5(''),
            dcc.Graph(
                id='g4',
                figure=go.Figure(go.Funnel(
                                y = df_Top5_Group['Group'].tolist(),
                                x = df_Top5_Group['Count'].tolist(),
                                
                                ),
	                			layout=go.Layout(title='Terrorism By Most Influential Groups')
                			),   
                    config={
                        'displayModeBar': False
                        },      
                    )
        ], style={'width': '43%', 'display': 'inline-block'}, className="class_g4"),     




    # ###########################################################################




    ###########################################################################

    ],style={'width': '100%'}, className="row")

])


app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})  
#=====================================================================


# @app.callback(
#     Output('click-data', 'children'),
#     [Input('g1', 'clickData')])
# def display_click_data(clickData):
#     return json.dumps(clickData, indent=2)


# Callback for Line Chart
#######################################################################
# @app.callback(Output('g2','figure'),
#               [Input('g1', 'clickData')])
# def update_graph(clickData):

#     if isinstance(clickData, type(None)):
#         return {
#                 'data': [ { 'x': df_Terror_By_Year['Year'],'y': df_Terror_By_Year['Terrorist_Activity_Count'],  'type': 'line', 'name': 'Terrorism1' } ],
#                 'layout': {'title': 'Terrorism Count By Year2'}
#                 }
#     else:
#         # print(clickData['points'][0]['x'])
#         # print(df_Terror_By_Year[df_Terror_By_Year['Year']==clickData['points'][0]['x']]['Terrorist_Activity_Count'])
#         return {
#                 'data': [ { 'x': df_Terror_By_Year[df_Terror_By_Year['Year']==clickData['points'][0]['x']]['Year'],'y': df_Terror_By_Year[df_Terror_By_Year['Year']==clickData['points'][0]['x']]['Terrorist_Activity_Count'],  'type': 'line', 'name': 'Terrorism1' } ],
#                 'layout': {'title': 'Terrorism Count By Year2'}
#                 }

#####################################################################


#####################################################################


# Callback for Pie Chart
#update_pie_year(df_terror[df_terror['Year']==clickData['points'][0]['x']])[0]
#######################################################################
@app.callback(Output('g3','figure'),
              [Input('g1', 'clickData')])

def update_pie_chart(clickData):

    if isinstance(clickData, type(None)):
        return (go.Figure(
                    data=[go.Pie(labels=pie_data,
                                values= pie_count)],
                                layout=go.Layout(
                                title='Terrorism By Region')
                        )       
                )
    else:
        return (go.Figure(
                    data=[go.Pie(labels=df_terror[df_terror['Year']==clickData['points'][0]['x']][['Region','EventId']].groupby(['Region']).count().reset_index().rename(columns={'EventId':'Count'})['Region'].tolist(),
                                values= df_terror[df_terror['Year']==clickData['points'][0]['x']][['Region','EventId']].groupby(['Region']).count().reset_index().rename(columns={'EventId':'Count'})['Count'].tolist())],
                                layout=go.Layout(
                                title='Terrorism By Region')
                        )       
                )

######################################################################
# Callback for range slider
# @app.callback(
#     Output('g1', 'figure'),
#     [Input('range-slider1', 'value')])

# def update_fig1(selected_year_range):

#     #print(selected_year_range)

#     filtered_df = df_Terror_By_Year[(df_Terror_By_Year['Year'] >= selected_year_range[0]) & (df_Terror_By_Year['Year'] <= selected_year_range[1])]

#     return {
#     'data': [ { 'x': filtered_df['Year'],'y': filtered_df['Count'],  'type': 'bar', 'name': 'Terrorism'} ],
#     'layout': {'title': 'Terrorism Count By Year'}
#     }


#####################################################################



#=====================================================================
if __name__ == '__main__':
    app.run_server(debug=True)