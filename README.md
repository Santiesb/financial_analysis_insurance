# Financial Analysis for Chatbot Implementation

## Overview
This project evaluates the financial impact of implementing a chatbot in an insurance company (insurance_company). It includes various financial scenarios to analyze cost savings, customer retention, and revenue growth. The analysis is conducted using Streamlit, allowing interactive comparisons between different financial assumptions.

## Features
- Scenario-based financial projections
- Retention and cost savings calculations
- Interactive visualization using Streamlit
- Logistic growth models for chatbot adoption
- Comparison between chatbot implementation and non-implementation scenarios

## Installation
To set up the environment, clone the repository and install the dependencies:

```sh
git clone https://github.com/your-username/financial_analysis_insurance.git
cd financial_analysis_insurance
pip install -r requirements.txt
```

## Running the Application
To launch the Streamlit application, run:

```sh
streamlit run scenario_creator.py
```

## Project Structure
```
financial_analysis/
│-- scenario_creator.py     # Main Streamlit app
│-- assumptions_config.py   # Configuration for financial assumptions
│-- helper_functions.py     # Core financial calculations
│-- visuals.py              # Visualization functions
│-- elements_streamlit.py   # UI elements for Streamlit
│-- requirements.txt        # Dependencies
│-- Dockerfile              # Containerization setup
```

## Deployment on Streamlit Cloud
1. Push the repository to GitHub.
2. Go to [Streamlit Cloud](https://share.streamlit.io/) and log in.
3. Select "New App" and choose your repository.
4. Specify the file to run (`scenario_creator.py`).
5. Click "Deploy" and access the hosted application.

## License
This project is licensed under the MIT License.

## Authors
- **Your Name** - [GitHub](https://github.com/your-username)