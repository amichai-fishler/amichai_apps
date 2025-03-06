import streamlit as st
import pandas as pd


def is_positive_number(value):
    try:
        # Remove commas from the input
        value = value.replace(",", "")
        # Convert the input to a float
        number = float(value)
        # Check if the number is positive
        return number > 0
    except ValueError:
        return False


# Constants
SCRAPE_CONSUMPTION = 0.00019
REDIRECT_CONSUMPTION = 0.0017
GB_COST_DICT = {'IP Royal': 3.15, 'Proxy Empire': 0.55, 'Proxy Seller': 1.0}
# Calculated based on all production data for the date range Feb 20th - Feb 26th 2025
IMPERSONATORS_SHARE = 0.08
COMPETITORS_SHARE = 0.50
OFFICIAL_SHARE = 0.25

st.write("""
# Quota Calculations
""")

# Inputs
total_monthly_cost = st.text_input("What is the monthly revenue from the organization:")
if not is_positive_number(total_monthly_cost):
    st.write(f"The monthly revenue must be positive number. You entered '{total_monthly_cost}'")

scraping_proxy_provider = st.selectbox('Which Proxy Provider will be used for Scraping?',
                                       ('IP Royal', 'Proxy Empire', 'Proxy Seller'))
redirect_proxy_provider = st.selectbox('Which Proxy Provider will be used for Redirect Scraping?',
                                       ('IP Royal', 'Proxy Empire', 'Proxy Seller'))

official_click_share = st.slider("What share of official ads will be clicked?", 0, 100, 10) / 100
competitor_click_share = st.slider("What share of competitor ads will be clicked?", 0, 100, 10) / 100

# Output
if is_positive_number(total_monthly_cost):
    # Daily cost should be up to 5% from daily revenue
    daily_cost = (1 / 30) * 0.05 *  float(total_monthly_cost.replace(",", ""))
    coefficient = (SCRAPE_CONSUMPTION * GB_COST_DICT[scraping_proxy_provider]) + (
            REDIRECT_CONSUMPTION * GB_COST_DICT[redirect_proxy_provider] * (
            IMPERSONATORS_SHARE + COMPETITORS_SHARE * competitor_click_share + OFFICIAL_SHARE * official_click_share))
    quota = daily_cost / coefficient
    st.write(f"The Daily Quota Should Be '{int(quota):,}'")


