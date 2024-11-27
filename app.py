# Note: Directory containing app:
# /Users/cea/Desktop/Data Analysis and Machine Learning/Python/Dash-dashboard/
# python3 app.py

############################################################

# # Import statements

import dash
from dash import Dash, html, dcc, Input, Output, dash_table
import dash.dash_table.FormatTemplate as FormatTemplate
import datetime

import dash_bootstrap_components as dbc
import plotly.express as px

import pandas as pd
from scipy.stats import pearsonr

# # #

app = dash.Dash(__name__,
    meta_tags=[{'name': 'viewport',
    'content': 'width=device-width, initial-scale=1.0'}], 
    title='Sales Data Analysis'
    )

server = app.server

df = pd.read_csv(
    "data/sales_data.csv", sep=','
)

# # Boxplot of average order values, aggregated by numbers of orders per customer # #

box_fig = px.bar(data_frame = df,
               y = 'Average Order Value',
               x = 'Historic Number Of Orders',
                template="plotly_dark",
                color_discrete_sequence=['#0488c2']
                # color='Historic Number Of Orders', # Display bars in multiple colors
                )

box_fig.update_xaxes(dtick=1, title_text='Hist No. Of Orders per Cust')
box_fig.update_yaxes(tickprefix="$", title_text='Avg Order Val per Cust')
box_fig.layout.update(showlegend=False) 
box_fig.update_layout(margin_r=0, margin_l=0, margin_t=0, margin_b=0, font_size=10)

box_fig.update_layout({
'plot_bgcolor': 'rgba(0, 0, 0, 0)',
'paper_bgcolor': 'rgba(0, 0, 0, 0)',
})

hist = px.histogram(df, 
                   x = 'Average Order Value',
                   title='', 
                   template="plotly_dark",
                   histnorm='percent',
                   opacity=0.6, color_discrete_sequence=['#0488c2'])

hist.update_xaxes(tickprefix='$', title_text='Avg Order Val per Cust')
hist.update_yaxes(ticksuffix='%', title_text='Pct of Customers')
hist.update_layout(margin_r=0, margin_l=0, 
    margin_t=0, margin_b=0, 
    font_size=10, 
    )

hist.update_layout({
'plot_bgcolor': 'rgba(0, 0, 0, 0)',
'paper_bgcolor': 'rgba(0, 0, 0, 0)',
})

hist.update_traces(nbinsx=30, selector=dict(type='histogram'))

# # Scatter plot: days active vs number of orders # #

active_histord_r = pearsonr(df['Historic Number Of Orders'], df['days active'])

scat1 = px.scatter(data_frame = df,
                     y = 'days active',
                     x = 'Historic Number Of Orders',
                     # width=200, height=200,
                     template="plotly_dark",
                     trendline="ols",
                    trendline_color_override="#76b5c5",
                    color_discrete_sequence=['#0488c2'],
                    opacity=0.7
                    )

scat1.update_xaxes(title_text='Hist No. Of Orders per Cust')
scat1.update_yaxes(title_text='Cust Days Active')

scat1.update_layout(margin_r=0, margin_l=0, font_size=10)

scat1.update_layout(
    title={
        'text': f'Pearson\'s R: {active_histord_r[0]:.2f}',
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
scat1.update_layout({
'plot_bgcolor': 'rgba(0, 0, 0, 0)',
'paper_bgcolor': 'rgba(0, 0, 0, 0)',
})


# # Scatter plot: lifetime value vs days active # #

active_histval_r = pearsonr(df['Historic Customer Lifetime Value'], df['days active'])

scat2 = px.scatter(data_frame = df,
                     y = 'Historic Customer Lifetime Value',
                     x = 'days active', 
                     template="plotly_dark",
                     trendline="ols",
                    trendline_color_override="#76b5c5",
                    color_discrete_sequence=['#0488c2'],
                    opacity=0.7)

scat2.update_xaxes(title_text='Cust Days Active')
scat2.update_yaxes(tickprefix="$", title_text='Hist Cust Lifetime Val')

scat2.update_layout(margin_r=0, margin_l=0, font_size=10)

scat2.update_layout(
    title={
        'text': f'Pearson\'s R: {active_histval_r[0]:.2f}',
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
scat2.update_layout({
'plot_bgcolor': 'rgba(0, 0, 0, 0)',
'paper_bgcolor': 'rgba(0, 0, 0, 0)',
})

# # Scatter plot: number of orders vs lifetime value # #

histord_histval_r = pearsonr(df['Historic Number Of Orders'], df['Historic Customer Lifetime Value'])

scat3 = px.scatter(data_frame = df,
                     y = 'Historic Customer Lifetime Value',
                     x = 'Historic Number Of Orders',
                     template="plotly_dark",
                     trendline="ols",
                    trendline_color_override="#76b5c5",
                    color_discrete_sequence=['#0488c2'],
                    opacity=0.7)

scat3.update_xaxes(title_text='Hist No. Of Orders per Cust')
scat3.update_yaxes(tickprefix="$", title_text='Hist Cust Lifetime Val')

scat3.update_layout(
    title={
        'text': f'Pearson\'s R: {histord_histval_r[0]:.2f}',
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'}
        )

scat3.update_layout(margin_r=0, margin_l=0, font_size=10)
scat3.update_layout({
'plot_bgcolor': 'rgba(0, 0, 0, 0)',
'paper_bgcolor': 'rgba(0, 0, 0, 0)',
})

# # Pandas data frame:

df_order_val = df.groupby('Historic Number Of Orders')['Average Order Value'].agg(['median', 'min', 'max', 'count']).reset_index()

df_order_val['pct_of_total'] = df_order_val['count']/df_order_val['count'].sum()

# Note: the following 'data_bars' code for 
# conditional formatting of Dash data table
# is from 'Displaying data bars' vignette on plotly.com

def data_bars(df, column):
    n_bins = 100
    bounds = [i * (1.0 / n_bins) for i in range(n_bins + 1)]
    ranges = [
        ((df[column].max() - df[column].min()) * i) + df[column].min()
        for i in bounds
    ]
    styles = []
    for i in range(1, len(bounds)):
        min_bound = ranges[i - 1]
        max_bound = ranges[i]
        max_bound_percentage = bounds[i] * 100
        styles.append({
            'if': {
                'filter_query': (
                    '{{{column}}} >= {min_bound}' +
                    (' && {{{column}}} < {max_bound}' if (i < len(bounds) - 1) else '')
                ).format(column=column, min_bound=min_bound, max_bound=max_bound),
                'column_id': column
            },
            'background': (
                """
                    linear-gradient(90deg,
                    #0074D9 0%,
                    #0074D9 {max_bound_percentage}%,
                    #414a4e {max_bound_percentage}%,
                    #414a4e 100%)
                """.format(max_bound_percentage=max_bound_percentage)
            ),
            'paddingBottom': 2,
            'paddingTop': 2
        })

    return styles

# # Plotly Table

table = dash_table.DataTable(df_order_val.to_dict('records'),

    css=[{'selector': 'table', 'rule': 'table-layout: fixed'}],

    style_cell_conditional=[

        {'if': {'column_id': 'min'},
         'width': '18%',},

        {'if': {'column_id': 'median'},
         'width': '18%'},

        {'if': {'column_id': 'max'},
         'width': '18%', 'padding-right': '10px',},

        {'if': {'column_id': 'Historic Number Of Orders'},
         'width': '20%'},

         ],

    style_data_conditional=(

        data_bars(df_order_val, 'pct_of_total') +

        [
            {'if': {'column_id': 'Historic Number Of Orders',},
                'backgroundColor': '#414a4e',
                'color': 'white'},

            ]
        ),

    columns=[
            
            {'id': 'min',
            'name': 'min',
            'type': 'numeric',
            'format': FormatTemplate.money(0)},

            {'id': 'median',
            'name': 'median',
            'type': 'numeric',
            'format': FormatTemplate.money(0)}, 

            {'id': 'max',
            'name': 'max',
            'type': 'numeric',
            'format': FormatTemplate.money(0)}, 

            {'id': 'Historic Number Of Orders',
            'name': 'No. Orders',
            'type': 'numeric'}, 

            {'id': 'pct_of_total',
            'name': 'Pct of Cust',
            'type': 'numeric',
            'format': FormatTemplate.percentage(1)
        }],

    style_as_list_view=True,

    style_header={
        'backgroundColor': 'rgba(0, 0, 0, 0)',
        'color': 'white',
        'text-align': 'left',
        # 'font-family': 'arial',
        'font-size': '12px',
    },

    style_data={
        'backgroundColor': 'rgba(0, 0, 0, 0)',
        'color': 'white',
        # 'font-family': 'arial',
        'font-size': '12px',
    },

    )

# Dropdown Selector for Scatter Plots

dropdown = dcc.Dropdown(
                id="type-dropdown-1",
                options=['Days Active vs No. Orders', #scat1
                'Lifetime Value vs Days Active', # scat2
                'Lifetime Value vs No. Orders'], # scat3
                       value='Days Active vs No. Orders',
                        style={'width': '275px', 'backgroundColor':'#1B2631'},
                        )

# Get current date

now = datetime.datetime.now()
today = now.strftime("%Y-%m-%d")

# # App layout section # #

app.layout = dbc.Container([

    dbc.Row([

        dbc.Col([
            html.H1("Sales Data Analysis", 
                className="text-center",
                 style={'color': '#e8e9ea', 'margin-top' : '1%', 'margin-bottom' : '2%'}),
                ], width=10),
            ], justify="center"),

    dbc.Row([

        dbc.Col(
            html.H6(f"As of {today} ◼ Total Customers = {df.shape[0]} ◼︎ Total orders = {df['Historic Number Of Orders'].sum().astype(int)}", 
                className="text-center",
                  style={'color': '#e8e9ea', 'padding-top' : '1%', 'padding-bottom' : '1%',
                  'backgroundColor':'#253748',
                  "border-radius": "5px"}),
                width=6)
            ], justify="center", style={'margin-top' : '0%', 'margin-bottom' : '1%'}),

    dbc.Row([

        dbc.Col([
            dcc.Graph(figure=hist, style={"height": "30vh", 'margin-top' : '3%'}, 
                className="d-flex flex-wrap align-content-end"),
            html.Br(),
            dcc.Graph(figure=box_fig, style={"height": "35vh"}),

                ], width={"size": 4}, className="p-4"),

        dbc.Col([
            html.H6('Aggregate Data', 
                className="text-center",
                style={'color': '#e8e9ea'}
                ),
            html.Div(table)
                ], width=4, className="p-4"),

        dbc.Col([
            html.H6('Select Scatter Plot', 
                className="text-center",
                style={'color': '#e8e9ea', 'margin-bottom' : '2%'}),
            html.Div(
                    dropdown, className='d-flex justify-content-center',
                    style={'margin-bottom' : '3%'}
                    ),
            html.Div(id="measure-vs-measure-1"),

                ], width=4, className="p-4"),

            ], style={"border":"2px #2E4053 solid", 
            "border-radius": "15px", 
            "margin-left": "2%", "margin-right": "2%",
            'box-shadow': '0px 0px 5px 2px rgba(73, 137, 171, .5)'}
            )

    ], className="vh-100", fluid=True, style={'backgroundColor':'#1B2631'})

# # 

@app.callback(
    Output("measure-vs-measure-1", "children"),
    Input("type-dropdown-1", "value"),
)

def select_figure(value):

    if value == "Days Active vs No. Orders":
        return dcc.Graph(figure=scat1, id='graph', style={"height": "60vh"})

    elif value == "Lifetime Value vs Days Active":
        return dcc.Graph(figure=scat2, id='graph', style={"height": "60vh"})

    elif value == "Lifetime Value vs No. Orders":
        return dcc.Graph(figure=scat3, id='graph', style={"height": "60vh"})  

if __name__ == "__main__":
    app.run_server(debug=True)
