import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd


def plot_waterfall(scenario_df, scenario_name, y_max):
    components = {
        "New Customers": scenario_df["New Customers (M)"].sum(),
        "Retention": scenario_df["Retention Profit (€M)"].sum(),
        "Savings": scenario_df["Chatbot Savings (€M)"].sum(),
        "Costs": -scenario_df["Costs (€M)"].sum()
    }

    labels = list(components.keys())
    values = list(components.values())
    cumulative = np.cumsum(values)

    fig, ax = plt.subplots(figsize=(12, 6))  # Adjusted figsize for better width

    # Custom red tones
    colors = ["#FF9999", "#FF6666", "#FF3333", "#FF0000"]

    # Plot bars
    for i, (label, value) in enumerate(zip(labels, values)):
        start = cumulative[i] - value if i > 0 else 0
        ax.bar(label, value, bottom=start, color=colors[i])
        ax.text(i, 
                1, 
                f"{value:.1f}M", 
                ha="center", 
                color="red" if value < 0 else "black", 
                fontsize=12)
        if value < 0:
            ax.text(i, 
                    start, 
                    f"{cumulative[i]:.1f}M", 
                    ha="center", 
                    va="baseline", 
                    color="black", 
                    fontweight="bold", 
                    fontsize=12)
        else:
            ax.text(i, 
                    start + value, 
                    f"{cumulative[i]:.1f}M", 
                    ha="center", 
                    va="bottom", 
                    color="black", 
                    fontweight="bold", 
                    fontsize=12)

    # Remove the box around the plot
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    # Set y-axis limits to ensure all columns fit within the chart
    ax.set_ylim(0, y_max +  y_max)

    # Remove y-axis values
    ax.set_yticklabels([])
    ax.yaxis.set_ticks([])

    # Adjust the layout to make sure everything fits
    plt.tight_layout()
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.2)  # Adjust the padding as needed

    # Set x-axis label size
    ax.tick_params(axis='x', labelsize=18)

    ax.set_ylabel("Cumulative Profit Contribution (€M)", fontsize=15)
    st.pyplot(fig)


def compare_assumptions(assumptions1, assumptions2):
    categories = {
        "Costes de implementación": ["first_year_costs", "recurring_monthly_costs"],
        "Negocio": ["initial_mapfre_health_policies", "avg_contacts_phone_web_daily", "health_insurance_yearly_company_growth_rate", "perc_estimated_current_conversion", "conversion_increase", "max_conversion_rate"],  
        "Retencion": ["nps_increase"],
        "Financiero y Costes": ["mapfre_avg_policy_price", "discount_rate", "avg_telephone_cost_per_interaction", "avg_chatbot_cost_per_interaction", "perc_contacts_handled_by_chatbot_initial", "perc_contacts_handled_by_chatbot_growth"]
    }

    absolute_keys = {
        "initial_mapfre_health_policies": "Pólizas de salud de Mapfre a 2024",
        "avg_contacts_phone_web_daily": "Interacciones diarias promedio (teléfono + web)"
        }
    
    percentage_keys = {
        "health_insurance_yearly_company_growth_rate": "Tasa de crecimiento anual de Mapfre",
        "perc_estimated_current_conversion": "Porcentaje estimado de conversión actual",
        "avg_chatbot_cost_per_interaction": "Porcentaje de abaratamiento de costes interacciones del chatbot",
        "conversion_increase": "Incremento de conversión anual",
        "max_conversion_rate": "Tasa máxima de conversión potencialmente alcanzable",
        "perc_contacts_handled_by_chatbot_initial": "Porcentaje de contactos manejados por el chatbot inicialmente",
        "perc_contacts_handled_by_chatbot_growth": "Crecimiento del porcentaje de contactos manejados por el chatbot",
        "nps_increase": "Incremento del NPS a raíz de la implementación",
        "discount_rate": "Tasa de inflación considerada en las proyecciones"
    }

    monetary_big_keys = {
        "first_year_costs": "Costes del primer año (implementación del chatbot)",
        "recurring_monthly_costs": "Costes mensuales recurrentes"
    }

    monetary_small_keys = {
        "avg_telephone_cost_per_interaction": "Costo promedio por interacción telefónica",
        "mapfre_avg_policy_price": "Valor promedio de las pólizas en Mapfre"
    }

    table_data = []
    for category, keys in categories.items():
        for key in keys:
            value1 = assumptions1.get(key)
            value2 = assumptions2.get(key)
            if key in percentage_keys:
                value1 = f"{value1 * 100:.2f}%" if value1 is not None else None
                value2 = f"{value2 * 100:.2f}%" if value2 is not None else None
                assumption_name = percentage_keys[key]
            elif key in monetary_big_keys:
                value1= f"€{value1/1000000 :.2f}M" if value1 is not None else None
                value2= f"€{value2/1000000 :.2f}M" if value2 is not None else None
                assumption_name = monetary_big_keys[key]
            elif key in monetary_small_keys:
                value1= f"€{value1 :.2f}" if value1 is not None else None
                value2= f"€{value2 :.2f}" if value2 is not None else None
                assumption_name = monetary_small_keys[key]
            elif key in absolute_keys:
                value1 = f"{value1:.0f}" if value1 is not None else None
                value2 = f"{value2:.0f}" if value2 is not None else None
                assumption_name = absolute_keys[key]
            else:
                assumption_name = key.replace("_", " ").capitalize()
            table_data.append({
                "Category": category,
                "Assumption": assumption_name,
                "Scenario 1": value1,
                "Scenario 2": value2
            })

    comparison_table = pd.DataFrame(table_data)
    st.dataframe(comparison_table, height=600, width=1200)
