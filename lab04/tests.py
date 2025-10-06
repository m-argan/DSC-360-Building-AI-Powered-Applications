import pandas as pd

url = "your_url_here.csv"  # Replace with the actual URL
try:
    df = pd.read_csv(url, sep=';')
    print(df)
except Exception as e:
    print(f"An error occurred: {e}")