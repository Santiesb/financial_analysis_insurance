import streamlit as st
import sys
import os
from scipy.special import expit  # For logistic growth
# Add the docs/financial_analysis directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'docs', 'financial_analysis'))

import helper_functions as hf
import assumptions_config as ac
import elements_streamlit as elements

##### NEEDED:
# If there is no investment, the costs are 0 per month, ROI is 100% the costs cannot be the same in a model where 
# the chatbot is implemented and other where it is not

# Set the page layout to wide
st.set_page_config(layout="wide")

# ---------------- Streamlit Application ----------------

# In main flow:
st.sidebar.header("Configuración de los escenarios")

# Time frame outside scenarios for shared configuration
years = ac.scenario_timeframe()

# Create collapsible scenario configurations
st.sidebar.subheader("Escenario 1")
assumptions1 = elements.create_scenario_config("Escenario 1")
st.sidebar.subheader("Escenario 2")
assumptions2 = elements.create_scenario_config("Escenario 2")

# Create DataFrames
df1 = hf.calculate_financials(years, assumptions1)
df2 = hf.calculate_financials(years, assumptions2)

# ---------------- Visualization ----------------

# Header with image
st.header("Análisis de sensibilidad de la implementación de Paco")

# Scenario Metrics Comparison
st.subheader("Comparación de Métricas de Escenarios")
elements.scenario_metrics_comparison(df1, df2)

# Scenario Comparison
st.subheader("Comparación de Escenarios")
elements.scenario_comparison(df1, df2)

# Cumulative Profit Contribution
st.subheader("Contribución Acumulada al Beneficio")
elements.cumulative_profit_contribution(df1, df2)

# Assumptions Comparison Table
st.subheader("Tabla de Comparación de Supuestos")
elements.assumptions_comparison_table(assumptions1, assumptions2)