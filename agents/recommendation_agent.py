from typing import Dict, List, Any


class RecommendationAgent:

    def __init__(self, product_agent):
        """Initialize the recommendation agent with a product agent."""
        self.product_agent = product_agent

    def generate_recommendations(self, customer_data: Dict[str,
                                                           Any]) -> List[Dict]:
        """Generate personalized product recommendations for a customer."""
        print(
            f"Generating recommendations for customer: {customer_data['customer_id']}"
        )

        recommendations = []

        # If the customer has purchase history, recommend similar products
        if customer_data['found'] and customer_data['purchase_history']:
            print("Basing recommendations on purchase history")
            for purchased_item in customer_data['purchase_history']:
                similar_products = self.product_agent.get_similar_products(
                    purchased_item, n=3)
                for product in similar_products:
                    if product not in recommendations:
                        recommendations.append(product)

        # If we don't have enough recommendations yet, use browsing history
        if len(recommendations) < 10 and customer_data['browsing_history']:
            print("Adding recommendations based on browsing history")
            browsed_products = self.product_agent.get_products_by_categories(
                customer_data['browsing_history'])

            # Sort by recommendation probability if available
            if browsed_products and 'Probability_of_Recommendation' in browsed_products[
                    0]:
                browsed_products.sort(
                    key=lambda x: x.get('Probability_of_Recommendation', 0),
                    reverse=True)

            # Add products until we reach 10 or run out
            for product in browsed_products:
                if product not in recommendations:
                    recommendations.append(product)
                    if len(recommendations) >= 10:
                        break

        # If we still don't have 10 recommendations, add top products
        if len(recommendations) < 10:
            print("Adding top products to reach 10 recommendations")
            top_products = self.product_agent.get_top_products(n=10)

            for product in top_products:
                if product not in recommendations:
                    recommendations.append(product)
                    if len(recommendations) >= 10:
                        break

        # Limit to 10 recommendations
        recommendations = recommendations[:10]

        return recommendations
