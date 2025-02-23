import streamlit as st
import pandas as pd
import altair as alt

# Load and preprocess data
columns = ["Date", "Q-E", "ZN-E", "PH-E", "DBO-E", "DQO-E", "SS-E", "SSV-E", "SED-E", "COND-E", 
           "PH-P", "DBO-P", "SS-P", "SSV-P", "SED-P", "COND-P", "PH-D", "DBO-D", "DQO-D", "SS-D", 
           "SSV-D", "SED-D", "COND-D", "RD-DBO-P", "RD-SS-P", "RD-SED-P", "RD-DBO-S", "RD-DQO-S", 
           "RD-DBO-G", "RD-DQO-G", "RD-SS-G", "RD-SED-G"]

df = pd.read_csv("water-treatment.data", names=columns, na_values="?")
df["BOD_Removal_Efficiency"] = ((df["DBO-E"] - df["DBO-D"]) / df["DBO-E"]) * 100
df_clean = df.dropna(subset=["BOD_Removal_Efficiency"])
df_clean = df_clean[(df_clean["BOD_Removal_Efficiency"] >= 0) & (df_clean["BOD_Removal_Efficiency"] <= 100)].reset_index(drop=True)

# Dashboard title & description
st.title("🚰 Wastewater Treatment Efficiency Dashboard")
st.markdown("Analyzing **Biochemical Oxygen Demand (BOD)** removal efficiency from real wastewater data.")
with st.expander("📝 Executive Summary (Non-Technical)"):
    st.markdown("""
    ### What is this Dashboard about?
    This dashboard measures how effectively a wastewater treatment plant cleans wastewater. Specifically, it focuses on **Biochemical Oxygen Demand (BOD)**, a key indicator of water quality.

    ### Why is BOD Important?
    - **High BOD** means wastewater contains lots of organic matter (pollution).
    - **Low BOD** means the water is clean and safe for releasing into the environment or reusing.

    ### What does Efficiency mean?
    Efficiency shows the percentage of pollutants the plant removes from wastewater.
    
    **Example:**  
    If wastewater entering the plant has a BOD of 200 mg/L, and water leaving has a BOD of 20 mg/L, the efficiency is:

    \[
    Efficiency = \frac{200 - 20}{200} \times 100 = 90\%
    \]

    ### How to use this Dashboard:
    - Use the slider to filter days by efficiency range.
    - View trends in efficiency over time.
    - Check the average efficiency to understand overall plant performance.

    ### What to look for:
    - **Consistent high efficiency (85%-95%)** indicates optimal plant performance.
    - **Low efficiency days** might signal maintenance needs or operational issues.
    
    This helps engineers and decision-makers ensure the plant operates effectively and reliably.
    """)


# Sidebar info panel
with st.sidebar:
    st.header("💡 Project Details")
    st.markdown("""
        **Dataset:** Wastewater treatment data  
        **Goal:** Analyze & visualize BOD efficiency  
        **Adjust the slider below to filter by efficiency.**
    """)

# Metrics summary
avg_efficiency = df_clean['BOD_Removal_Efficiency'].mean()
min_eff, max_eff = df_clean['BOD_Removal_Efficiency'].min(), df_clean['BOD_Removal_Efficiency'].max()

col1, col2 = st.columns(2)
col1.metric("📈 Avg BOD Efficiency", f"{avg_efficiency:.2f}%")
col2.metric("🔄 Efficiency Range", f"{min_eff:.2f}% - {max_eff:.2f}%")

# Slider for filtering data
eff_range = st.slider("Select Efficiency Range (%):", 
                      int(min_eff), int(max_eff), 
                      (int(min_eff), int(max_eff)))

df_filtered = df_clean[
    (df_clean["BOD_Removal_Efficiency"] >= eff_range[0]) &
    (df_clean["BOD_Removal_Efficiency"] <= eff_range[1])
]

st.write(f"Showing {len(df_filtered)} samples within the selected range.")

# Interactive efficiency line chart
chart = alt.Chart(df_filtered.reset_index()).mark_line(point=True).encode(
    x=alt.X('index', title="Sample Number"),
    y=alt.Y('BOD_Removal_Efficiency', title="Efficiency (%)"),
    tooltip=['index', 'BOD_Removal_Efficiency']
).interactive().properties(
    title="Efficiency Over Time",
    width=700,
    height=400
)
st.altair_chart(chart, use_container_width=True)

# Optional: Histogram of Efficiency Distribution
hist_chart = alt.Chart(df_filtered).mark_bar().encode(
    alt.X("BOD_Removal_Efficiency", bin=alt.Bin(maxbins=30), title='Efficiency (%)'),
    y='count()',
    tooltip=['count()']
).properties(
    title="Distribution of Efficiency",
    width=700,
    height=350
)
st.altair_chart(hist_chart, use_container_width=True)

# Optional: Show Raw Data
if st.checkbox("📊 Show Raw Data Table"):
    st.dataframe(df_filtered.style.highlight_max(axis=0))

st.markdown("---")
st.markdown("""
### 🧑‍💻 About Me
Created by [**Fidel Gatimu**](https://github.com/FidelGatimu).

Connect with me on:
- [![GitHub](https://img.shields.io/badge/GitHub-181717?logo=github&logoColor=white)](https://github.com/FidelGatimu)
- [![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/fidelgatimu/)
""")

