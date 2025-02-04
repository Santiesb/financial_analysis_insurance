import streamlit as st
import altair as alt
import assumptions_config as ac
import visuals as visuals
import helper_functions as hf
import pandas as pd

def create_scenario_config(scenario_name: str):
    """
    Creates a collapsible configuration section for a scenario.

    Parameters:
    scenario_name (str): The name of the scenario.

    Returns:
    dict: Assumptions for the scenario.
    """
    with st.sidebar.expander(f"{scenario_name} Config", expanded=True):
        assumptions = ac.input_assumptions(scenario_name)
        return assumptions
    
def scenario_metrics_comparison(df1, df2):
    """
    Creates the Scenario Metrics Comparison section.

    Parameters:
    df1 (pd.DataFrame): DataFrame for Scenario 1.
    df2 (pd.DataFrame): DataFrame for Scenario 2.
    """
    metrics = st.multiselect("Select Metrics", df1.columns[1:])

    if metrics:
        col1, col2 = st.columns([10, 10])  # Adjust the width ratio as needed

        # Calculate the maximum y-axis limit across both scenarios
        max_y1 = df1[metrics].max().max()
        max_y2 = df2[metrics].max().max()
        y_max = max(max_y1, max_y2) * 1.1

        with col1:
            st.subheader("Scenario 1")
            chart1 = alt.Chart(df1).transform_fold(
                metrics,
                as_=['Metric', 'Value']
            ).mark_line().encode(
                x='Year:Q',
                y=alt.Y('Value:Q', scale=alt.Scale(domain=[0, y_max])),
                color='Metric:N',
                tooltip=['Year:Q', 'Value:Q']
            ).properties(
                height=400,
                width='container'
            ).configure_legend(
                orient='bottom'
            )
            st.altair_chart(chart1, use_container_width=True)

        with col2:
            st.subheader("Scenario 2")
            chart2 = alt.Chart(df2).transform_fold(
                metrics,
                as_=['Metric', 'Value']
            ).mark_line().encode(
                x='Year:Q',
                y=alt.Y('Value:Q', scale=alt.Scale(domain=[0, y_max])),
                color='Metric:N',
                tooltip=['Year:Q', 'Value:Q']
            ).properties(
                height=400,
                width='container'
            ).configure_legend(
                orient='bottom'
            )
            st.altair_chart(chart2, use_container_width=True)

def scenario_comparison(df1, df2):
    """
    Creates the Scenario Comparison section.

    Parameters:
    df1 (pd.DataFrame): DataFrame for Scenario 1.
    df2 (pd.DataFrame): DataFrame for Scenario 2.
    """
    comparison_metric = st.selectbox("Select Metric for Comparison", df1.columns[1:])
    if comparison_metric:
        comparison_df = pd.DataFrame({
            "Year": df1["Year"],
            f"Scenario 1 - {comparison_metric}": df1[comparison_metric],
            f"Scenario 2 - {comparison_metric}": df2[comparison_metric]
        }).set_index("Year")

        # Calculate the maximum y-axis limit for the comparison chart
        max_y_comparison = comparison_df.max().max() * 1.1

        # Create the comparison chart using Altair
        comparison_chart = alt.Chart(comparison_df.reset_index()).transform_fold(
            [f"Scenario 1 - {comparison_metric}", f"Scenario 2 - {comparison_metric}"],
            as_=['Scenario', 'Value']
        ).mark_line().encode(
            x=alt.X('Year:Q', axis=alt.Axis(format='d', title='Year')),
            y=alt.Y('Value:Q', axis=alt.Axis(title=comparison_metric), scale=alt.Scale(domain=[0, max_y_comparison])),
            color='Scenario:N',
            tooltip=['Year:Q', 'Value:Q']
        ).properties(
            height=400,
            width='container'
        )
        st.altair_chart(comparison_chart, use_container_width=True)

def cumulative_profit_contribution(df1, df2):
    """
    Creates the Cumulative Profit Contribution section.

    Parameters:
    df1 (pd.DataFrame): DataFrame for Scenario 1.
    df2 (pd.DataFrame): DataFrame for Scenario 2.
    """
    y_max = hf.calculate_max_y_limit(df1, df2)
    with st.container():
        col1, col2 = st.columns([5, 5])

        with col1:
            st.subheader("Scenario 1")
            visuals.plot_waterfall(df1, "Scenario 1", y_max)

        with col2:
            st.subheader("Scenario 2")
            visuals.plot_waterfall(df2, "Scenario 2", y_max)

def assumptions_comparison_table(assumptions1, assumptions2):
    """
    Creates the Assumptions Comparison Table section.

    Parameters:
    assumptions1 (dict): Assumptions for Scenario 1.
    assumptions2 (dict): Assumptions for Scenario 2.
    """
    with st.container():
        visuals.compare_assumptions(assumptions1, assumptions2)