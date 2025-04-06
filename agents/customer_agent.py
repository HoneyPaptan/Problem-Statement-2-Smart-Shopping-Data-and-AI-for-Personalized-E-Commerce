import pandas as pd
from typing import Dict, List, Any


class CustomerAgent:

    def __init__(self, customer_data_path="customer_data_collection.csv"):
        """Initialize the customer agent with customer data."""
        self.customer_data_path = customer_data_path
        try:
            self.customer_data = pd.read_csv(customer_data_path)
            # Convert string representations of lists to actual lists
            for col in ['Browsing_History', 'Purchase_History']:
                self.customer_data[col] = self.customer_data[col].apply(eval)
            print(f"Loaded {len(self.customer_data)} customer records")
        except Exception as e:
            print(f"Error loading customer data: {e}")
            self.customer_data = pd.DataFrame()

    def get_customer_data(self, customer_id: str) -> Dict[str, Any]:
        """Retrieve data for a specific customer."""
        customer = self.customer_data[self.customer_data['Customer_ID'] ==
                                      customer_id]

        if customer.empty:
            print(f"Customer {customer_id} not found")
            return {
                'customer_id': customer_id,
                'found': False,
                'browsing_history': [],
                'purchase_history': [],
                'customer_type': 'new'
            }

        customer_data = customer.iloc[0].to_dict()
        return {
            'customer_id': customer_id,
            'found': True,
            'browsing_history': customer_data['Browsing_History'],
            'purchase_history': customer_data['Purchase_History'],
            'customer_type': customer_data['Customer_Segment'],
            'age': customer_data['Age'],
            'gender': customer_data['Gender'],
            'location': customer_data['Location'],
            'avg_order_value': customer_data['Avg_Order_Value'],
            'holiday': customer_data['Holiday'],
            'season': customer_data['Season']
        }
