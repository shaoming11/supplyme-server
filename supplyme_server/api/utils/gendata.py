import pandas as pd
import json
import re
from typing import List, Dict

def normalize_company_name_for_url(name: str) -> str:
    """Convert company name to ImportYeti URL format"""
    # Just normalize the actual company name from CSV - no additions or removals
    
    # Remove special characters except spaces, letters, numbers, and &
    name = re.sub(r'[^\w\s&-]', '', name)
    
    # Replace multiple spaces with single space
    name = re.sub(r'\s+', ' ', name)
    
    # Replace spaces and & with hyphens
    name = re.sub(r'[\s&]+', '-', name)
    
    # Remove multiple consecutive hyphens
    name = re.sub(r'-+', '-', name)
    
    # Remove leading/trailing hyphens and convert to lowercase
    name = name.strip('-').lower()
    
    return name

def process_unicorn_companies(csv_file_path: str) -> List[Dict[str, str]]:
    """Process unicorn companies CSV and create ImportYeti data"""
    
    print(f"📖 Reading CSV file: {csv_file_path}")
    
    # Read the CSV file
    try:
        df = pd.read_csv(csv_file_path)
        print(f"✅ Successfully loaded {len(df)} companies")
    except FileNotFoundError:
        print(f"❌ Error: File '{csv_file_path}' not found!")
        return []
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")
        return []
    
    # Check if required columns exist
    required_columns = ['Company', 'Country']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        print(f"❌ Error: Missing columns: {missing_columns}")
        print(f"Available columns: {list(df.columns)}")
        return []
    
    print(f"📊 Available columns: {list(df.columns)}")
    
    # Process each company
    companies_data = []
    skipped_companies = []
    
    for index, row in df.iterrows():
        try:
            company_name = str(row['Company']).strip()
            company_country = str(row['Country']).strip()
            
            # Skip if essential data is missing
            if pd.isna(row['Company']) or company_name == '' or company_name == 'nan':
                skipped_companies.append(f"Row {index + 1}: Missing company name")
                continue
                
            if pd.isna(row['Country']) or company_country == '' or company_country == 'nan':
                skipped_companies.append(f"Row {index + 1}: Missing country for {company_name}")
                continue
            
            # Normalize company name for URL
            normalized_name = normalize_company_name_for_url(company_name)
            
            # Skip if normalization resulted in empty string
            if not normalized_name:
                skipped_companies.append(f"Row {index + 1}: Could not normalize '{company_name}'")
                continue
            
            # Create ImportYeti URL
            importyeti_url = f"https://www.importyeti.com/company/{normalized_name}"
            
            # Add to results
            companies_data.append({
                "company_name": company_name,
                "importyeti_url": importyeti_url,
                "company_country": company_country
            })
            
        except Exception as e:
            skipped_companies.append(f"Row {index + 1}: Error processing - {e}")
            continue
    
    # Print statistics
    print(f"\n📈 Processing Results:")
    print(f"   ✅ Successfully processed: {len(companies_data)} companies")
    print(f"   ⚠️  Skipped: {len(skipped_companies)} companies")
    
    if skipped_companies and len(skipped_companies) <= 10:
        print(f"\n⚠️  Skipped companies:")
        for skip_msg in skipped_companies:
            print(f"     {skip_msg}")
    elif len(skipped_companies) > 10:
        print(f"\n⚠️  Skipped companies (showing first 10):")
        for skip_msg in skipped_companies[:10]:
            print(f"     {skip_msg}")
        print(f"     ... and {len(skipped_companies) - 10} more")
    
    return companies_data

def save_to_json(companies_data: List[Dict[str, str]], output_file: str):
    """Save companies data to JSON file"""
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(companies_data, f, indent=2, ensure_ascii=False)
        print(f"💾 Successfully saved to: {output_file}")
        return True
    except Exception as e:
        print(f"❌ Error saving JSON: {e}")
        return False

def analyze_data(companies_data: List[Dict[str, str]]):
    """Analyze the processed data and show statistics"""
    
    if not companies_data:
        return
    
    # Count companies by country
    country_counts = {}
    for company in companies_data:
        country = company["company_country"]
        country_counts[country] = country_counts.get(country, 0) + 1
    
    # Sort countries by company count
    sorted_countries = sorted(country_counts.items(), key=lambda x: x[1], reverse=True)
    
    print(f"\n🌍 Top 15 Countries by Unicorn Count:")
    for i, (country, count) in enumerate(sorted_countries[:15]):
        percentage = (count / len(companies_data)) * 100
        print(f"   {i+1:2d}. {country}: {count} companies ({percentage:.1f}%)")
    
    print(f"\n🔗 Sample ImportYeti URLs:")
    for i in range(min(5, len(companies_data))):
        company = companies_data[i]
        print(f"   {company['company_name']} -> {company['importyeti_url']}")
    
    print(f"\n📋 Total unique countries: {len(country_counts)}")

def main():
    """Main function to process unicorn companies CSV"""
    
    # Configuration
    csv_file_path = "World_Wide-Unicorn-Company-List.csv"  # Update this path if needed
    output_file = "companylist.json"
    
    print("🦄 Unicorn Companies to ImportYeti JSON Converter")
    print("=" * 50)
    
    # Process the CSV file
    companies_data = process_unicorn_companies(csv_file_path)
    
    if not companies_data:
        print("❌ No companies were processed successfully. Exiting.")
        return
    
    # Save to JSON
    if save_to_json(companies_data, output_file):
        # Analyze and show statistics
        analyze_data(companies_data)
        
        print(f"\n🎉 Processing complete!")
        print(f"   📁 Input: {csv_file_path}")
        print(f"   📁 Output: {output_file}")
        print(f"   📊 Companies processed: {len(companies_data)}")
    
    else:
        print("❌ Failed to save JSON file.")

# Additional utility function to preview the CSV structure
def preview_csv(csv_file_path: str, num_rows: int = 5):
    """Preview the CSV file structure"""
    try:
        df = pd.read_csv(csv_file_path)
        print(f"📋 CSV Preview (first {num_rows} rows):")
        print(df.head(num_rows).to_string())
        print(f"\n📊 Total rows: {len(df)}")
        print(f"📊 Columns: {list(df.columns)}")
        
        # Show sample data for key columns
        if 'Company' in df.columns:
            print(f"\n🏢 Sample companies: {df['Company'].head(3).tolist()}")
        if 'Country' in df.columns:
            print(f"🌍 Sample countries: {df['Country'].head(3).tolist()}")
            
    except Exception as e:
        print(f"❌ Error previewing CSV: {e}")

if __name__ == "__main__":
    # Uncomment the line below to preview CSV structure first
    # preview_csv("World_WideUnicornCompanyList.csv")
    
    main()