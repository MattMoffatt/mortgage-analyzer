# Mortgage Analyzer

A Streamlit application for analyzing current mortgages and comparing refinance or new purchase scenarios.

All of the visualization code was written by Claude AI. This was a learning project for me to understand OOP
and streamlit better and I had no desire to also spend the time to learn how to build python visualizations.

## Data Flow

1. Users input their current mortgage details in the "💸 Current Mortgage" page
2. Users create a new mortgage scenario (refinance option coming) in the "🆕 New Scenario" page
3. The "📈 Comparison" page analyzes and visualizes the differences between the current mortgage and the new scenario
4. All mortgage calculations are handled by the core classes in `src/models/`

## How to run app

1. Clone or fork the repo in your desired location
2. Create a virtual environment for your project and install the necessary dependencies with
```bash
pip install -r requirements.txt
```
3. Either navigate into the `app/` directory and run in your terminal

```bash
streamlit run home_page.py
```

Or, in the `mortgage-analyzer/` directory run

```bash
streamlit run app/home_page.py
```

This will open the app in a webpage on an available local host

4. To quit the app from the terminal, hit 'Ctrl + C' or just exit the webpage and close the terminal

## Directory Structure

```
mortgage-analyzer/
├── src/                 
│   ├── models/                     
│   │   └── mortgage_classes.py     # Core mortgage calculation classes
│   ├── utils/                      
|   |   ├── mortgage_utils.py       # Helper functions for the current and new mortgage pages
|   |   ├── navigation_utils.py     # Helper functions for page navigation functionality
│   │   └── session_utils.py        # Helper functions for general session state handling
│   └── visualizations/             
│       └── mortgage_charts.py      # Chart building functions - solely coded by Claude AI
├── app/                 
│   ├── pages/                      # Individual pages of the multi-page app
│   │   ├── 01_💸_Current_Mortgage.py  # Input current mortgage details and run calculations
│   │   ├── 02_🆕_New_Scenario.py      # Input new mortgage details and run calculations (refi options will be added later)
│   │   └── 03_📈_Comparison.py        # Visualize comparisons between the current mortgage and new mortgage
│   └── home_page.py                # Application entry point
├── requirements.txt                # Project dependencies
└── README.md                       # Project documentation
```

## Future Additions/Updates

* "🆕 New Scenario" page:
    - add "Refinance" tab widgets and calculation code

* "📈 Comparison" page:
    - Refactor comparison calculation logic to effectively evaluate Refinance opportunities vs. new purchases
