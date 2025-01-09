import streamlit as st
from upload import DataLoading
import pandas as pd
from helper import *  # Assuming process_data is defined here
import openpyxl

# Set page configuration
st.set_page_config(page_title="HIC_Project", page_icon=":house:", layout="wide")

def main():
    # Implementation selection
    implementation = st.selectbox(
        "Select Implementation:",
        ("", "Dashgreatlakes", "New England"),
        index=0
    )

    # Ensure implementation is selected before proceeding
    if implementation:
        # Set column mapping based on the selected implementation
        if implementation == "Dashgreatlakes":
            column_mapping = DASH_column_mapping
        elif implementation == "New England":
            column_mapping = NE_column_mapping

        setup_header()

        # Create tabs for Upload and Data Display
        tab1, tab2 = st.tabs(["File Upload", "Data Display and Download"])

        # Tab for file uploads
        with tab1:
            upload_dict = DataLoading.load_and_display_data()

        processed_dfs = {}
        for file_type, df in upload_dict.items():
            if df is not None:
                processed_dfs[file_type] = process_data(df, column_mapping)

        # Tab for displaying processed data
        with tab2:
            for file_type, processed_df in processed_dfs.items():
                st.subheader(f"{file_type} Data")
                st.dataframe(processed_df)

        setup_footer()

if __name__ == "__main__":
    main()
