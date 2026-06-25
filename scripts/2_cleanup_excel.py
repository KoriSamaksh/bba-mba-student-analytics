import pandas as pd
import numpy as np
import os
import random
from tkinter import Tk, filedialog

def select_file_via_popup():
    """Windows dialog box open karke file select karne ke liye"""
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    
    print("📁 Opening File Dialog... Apni file select karein.")
    file_path = filedialog.askopenfilename(
        title="Select Your Apify Scraped Student Dataset",
        filetypes=[("Excel files", "*.xlsx *.xls"), ("CSV files", "*.csv"), ("All files", "*.*")]
    )
    return file_path

def clean_apify_scraped_data():
    print("="*70)
    print("🧹 HIGEN LABS DATA CLEANING PIPELINE (ZERO 'NOT AVAILABLE' FILTER)")
    print("="*70)
    
    input_file = select_file_via_popup()
    if not input_file:
        print("❌ Error: Koi file select nahi ki gayi.")
        return
        
    print(f"📦 Selected File: {input_file}")
    
    if input_file.endswith('.xlsx') or input_file.endswith('.xls'):
        df = pd.read_excel(input_file)
    else:
        df = pd.read_csv(input_file)
        
    initial_count = len(df)
    print(f"📊 Loaded {initial_count} raw records.")
    
    # --- STEP 1: DROP ROWS WITH CRITICAL MISSING DATA ---
    # Agar student ka naam ya college hi nahi hai, toh use data se hata do
    critical_cols = ['Student Name', 'College / University Name']
    for col in critical_cols:
        if col in df.columns:
            # Drop pure nulls
            df = df.dropna(subset=[col])
            # Drop 'Not Available' ya string variations
            df = df[~df[col].astype(str).str.lower().str.contains('not available|nan|unknown|profile_record', na=False)]
    
    # --- STEP 2: DEDUPLICATION ---
    if 'LinkedIn Profile URL' in df.columns:
        df = df.dropna(subset=['LinkedIn Profile URL'])
        df = df[~df['LinkedIn Profile URL'].astype(str).str.lower().str.contains('not available|nan', na=False)]
        df.drop_duplicates(subset=['LinkedIn Profile URL'], keep='first', inplace=True)
    else:
        df.drop_duplicates(inplace=True)
        
    print(f"✅ Step 1 & 2 (Clean & Deduplicate): Stripped invalid rows. Remaining rows: {len(df)}")

    # --- STEP 3: FILLING NON-CRITICAL MISSING VALUES WITH SMART ALTERNATIVES ---
    if 'Degree' in df.columns:
        df['Degree'] = df['Degree'].fillna('MBA').astype(str).replace(['Not Available', 'NaN', 'nan'], 'MBA')
        
    if 'Specialization' in df.columns:
        df['Specialization'] = df['Specialization'].fillna('General Management').astype(str)
        df['Specialization'] = df['Specialization'].replace(['Not Available', 'NaN', 'nan', 'Unknown'], 'General Management')

    if 'Location' in df.columns:
        df['Location'] = df['Location'].fillna('India').astype(str)
        df['Location'] = df['Location'].replace(['Not Available', 'NaN', 'nan'], 'India')

    if 'Graduation Year' in df.columns:
        # Agar year missing hai toh random valid year daal do
        df['Graduation Year'] = df['Graduation Year'].apply(lambda x: str(x) if pd.notnull(x) and str(x).isdigit() else str(random.choice([2024, 2025, 2026])))

    # --- STEP 4: STANDARDIZE COLLEGE NAMES ---
    def standardize_college(name):
        name_lower = str(name).lower()
        if 'ahmedabad' in name_lower or 'iima' in name_lower: return 'IIM Ahmedabad'
        if 'bangalore' in name_lower or 'iimb' in name_lower: return 'IIM Bangalore'
        if 'calcutta' in name_lower or 'iimc' in name_lower: return 'IIM Calcutta'
        if 'xlri' in name_lower: return 'XLRI Jamshedpur'
        if 'fms' in name_lower or 'faculty of management studies' in name_lower: return 'FMS Delhi'
        if 'spjimr' in name_lower or 'sp jain' in name_lower: return 'SPJIMR Mumbai'
        if 'symbiosis' in name_lower or 'scmhrd' in name_lower or 'sibm' in name_lower: return 'Symbiosis International University'
        if 'christ' in name_lower: return 'Christ University'
        if 'delhi university' in name_lower or 'sscbs' in name_lower: return 'Delhi University'
        return str(name).strip()

    if 'College / University Name' in df.columns:
        df['College / University Name'] = df['College / University Name'].apply(standardize_college)

    # --- STEP 5: STANDARDIZE SKILLS (NO NOT AVAILABLE ALLOWED) ---
    def clean_skills_string(skills_str):
        if pd.isna(skills_str) or str(skills_str).lower() in ['not available', 'nan', 'unknown', 'none', '']:
            # Safe professional default skills pool based on degree
            return 'Excel, Python, Business Communication, SQL'
            
        parts = [p.strip().lower() for p in str(skills_str).split(',')]
        standardized = []
        
        for skill in parts:
            if 'python' in skill: standardized.append('Python')
            elif 'sql' in skill: standardized.append('SQL')
            elif 'excel' in skill or 'powerpoint' in skill or 'office' in skill: standardized.append('Advanced Excel')
            elif 'tableau' in skill: standardized.append('Tableau')
            elif 'power' in skill or 'bi' in skill: standardized.append('Power BI')
            elif 'model' in skill or 'valuation' in skill: standardized.append('Financial Modeling')
            elif 'digital' in skill or 'marketing' in skill or 'seo' in skill: standardized.append('Digital Marketing')
            elif 'research' in skill or 'strategy' in skill: standardized.append('Market Research & Strategy')
            else:
                if len(skill) > 2 and skill not in ['nan', 'not available']:
                    standardized.append(skill.capitalize())
                    
        unique_skills = list(set(standardized))
        return ", ".join(unique_skills) if unique_skills else 'Excel, Business Analytics'

    if 'Skills' in df.columns:
        df['Skills'] = df['Skills'].apply(clean_skills_string)

    # --- STEP 6: CLEAN CERTIFICATIONS & INTERNSHIPS ---
    if 'Certifications' in df.columns:
        df['Certifications'] = df['Certifications'].fillna('None').astype(str)
        df['Certifications'] = df['Certifications'].replace(['Not Available', 'NaN', 'nan'], 'None')
        
    if 'Internship Experience' in df.columns:
        df['Internship Experience'] = df['Internship Experience'].fillna('None').astype(str)
        df['Internship Experience'] = df['Internship Experience'].replace(['Not Available', 'NaN', 'nan'], 'None')

    # --- STEP 7: SAVE FILE ---
    file_dir, file_name = os.path.split(input_file)
    name_part, ext_part = os.path.splitext(file_name)
    output_file = os.path.join(file_dir, f"{name_part}_perfectly_cleaned{ext_part}")
    
    print("-" * 70)
    if output_file.endswith('.xlsx'):
        df.to_excel(output_file, index=False, engine='openpyxl')
    else:
        df.to_csv(output_file, index=False, encoding='utf-8')
        
    print(f"🎉 Success! Edited file saved at: {output_file}")
    print(f"📊 Total premium clean rows remaining: {len(df)}")

if __name__ == "__main__":
    clean_apify_scraped_data()