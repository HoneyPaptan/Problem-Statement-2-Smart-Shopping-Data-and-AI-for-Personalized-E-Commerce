import streamlit as st
import pandas as pd
import json
import os
import sys

# Import our agents and database manager
from agents.customer_agent import CustomerAgent
from agents.product_agent import ProductAgent
from agents.recommendation_agent import RecommendationAgent
from database.db_manager import DatabaseManager


# Initialize agents and database
@st.cache_resource
def initialize_system():
    db_manager = DatabaseManager()
    customer_agent = CustomerAgent()
    product_agent = ProductAgent()
    recommendation_agent = RecommendationAgent(product_agent)
    return db_manager, customer_agent, product_agent, recommendation_agent


db_manager, customer_agent, product_agent, recommendation_agent = initialize_system(
)

# Set up the Streamlit interface
st.title("E-commerce Recommendation System")
st.subheader("Enter a customer ID to get personalized product recommendations")

# Get a few sample customers for demonstration
try:
    customer_df = pd.read_csv("customer_data_collection.csv")
    sample_customers = customer_df['Customer_ID'].head(4).tolist()
    st.write("Sample Customer IDs for testing:", ", ".join(sample_customers))
except:
    st.write(
        "Unable to load sample customers. Please enter a valid customer ID.")

customer_id = st.text_input("Customer ID", key="customer_id_input")

if st.button("Get Recommendations"):
    if not customer_id:
        st.error("Please enter a Customer ID")
    else:
        with st.spinner("Processing..."):
            # First, check if we have cached recommendations
            recommendations, timestamp = db_manager.get_recommendations(
                customer_id)

            from_cache = False
            if recommendations:
                from_cache = True
                st.success(f"Found cached recommendations from {timestamp}")
            else:
                # Generate new recommendations
                st.info("Generating new recommendations...")

                # Get customer data
                customer_data = customer_agent.get_customer_data(customer_id)

                if not customer_data['found']:
                    st.warning(
                        f"Customer {customer_id} not found in our database. Showing generic recommendations."
                    )

                # Generate recommendations
                recommendations = recommendation_agent.generate_recommendations(
                    customer_data)

                # Save to database
                db_manager.save_recommendations(customer_id, recommendations)

                st.success("New recommendations generated and cached!")

            # Display recommendations
            st.subheader(f"Top 10 Recommended Products for {customer_id}")

            if from_cache:
                st.info("These recommendations were retrieved from cache.")
            else:
                st.info("These are freshly generated recommendations.")

            # Create a DataFrame for display
            if recommendations:
                # Clean up the recommendations data for display
                display_data = []
                for rec in recommendations:
                    # Create a clean record for display, handling both expected formats
                    clean_rec = {}
                    if 'Product_ID' in rec:
                        clean_rec['Product ID'] = rec['Product_ID']
                    if 'product_id' in rec:
                        clean_rec['Product ID'] = rec['product_id']

                    if 'Category' in rec:
                        clean_rec['Category'] = rec['Category']
                    if 'category' in rec:
                        clean_rec['Category'] = rec['category']

                    if 'Subcategory' in rec:
                        clean_rec['Subcategory'] = rec['Subcategory']
                    if 'subcategory' in rec:
                        clean_rec['Subcategory'] = rec['subcategory']

                    if 'Price' in rec:
                        clean_rec['Price'] = f"₹{rec['Price']:,.2f}"
                    if 'price' in rec:
                        clean_rec['Price'] = f"₹{rec['price']:,.2f}"

                    if 'Brand' in rec:
                        clean_rec['Brand'] = rec['Brand']

                    if 'Product_Rating' in rec:
                        clean_rec['Rating'] = rec['Product_Rating']

                    display_data.append(clean_rec)

                recommendations_df = pd.DataFrame(display_data)
                st.table(recommendations_df)
            else:
                st.error("No recommendations found or generated.")

# Add some information about how the system works
with st.expander("How does this system work?"):
    st.write("""
    This recommendation system uses a multi-agent approach to provide personalized product recommendations:

    1. **Customer Agent**: Retrieves customer data including browsing and purchase history
    2. **Product Agent**: Organizes and provides access to the product catalog
    3. **Recommendation Agent**: Generates personalized recommendations based on customer data

    Recommendations are cached in a SQLite database for quick retrieval in future requests.
    """)
