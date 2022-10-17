from sys import path_importer_cache
from docxtpl import DocxTemplate
# import docx
import pandas as pd
import streamlit as st
import streamlit_authenticator as stauth
from pathlib import Path
from docx2pdf import convert
# import fpdf
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode

# instead of creating the word docs in the app, have em ready in github folder
st.set_page_config(page_title='Beta Dashboard', layout='wide')

# https://github.com/mkhorasani/Streamlit-Authenticator
names = ['demo_email', 'rick_sanchez', 'nick', 'mike', 'brandon', 'anton']
usernames = ['demo','rsanchez', 'nwolfe', 'rackspace', 'bmoore', 'aloon']
passwords = ['demo_acct', 'morty', 'fred', 'rackspace2022', 'rackspace2022b', 'telarus22']

admin_names = ['demo_email', 'nick', 'mike']
admin_usernames = ['demo', 'nwolfe', 'rackspace']
admin_passwords = ['demo_acct', 'fred', 'rackspace2022']

hashed_passwords = stauth.Hasher(passwords).generate()

authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
    'cOOkiE_poStSHowcHasINgAlL', 'keyY1969chasinGthEshoWsS', cookie_expiry_days=1)

# path_image = Path(__file__) / 'chasetek.jpg' # demo file 
st.image('images/leadst.png', width = 400)

name, authentication_status, username = authenticator.login('Login','main')

if authentication_status:
    # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/

    # ---- MAINPAGE ----
    st.title('Beta Dashboard')
    st.markdown('##')

    # ---- READ EXCEL ----
    @st.cache
    def get_data_from_excel(sheet, excelFileName):
         path_excel = excelFileName # demo file 
         df = pd.read_excel(
             io = path_excel,
             engine = 'openpyxl',
             sheet_name = sheet)
        
         return df

    if admin_names.count(name) > 0:
        dfshow = pd.read_csv('leads.csv')
        dfex = pd.read_csv('leadd.csv')
        print("admin")

    else:
        dfshow = pd.read_csv('leads.csv')
        dfex = pd.read_csv('leadd.csv')
        print("non-admin")
    
    # ---- SIDEBAR ----
    st.sidebar.header('Please Filter Here:')
    
    # add gov = st.sidebar.radio for gov or not gov 
    # if gov == Yes select rows where email contains .gov 
    # else select rows where not equal 

    state = st.sidebar.multiselect('Select the State:',
        options=['All', 'AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA',
           'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME',
           'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM',
           'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
           'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY'])
    
    if 'All' in state:
        state = ['All', 'AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA',
           'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME',
           'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM',
           'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
           'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']

    df_selection = dfshow.query('(State == @state)')
    df1_selection = dfex.query('(State == @state)')

    mobility_score = st.sidebar.radio('Are you selling Mobility solutions?',
        ['Yes', 'No'])
    if mobility_score == 'Yes':
        df_selection.sort_values(by = ['mobility_total_kcount'], ascending = False, inplace = True)
        df1_selection.sort_values(by = ['mobility_total_kcount'], ascending = False, inplace = True)

    ucaas_score = st.sidebar.radio('Are you selling Ucaas/Ccaas solutions?',
        ['Yes', 'No'])
    if ucaas_score == 'Yes':
        df_selection.sort_values(by = ['ucaas_ccaas_total_kcount'], ascending = False, inplace = True)
        df1_selection.sort_values(by = ['ucaas_ccaas_total_kcount'], ascending = False, inplace = True)
        
    cloud_score = st.sidebar.radio('Are you selling Cloud solutions?',
        ['Yes', 'No'])
    if cloud_score == 'Yes':
        df_selection.sort_values(by = ['cloud_total_kcount'], ascending = False, inplace = True)
        df1_selection.sort_values(by = ['cloud_total_kcount'], ascending = False, inplace = True)
        
    cyber_score = st.sidebar.radio('Are you selling Cybersecurity solutions?',
        ['Yes', 'No'])
    if cyber_score == 'Yes':
        df_selection.sort_values(by = ['cyber_total_kcount'], ascending = False, inplace = True)
        df1_selection.sort_values(by = ['cyber_total_kcount'], ascending = False, inplace = True)

    data_score = st.sidebar.radio('Are you selling Data Center solutions?',
        ['Yes', 'No'])
    if data_score == 'Yes':
        df_selection.sort_values(by = ['data_center_total_kcount'], ascending = False, inplace = True)
        df1_selection.sort_values(by = ['data_center_total_kcount'], ascending = False, inplace = True)

     #Interactive Grid Component
    #https://towardsdatascience.com/make-dataframes-interactive-in-streamlit-c3d0c4f84ccb

    gb = GridOptionsBuilder.from_dataframe(df_selection)
    gb.configure_pagination(paginationAutoPageSize=True) #Add pagination
    gb.configure_side_bar() #Add a sidebar
    gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children") #Enable multi-row selection
    gridOptions = gb.build()

    grid_response = AgGrid(
        df_selection,
        gridOptions=gridOptions,
        data_return_mode='AS_INPUT', 
        update_mode='MODEL_CHANGED', 
        fit_columns_on_grid_load=False,
        theme = 'streamlit', #Add theme color to the table
        enable_enterprise_modules=True, #displays filter if true
        height=350, 
        reload_data=True
    )

    data = grid_response['data']
    selected = grid_response['selected_rows'] 
    df = pd.DataFrame(selected) #Pass the selected rows to a new dataframe df

    #Use session_state to store selected df so it doesnt delete on reload
    # selected_indices = st.multiselect('Select rows:', df_selection.index)
    selected_rows = df #df_selection.loc[selected_indices]
    df1_selected = df # df1_selection.loc[selected_indices]
    st.write('### Current Selection', selected_rows)
    
    # st.dataframe(df_selection)

    # selected_indices = st.multiselect('Select rows:', df_selection.index)
    # selected_rows = df_selection.loc[selected_indices]
    # df1_selected = df1_selection.loc[selected_indices]
    # st.write('### Current Selection', selected_rows)

    # CSV Download buttons 
    export_choice = st.radio('Do you want to export the current selection or all companies to Excel?', ('Current Selection', 'All companies'))

    if export_choice == 'Current Selection':
        st.download_button(
            label = 'Export current selection to Excel', 
            data = df1_selected.to_csv(), 
            file_name='selected_leads.csv', 
            mime='text/csv')
    else:
        st.download_button(
            label = 'Export all companies to Excel', 
            data = dfex.to_csv(), 
            file_name='all_leads.csv', 
            mime='text/csv')

    # Store pdfs in github and allow the user to download from there
    company = st.selectbox('Select Company to export:', dfshow.Company)
    file_path = f'npdfs/{company}_report_c.pdf'
    with open(file_path, 'rb') as file:
        btn = st.download_button(
             label='Export to PDF',
             data=file,
             file_name=f'{company}_report_c.pdf')

    #def to_pdf():
        #companies = dfshow.Company.to_list()
        #for c in companies: 
         #   file_path = f'npdfs/{c}_report_c.pdf'
        #with open(file_path, 'rb') as file:
         #   file2 = st.download_button(
          #      label='Export to PDF',
           #     data=file,
            #    file_name= [f'{c}_report_c.pdf' for c in companies])
        #return file2
    
    #button_bpdf = st.button(label = 'Export you current selection to PDF')
    #if button_bpdf:
     #   to_pdf()

elif authentication_status == False:
    st.error('Username/password is incorrect')

elif authentication_status == None:
    st.warning('Please enter your username and password')


# Improvements

# Provide 2 options:
# export en masse (all selection in one file) (MAX 10)
# export separately 

# Add logo to the page
# Add authentication groups for different data access (Eventually different dashboards)
# Make list objects selectable elements
# Add a way for the user to bulk download the selection or all word docs using current selection
# Make a function for the download button
# use this button format for multiple buttons in a single line
    # col1, col2, col3 = st.columns([1,1,1])

    #with col1:
        #st.button('1')
    #with col2:
        #st.button('2')
    #with col3:
        #st.button('3')
## https://towardsdatascience.com/secure-your-streamlit-app-with-django-bb0bee2a6519
## https://towardsdatascience.com/streamlit-access-control-dae3ab8b7888
## https://medium.com/@theprasadpatil/how-to-create-a-pdf-report-from-excel-using-python-b882c725fcf6
