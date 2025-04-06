import pandas as pd
from typing import Dict, List, Any


class ProductAgent:

    def __init__(self, product_catalog_path="product_recommendation_data.csv"):
        """Initialize the product agent with product catalog data."""
        self.product_catalog_path = product_catalog_path
        try:
            self.product_catalog = pd.read_csv(product_catalog_path)
            # Convert string representations of lists to actual lists if they exist
            if 'Similar_Product_List' in self.product_catalog.columns:
                self.product_catalog[
                    'Similar_Product_List'] = self.product_catalog[
                        'Similar_Product_List'].apply(eval)
            print(f"Loaded {len(self.product_catalog)} products")
        except Exception as e:
            print(f"Error loading product catalog: {e}")
            self.product_catalog = pd.DataFrame()

        # Create category mapping for quick access
        self.category_products = {}
        self.subcategory_products = {}

        if not self.product_catalog.empty:
            # Group products by category
            for category in self.product_catalog['Category'].unique():
                self.category_products[category] = self.product_catalog[
                    self.product_catalog['Category'] == category].to_dict(
                        'records')

            # Group products by subcategory
            for subcategory in self.product_catalog['Subcategory'].unique():
                self.subcategory_products[subcategory] = self.product_catalog[
                    self.product_catalog['Subcategory'] ==
                    subcategory].to_dict('records')

    def get_products_by_categories(self, categories: List[str]) -> List[Dict]:
        """Get products from specified categories."""
        result = []
        for category in categories:
            if category in self.category_products:
                result.extend(self.category_products[category])
        return result

    def get_products_by_subcategories(self,
                                      subcategories: List[str]) -> List[Dict]:
        """Get products from specified subcategories."""
        result = []
        for subcategory in subcategories:
            if subcategory in self.subcategory_products:
                result.extend(self.subcategory_products[subcategory])
        return result

    def get_top_products(self, n=10) -> List[Dict]:
        """Get top N products based on recommendation probability."""
        if 'Probability_of_Recommendation' in self.product_catalog.columns:
            top_products = self.product_catalog.sort_values(
                by='Probability_of_Recommendation',
                ascending=False).head(n).to_dict('records')
        elif 'Product_Rating' in self.product_catalog.columns:
            top_products = self.product_catalog.sort_values(
                by='Product_Rating',
                ascending=False).head(n).to_dict('records')
        else:
            # If no ranking metric found, just take first n
            top_products = self.product_catalog.head(n).to_dict('records')
        return top_products

    def get_similar_products(self, subcategory: str, n=5) -> List[Dict]:
        """Get products similar to the specified subcategory."""
        # First try to get products from the same subcategory
        similar_products = self.product_catalog[
            self.product_catalog['Subcategory'] == subcategory].to_dict(
                'records')

        # If not enough products found, get more from products with similar items in their Similar_Product_List
        if len(
                similar_products
        ) < n and 'Similar_Product_List' in self.product_catalog.columns:
            for _, product in self.product_catalog.iterrows():
                if subcategory in product['Similar_Product_List'] and len(
                        similar_products) < n:
                    if product.to_dict() not in similar_products:
                        similar_products.append(product.to_dict())

        # Sort by recommendation probability if available
        if similar_products and 'Probability_of_Recommendation' in similar_products[
                0]:
            similar_products.sort(
                key=lambda x: x.get('Probability_of_Recommendation', 0),
                reverse=True)

        return similar_products[:n]
