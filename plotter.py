import pandas as pd
import numpy as np
import geopandas as gpd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
from datetime import timedelta

def plot_patient_mix(this_hospital_financial_data, payment_types, plot_colors, input_hospital_name, output_hospital_name):
  plot_index = pd.to_datetime(this_hospital_financial_data['Fiscal Year Ending'])
  total_patients = np.zeros(len(plot_index))

  fig = make_subplots()
  for trc_cnt, trace_fill in enumerate(payment_types):
    if trc_cnt == 0:
      fill_type = 'tozeroy'
    else:
      fill_type = 'tonexty'
      
    patient_mix_vals = this_hospital_financial_data[trace_fill].replace('.', 0.0).astype(float).fillna(0.0)  
    total_patients += np.asarray(patient_mix_vals)
    label_name = trace_fill.replace(' Payer Mix', '')
    if len(label_name) > 20:
       label_name = label_name[:20]
       
    fig.add_trace(go.Scatter(x=plot_index, y=total_patients, name=label_name,
                          fill = fill_type, mode ='lines', fillcolor = plot_colors[trc_cnt], 
                          marker=dict(color = plot_colors[trc_cnt], line = dict(width = 0.5))))
                          
  fig.update_layout(title=input_hospital_name + ' (' + output_hospital_name + ')', 
                    title_font=dict(size=18,
                               color='darkslategray',
                               family='Times New Roman'))
  fig.update_yaxes(title = 'Patient Mix (%)', range = [0,1])
  fig.update_xaxes(title = 'Year')
  os.makedirs('FinancialFigures', exist_ok = True)    
  os.makedirs(os.path.join('FinancialFigures', output_hospital_name), exist_ok = True)    
  fig.write_html(os.path.join('FinancialFigures', output_hospital_name, 'patient_mix.html'))

def plot_op_income(this_hospital_financial_data, payment_types, plot_colors, input_hospital_name, output_hospital_name):
  
  plot_index = pd.to_datetime(this_hospital_financial_data['Fiscal Year Ending'])
  total_patients = np.zeros(len(plot_index))

  fig = make_subplots()
  running_tot_op_inc = np.zeros(len(plot_index))
  for trc_cnt, trace_fill in enumerate(payment_types):
    op_inc_vals = np.asarray(this_hospital_financial_data[trace_fill].replace('.', 0.0).astype(float).fillna(0.0))
    label_name = trace_fill.replace(' Hospital Operating Profit (Loss)', '')
    if len(label_name) > 20:
       label_name = label_name[:20]
    for plt_cnt, idx in enumerate(plot_index):
      start_date = idx - timedelta((len(payment_types) - trc_cnt) * 30)
      end_date = idx - timedelta((len(payment_types) - trc_cnt - 1) * 30)
      if plt_cnt == 0:
        show_legend = True
      else:
        show_legend = False
      
      fig.add_trace(go.Scatter(x=[start_date, end_date], y=[running_tot_op_inc[plt_cnt], running_tot_op_inc[plt_cnt]], name=label_name,
                        mode ='lines', marker=dict(color = plot_colors[trc_cnt], line = dict(width = 0.5)), showlegend = False))
      if trc_cnt < 2:
        running_tot_op_inc[plt_cnt] -= op_inc_vals[plt_cnt]
      else:
        running_tot_op_inc[plt_cnt] += op_inc_vals[plt_cnt]
      fig.add_trace(go.Scatter(x=[start_date, end_date], y=[running_tot_op_inc[plt_cnt], running_tot_op_inc[plt_cnt]], name=label_name,
                        fill = 'tonexty', mode ='lines', fillcolor = plot_colors[trc_cnt], 
                        marker=dict(color = plot_colors[trc_cnt], line = dict(width = 0.5)), showlegend = show_legend))
  fig.add_trace(go.Scatter(x=plot_index, y=running_tot_op_inc, name='Total Operating Income',
                    mode ='lines', marker=dict(color = 'black', line = dict(width = 3.5)), showlegend = True))
  fig.update_layout(title=input_hospital_name + ' (' + output_hospital_name + ')', 
                    title_font=dict(size=18,
                               color='darkslategray',
                               family='Times New Roman'))
  fig.update_yaxes(title = 'Operating Income ($)')
  fig.update_xaxes(title = 'Year')
  os.makedirs('FinancialFigures', exist_ok = True)    
  os.makedirs(os.path.join('FinancialFigures', output_hospital_name), exist_ok = True)    
  fig.write_html(os.path.join('FinancialFigures', output_hospital_name, 'operating_income.html'))

def plot_op_income_small(this_hospital_financial_data, payment_types, plot_colors, input_hospital_name, output_hospital_name):
  
  plot_index = pd.to_datetime(this_hospital_financial_data['Fiscal Year Ending'])
  total_patients = np.zeros(len(plot_index))

  fig = make_subplots()
  running_tot_op_inc = np.zeros(len(plot_index))
  for trc_cnt, trace_fill in enumerate(payment_types):
    op_inc_vals = np.asarray(this_hospital_financial_data[trace_fill].replace('.', 0.0).astype(float).fillna(0.0))
    for plt_cnt, idx in enumerate(plot_index):      
      if trc_cnt < 2:
        running_tot_op_inc[plt_cnt] -= op_inc_vals[plt_cnt]
      else:
        running_tot_op_inc[plt_cnt] += op_inc_vals[plt_cnt]
  fig.add_trace(go.Scatter(x=plot_index, y=running_tot_op_inc, name='Total Operating Income',
                    mode ='lines', showlegend = False))
  fig.update_layout(title=output_hospital_name)
  fig.update_yaxes(title = 'Operating Income ($)')
  fig.update_xaxes(title = 'Year')
  os.makedirs('FinancialFigures', exist_ok = True)    
  os.makedirs(os.path.join('FinancialFigures', output_hospital_name), exist_ok = True)    
  fig.write_html(os.path.join('FinancialFigures', output_hospital_name, 'operating_income_small.html'), include_plotlyjs='cdn')

def plot_patient_mix_small(this_hospital_financial_data, payment_types, plot_colors, input_hospital_name, output_hospital_name):
  plot_index = pd.to_datetime(this_hospital_financial_data['Fiscal Year Ending'])
  total_patients = np.zeros(len(plot_index))

  fig = make_subplots()
  for trc_cnt, trace_fill in enumerate(payment_types):
    if trc_cnt == 0:
      fill_type = 'tozeroy'
    else:
      fill_type = 'tonexty'
      
    patient_mix_vals = this_hospital_financial_data[trace_fill].replace('.', 0.0).astype(float).fillna(0.0)  
    total_patients += np.asarray(patient_mix_vals)
    label_name = trace_fill.replace(' Payer Mix', '')
    if len(label_name) > 20:
       label_name = label_name[:20]
       
    fig.add_trace(go.Scatter(x=plot_index, y=total_patients, name=label_name,
                          fill = fill_type, mode ='lines', fillcolor = plot_colors[trc_cnt]))
                          
  fig.update_layout(title=output_hospital_name)
  fig.update_yaxes(title = 'Patient Mix (%)')
  fig.update_xaxes(title = 'Year')
  os.makedirs('FinancialFigures', exist_ok = True)    
  os.makedirs(os.path.join('FinancialFigures', output_hospital_name), exist_ok = True)    
  fig.write_html(os.path.join('FinancialFigures', output_hospital_name, 'patient_mix_small.html'))
