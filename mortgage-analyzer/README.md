# Mortgage Analyzer

A comprehensive Streamlit application for analyzing current mortgages and comparing both refinance and new purchase scenarios with intelligent recommendations and break-even analysis.

All of the visualization code was written by Claude AI. This was a learning project for me to understand OOP and Streamlit better, with no desire to spend time learning Python visualizations from scratch.

## Features

### 🏠 Current Mortgage Analysis
- Input existing mortgage details and track current equity position
- Calculate remaining payments and loan timeline
- Track PMI requirements and removal timeline

### 🆕 New Purchase Scenarios
- Compare potential new home purchases against current mortgage
- Calculate down payment requirements and closing costs
- Analyze monthly payment changes and equity implications

### 🔄 Refinance Analysis
- **Rate-and-term refinancing** with break-even calculations
- **Cash-out refinancing** with net proceeds after closing costs
- LTV-based PMI calculations and removal timelines
- Intelligent recommendations based on savings and payback periods

### 📊 Advanced Comparisons
- Side-by-side scenario comparisons with professional formatting
- Break-even analysis for refinancing decisions
- Comprehensive visualizations including amortization schedules
- Scenario-specific recommendations and considerations

## Data Flow

1. **Current Mortgage Setup**: Input existing mortgage details in "💸 Current Mortgage"
2. **Scenario Creation**: Create refinance or purchase scenarios in "🆕 New Scenario" 
3. **Intelligent Analysis**: Compare scenarios with break-even analysis in "📈 Comparison"
4. **Professional Recommendations**: Get scenario-specific advice and considerations
5. **Detailed Visualizations**: Explore amortization schedules, equity growth, and payment breakdowns

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
│   │   └── mortgage_classes.py     # Core mortgage classes (CurrentMortgage, NewMortgageScenario, RefinanceScenario)
│   ├── utils/                      
│   │   ├── mortgage_utils.py       # Data persistence and calculation utilities for all mortgage types
│   │   ├── navigation_utils.py     # Page navigation and session management
│   │   └── session_utils.py        # Session state initialization and management
│   └── visualizations/             
│       └── mortgage_charts.py      # Comprehensive charting and visualization functions
├── app/                 
│   ├── pages/                      # Multi-page Streamlit application
│   │   ├── 00_🏡_Home_Page_(pun_intended).py  # Welcome page and app navigation
│   │   ├── 01_💸_Current_Mortgage.py          # Current mortgage input and analysis
│   │   ├── 02_🆕_New_Scenario.py              # New purchase and refinance scenario creation
│   │   └── 03_📈_Comparison.py                # Advanced scenario comparison and recommendations
│   └── home_page.py                # Application entry point
├── requirements.txt                # Project dependencies
└── README.md                       # Project documentation
```

## Technical Implementation

### Core Architecture
- **Object-Oriented Design**: Three main mortgage classes with proper inheritance and validation
- **State Management**: Persistent session state across page navigation
- **Modular Structure**: Separated concerns for models, utilities, and visualizations

### Key Classes
- **`CurrentMortgage`**: Represents existing mortgage with age calculations and equity tracking
- **`NewMortgageScenario`**: New purchase scenarios with down payment and PMI calculations  
- **`RefinanceScenario`**: Refinancing scenarios with LTV analysis and cash-out support

### Advanced Features
- **Break-Even Analysis**: Calculates months to recoup refinancing costs
- **PMI Intelligence**: Automatic PMI calculations based on loan-to-value ratios
- **Currency Formatting**: Professional financial formatting throughout the application
- **Scenario Flexibility**: Supports both rate-and-term and cash-out refinancing

## Future Enhancements

### Potential Additions
- **ARM Analysis**: Support for adjustable-rate mortgages
- **Tax Calculator**: Integration with mortgage interest deduction scenarios
- **Market Data**: Real-time interest rate integration
- **Export Features**: PDF reports and data export capabilities
- **Mobile Optimization**: Enhanced responsive design for mobile devices

### Technical Improvements
- **Database Integration**: Persistent data storage beyond session state
- **User Authentication**: Multi-user support with saved scenarios
- **API Integration**: Real estate and mortgage rate data feeds
