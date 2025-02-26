# Mortgage Analyzer

A Streamlit application for analyzing current mortgages and comparing refinance or new purchase scenarios.

## Data Flow

1. Users input their current mortgage details in the first page
2. Users create one or more new mortgage scenarios in the second page
3. The comparison page analyzes and visualizes the differences between scenarios
4. All mortgage calculations are handled by the core classes in `src/models/`

## Installation

```bash
pip install -r requirements.txt
```

## Directory Structure - including future additions

```
mortgage-analyzer/
├── src/                 # Core application code
│   ├── models/          # Data models and business logic
│   │   └── mortgage_classes.py    # Core mortgage calculation classes
│   ├── utils/           # Utility functions and helpers
│   └── visualizations/  # Chart generation and data visualization
├── app/                 # Streamlit application
│   ├── pages/           # Individual pages of the multi-page app
│   │   ├── 01_current_mortgage.py
│   │   ├── 02_new_scenarios.py
│   │   └── 03_comparison.py
│   └── main.py          # Application entry point
├── requirements.txt     # Project dependencies
└── README.md            # Project documentation
```

## Future Extensibility

The project structure allows for easy addition of:
- New mortgage analysis features
- Additional visualization types
- Extended comparison metrics
- Data export capabilities
