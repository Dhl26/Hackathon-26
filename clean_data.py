import pandas as pd
import os
import re

# ==========================================
# MAPPINGS AND CORRECTIONS
# ==========================================

# Corrections for State names
# Key: Incorrect/Variant Name (normalized to Title Case), Value: Correct Name
STATE_CORRECTIONS = {
    'Jammu And Kashmir': 'Jammu and Kashmir',
    'Jammu & Kashmir': 'Jammu and Kashmir',
    'Orissa': 'Odisha',
    'Pondicherry': 'Puducherry',
    'West Bangal': 'West Bengal',
    'Westbengal': 'West Bengal',
    'West Bengli': 'West Bengal',
    'West Bengal': 'West Bengal',
    'Andaman & Nicobar Islands': 'Andaman and Nicobar Islands',
    'Andaman And Nicobar Islands': 'Andaman and Nicobar Islands',
    'Dadra & Nagar Haveli': 'Dadra and Nagar Haveli and Daman and Diu',
    'Dadra And Nagar Haveli': 'Dadra and Nagar Haveli and Daman and Diu',
    'Dadra and Nagar Haveli': 'Dadra and Nagar Haveli and Daman and Diu', # Just in case
    'Daman And Diu': 'Dadra and Nagar Haveli and Daman and Diu',
    'Daman & Diu': 'Dadra and Nagar Haveli and Daman and Diu',
    'The Dadra And Nagar Haveli And Daman And Diu': 'Dadra and Nagar Haveli and Daman and Diu',
    'Dadra And Nagar Haveli And Daman And Diu': 'Dadra and Nagar Haveli and Daman and Diu',
    'Andhra Pradesh': 'Andhra Pradesh',
    'Chhatisgarh': 'Chhattisgarh',
    'Uttaranchal': 'Uttarakhand',
    'Tamilnadu': 'Tamil Nadu',
    # Cities mapping to States
    'Jaipur': 'Rajasthan',
    'Nagpur': 'Maharashtra',
    'Darbhanga': 'Bihar',
    'Madanapalle': 'Andhra Pradesh',
    'Balanagar': 'Telangana',
    'Puttenahalli': 'Karnataka',
    'Raja Annamalai Puram': 'Tamil Nadu',
}

# Key: Pincode (string), Value: State Name
# Pre-populate with known fixes or standard mappings if needed
PINCODE_TO_STATE = {
    '100000': 'Delhi', 
}

# Corrections for District names
# Key: Incorrect/Variant Name (normalized to Title Case), Value: Correct Name
DISTRICT_CORRECTIONS = {
    'Allahabad': 'Prayagraj',
    'Faizabad': 'Ayodhya',
    'Shrawasti': 'Shravasti',
    'Siddharth Nagar': 'Siddharthnagar',
    'Bara Banki': 'Barabanki',
    'Kushi Nagar': 'Kushinagar',
    'Kushinagar *': 'Kushinagar',
    'Bulandshahar': 'Bulandshahr',
    'Rae Bareli': 'Raebareli',
    'Jyotiba Phule Nagar': 'Amroha',
    'Sant Ravidas Nagar': 'Bhadohi',
    'Sant Ravidas Nagar Bhadohi': 'Bhadohi',
    'Burdwan': 'Bardhaman', # Or Purba/Paschim split if unsure, but standardizing spelling helps
    'Darjiling': 'Darjeeling',
    'Haora': 'Howrah',
    'Hawrah': 'Howrah',
    'Hugli': 'Hooghly',
    'Hooghiy': 'Hooghly',
    'Maldah': 'Malda',
    'Puruliya': 'Purulia',
    'Hardwar': 'Haridwar',
    # West Bengal Cleanups
    'Barddhaman': 'Bardhaman',
    'Burdwan': 'Bardhaman',
    'Paschim Bardhaman': 'Paschim Bardhaman', # Already correct?
    'Purba Bardhaman': 'Purba Bardhaman', # Already correct?
    'Dakshin Dinajpur': 'Dakshin Dinajpur',
    'South Dinajpur': 'Dakshin Dinajpur',
    'North Dinajpur': 'Uttar Dinajpur',
    'Uttar Dinajpur': 'Uttar Dinajpur',
    'East Midnapore': 'Purba Medinipur',
    'East Midnapur': 'Purba Medinipur',
    'West Midnapore': 'Paschim Medinipur',
    'West Medinipur': 'Paschim Medinipur',
    'Medinipur': 'Paschim Medinipur', # Assumption, or maybe Purba. Usually refers to West/Paschim HQ.
    'North Twenty Four Parganas': 'North 24 Parganas',
    'South Twenty Four Parganas': 'South 24 Parganas',
    'South 24 Pargana': 'South 24 Parganas',
    'Koch Bihar': 'Cooch Behar',
    'South Dumdum(M)': 'South Dumdum',
    # Add more here as discovered
}

def clean_text(text):
    """
    Standardizes text by:
    1. Converting to string.
    2. Stripping whitespace.
    3. Removing multiple spaces.
    4. Removing trailing asterisks (*).
    5. Converting to Title Case.
    """
    if pd.isna(text):
        return text
    text = str(text).strip()
    text = re.sub(r'\s+', ' ', text) # Replace multiple spaces with single space
    text = re.sub(r'\s*\*\s*$', '', text) # Remove trailing asterisk (e.g. "Name *")
    return text.title()

def fix_state_by_pincode(row):
    state = row['state']
    pincode = str(row['pincode']).strip().replace('.0', '') # Handle float strings
    
    # Check if state is invalid ('100000' or None/NaN)
    if pd.isna(state) or state == '100000':
        # Lookup in global map
        if pincode in PINCODE_TO_STATE:
            return PINCODE_TO_STATE[pincode]
    return state

def process_files(source_dir, target_dir):
    """
    Walks through source_dir, cleans CSV files, and saves to target_dir.
    """
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.endswith('.csv') or file.endswith('.xlsx'):
                source_path = os.path.join(root, file)
                
                # Determine relative path to maintain structure
                rel_path = os.path.relpath(root, source_dir)
                target_folder = os.path.join(target_dir, rel_path)
                
                if not os.path.exists(target_folder):
                    os.makedirs(target_folder)
                
                target_path = os.path.join(target_folder, file)
                
                print(f"Processing: {source_path}")
                
                try:
                    # Detect format
                    if file.endswith('.csv'):
                        df = pd.read_csv(source_path)
                    else:
                        df = pd.read_excel(source_path)
                    
                    # Clean State Column
                    if 'state' in df.columns:
                        # 0. Basic cleanup first
                        df['state'] = df['state'].apply(clean_text)
                        
                        # 1. Build Pincode Map from VALID states in this file
                        if 'pincode' in df.columns:
                            valid_rows = df[~df['state'].isin(['100000', pd.NA, float('nan')]) & df['state'].notna()]
                            # Create a map: pincode -> state. 
                            # Note: A pincode might span states in rare edge cases, but we take the first/last entry.
                            local_map = pd.Series(valid_rows.state.values, index=valid_rows.pincode.astype(str).str.replace('.0', '')).to_dict()
                            PINCODE_TO_STATE.update(local_map)
                        
                        # 2. Apply mapping corrections
                        df['state'] = df['state'].replace(STATE_CORRECTIONS)
                        
                        # 3. Fix '100000' or missing states using Pincode
                        if 'pincode' in df.columns:
                             df['state'] = df.apply(fix_state_by_pincode, axis=1)

                        # 4. Remove rows with invalid states (still mapped to None or not found)
                        df.dropna(subset=['state'], inplace=True)
                        df = df[df['state'] != '100000'] # Drop '100000' data as requested
                        
                    # Clean District Column
                    if 'district' in df.columns:
                        df['district'] = df['district'].apply(clean_text)
                        df['district'] = df['district'].replace(DISTRICT_CORRECTIONS)

                        # Re-assign States based on District (Critical for Map Matching)
                        # 1. Ladakh
                        ladakh_districts = ['Leh', 'Kargil', 'Leh (Ladakh)', 'Ladakh']
                        mask_ladakh = df['district'].isin(ladakh_districts)
                        df.loc[mask_ladakh, 'state'] = 'Ladakh'

                        # 2. Telangana (Old districts often mislabelled as AP in older data)
                        telangana_districts = [
                            'Adilabad', 'Hyderabad', 'Karimnagar', 'Khammam', 'Mahbubnagar', 
                            'Medak', 'Nalgonda', 'Nizamabad', 'Rangareddy', 'Warangal', 
                            'Ranga Reddy', 'Bhadradri Kothagudem', 'Jagtial', 'Jangaon', 
                            'Jayashankar Bhupalpally', 'Jogulamba Gadwal', 'Kamareddy', 
                            'Komaram Bheem Asifabad', 'Mahabubabad', 'Mancherial', 'Medchal Malkajgiri', 
                            'Mulugu', 'Nagarkurnool', 'Narayanpet', 'Nirmal', 'Peddapalli', 
                            'Rajanna Sircilla', 'Sangareddy', 'Siddipet', 'Suryapet', 'Vikarabad', 
                            'Wanaparthy', 'Yadadri Bhuvanagiri'
                        ]
                        # Only re-assign if currently 'Andhra Pradesh' or 'Telangana' (to standardize)
                        mask_tg = df['district'].isin(telangana_districts)
                        df.loc[mask_tg, 'state'] = 'Telangana'

                    # Save
                    if file.endswith('.csv'):
                        df.to_csv(target_path, index=False)
                    else:
                        df.to_excel(target_path, index=False)
                        
                    print(f"Saved cleaned file to: {target_path}")

                except Exception as e:
                    print(f"Error processing {source_path}: {e}")

if __name__ == "__main__":
    SOURCE_DIRECTORY = "Dataset"
    TARGET_DIRECTORY = "Dataset_Cleaned"
    
    print(f"Starting cleanup from '{SOURCE_DIRECTORY}' to '{TARGET_DIRECTORY}'...")
    process_files(SOURCE_DIRECTORY, TARGET_DIRECTORY)
    print("Cleanup completed.")
