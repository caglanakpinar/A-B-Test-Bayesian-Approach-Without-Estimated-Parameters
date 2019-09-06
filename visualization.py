import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import webbrowser

import constants

def create_dashboard(parameters):
    result, result_rfm = pd.DataFrame(), pd.DataFrame()
    try:
        result = pd.read_csv('daily_ab_test_results.csv')
        if parameters['is_segmented']:
            result_rfm = pd.read_csv('daily_ab_test_results_rfm.csv')
    except:
        print("""
        In order to use dashboard function, pls import your results as 
        'daily_ab_test_results.csv' and if you have segmented test results, pls import as
        'daily_ab_test_results_rfm.csv'
        """)
    filters = create_filters(result, result_rfm)
    creating_dashboard_prototype(filters, result, result_rfm)
    print("Dashboard is created successfully!...")

def create_filters(result, result_rfm):
    metrics = list(result['metrics'].unique()) + ['ALL']
    days = list(result['day'].unique()) + ['ALL']
    t_test_H0 = list(result['t_test_H0'].unique()) + ['ALL']
    chi_square_H0 = list(result['chi_square_H0'].unique()) + ['ALL']
    bayesian_winnig_ratios_list = list(result['bayesian_approach_confidence'].unique())
    bayesian_w_r_bins = (max(bayesian_winnig_ratios_list) - min(bayesian_winnig_ratios_list)) / 10
    bayesian_winnig_ratios = list(np.arange(min(bayesian_winnig_ratios_list),
                                            max(bayesian_winnig_ratios_list),
                                            (max(bayesian_winnig_ratios_list) - min(bayesian_winnig_ratios_list)) / 10
                                            )) + ['ALL']
    if len(result_rfm) == 0:
        rfm_values = constants.DEFAULT_RFM + ['ALL']
    else:
        rfm_values = list(result_rfm[result_rfm['rfm'] == result_rfm['rfm']]['rfm']) + ['ALL']
    return {'metrics': metrics, 'days': days, 't_test_H0': t_test_H0, 'chi_square_H0': chi_square_H0,
            'bayesian_winnig_ratios_list': bayesian_winnig_ratios_list, 'bayesian_w_r_bins': bayesian_w_r_bins,
            'bayesian_winnig_ratios': bayesian_winnig_ratios, 'rfm_values': rfm_values}

def creating_dashboard_prototype(filters, result, result_rfm):
    bayesian_w_r_bins = filters['bayesian_w_r_bins']
    winnig_ratios = filters['bayesian_winnig_ratios']
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css'] # internet access to get .css file
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
    app.layout = html.Div([
        html.Div([
            html.Div([
                dcc.Dropdown(
                    id='crossfilter-metrics',
                    options=[{'label': i, 'value': i} for i in filters['metrics']],
                    multi=True,
                    value='ALL'
                )
            ],
                style={'width': '30%', 'display': 'inline-block'}),
            html.Div([
                dcc.Dropdown(
                    id='crossfilter-day',
                    options=[{'label': i, 'value': i} for i in filters['days']],
                    value='ALL',
                    multi=True,
                )
            ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
        ], style={
            'borderBottom': 'thin lightgrey solid',
            'backgroundColor': 'rgb(250, 250, 250)',
            'padding': '10px 5px'
        }),
        html.Div([
            html.Div([
                dcc.Dropdown(
                    id='crossfilter-t_test_H0',
                    options=[{'label': i, 'value': i} for i in filters['t_test_H0']],
                    value='ALL',
                    multi=True,
                )
            ],
                style={'width': '30%', 'display': 'inline-block'}),
            html.Div([
                dcc.Dropdown(
                    id='crossfilter-chi_square_H0',
                    options=[{'label': i, 'value': i} for i in filters['chi_square_H0']],
                    value='ALL'
                )
            ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
        ], style={
            'borderBottom': 'thin lightgrey solid',
            'backgroundColor': 'rgb(250, 250, 250)',
            'padding': '10px 5px'
        }),
        html.Div([
            html.Div([
                dcc.Dropdown(
                    id='crossfilter-bayesian_winnig_ratios',
                    options=[{'label': i, 'value': i} for i in filters['bayesian_winnig_ratios']],
                    value='ALL'
                )
            ],
                style={'width': '30%', 'display': 'inline-block'}),
            html.Div([
                dcc.Dropdown(
                    id='crossfilter-rfm_values',
                    options=[{'label': i, 'value': i} for i in filters['rfm_values']],
                    value='ALL',
                    multi=True
                )
            ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
        ], style={
            'borderBottom': 'thin lightgrey solid',
            'backgroundColor': 'rgb(250, 250, 250)',
            'padding': '10px 5px'
        }),
        html.Div([
            dcc.Graph(
                id='daily-control_and_validation_sets-line',
                hoverData={'points': [{'customdata': '2019-08-05'}]}
            )
        ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 10'}),
        html.Div([
            dcc.Graph(
                id='daily-winners-line',
                hoverData={'points': [{'customdata': '5cca08a9f878f40008f9adae'}]}
            )
        ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 10'}),
        html.Div([
            dcc.Graph(
                id='daily-control-valid-with-rfm-scatter',
                hoverData={'points': [{'customdata': '5cca08a9f878f40008f9adae'}]}
            )
        ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 10'}),
        html.Div([
            dcc.Graph(
                id='metric-winners-bar',
                hoverData={'points': [{'customdata': '5cca08a9f878f40008f9adae'}]}
            )
        ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 10'})
    ])
    # daily winners` results
    @app.callback(
        dash.dependencies.Output('daily-control_and_validation_sets-line', 'figure'),
        [dash.dependencies.Input('crossfilter-metrics', 'value'),
         dash.dependencies.Input('crossfilter-day', 'value'),
         dash.dependencies.Input('crossfilter-t_test_H0', 'value'),
         dash.dependencies.Input('crossfilter-chi_square_H0', 'value'),
         dash.dependencies.Input('crossfilter-bayesian_winnig_ratios', 'value'),
         dash.dependencies.Input('crossfilter-rfm_values', 'value')
         ]
    )
    def update_graph(metrics, days, t_test_H0, chi_square_H0, winnig_ratios, rfm_values):
        print(metrics, days, t_test_H0, chi_square_H0, winnig_ratios, rfm_values)
        query_str = ""
        # metrics
        if 'ALL' not in metrics:
            metrics_str = "', '".join(metrics)
            query_str += " metrics in " + "('" + metrics_str + "')"
        # days
        if 'ALL' not in days:
            day_str = ", ".join(days)
            is_started = " " if query_str == "" else " and "
            query_str += is_started + " in ('" + day_str + "')"
        # t- Test HO: Accepted / Rejected
        if t_test_H0 != 'ALL':
            is_started = " " if query_str == "" else " and "
            query_str += is_started + " t_test_H0 == @t_test_H0 "
        # Chi Square - Test HO: Accepted / Rejected
        if chi_square_H0 != 'ALL':
            is_started = " " if query_str == "" else " and "
            query_str += is_started + " t_test_H0 == @chi_square_H0 "
        # winnig_ratios
        if winnig_ratios != 'ALL':
            winnig_ratios, winnig_ratios_2 = round(winnig_ratios, 4), round(winnig_ratios, 4) - bayesian_w_r_bins
            print(winnig_ratios, winnig_ratios_2)
            is_started = " " if query_str == "" else " and "
            query_str += is_started + " win_ratio >= @winnig_ratios_2 and win_ratio < @winnig_ratios "
        # segments
        if len(result_rfm) == 0:
            dff = result.query(query_str) if query_str != "" else result
        else:
            if 'ALL' not in rfm_values:
                rfm_str = ", ".join(rfm_values)
                is_started = " " if query_str == "" else " and "
                query_str += is_started + " rfm in ('" + rfm_str + "')"
                dff = result.query(query_str) if query_str != "" else result_rfm
            else:
                dff = result.query(query_str) if query_str != "" else result
        dff = result.query(query_str) if query_str != "" else result
        dff_pivoted = dff.pivot_table(index='day',
                                      aggfunc={'p_control': 'mean', 'p_validation': 'mean'}).reset_index()
        dff_pivoted = dff_pivoted.sort_values(by='day', ascending=True)
        return {
            'data': [go.Scatter(
                x=dff_pivoted['day'],
                y=dff_pivoted['p_control'],
                text=dff_pivoted['day'],
                customdata=dff_pivoted['day'],
                mode='lines+markers',
                name='Control',
                marker={
                    'size': 15,
                    'opacity': 0.5,
                    'line': {'width': 0.5, 'color': 'white'}
                }
            ),
                go.Scatter(
                    x=dff_pivoted['day'],
                    y=dff_pivoted['p_validation'],
                    text=dff_pivoted['day'],
                    customdata=dff_pivoted['day'],
                    mode='lines+markers',
                    name='Validation',
                    marker={
                        'size': 15,
                        'opacity': 0.5,
                        'line': {'width': 0.5, 'color': 'white'}
                    }
                )],
            'layout': go.Layout(
                xaxis={
                    'title': 'days',
                },
                yaxis={
                    'title': 'CTR'
                },
                margin={'l': 40, 'b': 30, 't': 10, 'r': 0},
                height=450,
                hovermode='closest'
            )
        }
    # rfm values of test results
    @app.callback(
        dash.dependencies.Output('daily-control-valid-with-rfm-scatter', 'figure'),
        [dash.dependencies.Input('crossfilter-metrics', 'value'),
         dash.dependencies.Input('crossfilter-day', 'value'),
         dash.dependencies.Input('crossfilter-t_test_H0', 'value'),
         dash.dependencies.Input('crossfilter-chi_square_H0', 'value'),
         dash.dependencies.Input('crossfilter-bayesian_winnig_ratios', 'value'),
         dash.dependencies.Input('crossfilter-rfm_values', 'value'),
         dash.dependencies.Input('daily-control_and_validation_sets-line', 'hoverData'),
         ]
    )
    def update_graph(metrics, days, t_test_H0, chi_square_H0, winnig_ratios, rfm_values, hoverData):
        query_str = ""
        if len(result_rfm) != 0:
            # metrics
            if 'ALL' not in metrics:
                metrics_str = "', '".join(metrics)
                query_str += " metrics in " + "('" + metrics_str + "')"
            # days
            if 'ALL' not in days:
                day_str = ", ".join(days)
                is_started = " " if query_str == "" else " and "
                query_str += is_started + " day in ('" + day_str + "')"
                # t- Test HO: Accepted / Rejected
            if t_test_H0 != 'ALL':
                is_started = " " if query_str == "" else " and "
                query_str += is_started + " t_test_H0 == @t_test_H0 "
            # Chi Square - Test HO: Accepted / Rejected
            if chi_square_H0 != 'ALL':
                is_started = " " if query_str == "" else " and "
                query_str += is_started + " t_test_H0 == @chi_square_H0 "
            # winnig_ratios
            if winnig_ratios != 'ALL':
                winnig_ratios, winnig_ratios_2 = round(winnig_ratios, 4), round(winnig_ratios, 4) - bayesian_w_r_bins
                print(winnig_ratios, winnig_ratios_2)
                is_started = " " if query_str == "" else " and "
                query_str += is_started + " win_ratio >= @winnig_ratios_2 and win_ratio < @winnig_ratios "
            # segments
            if 'ALL' not in rfm_values:
                rfm_str = ", ".join(rfm_values)
                is_started = " " if query_str == "" else " and "
                query_str += is_started + " rfm in ('" + rfm_str + "')"
            dff_segment = result_rfm.query(query_str) if query_str != "" else result_rfm
            # day from daily-control_and_validation_sets-line graph
            dff_segment = dff_segment[dff_segment['day'] == hoverData['points'][0]['customdata']]
            dff_pivoted = dff_segment.pivot_table(index='rfm',
                                                  aggfunc={'p_control': 'mean', 'p_validation': 'mean'}).reset_index()
            print(len(dff_pivoted))
            dff_pivoted['diff'] = dff_pivoted['p_validation'] - dff_pivoted['p_control']
            print(dff_pivoted)
            return {
                'data': [go.Scatter(
                    x=dff_pivoted['rfm'],
                    y=dff_pivoted['diff'],
                    text=dff_pivoted['rfm'],
                    customdata=dff_pivoted['rfm'],
                    mode='markers',
                    marker={
                        'size': 15,
                        'opacity': 0.5,
                        'line': {'width': 0.5, 'color': 'white'}
                    }
                )],
                'layout': go.Layout(
                    xaxis={
                        'title': 'days',
                    },
                    yaxis={
                        'title': 'Validation - Control CTR Difference '
                    },
                    margin={'l': 40, 'b': 30, 't': 10, 'r': 0},
                    height=450,
                    hovermode='closest'
                )
            }
    # daily winning ratios
    @app.callback(
        dash.dependencies.Output('daily-winners-line', 'figure'),
        [dash.dependencies.Input('crossfilter-metrics', 'value'),
         dash.dependencies.Input('crossfilter-day', 'value'),
         dash.dependencies.Input('crossfilter-t_test_H0', 'value'),
         dash.dependencies.Input('crossfilter-chi_square_H0', 'value'),
         dash.dependencies.Input('crossfilter-bayesian_winnig_ratios', 'value'),
         dash.dependencies.Input('crossfilter-rfm_values', 'value')
         ]
    )
    def update_graph(metrics, days, t_test_H0, chi_square_H0, winnig_ratios, rfm_values):
        print(metrics, days, t_test_H0, chi_square_H0, winnig_ratios, rfm_values)
        query_str = ""
        # metrics
        if 'ALL' not in metrics:
            metrics_str = "', '".join(metrics)
            query_str += " metrics in " + "('" + metrics_str + "')"
        # days
        if 'ALL' not in days:
            day_str = ", ".join(days)
            is_started = " " if query_str == "" else " and "
            query_str += is_started + " in ('" + day_str + "')"
        # t- Test HO: Accepted / Rejected
        if t_test_H0 != 'ALL':
            is_started = " " if query_str == "" else " and "
            query_str += is_started + " t_test_H0 == @t_test_H0 "
        # Chi Square - Test HO: Accepted / Rejected
        if chi_square_H0 != 'ALL':
            is_started = " " if query_str == "" else " and "
            query_str += is_started + " t_test_H0 == @chi_square_H0 "
        # winnig_ratios
        if winnig_ratios != 'ALL':
            winnig_ratios, winnig_ratios_2 = round(winnig_ratios, 4), round(winnig_ratios, 4) - bayesian_w_r_bins
            print(winnig_ratios, winnig_ratios_2)
            is_started = " " if query_str == "" else " and "
            query_str += is_started + " win_ratio >= @winnig_ratios_2 and win_ratio < @winnig_ratios "
        # segments
        if len(result_rfm) == 0:
            dff = result.query(query_str) if query_str != "" else result
        else:
            if 'ALL' not in rfm_values:
                rfm_str = ", ".join(rfm_values)
                is_started = " " if query_str == "" else " and "
                query_str += is_started + " rfm in ('" + rfm_str + "')"
                dff = result.query(query_str) if query_str != "" else result_rfm
            else:
                dff = result.query(query_str) if query_str != "" else result
        dff = result.query(query_str) if query_str != "" else result
        dff_pivoted = dff.pivot_table(index='day',
                                      aggfunc={'win_ratio': 'mean'}).reset_index()
        dff_pivoted = dff_pivoted.sort_values(by='day', ascending=True)
        return {
            'data': [go.Scatter(
                x=dff_pivoted['day'],
                y=dff_pivoted['win_ratio'],
                text=dff_pivoted['day'],
                customdata=dff_pivoted['day'],
                mode='lines+markers',
                name='How many times Validation CTR wins Control CRT ?',
                marker={
                    'size': 15,
                    'opacity': 0.5,
                    'line': {'width': 0.5, 'color': 'white'}
                }
            )],
            'layout': go.Layout(
                xaxis={
                    'title': 'days',
                },
                yaxis={
                    'title': 'Validation Wining Ratios'
                },
                margin={'l': 40, 'b': 30, 't': 10, 'r': 0},
                height=450,
                hovermode='closest'
            )
        }
    # metrics of winning bar chart
    @app.callback(
        dash.dependencies.Output('metric-winners-bar', 'figure'),
        [dash.dependencies.Input('crossfilter-metrics', 'value'),
         dash.dependencies.Input('crossfilter-day', 'value'),
         dash.dependencies.Input('crossfilter-t_test_H0', 'value'),
         dash.dependencies.Input('crossfilter-chi_square_H0', 'value'),
         dash.dependencies.Input('crossfilter-bayesian_winnig_ratios', 'value'),
         dash.dependencies.Input('crossfilter-rfm_values', 'value'),
         dash.dependencies.Input('daily-winners-line', 'hoverData'),
         ]
    )
    def update_graph(metrics, days, t_test_H0, chi_square_H0, winnig_ratios, rfm_values, hoverData):
        query_str = ""
        if len(result_rfm) != 0:
            # metrics
            if 'ALL' not in metrics:
                metrics_str = "', '".join(metrics)
                query_str += " metrics in " + "('" + metrics_str + "')"
            # days
            if 'ALL' not in days:
                day_str = ", ".join(days)
                is_started = " " if query_str == "" else " and "
                query_str += is_started + " day in ('" + day_str + "')"
                # t- Test HO: Accepted / Rejected
            if t_test_H0 != 'ALL':
                is_started = " " if query_str == "" else " and "
                query_str += is_started + " t_test_H0 == @t_test_H0 "
            # Chi Square - Test HO: Accepted / Rejected
            if chi_square_H0 != 'ALL':
                is_started = " " if query_str == "" else " and "
                query_str += is_started + " t_test_H0 == @chi_square_H0 "
            # winnig_ratios
            if winnig_ratios != 'ALL':
                winnig_ratios, winnig_ratios_2 = round(winnig_ratios, 4), round(winnig_ratios, 4) - bayesian_w_r_bins
                print(winnig_ratios, winnig_ratios_2)
                is_started = " " if query_str == "" else " and "
                query_str += is_started + " win_ratio >= @winnig_ratios_2 and win_ratio < @winnig_ratios "
            # segments
            if 'ALL' not in rfm_values:
                rfm_str = ", ".join(rfm_values)
                is_started = " " if query_str == "" else " and "
                query_str += is_started + " rfm in ('" + rfm_str + "')"
            dff_segment = result_rfm.query(query_str) if query_str != "" else result_rfm
            # day from daily-control_and_validation_sets-line graph
            dff_segment = dff_segment[dff_segment['day'] == hoverData['points'][0]['customdata']]
            dff_pivoted = dff_segment.pivot_table(index='metrics',
                                                  aggfunc={'win_ratio': 'mean'}).reset_index()
            return {
                'data': [go.Bar(name='  asdasdad', x=dff_pivoted['metrics'], y=dff_pivoted['win_ratio'])],
                'layout': go.Layout(
                    xaxis={
                        'title': 'metrics',
                    },
                    yaxis={
                        'title': 'Validation Winning Ratios'
                    },
                    margin={'l': 40, 'b': 30, 't': 10, 'r': 0},
                    height=450,
                    hovermode='closest'
                )
            }

    webbrowser.open('http://127.0.0.1:8050/')
    app.run_server(debug=False)