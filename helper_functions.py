import numpy as np
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# ---------------- Helper Functions ----------------

def logistic_growth(time_period, initial_value, rate_of_growth, max_value=1.0, midpoint=5):
    """
    Calculate logistic growth for a given time period.
    
    Parameters:
    time_period (int): The time period (e.g., year) for the growth calculation.
    initial_value (float): The initial value at the start of the time period.
    rate_of_growth (float): The rate at which the value grows over time.
    max_value (float): The maximum value that can be reached (carrying capacity).
    midpoint (int): The midpoint of the logistic function where the growth is most rapid.

    Returns:
    float: The value after applying logistic growth.
    """
    return max_value / (1 + np.exp(-rate_of_growth * (time_period - midpoint))) + initial_value

def calculate_chatbot_adoption_rate(time_period, initial_adoption_rate, adoption_growth_rate):
    """
    Calculate the chatbot adoption rate using logistic growth.
    
    Parameters:
    time_period (int): The time period (e.g., year) for the growth calculation.
    initial_adoption_rate (float): The initial rate of chatbot adoption.
    adoption_growth_rate (float): The annual growth rate of chatbot adoption.

    Returns:
    float: The chatbot adoption rate after applying logistic growth.
    """
    return logistic_growth(time_period, 
                           initial_adoption_rate, # Initial adoption % of contacts handled by the chatbot
                           adoption_growth_rate,
                           max_value=1,
                           midpoint=10) ## Should this be the max that the chatbot can handle?

def calculate_growth_factor(time_period, initial_growth_value, growth_rate, max_growth_value=0.3):
    """
    Calculate the growth factor using logistic growth.
    
    Parameters:
    time_period (int): The time period (e.g., year) for the growth calculation.
    initial_growth_value (float): The initial growth value at the start of the time period.
    growth_rate (float): The rate at which the growth value increases over time.
    max_growth_value (float): The maximum growth value that can be reached.

    Returns:
    float: The growth factor after applying logistic growth.
    """
    return logistic_growth(time_period, 
                           initial_growth_value,
                           growth_rate,
                           max_growth_value)

def adjust_total_contacts(total_contacts, growth_adjustment, max_growth_value):
    """
    Adjust the total contacts based on the growth adjustment.
    
    Parameters:
    total_contacts (int): The initial number of total contacts.
    growth_adjustment (float): The growth adjustment factor to be applied.
    max_growth_value (float): The maximum growth value that can be reached.

    Returns:
    int: The adjusted total contacts.
    """
    adjusted_contacts = total_contacts * (1 + growth_adjustment)
    return min(adjusted_contacts, total_contacts * (1 + max_growth_value))

def calculate_contacts(initial_contacts, 
                       initial_phone_rate, 
                       initial_web_rate,
                       initial_chatbot_rate,
                       phone_decrease_rate,
                       web_decrease_rate, 
                       chatbot_increase_rate, 
                       time_period, 
                       initial_growth_value=0.01, 
                       growth_rate=0.01, 
                       max_growth_value=0.2):
    """
    Calculate total contact volume handled by phone, web, and chatbot.
    
    Parameters:
    initial_contacts (int): Total annual phone/web contacts.
    initial_phone_rate (float): Initial rate of phone contacts.
    initial_web_rate (float): Initial rate of web contacts.
    initial_chatbot_rate (float): Initial rate of chatbot contacts.
    phone_decrease_rate (float): Annual decrease rate of phone contacts.
    web_decrease_rate (float): Annual decrease rate of web contacts.
    chatbot_increase_rate (float): Annual increase rate of chatbot contacts.
    time_period (int): Current year in the projection.
    initial_growth_value (float): Initial growth value for total contacts.
    growth_rate (float): Rate of growth for the linear model.
    max_growth_value (float): Maximum growth value for total contacts.

    Returns:
    tuple: Total contacts handled, phone contacts, web contacts, and chatbot contacts.
    """
    # Adjust total contacts based on growth factor
    total_contacts = adjust_total_contacts(initial_contacts, initial_growth_value + growth_rate * time_period, max_growth_value)
    
    # Calculate linear growth for each type of contact
    chatbot_rate = min(initial_chatbot_rate + chatbot_increase_rate * time_period, 1.0)
    web_rate = max(initial_web_rate - web_decrease_rate * time_period, 0.0)
    phone_rate = max(initial_phone_rate - phone_decrease_rate * time_period, 0.0)
    
    # Ensure the sum of the rates does not exceed 100%
    total_rate = chatbot_rate + web_rate + phone_rate
    if total_rate > 1.0:
        chatbot_rate /= total_rate
        web_rate /= total_rate
        phone_rate /= total_rate
    
    # Calculate the number of contacts for each type
    chatbot_contacts = total_contacts * chatbot_rate
    web_contacts = total_contacts * web_rate
    phone_contacts = total_contacts * phone_rate
    
    return total_contacts, phone_contacts, web_contacts, chatbot_contacts

def calculate_new_customers(total_contacts, conversion_rate, avg_market_policy_price, insurance_company_avg_policy_price, price_elasticity):
    """
    Calculate the number of new customers, adjusted for price sensitivity.
    - total_contacts: Total number of contacts.
    - conversion_rate: Conversion rate of contacts to customers.
    - avg_market_policy_price: Current average market policy price. AVG. MARKET
    - insurance_company_avg_policy_price: insurance_company policy price for comparison. insurance_company
    - price_elasticity: Price elasticity factor.

    Returns the adjusted number of new customers.
    """
    price_adjustment_factor = (avg_market_policy_price / insurance_company_avg_policy_price) ** price_elasticity
    new_customers = total_contacts * conversion_rate * price_adjustment_factor
    return new_customers

def calculate_retention_profit(new_customers, initial_insurance_company_health_policies, nps_increase, nps_diminishing_rate, year, insurance_company_avg_policy_price):
    """
    Calculate profit from customer retention improvements due to NPS increase.
    - new_customers: Number of new customers acquired in the year.
    - initial_insurance_company_health_policies: Total existing policies at the start of the year.
    - nps_increase: Percentage increase in retention due to NPS improvement.
    - nps_diminishing_rate: Annual rate at which the NPS effect diminishes.
    - year: Current year in the projection.
    - insurance_company_avg_policy_price: Average annual revenue per policy.

    Returns the revenue generated from retained customers.
    """
    retention_effect = nps_increase * (1 - (year * nps_diminishing_rate))
    retention_effect = retention_effect # max(retention_effect, 0)  # Ensure retention effect doesn't drop below 0.
    retained_customers = initial_insurance_company_health_policies * retention_effect + new_customers * retention_effect
    return retained_customers * insurance_company_avg_policy_price

def calculate_chatbot_savings(contact_volume, phone_cost, chatbot_cut_cost):
    """
    Calculate savings from replacing phone interactions with chatbot interactions.
    - contact_volume: Total number of contacts handled.
    - phone_cost: Cost per phone interaction.
    - chatbot_cut_cost: Percentage cost reduction per chatbot interaction compared to phone.

    Returns the total savings achieved.
    """
    savings_per_contact = phone_cost - (phone_cost * (1 - chatbot_cut_cost))
    savings_per_contact = max(savings_per_contact, 0)  # Ensure savings are non-negative.
    return contact_volume * savings_per_contact

def diminishing_conversion_rate(base_rate, increase_rate, year, max_rate):
    """
    Model diminishing returns for conversion rate improvements over time.
    - base_rate: Initial conversion rate.
    - increase_rate: Annual improvement in conversion rate.
    - year: Current year in the projection.
    - max_rate: Maximum achievable conversion rate.

    Returns the conversion rate for the given year.
    """
    return min(base_rate + (increase_rate / (1 + 0 * year)), max_rate)

def calculate_costs(yearly_recurrent_cost, economies_scale_cost_factor, year):
    """
    Calculate costs with economies of scale applied over time.
    - yearly_recurrent_cost: Initial annual cost.
    - economies_scale_cost_factor: Annual cost reduction due to economies of scale.
    - year: Current year in the projection.

    Returns the adjusted cost for the year.
    """
    return yearly_recurrent_cost / (1 + economies_scale_cost_factor * year)

def calculate_financials(time_period, assumptions, no_implementation=False):
    """
    Main function to calculate financial projections for the given time frame and assumptions.
    - time_period: Number of years in the projection.
    - assumptions: Dictionary containing all model assumptions.

    Returns a DataFrame with yearly financial metrics.
    """
    rows = []
    cumulative_costs = 0
    cumulative_profit = 0

    insurance_company_avg_policy_price = assumptions["insurance_company_avg_policy_price"]  # insurance_company policy price for comparison
    avg_market_policy_price = assumptions["avg_market_policy_price"]  # Average market policy price
    price_elasticity = assumptions["price_elasticity"]  # Default price elasticity factor

    for year in range(time_period + 1):
        if no_implementation:
            # If no implementation, set chatbot-related values to zero
            total_contacts = assumptions["avg_contacts_phone_web_daily"] * 365
            phone_contacts = total_contacts * assumptions["initial_phone_rate"]
            web_contacts = total_contacts * assumptions["initial_web_rate"]
            chatbot_contacts = 0
        
        else:
            # Calculate total contact volume (phone, web, and chatbot)
            total_contacts, phone_contacts, web_contacts, chatbot_contacts = calculate_contacts(
                assumptions["avg_contacts_phone_web_daily"] * 365,
                assumptions["initial_phone_rate"],
                assumptions["initial_web_rate"],
                assumptions["initial_chatbot_rate"],
                assumptions["phone_decrease_rate"],
                assumptions["web_decrease_rate"],
                assumptions["chatbot_increase_rate"],
                year,
                initial_growth_value=0.0,  # Grow from the base contacts
                growth_rate=0.01,           # 1% annually
                max_growth_value=year/100       # Until the max year selected
            )
            
            # Calculate the conversion rate with diminishing returns
            conversion_rate = diminishing_conversion_rate(
                assumptions["perc_estimated_current_conversion"],
                assumptions["conversion_increase"],
                year,
                assumptions["max_conversion_rate"]
            )
            
            # Calculate new customers from total contacts and conversion rate
            new_customers = calculate_new_customers(
                total_contacts,
                conversion_rate,
                avg_market_policy_price,
                insurance_company_avg_policy_price,
                price_elasticity
            )

            # Calculate retention profit
            retention_profit = calculate_retention_profit(
                new_customers = new_customers,
                initial_insurance_company_health_policies = assumptions["initial_insurance_company_health_policies"],
                nps_increase = assumptions["nps_increase"],
                nps_diminishing_rate=assumptions["nps_diminishing_rate"],
                year = year,
                insurance_company_avg_policy_price = insurance_company_avg_policy_price
            )

            # Calculate savings from chatbot adoption
            chatbot_savings = calculate_chatbot_savings(
                total_contacts,
                assumptions["avg_telephone_cost_per_interaction"],
                assumptions["avg_chatbot_cost_per_interaction"]
            ) if not no_implementation else 0


            # Calculate costs, including economies of scale
            costs = calculate_costs(
                assumptions["recurring_monthly_costs"] * 12,
                assumptions["economies_scale_cost_factor"],
                year
            )
            if year == 0:
                costs += assumptions["first_year_costs"]  # Add one-time implementation costs in Year 0.

            # Calculate net profit and cumulative values
            net_profit = retention_profit + chatbot_savings - costs
            cumulative_costs += costs
            cumulative_profit += net_profit

            # Append yearly metrics to the results
            rows.append({
                "Year": year,
                "Total Contacts (M)": total_contacts / 1_000_000,
                "Phone Contacts (M)": phone_contacts / 1_000_000,
                "Web Contacts (M)": web_contacts / 1_000_000,
                "Chatbot Contacts (M)": chatbot_contacts / 1_000_000,
                "New Customers (M)": new_customers / 1_000_000,
                "Retention Profit (€M)": retention_profit / 1_000_000,
                "Chatbot Savings (€M)": chatbot_savings / 1_000_000,
                "Costs (€M)": costs / 1_000_000,
                "Net Profit (€M)": net_profit / 1_000_000,
                "Cumulative Costs (€M)": cumulative_costs / 1_000_000,
                "Cumulative Profit (€M)": cumulative_profit / 1_000_000,
                "ROI (%)": (cumulative_profit / cumulative_costs * 100) if cumulative_costs > 0 else 0
    })

    return pd.DataFrame(rows)

# ---------------- Validation Functions ----------------



# Calculate the maximum y-axis limit across both scenarios
def calculate_max_y_limit(df1, df2):
    max_y1 = df1[["New Customers (M)", "Retention Profit (€M)", "Chatbot Savings (€M)", "Costs (€M)"]].sum().max()
    max_y2 = df2[["New Customers (M)", "Retention Profit (€M)", "Chatbot Savings (€M)", "Costs (€M)"]].sum().max()
    return max(max_y1, max_y2) * 1.1