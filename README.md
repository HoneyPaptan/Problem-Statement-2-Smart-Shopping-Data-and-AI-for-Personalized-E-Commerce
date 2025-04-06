# E-commerce Recommendation System

This project implements a multi-agent system for personalized product recommendations in an e-commerce context using Streamlit, Python, and SQLite.

## Project Structure

```
e-commerce-recommendation-system/
├── customer_data_collection.csv     # Customer data
├── product_recommendation_data.csv  # Product catalog
├── agents/
│   ├── __init__.py
│   ├── customer_agent.py            # Agent for retrieving customer data
│   ├── product_agent.py             # Agent for managing product data
│   └── recommendation_agent.py      # Agent for generating recommendations
├── database/
│   └── db_manager.py                # SQLite database manager
├── app.py                          # Streamlit application
├── main.py                         # Setup script
└── requirements.txt                # Python dependencies
```

## Setup Instructions

1. Make sure the data files are present:
   - `customer_data_collection.csv`: Contains customer data
   - `product_recommendation_data.csv`: Contains product data

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the setup script:
   ```
   python main.py
   ```

4. Run the Streamlit application:
   ```
   streamlit run app.py
   ```

## System Components

### Agents

- **Customer Agent**: Retrieves customer data including browsing and purchase history
- **Product Agent**: Manages product catalog data and provides access methods
- **Recommendation Agent**: Generates personalized recommendations based on customer data

### Database

- SQLite database for caching recommendations
- Stores customer_id, recommendations, and timestamp

### Streamlit Interface

- Simple UI for entering customer ID and displaying recommendations
- Shows whether recommendations were retrieved from cache or freshly generated

## Usage

1. Enter a customer ID in the text input field
2. Click "Get Recommendations"
3. View the top 10 recommended products