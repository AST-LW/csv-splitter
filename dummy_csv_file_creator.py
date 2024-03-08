import pandas as pd
import numpy as np


def create_dummy_csv_file():
    # Set the random seed for reproducibility
    np.random.seed(42)

    # Define the number of rows
    num_rows = 1683333  # Adjust as needed

    # Create dummy data with 5 columns
    data = {
        'Column1': np.random.randint(1, 100, num_rows),
        'Column2': np.random.choice(['A', 'B', 'C'], num_rows),
        'Column3': np.random.rand(num_rows),
        'Column4': np.random.choice([True, False], num_rows),
        'Column5': np.random.uniform(10.0, 20.0, num_rows)
    }

    # Create a DataFrame
    df = pd.DataFrame(data)

    # Save the DataFrame to a CSV file
    df.to_csv('dummy_data.csv', index=False)

    print("Dummy CSV file created successfully.")
