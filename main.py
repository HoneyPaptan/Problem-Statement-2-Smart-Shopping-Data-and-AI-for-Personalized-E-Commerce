import os
import sys


def setup_project():
    """Setup the project by creating necessary directories and preparing the environment."""
    print("Setting up E-commerce Recommendation System...")

    # Create directories if they don't exist
    directories = ["agents", "database"]
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")

    # Check if data files exist
    required_files = [
        "customer_data_collection.csv", "product_recommendation_data.csv"
    ]
    missing_files = []

    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)

    if missing_files:
        print(
            f"Warning: The following required data files are missing: {', '.join(missing_files)}"
        )
        print(
            "Please make sure these files are placed in the root directory before running the application."
        )
    else:
        print("All required data files are present.")

    # Create __init__.py in agents directory if it doesn't exist
    if not os.path.exists("agents/__init__.py"):
        with open("agents/__init__.py", "w") as f:
            f.write(
                "# This file is required to make Python treat the directory as a package\n"
            )

    print("Setup complete! You can now run the Streamlit app with:")
    print("streamlit run app.py")


if __name__ == "__main__":
    setup_project()
