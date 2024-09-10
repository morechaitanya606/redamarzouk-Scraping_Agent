import os
import json
import pandas as pd
from datetime import datetime
from firecrawl import FirecrawlApp
from openai import OpenAI

def load_dotenv():
    # Simulate loading environment variables
    os.environ['OPENAI_API_KEY'] = 'your-openai-api-key'
    os.environ['FIRECRAWL_API_KEY'] = 'your-firecrawl-api-key'

load_dotenv()

def scrape_data(url):
    app = FirecrawlApp(api_key=os.getenv('FIRECRAWL_API_KEY'))
    scraped_data = app.scrape_url(url)
    if 'markdown' in scraped_data:
        return scraped_data['markdown']
    else:
        raise KeyError("The key 'markdown' does not exist in the scraped data.")

def save_raw_data(raw_data, timestamp, output_folder='output'):
    os.makedirs(output_folder, exist_ok=True)
    raw_output_path = os.path.join(output_folder, f'rawData_{timestamp}.md')
    with open(raw_output_path, 'w', encoding='utf-8') as f:
        f.write(raw_data)
    print(f"Raw data saved to {raw_output_path}")

def format_data(data, fields=None):
    if fields is None:
        fields = ["Address", "Real Estate Agency", "Price", "Beds", "Baths", "Sqft", "Home Type", "Listing Age", "Picture of home URL", "Listing URL"]
    # Assume data is already in a suitable format for extraction
    formatted_data = {field: data.get(field, '') for field in fields}
    return formatted_data

def save_formatted_data(formatted_data, timestamp, output_folder='output'):
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, f'sorted_data_{timestamp}.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(formatted_data, f, indent=4)
    print(f"Formatted data saved to {output_path}")
    
    # Convert to DataFrame and save to Excel
    df = pd.DataFrame([formatted_data])
    excel_output_path = os.path.join(output_folder, f'sorted_data_{timestamp}.xlsx')
    df.to_excel(excel_output_path, index=False)
    print(f"Formatted data saved to Excel at {excel_output_path}")

if __name__ == "__main__":
    url = 'https://www.zillow.com/salt-lake-city-ut/'
    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        raw_data = scrape_data(url)
        save_raw_data(raw_data, timestamp)
        formatted_data = format_data(raw_data)
        save_formatted_data(formatted_data, timestamp)
    except Exception as e:
        print(f"An error occurred: {e}")
