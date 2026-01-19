import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from glob import glob
import os
import json
import sys
import numpy as np

# Page Configuration
st.set_page_config(
    page_title="UIDAI Insights Dashboard",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main { background-color: #f5f7f9; font-family: 'Inter', sans-serif; }
    .metric-card {
        background-color: white; padding: 20px; border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: center;
        border: 1px solid #e0e0e0;
    }
    .metric-value { font-size: 2rem; font-weight: 700; color: #0047AB; }
    .metric-label { color: #6c757d; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px; }
    h1, h2, h3 { color: #1a1a1a; }
    .stSelectbox label { color: #333; font-weight: 600; }
    .highlight-box {
        background-color: #e8f4fd; border-left: 5px solid #0047AB;
        padding: 15px; margin: 10px 0; border-radius: 5px;
    }
    .problem-box {
        background-color: #fde8e8; border-left: 5px solid #dc3545;
        padding: 15px; margin: 10px 0; border-radius: 5px;
    }
    .scheme-box {
        background-color: #e3fcef; border-left: 5px solid #0f5132;
        padding: 15px; margin: 10px 0; border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# MAPPINGS
# ==========================================
STATE_GEO_MAP = {
    'Odisha': 'Orissa',
    'Uttarakhand': 'Uttaranchal',
    'Andaman and Nicobar Islands': 'Andaman and Nicobar',
    # 'Ladakh': 'Jammu and Kashmir',  # REMOVED: Now exists in patched map
    'Dadra and Nagar Haveli and Daman and Diu': 'Daman and Diu',
    'Telangana': 'Telangana', # Ensure direct mapping
}

def get_geo_state_name(data_name):
    return STATE_GEO_MAP.get(data_name, data_name)

# ==========================================
# DATA LOADING
# ==========================================
@st.cache_data
def load_data():
    base_path = "Dataset_Cleaned"
    
    def load_category(folder, cat_name):
        files = glob(os.path.join(base_path, folder, "*.csv"))
        if not files: return pd.DataFrame()
        df = pd.concat((pd.read_csv(f) for f in files), ignore_index=True)
        df['Category'] = cat_name
        df['c_state'] = df['state'].apply(get_geo_state_name)
        # Parse Dates
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y', errors='coerce')
        return df

    # Enrolment
    df_enrol = load_category("api_data_aadhar_enrolment", "Enrolment")
    if not df_enrol.empty:
        df_enrol['Total'] = df_enrol['age_0_5'] + df_enrol['age_5_17'] + df_enrol['age_18_greater']

    # Biometric
    df_bio = load_category("api_data_aadhar_biometric", "Biometric Update")
    if not df_bio.empty:
        df_bio['Total'] = df_bio['bio_age_5_17'] + df_bio['bio_age_17_']
        
    # Demographic
    df_demo = load_category("api_data_aadhar_demographic", "Demographic Update")
    if not df_demo.empty:
        df_demo['Total'] = df_demo['demo_age_5_17'] + df_demo['demo_age_17_']

    return df_enrol, df_bio, df_demo

@st.cache_data
def load_geojson():
    try:
        with open('india_states.geojson', 'r') as f:
            states = json.load(f)
        with open('india_districts.geojson', 'r') as f:
            districts = json.load(f)
        return states, districts
    except:
        return None, None

with st.spinner('Loading Data & Maps...'):
    df_enrol, df_bio, df_demo = load_data()
    geojson_states, geojson_districts = load_geojson()

# ==========================================
# APP LAYOUT
# ==========================================

st.sidebar.image("https://upload.wikimedia.org/wikipedia/en/thumb/c/cf/Aadhaar_Logo.svg/1200px-Aadhaar_Logo.svg.png", width=150)
st.sidebar.title("Navigation")
app_mode = st.sidebar.radio("Go to:", [
    "🇮🇳 Dashboard Overview",
    "🎯 Strategic Action Center",
    "📜 Active Govt Schemes"
])

# ==========================================
# 1. DASHBOARD OVERVIEW
# ==========================================
if app_mode == "🇮🇳 Dashboard Overview":
    st.title("🇮🇳 Aadhaar Saturation Dashboard")
    
    metric_choice = st.radio("Select Metric:", ["Enrolment", "Biometric", "Demographic"], horizontal=True)
    
    if metric_choice == "Enrolment": curr_df = df_enrol
    elif metric_choice == "Biometric": curr_df = df_bio
    else: curr_df = df_demo
    
    # KPIS
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{curr_df["Total"].sum():,.0f}</div><div class="metric-label">Total Volume</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{len(curr_df["state"].unique())}</div><div class="metric-label">States Active</div></div>', unsafe_allow_html=True)
    with c3:
        top_state = curr_df.groupby('state')['Total'].sum().idxmax()
        st.markdown(f'<div class="metric-card"><div class="metric-value">{top_state}</div><div class="metric-label">Top State</div></div>', unsafe_allow_html=True)

    st.divider()
    
    # --- INTERACTIVE MAP ---
    st.subheader(f"🗺️ State-wise {metric_choice} Density")
    st.info("💡 Click on any state to view district-level breakdown.")
    
    state_agg = curr_df.groupby('c_state')['Total'].sum().reset_index()
    
    if geojson_states:
        fig_india = px.choropleth(
            state_agg, geojson=geojson_states, featureidkey='properties.NAME_1',
            locations='c_state', color='Total', color_continuous_scale="Viridis",
            hover_name='c_state', title=""
        )
        fig_india.update_geos(fitbounds="locations", visible=False)
        fig_india.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, height=500)
        
        select_event = st.plotly_chart(fig_india, use_container_width=True, on_select="rerun", selection_mode="points")
    else:
        st.error("Map data missing. Please check geojson files.")
        select_event = None

    # --- DRILL DOWN ---
    selected_state_geo = None
    if select_event and select_event.get("selection") and select_event["selection"]["points"]:
        point = select_event["selection"]["points"][0]
        if "pointIndex" in point:
            idx = point["pointIndex"]
            selected_state_geo = state_agg.iloc[idx]['c_state']

    all_states = sorted(curr_df['state'].unique())
    default_idx = 0
    
    if selected_state_geo:
        matches = [k for k,v in STATE_GEO_MAP.items() if v == selected_state_geo]
        ds_name = matches[0] if matches else selected_state_geo
        if ds_name in all_states:
             default_idx = all_states.index(ds_name)

    st.subheader("🔍 District Deep Dive")
    target_state = st.selectbox("Select State:", all_states, index=default_idx)
    
    state_df = curr_df[curr_df['state'] == target_state]
    dist_agg = state_df.groupby('district')['Total'].sum().reset_index().sort_values('Total', ascending=False)
    
    col_map, col_chart = st.columns([3, 2])
    
    with col_map:
        st.markdown(f"**📍 Map of {target_state}**")
        target_geo_name = STATE_GEO_MAP.get(target_state, target_state)
        
        if geojson_districts:
            # Filter features for this state
            state_features = [f for f in geojson_districts['features'] if f['properties']['NAME_1'] == target_geo_name]
            
            if state_features:
                st_dist_geo = {"type": "FeatureCollection", "features": state_features}
                fig_st = px.choropleth(
                     dist_agg, geojson=st_dist_geo, featureidkey='properties.NAME_2',
                     locations='district', color='Total', color_continuous_scale="Plasma"
                )
                fig_st.update_geos(fitbounds="locations", visible=False)
                fig_st.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, height=400)
                st.plotly_chart(fig_st, use_container_width=True)
            else:
                st.warning("No district map available for this state.")
    
    with col_chart:
        st.markdown("**📊 District Rankings**")
        st.dataframe(dist_agg, height=400, hide_index=True, use_container_width=True)

# ==========================================
# 2. STRATEGIC ACTION CENTER
# ==========================================
# ==========================================
# 2. STRATEGIC ACTION CENTER
# ==========================================
elif app_mode == "🎯 Strategic Action Center":
    st.title("🎯 Strategic Action Center")
    st.markdown("Advanced analytics to identify gaps, compliance risks, and active government schemes linkages.")

    # --- GLOBAL FILTERS ---
    st.markdown("### 🔍 Regional Analysis Filters")
    col_f1, col_f2 = st.columns(2)
    
    # State Filter
    all_states = sorted(df_enrol['state'].unique())
    selected_state = col_f1.selectbox("Filter by State:", ["All India"] + all_states)
    
    # District Filter (Conditional)
    selected_district = "All Districts"
    if selected_state != "All India":
        state_districts = sorted(df_enrol[df_enrol['state'] == selected_state]['district'].unique())
        selected_district = col_f2.selectbox("Filter by District:", ["All Districts"] + state_districts)
    else:
        col_f2.write("") # Spacer

    # --- APPLY FILTERS ---
    enrol_filtered = df_enrol.copy()
    bio_filtered = df_bio.copy()
    
    if selected_state != "All India":
        enrol_filtered = enrol_filtered[enrol_filtered['state'] == selected_state]
        bio_filtered = bio_filtered[bio_filtered['state'] == selected_state]
        
        if selected_district != "All Districts":
            enrol_filtered = enrol_filtered[enrol_filtered['district'] == selected_district]
            bio_filtered = bio_filtered[bio_filtered['district'] == selected_district]

    st.divider()

    tabs = st.tabs(["📊 Age Cohort & Schemes", "📈 Temporal Trends", "🚨 Risk & Anomalies", "💡 Solution Framework"])

    # --- TAB 1: AGE COHORT & SCHEMES ---
    with tabs[0]:
        st.subheader(f"🧩 Age Cohort: {selected_state} - {selected_district}")
        
        # 1. Heatmap: State vs Age Group OR District vs Age Group
        group_col = 'state' if selected_state == "All India" else 'district'
        chart_title = "State-wise Age Group Composition" if selected_state == "All India" else f"District-wise Age Group Composition ({selected_state})"
        
        # Aggregate
        heat_data = enrol_filtered.groupby(group_col)[['age_0_5', 'age_5_17', 'age_18_greater']].sum().reset_index()
        
        if not heat_data.empty:
            heat_data['Total'] = heat_data.sum(axis=1, numeric_only=True)
            # Avoid division by zero
            heat_data = heat_data[heat_data['Total'] > 0]
            
            heat_data['0-5 (%)'] = heat_data['age_0_5'] / heat_data['Total']
            heat_data['5-17 (%)'] = heat_data['age_5_17'] / heat_data['Total']
            heat_data['18+ (%)'] = heat_data['age_18_greater'] / heat_data['Total']
            
            heat_df_final = heat_data.set_index(group_col)[['0-5 (%)', '5-17 (%)', '18+ (%)']]
            
            fig_heat = px.imshow(heat_df_final, text_auto='.1%', aspect="auto", color_continuous_scale="RdBu_r",
                                 title=chart_title)
            st.plotly_chart(fig_heat, use_container_width=True)
        else:
            st.warning("No data available for the selected filters.")

        st.divider()

        # 2. Age-Specific Schemes & Analysis
        c1, c2 = st.columns(2)
        
        with c1:
            st.markdown("### 👶 Early Childhood (0-5 Years)")
            st.info("Critical for: Welfare benefits (Health, Nutrition)")
            
            st.markdown("""
            <div class="scheme-box">
            <b>🏛️ Linked Schemes:</b><br>
            • <b>POSHAN Abhiyaan</b> (Nutrition)<br>
            • <b>ICDS</b> (Integrated Child Development)<br>
            • <b>Mission Indradhanush</b> (Immunization)
            </div>
            """, unsafe_allow_html=True)
            
            if not heat_data.empty:
                avg_0_5 = heat_data['0-5 (%)'].mean()
                st.metric(f"Avg 0-5 Share ({selected_state})", f"{avg_0_5:.1%}")
            
        with c2:
            st.markdown("### 🏫 School Going (5-17 Years)")
            st.info("Critical for: Education, Scholarships, Mid-day Meals")
            
            st.markdown("""
            <div class="scheme-box">
            <b>🏛️ Linked Schemes:</b><br>
            • <b>PM POSHAN</b> (Mid-Day Meal)<br>
            • <b>Samagra Shiksha</b><br>
            • <b>National Scholarship Portal</b>
            </div>
            """, unsafe_allow_html=True)
            
            if not heat_data.empty:
                avg_5_17 = heat_data['5-17 (%)'].mean()
                st.metric(f"Avg 5-17 Share ({selected_state})", f"{avg_5_17:.1%}")

    # --- TAB 2: TEMPORAL TRENDS ---
    with tabs[1]:
        st.subheader("📈 Temporal Patterns")
        
        if 'date' in enrol_filtered.columns and not enrol_filtered.empty:
            # Aggregate by month
            trend_df = enrol_filtered.set_index('date').resample('M')['Total'].sum().reset_index()
            
            if not trend_df.empty:
                # Plot
                fig_trend = go.Figure()
                fig_trend.add_trace(go.Scatter(x=trend_df['date'], y=trend_df['Total'], mode='lines+markers', name='Enrolment Volume', line=dict(color='#0047AB', width=3)))
                
                # Peak Annotation
                if len(trend_df) > 1:
                    peak_date = trend_df.loc[trend_df['Total'].idxmax()]['date']
                    fig_trend.add_annotation(x=peak_date, y=trend_df['Total'].max(), text="🚀 Peak", showarrow=True, arrowhead=1)
                
                fig_trend.update_layout(title=f"Monthly Enrolment Trend: {selected_state}", hovermode="x unified")
                st.plotly_chart(fig_trend, use_container_width=True)
                
                # Diagnostics
                if len(trend_df) >= 3:
                    last_3_months = trend_df.tail(3)['Total'].mean()
                    # Safe previous calculation
                    prev_slice = trend_df.iloc[-6:-3] if len(trend_df) >= 6 else trend_df.iloc[:-3]
                    prev_3_months = prev_slice['Total'].mean() if not prev_slice.empty else last_3_months

                    c1_trend, c2_trend = st.columns([3, 1])
                    with c1_trend:
                        if prev_3_months > 0:
                            change = (last_3_months / prev_3_months) - 1
                            if change < -0.05:
                                st.error(f"⚠️ **Decline Detected:** Activity is {change:.1%} lower than previous period.")
                            elif change > 0.05:
                                st.success(f"✅ **Growth Detected:** Activity is up by +{change:.1%}!")
                            else:
                                st.info("⚖️ **Steady State:** Enrolment is stable.")
                        else:
                            st.info("Insufficient historical data for trend analysis.")
        else:
            st.warning("Temporal data not available for this selection.")

    # --- TAB 3: RISK & ANOMALIES ---
    with tabs[2]:
        st.subheader("🚨 Risk Dashboard")
        
        # Calculate Ratios using FILTERED data
        if not enrol_filtered.empty and not bio_filtered.empty:
            risk_df = enrol_filtered.groupby(['state', 'district'])[['age_5_17']].sum().reset_index()
            bio_risk_grouped = bio_filtered.groupby(['state', 'district'])[['bio_age_5_17']].sum().reset_index()
            
            full_risk = pd.merge(risk_df, bio_risk_grouped, on=['state', 'district'], how='inner')
            
            if not full_risk.empty:
                full_risk['Update_Ratio'] = full_risk['bio_age_5_17'] / full_risk['age_5_17']
                
                conditions = [
                    (full_risk['Update_Ratio'] < 0.2),
                    (full_risk['Update_Ratio'] >= 0.2) & (full_risk['Update_Ratio'] < 0.5),
                    (full_risk['Update_Ratio'] >= 0.5)
                ]
                choices = ['🔴 High Risk', '🟡 Medium Risk', '🟢 Low Risk']
                full_risk['Risk_Category'] = np.select(conditions, choices, default='Unknown')
                
                risk_counts = full_risk['Risk_Category'].value_counts().reset_index()
                risk_counts.columns = ['Risk Level', 'District Count']
                
                c1_risk, c2_risk = st.columns([1, 2])
                with c1_risk:
                    fig_donut = px.pie(risk_counts, values='District Count', names='Risk Level', hole=0.4, 
                                       color='Risk Level', color_discrete_map={'🔴 High Risk':'red', '🟡 Medium Risk':'orange', '🟢 Low Risk':'green'},
                                       title="Risk Profile")
                    st.plotly_chart(fig_donut, use_container_width=True)
                    
                with c2_risk:
                    st.markdown("**🔍 Top Risk Districts (Action Required)**")
                    st.dataframe(full_risk.sort_values('Update_Ratio').head(10)[['district', 'age_5_17', 'bio_age_5_17', 'Update_Ratio', 'Risk_Category']].style.format({'Update_Ratio': '{:.1%}'}), use_container_width=True)

                st.divider()
                
                # Geographic Map (Only specific to state if selected)
                map_target_state = selected_state if selected_state != "All India" else None
                
                # If specific state selected, show map automatically. If All India, let user choose from filtered list?
                # Actually, if All India, we might want to let them choose.
                
                st.markdown("#### 🗺️ Geographic Risk Distribution")
                
                if map_target_state:
                     risk_map_state = map_target_state
                else:
                     risk_map_state = st.selectbox("Select State to Map:", sorted(full_risk['state'].unique()))

                if risk_map_state and geojson_districts:
                    state_risk_df = full_risk[full_risk['state'] == risk_map_state]
                    geo_name = get_geo_state_name(risk_map_state)
                    
                    state_risk_feats = [f for f in geojson_districts['features'] 
                                        if f['properties'].get('NAME_1') == geo_name or 
                                           f['properties'].get('stname') == geo_name or
                                           f['properties'].get('NAME_1') == risk_map_state]
                    
                    if state_risk_feats:
                        risk_geo = {"type": "FeatureCollection", "features": state_risk_feats}
                        fig_risk_map = px.choropleth(
                            state_risk_df, geojson=risk_geo, featureidkey='properties.NAME_2',
                            locations='district', color='Update_Ratio',
                            color_continuous_scale="RdYlGn", range_color=[0, 1],
                            hover_name='district', hover_data={'age_5_17':True, 'Update_Ratio':':.1%'},
                            title=f"Biometric Update Efficiency: {risk_map_state}"
                        )
                        fig_risk_map.update_geos(fitbounds="locations", visible=False)
                        fig_risk_map.update_layout(margin={"r":0,"t":30,"l":0,"b":0}, height=400)
                        st.plotly_chart(fig_risk_map, use_container_width=True)
                    else:
                        st.warning(f"Boundary data not found for {risk_map_state}")
            else:
                st.info("No matching risk data for this selection.")
                
        # 2. Bio Activity by Age (Using Filtered Data)
        st.markdown("#### 🧬 Biometric Activity")
        bio_ages = bio_filtered[['bio_age_5_17', 'bio_age_17_']].sum().reset_index()
        bio_ages.columns = ['Age Group', 'Count']
        bio_ages['Age Group'] = bio_ages['Age Group'].replace({'bio_age_5_17': 'School Age (5-17)', 'bio_age_17_': 'Adults (18+)'})
        fig_bar = px.bar(bio_ages, x='Age Group', y='Count', color='Age Group', title=f"Update Activity: {selected_state}")
        st.plotly_chart(fig_bar, use_container_width=True)

    # --- TAB 4: SOLUTION FRAMEWORK ---
    with tabs[3]:
        st.subheader("💡 Solutions")
        
        # Use full_risk from previous block if available, else re-calculate
        # Better to just use the selected scope
        
        st.info(f"Generating recommendations for scope: **{selected_state}**")
        
        if selected_state != "All India":
             # Specific Recommendations
             if not enrol_filtered.empty:
                 avg_update_scope = bio_filtered['Total'].sum() / enrol_filtered['Total'].sum()
                 
                 c1_sol, c2_sol = st.columns(2)
                 with c1_sol:
                     st.metric("Aggregate Update Compliance", f"{avg_update_scope:.1%}")
                 
                 with c2_sol:
                     if avg_update_scope < 0.3:
                         st.error("⚠️ Critical Confidence Gap")
                         st.markdown("- **Action:** Initiate state-wide 'Update Mela'.")
                     else:
                         st.success("✅ Healthy Ecosystem")
                         st.markdown("- **Action:** Focus on maintaining service levels.")
        else:
            st.write("Select a specific state to generate targeted solution frameworks.")

# ==========================================
# 3. ACTIVE GOVT SCHEMES (New)
# ==========================================
elif app_mode == "📜 Active Govt Schemes":
    st.title("📜 Active Government Schemes & Coverage")
    st.markdown("Explore active government schemes linked to Aadhaar across different levels.")
    
    st_sch, center_sch = st.tabs(["🏛️ State-wise Schemes", "🇮🇳 Nationwide Schemes"])
    
    # Mock Data for Schemes
    central_schemes = [
        {"Scheme": "PM-KISAN", "Sector": "Agriculture", "Target": "Farmers", "Benefits": "Income Support (₹6000/yr)"},
        {"Scheme": "Ayushman Bharat (PM-JAY)", "Sector": "Health", "Target": "Low Income Families", "Benefits": "Health Insurance (₹5L)"},
        {"Scheme": "Pradhan Mantri Awas Yojana (PMAY)", "Sector": "Housing", "Target": "Urban/Rural Poor", "Benefits": "Housing Subsidy"},
        {"Scheme": "PM Ujjwala Yojana", "Sector": "Energy", "Target": "BPL Households", "Benefits": "LPG Connection Subsidy"},
        {"Scheme": "MGNREGA", "Sector": "Employment", "Target": "Rural Workforce", "Benefits": "100 Days Employment Guarantee"},
    ]
    
    state_schemes_map = {
        "Andhra Pradesh": ["YSR Rythu Bharosa", "Amma Vodi", "Jagananna Vidya Deevena"],
        "Telangana": ["Rythu Bandhu", "Dalit Bandhu", "Kalyana Lakshmi"],
        "Karnataka": ["Gruha Lakshmi", "Shakti Scheme", "Anna Bhagya"],
        "Maharashtra": ["Mahatma Jyotirao Phule Shetkari Karjmukti Yojana", "Shiv Bhojan Thali"],
        "Tamil Nadu": ["Moovalur Ramamirtham Ammaiyar", "Illam Thedi Kalvi"],
        "Uttar Pradesh": ["Kanya Sumangala Yojana", "Abhyudaya Yojana"],
        "West Bengal": ["Kanyashree Prakalpa", "Swasthya Sathi"],
        "Gujarat": ["Vahli Dikri Yojana", "Kisan Suryodaya Yojana"],
        "Odisha": ["KALIA Scheme", "Biju Swasthya Kalyan Yojana"],
        "Rajasthan": ["Chiranjeevi Health Insurance", "Indira Gandhi Urban Credit Card"],
        "Madhya Pradesh": ["Ladli Behna Yojana", "Sambal Yojana"]
    }
    
    with center_sch:
        st.subheader("🇮🇳 Central Government Schemes")
        st.table(pd.DataFrame(central_schemes))
    
    with st_sch:
        st.subheader("📍 State-Specific Schemes")
        selected_state_sch = st.selectbox("Select State:", sorted(state_schemes_map.keys()))
        
        if selected_state_sch in state_schemes_map:
            schemes = state_schemes_map[selected_state_sch]
            for s in schemes:
                st.markdown(f"""
                <div class="scheme-box">
                    <h4>{s}</h4>
                    <p>Status: <b>Active</b> | Integration: <b>Aadhaar Seeded</b></p>
                </div>
                """, unsafe_allow_html=True)
            
            st.info(f"Showing major flagship schemes for {selected_state_sch}. Database expansion in progress.")
        else:
            st.warning("Data for this state is being aggregated.")

