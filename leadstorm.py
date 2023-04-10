import pandas as pd
import os
import streamlit as st
import streamlit_authenticator as stauth
from st_aggrid import GridOptionsBuilder, AgGrid, DataReturnMode
import PyPDF2
from io import BytesIO
from PIL import Image

st.set_page_config(page_title='The Leadstorm', layout='wide')

names = ['demo_email', 'rick_sanchez', 'nick', 'mike', 'brandon', 'anton', 'mike5']
usernames = ['demo','rsanchez', 'nwolfe', 'rackspace', 'bmoore', 'aloon', 'mdevine']
passwords = ['demo_acct', 'morty', 'fred', 'rackspace2022', 'rackspace2022b', 'telarus22', 'five922']

admin_names = ['demo_email', 'nick', 'mike']
admin_usernames = ['demo', 'nwolfe', 'rackspace']
admin_passwords = ['demo_acct', 'fred', 'rackspace2022']

hashed_passwords = stauth.Hasher(passwords).generate()

authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
    'cOOkiE_poStSHowcHasINgAlL', 'keyY1969chasinGthEshoWsS', cookie_expiry_days=1)

path = os.path.dirname(__file__)
#my_file = path+ '/leads.png'

st.image('leads.png', width = 400)

name, authentication_status, username = authenticator.login('Login','main')

if authentication_status:

    @st.cache
    def load_data():
        pqt = 'masternewleads.parquet'
        return pd.read_parquet(pqt)
    
    if admin_names.count(name) > 0:
        dfshow = load_data()
        dfex = load_data()
        print("admin")

    else:
        dfshow = load_data()
        dfex = load_data()
        print("non-admin")
    
    st.sidebar.header('Please Filter Here:')
    
    state = st.sidebar.multiselect('Select the State:',
        options=['All', 'AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA',
           'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME',
           'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM',
           'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
           'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY'])

    if 'All' in state:
        state = ['AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA',
                'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME',
                'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM',
                'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
                'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']

    df_selection = dfshow.query('(State == @state)')
    df1_selection = dfex.query('(State == @state)')

    # Removed repeated code by creating a function to apply filters
    def apply_filter(df, column, ascending=True):
        return df.sort_values(by=column, ascending=ascending)

    mobility_score = st.sidebar.radio('Selling Mobility solutions?', ['Yes', 'No'])
    if mobility_score == 'Yes':
        df_selection = apply_filter(df_selection, 'mobility_total_kcount', False)
        df1_selection = apply_filter(df1_selection, 'mobility_total_kcount', False)

    ucaas_score = st.sidebar.radio('Selling Ucaas/Ccaas solutions?', ['Yes', 'No'])
    if ucaas_score == 'Yes':
        df_selection = apply_filter(df_selection, 'ucaas_ccaas_total_kcount', False)
        df1_selection = apply_filter(df1_selection, 'ucaas_ccaas_total_kcount', False)
        
    cloud_score = st.sidebar.radio('Selling Cloud solutions?', ['Yes', 'No'])
    if cloud_score == 'Yes':
        df_selection = apply_filter(df_selection, 'cloud_total_kcount', False)
        df1_selection = apply_filter(df1_selection, 'cloud_total_kcount', False)
        
    cyber_score = st.sidebar.radio('Selling Cybersecurity solutions?', ['Yes', 'No'])
    if cyber_score == 'Yes':
        df_selection = apply_filter(df_selection, 'cyber_total_kcount', False)
        df1_selection = apply_filter(df1_selection, 'cyber_total_kcount', False)

    data_score = st.sidebar.radio('Selling Data Center solutions?', ['Yes', 'No'])
    if data_score == 'Yes':
        df_selection = apply_filter(df_selection, 'data_center_total_kcount', False)
        df1_selection = apply_filter(df1_selection, 'data_center_total_kcount', False)

    gb = GridOptionsBuilder.from_dataframe(df_selection)
    gb.configure_pagination(paginationAutoPageSize=True)  # Add pagination
    gb.configure_side_bar()  # Add a sidebar
    gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children")  # Enable multi-row selection
    gridOptions = gb.build()

    grid_response = AgGrid(
        df_selection,
        gridOptions=gridOptions,
        data_return_mode='AS_INPUT',
        update_mode='MODEL_CHANGED',
        fit_columns_on_grid_load=False,
        theme='streamlit',  # Add theme color to the table
        enable_enterprise_modules=True,  # displays filter if true
        height=350,
        reload_data=True)

    data = grid_response['data']
    selected = grid_response['selected_rows']

    df = pd.DataFrame(selected)  # Pass the selected rows to a new dataframe df

    # Use session_state to store selected df so it doesn't delete on reload
    selected_rows = df
    df1_selected = df
    st.write('### Current Selection', selected_rows)

    export_choice = st.radio('Export the current selection or all companies to Excel?', ('Current Selection', 'All companies'))

    # Create a function to handle download button
    def download_button(label, data, file_name):
        return st.download_button(
            label=label,
            data=data.to_csv(),
            file_name=file_name,
            mime='text/csv')

    if export_choice == 'Current Selection':
        download_button('Export current selection to Excel', df1_selected, 'selected_leads.csv')
    else:
        download_button('Export all companies to Excel', dfex, 'all_leads.csv')

    # Function to merge selected PDFs into one file
    def merge_pdfs(selected_companies):
        merger = PyPDF2.PdfFileMerger()
        for company in selected_companies:
            file_path = f'{path}/npdfs/{company}_report_c.pdf'
            merger.append(file_path)
        merged_pdf = BytesIO()
        merger.write(merged_pdf)
        merged_pdf.seek(0)
        merger.close()
        return merged_pdf

    company = st.selectbox('Select Company to export:', dfshow.Company)
    file_path = f'{path}/npdfs/{company}_report_c.pdf'
    
    with open(file_path, 'rb') as file:
        st.download_button(
            label='Download PDF',
            data=file,
            file_name=f'{path + company}_report_c.pdf')
        
    # Add a download button for downloading selected companies as a PDF (max 10)
    if len(selected_rows) > 0 and len(selected_rows) <= 10:
        merged_pdf = merge_pdfs(selected_rows['Company'])

        st.download_button(
            label='Download selected companies as one PDF',
            data=merged_pdf,
            file_name='selected_companies.pdf',
            mime='application/pdf')
        
    elif len(selected_rows) > 10:
        st.warning("Please select a maximum of 10 companies for PDF download.")
    else:
        st.warning("No companies selected for PDF download.")

elif authentication_status == False:
    st.error('Username/password is incorrect')

elif authentication_status == None:
    st.warning('Please enter your username and password')


# for different permissions based on the user's group
user_groups = {
    'demo': 'group1',
    'rsanchez': 'group1',
    'nwolfe': 'group2',
    'rackspace': 'group2',
    'bmoore': 'group1',
    'aloon': 'group3',
    'mdevine': 'group3'
}

# ... (rest of the code remains the same)
# insert in the code above
#if authentication_status:
    # Get the authenticated user's group
    #user_group = user_groups.get(username)

    # Customize data access based on the user's group
    #if user_group == 'group1':
        #dfshow = pd.read_csv('masternewleads_group1.csv')
        #dfex = pd.read_csv('masternewleads_group1.csv')
    #elif user_group == 'group2':
     #   dfshow = pd.read_csv('masternewleads_group2.csv')
      #  dfex = pd.read_csv('masternewleads_group2.csv')
    #elif user_group == 'group3':
     #   dfshow = pd.read_csv('masternewleads_group3.csv')
      #  dfex = pd.read_csv('masternewleads_group3.csv')
    #else:
     #   st.error('User group not recognized')
      #  st.stop()

