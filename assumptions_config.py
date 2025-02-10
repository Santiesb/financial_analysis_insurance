import streamlit as st
# ---------------- Asumptions Input ----------------

def scenario_timeframe():
    """
    Sidebar widget to select the scenario time frame.
    """
    return st.sidebar.slider("Scenario Time Frame (Years)", 2, 10, 6)

def input_assumptions(scenario_name):
    """
    Configures assumptions for the given scenario. Assumptions are split into:
    - Fixed Assumptions: These remain constant and are based on historical or known company data.
    - Dynamic Assumptions: These are user-configurable and allow scenario customization.

    Args:
        scenario_name (str): The name of the scenario (e.g., "Scenario 1", "Scenario 2").

    Returns:
        dict: A dictionary of all assumptions for the given scenario.
    """
    

    # Dynamic Assumptions: User-configurable values

    perc_estimated_current_conversion = st.sidebar.number_input(
        f"{scenario_name} - Current Conversion Rate (%)",
        min_value=0.001,
        max_value=0.025,
        value=0.005,
        format="%.3f"  # Formato con 2 decimales
    )
    avg_telephone_cost_per_interaction = st.sidebar.number_input(
        f"{scenario_name} - Average Telephone Cost per Interaction (€)",
        value=1.5  # Default: €1.5 per phone interaction.
    )  # Average cost of a customer interaction via telephone.

    avg_chatbot_cost_per_interaction = st.sidebar.slider(
        f"{scenario_name} - Average Chatbot Cost Decrease per Interaction (%)",
        0.0, 0.6, 0.3  # Range: 0% to 100%, Default: 30%.  ### MEDIA DE LLAMADAS POR INTERACCION DE USUARIO 6/7--> CALCULAR CUANTAS INTERACCIONES SON NECESARIAS CON EL CHATBOT
    )  # Percentage cost reduction of chatbot vs. telephone interactions.

    insurance_company_avg_policy_price = st.sidebar.number_input(
        f"{scenario_name} - insurance_company Avg. Policy Value (€)",
        value=60  # Default: €70 per health insurance policy. TBC Maria
    )  # Average annual revenue generated per health insurance policy.

    # Return a dictionary of assumptions

    return {
        # Fixed Assumptions: Derived from company data and historical benchmarks
        # "years": scenario_timeframe(),  # Timeframe for the analysis, defined elsewhere.
        "initial_insurance_company_health_policies": 2_000_000,  # Starting insurance policies at the end of 2024 (from insurance_company investors report). TBC Maria
        "avg_contacts_phone_web_daily": 3_500,  # Average daily customer interactions (phone + web). AKA cotizaciones
        "nps_increase": 0.02,  # 2% improvement in retention from NPS enhancement.
        "nps_diminishing_rate": 0.01,  # 1% annual decline in the effect of NPS improvement.
        "economies_scale_cost_factor": 0.03,  # 3% annual efficiency gain due to economies of scale.
        "first_year_costs": 680_000 + 250_000 + 100_000,  # Total initial implementation costs:
        # - Design & implementation: €680k
        # - Database configuration & integration: €250k
        # - Testing: €100k
        "recurring_monthly_costs": 80_000,  # Monthly infrastructure costs after implementation. LLAMADAS API CHATBOT
        "conversion_increase": 0.005,  # Annual improvement in conversion rate (0.05%).
        "max_conversion_rate": 0.03,  # Maximum achievable conversion rate (3%).
        "discount_rate": 0.05,  # Discount rate for financial projections (5%).

        "avg_market_policy_price": 60,  # Base value of current health insurance policy (€60). TBC Maria
        "price_elasticity": 0.7,  # Price elasticity of demand for insurance policies (0.5).

        "initial_phone_rate": 0.6,
        "initial_web_rate": 1 - 0.6 - 0.05,
        "initial_chatbot_rate": 0.05, # Initial chatbot handling rate (%).
        
        "phone_decrease_rate": 0.02,
        "web_decrease_rate": -0.02,
        "chatbot_increase_rate": 0.05,
        # Dynamic Assumptions: Configurable by the user
          # perc_contacts_handled_by_chatbot_initial,  
        "insurance_company_avg_policy_price": insurance_company_avg_policy_price,  # Average annual revenue per policy (€).
        "health_insurance_yearly_company_growth_rate": 0.095,  # Company growth rate (%).
        "perc_estimated_current_conversion": perc_estimated_current_conversion,  # Initial conversion rate (%).
        "avg_telephone_cost_per_interaction": avg_telephone_cost_per_interaction,  # Cost per phone interaction (€).
        "avg_chatbot_cost_per_interaction": avg_chatbot_cost_per_interaction  # Cost per chatbot interaction (€).
    }