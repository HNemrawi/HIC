import streamlit as st
import numpy as np
import pandas as pd

HTML_HEADER_LOGO = """
            <div style="font-style: italic; color: #808080; text-align: left;">
            <a href="https://icalliances.org/" target="_blank"><img src="https://images.squarespace-cdn.com/content/v1/54ca7491e4b000c4d5583d9c/eb7da336-e61c-4e0b-bbb5-1a7b9d45bff6/Dash+Logo+2.png?format=750w" width="250"></a>
            </div>
            """
HTML_HEADER_TITLE = f'<h2 style="color:#00629b; text-align:center;">Breakdown by Project Name on HIC</h2>'

HTML_FOOTER = """
                <div style="font-style: italic; color: #808080; text-align: center;">
                    <a href="https://icalliances.org/" target="_blank">
                        <img src="https://images.squarespace-cdn.com/content/v1/54ca7491e4b000c4d5583d9c/eb7da336-e61c-4e0b-bbb5-1a7b9d45bff6/Dash+Logo+2.png?format=750w" width="99">
                    </a>
                    DASH™ is a trademark of Institute for Community Alliances.
                </div>
                <div style="font-style: italic; color: #808080; text-align: center;">
                    <a href="https://icalliances.org/" target="_blank">
                        <img src="https://images.squarespace-cdn.com/content/v1/54ca7491e4b000c4d5583d9c/1475614371395-KFTYP42QLJN0VD5V9VB1/ICA+Official+Logo+PNG+%28transparent%29.png?format=1500w" width="99">
                    </a>
                    © 2024 Institute for Community Alliances (ICA). All rights reserved.
                </div>
                    """

column_mapping = {
    'Timestamp': 'Timestamp',
    'Project Name on HIC' : 'HIC_Project',
    #adult_1
    'Gender': 'Gender',
    'Race/Ethnicity': 'Race/Ethnicity',
    'Age Range': 'age_range',
    'Currently Fleeing Domestic/Sexual/Dating Violence': 'DV',
    'Veteran Status': 'vet',
    '**SURVEYOR: Does this person have a disabling condition?': 'disability',
    'How long have you been literally homeless?': 'homeless_long',
    'How long have you been literally homeless this time?': 'homeless_long_this_time',
    'Including this time, how many separate times have you stayed in shelters or on the streets in the past three years?': 'homeless_times',
    'In total, how long did you stay in shelters or on the streets for those times?' : 'homeless_total',
    'Is this the first time you have stayed in a place not meant for human habitation, in an emergency shelter, in a motel/hotel room paid for by an organization, or transitional housing?': 'first_time',
    'Do you have, or have you ever been diagnosed with, any of the listed conditions of long duration?' : 'chronic_condition',
    'Specific length of time literally homeless:' : 'specific_homeless_long',
    'Specific length of time literally homeless this time' : 'specific_homeless_long_this_time',
    #household
    'Is/was anyone in your household staying with you tonight/last night (Wednesday night)?': 'has_company',
    'Which of the following describes the household that is/was with you on Wednesday night?': 'household',
    #adult_2
    'Adult/Parent #2: Gender': 'adult_2_Gender',
    'Adult/Parent #2: Race/Ethnicity': 'adult_2_Race/Ethnicity',
    'Adult/Parent #2: Age Range': 'adult_2_age_range',
    'Adult/Parent #2: Currently Fleeing Domestic/Sexual/Dating Violence': 'adult_2_DV',
    'Adult/Parent #2: Veteran Status': 'adult_2_vet',
    '**SURVEYOR: Does Adult/Parent #2 have a disabling condition?' : 'adult_2_disability',
    'Adult/Parent #2: How long have you been literally homeless?' : 'adult_2_homeless_long',
    'Adult/Parent #2: How long have you been literally homeless this time?': 'adult_2_homeless_long_this_time',
    'Adult/Parent #2: Including this time, how many separate times have you stayed in shelters or on the streets in the past three years?': 'adult_2_homeless_times',
    'Adult/Parent #2: In total, how long did you stay in shelters or on the streets for those times?' : 'adult_2_homeless_total',
    'Adult/Parent #2: Is this the first time you have stayed in a place not meant for human habitation, in an emergency shelter, in a motel/hotel room paid for by an organization, or transitional housing?' : 'adult_2_first_time',
    'Adult/Parent #2: Do you have, or have you ever been diagnosed with, any of the listed conditions of long duration?' : 'adult_2_chronic_condition',
     #adult_3
    'Adult/Parent #3: Gender': 'adult_3_Gender',
    'Adult/Parent #3: Race/Ethnicity': 'adult_3_Race/Ethnicity',
    'Adult/Parent #3: Age Range': 'adult_3_age_range',
    'Adult/Parent #3: Currently Fleeing Domestic/Sexual/Dating Violence': 'adult_3_DV',
    'Adult/Parent #3: Veteran Status': 'adult_3_vet',
    '**SURVEYOR: Does Adult/Parent #2 have a disabling condition?' : 'adult_3_disability',
    'Adult/Parent #3: How long have you been literally homeless?' : 'adult_3_homeless_long',
    'Adult/Parent #3: How long have you been literally homeless this time?': 'adult_3_homeless_long_this_time',
    'Adult/Parent #3: Including this time, how many separate times have you stayed in shelters or on the streets in the past three years?': 'adult_3_homeless_times',
    'Adult/Parent #3: In total, how long did you stay in shelters or on the streets for those times?' : 'adult_3_homeless_total',
    'Adult/Parent #3: Is this the first time you have stayed in a place not meant for human habitation, in an emergency shelter, in a motel/hotel room paid for by an organization, or transitional housing?' : 'adult_3_first_time',
    'Adult/Parent #3: Do you have, or have you ever been diagnosed with, any of the listed conditions of long duration?' : 'adult_3_chronic_condition',
    #children
    'Do you need to add information for a child in the household?': 'child_1',
    'Child #1: Do you have, or have you ever been diagnosed with, any of the listed conditions of long duration?' : 'child_1_chronic_condition',
    'Child #1: Gender': 'child_1_Gender',
    'Child #1: Race/Ethnicity': 'child_1_Race/Ethnicity',
    
    'Do you need to add information for another child?': 'child_2',
    'Child #2: Do you have, or have you ever been diagnosed with, any of the listed conditions of long duration?' : 'child_2_chronic_condition',
    'Child #2: Gender': 'child_2_Gender',
    'Child #2: Race/Ethnicity': 'child_2_Race/Ethnicity',
    
    'Do you need to add information for a third child?': 'child_3',
    'Child #3: Do you have, or have you ever been diagnosed with, any of the listed conditions of long duration?' : 'child_3_chronic_condition',
    'Child #3: Gender': 'child_3_Gender',
    'Child #3: Race/Ethnicity': 'child_3_Race/Ethnicity',
    
    'Do you need to add information for a fourth child?': 'child_4',
    'Child #4: Do you have, or have you ever been diagnosed with, any of the listed conditions of long duration?' : 'child_4_chronic_condition',
    'Child #4: Gender': 'child_4_Gender',
    'Child #4: Race/Ethnicity': 'child_4_Race/Ethnicity',
    
    'Do you need to add information for a fifth child?': 'child_5',
    'Child #5: Do you have, or have you ever been diagnosed with, any of the listed conditions of long duration?' : 'child_5_chronic_condition',
    'Child #5: Gender': 'child_5_Gender',
    'Child #5: Race/Ethnicity': 'child_5_Race/Ethnicity',
    
    'Do you need to add information for a sixth child?': 'child_6',
    'Child #6: Do you have, or have you ever been diagnosed with, any of the listed conditions of long duration?' : 'child_6_chronic_condition',
    'Child #6: Gender': 'child_6_Gender',
    'Child #6: Race/Ethnicity': 'child_6_Race/Ethnicity'}

def setup_header():
    """Set up the header of the Streamlit page."""
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown(HTML_HEADER_LOGO, unsafe_allow_html=True)
    with col2:
        st.markdown(HTML_HEADER_TITLE, unsafe_allow_html=True)

def setup_footer():
    """Set up the footer of the Streamlit page."""
    st.markdown(HTML_FOOTER, unsafe_allow_html=True)

def preprocess_df(df, column_mapping):
    """
    Renames specified columns in a DataFrame based on a mapping and retains only those columns.

    Parameters:
    df (pandas.DataFrame): The DataFrame to be processed.
    column_mapping (dict): A dictionary mapping from old column names to new names.

    Returns:
    pandas.DataFrame: The processed DataFrame with renamed and filtered columns.
    """

    # Strip whitespace from column names and remove duplicate columns
    df.columns = df.columns.str.strip()
    df = df.loc[:, ~df.columns.duplicated(keep='first')]

    # Check for missing columns
    missing_columns = [col for col in column_mapping if col not in df.columns]
    if missing_columns:
        st.error(f"Missing columns in data: {', '.join(missing_columns)}")

    # Filter and rename valid columns
    valid_columns = {k: v for k, v in column_mapping.items() if k in df.columns}
    df = df[valid_columns.keys()]
    df.rename(columns=valid_columns, inplace=True)

    return df

def initialize_count_columns(df):
    """
    Initialize count columns for different age groups in the DataFrame.

    Parameters:
    df (pandas.DataFrame): The DataFrame to be processed.

    Returns:
    pandas.DataFrame: The DataFrame with initialized count columns.
    """
    if not isinstance(df, pd.DataFrame):
        raise ValueError("Input is not a pandas DataFrame.")

    age_group_columns = ['count_adult', 'count_youth', 'count_child_hoh', 'count_child_hh']
    for column in age_group_columns:
        df[column] = 0

    return df

def update_age_group_counts(df, age_related_cols, child_related_cols):
    """
    Update count columns based on age group categories present in the DataFrame.

    Parameters:
    df (pandas.DataFrame): The DataFrame to be updated.
    age_related_cols (list): List of column names related to age groups.
    child_related_cols (list): List of column names related to children in the household.

    Returns:
    pandas.DataFrame: The DataFrame with updated age group counts.
    """
    if not isinstance(df, pd.DataFrame):
        raise ValueError("Input is not a pandas DataFrame.")

    adult_ages = ['25-34', '35-44', '45-54', '55-64', '65+']
    youth_ages = ['18-24']
    child_age = ['Under 18']

    for col in age_related_cols:
        if col not in df.columns:
            continue

        df[col] = df[col].fillna('')
        df['count_adult'] += df[col].isin(adult_ages).astype(int)
        df['count_youth'] += df[col].isin(youth_ages).astype(int)
        df['count_child_hoh'] += df[col].isin(child_age).astype(int)

    for col in child_related_cols:
        if col not in df.columns:
            continue

        df[col] = df[col].fillna('No')
        df['count_child_hh'] += (df[col] == 'Yes').astype(int)

    return df

def count_age_groups(df):
    """
    Count the number of adults, youth, and children in each household.

    Parameters:
    df (pandas.DataFrame): The DataFrame to be processed.

    Returns:
    pandas.DataFrame: The DataFrame with counted age groups.
    """
    if not isinstance(df, pd.DataFrame):
        raise ValueError("Input is not a pandas DataFrame.")

    age_related_cols = [col for col in ['age_range', 'adult_2_age_range', 'adult_3_age_range'] if col in df.columns]
    child_related_cols = [f'child_{i}' for i in range(1, 7) if f'child_{i}' in df.columns]

    df = initialize_count_columns(df)
    df = update_age_group_counts(df, age_related_cols, child_related_cols)

    df['total_person_in_household'] = df['count_adult'] + df['count_youth'] + df['count_child_hoh'] + df['count_child_hh']
    df['youth'] = df['count_adult'].apply(lambda x: 'Yes' if x == 0 else 'No')

    return df

def classify_household_type(df):
    """
    Classify the household based on the age groups present.

    Parameters:
    df (pandas.DataFrame): The DataFrame to be processed.

    Returns:
    pandas.DataFrame: The DataFrame with a new column 'household_type' classifying the household.

    Raises:
    ValueError: If required columns are missing in the DataFrame.
    """

    required_columns = ['count_adult', 'count_youth', 'count_child_hh', 'count_child_hoh']
    if not all(column in df.columns for column in required_columns):
        missing_cols = [col for col in required_columns if col not in df.columns]
        raise ValueError(f"Missing required columns: {', '.join(missing_cols)}")

    # Define conditions for classifying households
    has_adults_or_youth = df['count_adult'] + df['count_youth'] > 0
    has_children = df['count_child_hh'] > 0
    only_children = df['count_child_hoh'] > 0

    # Set up the conditions and choices for classification
    conditions = [
        has_adults_or_youth & has_children,
        has_adults_or_youth & ~has_children,
        only_children
    ]
    choices = ['Household with Children', 'Household without Children', 'Household with Only Children']
    
    # Apply conditions to classify households
    df['household_type'] = np.select(conditions, choices, default='Unknown')

    return df

def create_pivot_table(df):
    """
    Creates a pivot table from the provided dataframe.

    :param data: pandas DataFrame containing the necessary columns.
    :return: Pivot table as a pandas DataFrame.
    """
    df = df.pivot_table(
        index=['HIC_Project', 'household_type'], 
        values='total_person_in_household', 
        aggfunc=['count', 'sum']
    )

    # Renaming the columns for clarity
    df.columns = ['Count Households', 'Number of Clients']

    df.reset_index(inplace=True)
    df.rename(columns={'HIC_Project': 'Project Name on HIC', 'household_type': 'Household Type'}, inplace=True)
    return df

def process_data(df, column_mapping):
    """
    Processes the data through various steps including preprocessing, counting age groups,
    classifying household types"""
    try:
        # Step-by-step data processing
        df = preprocess_df(df, column_mapping)  # Preprocess DataFrame
        df = count_age_groups(df)  # Count age groups
        df = classify_household_type(df)  # Classify household types
        df = create_pivot_table(df)

        return df
    except Exception as e:
        st.error(f"Error in process_data: {e}")
        return pd.DataFrame()