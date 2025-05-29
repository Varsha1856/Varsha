import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- Freemium control ---
if "first_visit" not in st.session_state:
    st.session_state["first_visit"] = datetime.now()
    st.session_state["is_paid"] = False

def days_since_first_visit():
    return (datetime.now() - st.session_state["first_visit"]).days

# --- App Header ---
st.set_page_config(page_title="DataCompare Pro by Varsha", layout="wide")
st.markdown("## 📊 DataCompare Pro by Varsha")
st.markdown("Easily compare two datasets column by column. Upload, choose columns, and analyze differences.")
st.markdown("---")

# --- Upload Section ---
col1, col2 = st.columns(2)

with col1:
    file1 = st.file_uploader("🔹 Upload First CSV or Excel", type=["csv", "xlsx"], key="file1")
with col2:
    file2 = st.file_uploader("🔸 Upload Second CSV or Excel", type=["csv", "xlsx"], key="file2")

def load_file(file):
    if file.name.endswith('.csv'):
        return pd.read_csv(file)
    else:
        return pd.read_excel(file)

if file1 and file2:
    df1 = load_file(file1)
    df2 = load_file(file2)

    st.success("✅ Files uploaded successfully!")

    # --- Column Selection ---
    st.markdown("### 🔍 Select columns to compare")
    cols1 = st.multiselect("Choose columns from File 1", df1.columns.tolist(), key="cols1")
    cols2 = st.multiselect("Choose columns from File 2", df2.columns.tolist(), key="cols2")

    if len(cols1) != len(cols2):
        st.warning("⚠️ Please select the same number of columns in both files.")
    elif len(cols1) > 0:
        # --- Freemium Limitation ---
        if days_since_first_visit() > 3 and not st.session_state["is_paid"]:
            st.error("🚫 Trial expired! Please upgrade to a paid plan to continue using this feature.")
            st.stop()

        # --- Data Comparison ---
        st.markdown("### 📋 Comparison Result")

        df1_sel = df1[cols1].reset_index(drop=True)
        df2_sel = df2[cols2].reset_index(drop=True)

        comparison_result = pd.DataFrame()
        for i in range(len(cols1)):
            comparison_result[f"{cols1[i]} vs {cols2[i]}"] = df1_sel.iloc[:, i] == df2_sel.iloc[:, i]

        result_display = comparison_result.applymap(lambda x: "✅" if x else "❌")
        st.dataframe(result_display)

        # --- Summary ---
        st.markdown("### 📈 Summary")
        total = comparison_result.size
        matches = comparison_result.values.sum()
        st.success(f"✅ Matched: {matches} / {total}")
        st.error(f"❌ Mismatched: {total - matches}")

        # --- Watermark ---
        st.markdown("---")
        st.markdown("**Made with ❤️ by Varsha**", unsafe_allow_html=True)
else:
    st.info("⬆️ Please upload both files to begin comparison.")
