# Shopping Mall Sales Dashboard

This is a Streamlit-based dashboard for analyzing sales data from shopping malls.

## Prerequisites

- Python 3.8 or higher
- Required packages: streamlit, pandas, plotly

## Installation

1. Install Python from [python.org](https://www.python.org/downloads/) or Microsoft Store.

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Running the Dashboard

1. Ensure `data.json` and `dashboard.py` are in the same directory.

2. Run the Streamlit app:
   ```
   streamlit run dashboard.py
   ```

3. Open the provided URL in your browser (usually http://localhost:8501).

## Features

- **Key Performance Indicators (KPIs)**: Total sales, transactions, average order value, unique customers, total items sold.
- **Interactive Filters**: Date range, categories, shopping malls, gender, payment methods, age groups.
- **Visualizations**:
  - Sales by category (bar chart)
  - Sales by shopping mall (bar chart)
  - Monthly sales trend (line chart)
  - Payment method distribution (pie chart)
  - Sales by gender (bar chart)
  - Sales by age group (bar chart)
- **Data Table**: View filtered data (first 100 rows).

## Data

The dashboard uses `data.json` which contains invoice data with fields:
- invoice_no
- customer_id
- gender
- age
- category
- quantity
- total_price
- payment_method
- invoice_date
- shopping_mall

## Notes

- The dashboard is robust and handles data filtering efficiently.
- All visualizations are interactive and update based on selected filters.
- Data is cached for better performance.