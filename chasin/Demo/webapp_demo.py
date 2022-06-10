from sys import path_importer_cache
from docxtpl import DocxTemplate
import docx
import pandas as pd
import streamlit as st
import streamlit_authenticator as stauth
from pathlib import Path

# instead of creating the word docs in the app, have em ready in github folder
st.set_page_config(page_title='Demo Dashboard', page_icon=':bar_chart:', layout='wide')

# https://github.com/mkhorasani/Streamlit-Authenticator
names = ['demo_email', 'rick_sanchez']
usernames = ['demo','rsanchez']
passwords = ['demo_acct', 'morty']

admin_names = ['demo_email']
admin_usernames = ['demo']
admin_passwords = ['demo_acct']

hashed_passwords = stauth.Hasher(passwords).generate()

authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
    'cOOkiE_poStSHowcHasINgAlL', 'keyY1969chasinGthEshoWsS', cookie_expiry_days=0)

path_image = Path(__file__).parents[1] / f'Demo/chasetek.jpg' # demo file 
st.image(path_image.name)

name, authentication_status, username = authenticator.login('Login','main')

if authentication_status:
    # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/

    # ---- MAINPAGE ----
    st.title(':bar_chart: Demo Dashboard')
    st.markdown('##')

    # ---- READ EXCEL ----
    @st.cache
    def get_data_from_excel(sheet, excelFileName):
        path_excel = Path(__file__).parents[1] / f'Demo/{excelFileName}' # demo file 
        df = pd.read_excel(
            io = path_excel,
            engine = 'openpyxl',
            sheet_name = sheet)
        df = df.astype(str)
        df.set_index('Company', inplace=True)
        return df

    if (admin_names.count(name) > 0):
        dfshow = get_data_from_excel('NewShow', 'pdf_webapp1.xlsx')
        dfex = get_data_from_excel('NewEx', 'pdf_webapp1.xlsx')
        print("admin")
    else:
        dfshow = get_data_from_excel('NewShow', 'pdf_webapp.xlsx')
        dfex = get_data_from_excel('NewEx', 'pdf_webapp.xlsx')
        print("non-admin")
    
    
    
    # ---- SIDEBAR ----
    st.sidebar.header('Please Filter Here:')

    state = st.sidebar.multiselect('Select the State:',
        options=dfshow['State'].unique(),
        default=dfshow['State'].unique() )

    mobility_score = st.sidebar.multiselect('Select the Mobility score:',
        options=dfshow['mobility_ranking'].unique(),
        default=['1', '2', '3', '4'] )

    ucaas_score = st.sidebar.multiselect('Select the Ucaas/Ccaas score:',
        options=dfshow['ucaas_ccaas_ranking'].unique(),
        default=['1', '2', '3', '4'] )

    cyber_score = st.sidebar.multiselect('Select the Cyber score:',
        options=dfshow['cyber_ranking'].unique(),
        default=['1', '2', '3', '4'] )

    data_score = st.sidebar.multiselect('Select the Data Center score:',
        options=dfshow['DATA_Center_ranking'].unique(),
        default=['1', '2', '3', '4'] )
    

    df_selection = dfshow.query('(State == @state) & ((mobility_ranking == @mobility_score) | (ucaas_ccaas_ranking == @ucaas_score) | (cyber_ranking == @cyber_score) | (DATA_Center_ranking == @data_score))')
    df1_selection = dfex.query('(State == @state) & ((mobility_ranking == @mobility_score) | (ucaas_ccaas_ranking == @ucaas_score) | (cyber_ranking == @cyber_score) | (DATA_Center_ranking == @data_score))')

    st.dataframe(df_selection)

    selected_indices = st.multiselect('Select rows:', df_selection.index)
    selected_rows = df_selection.loc[selected_indices]
    df1_selected = df1_selection.loc[selected_indices]
    st.write('### Current Selection', selected_rows)

    # CSV Download buttons 
    export_choice = st.radio('Do you want to export the current selection or all companies to Excel?', ('Current Selection', 'All companies'))

    if export_choice == 'Current Selection':
        st.download_button(
            label = 'Export current selection to Excel', 
            data = df1_selected.to_csv(), 
            file_name='selected_companies.csv', 
            mime='text/csv')
    else:
        st.download_button(
            label = 'Export all companies to Excel', 
            data = dfex.to_csv(), 
            file_name='all_companies.csv', 
            mime='text/csv')

    # Store word docs in github and allow the user to download from there
    company = st.selectbox('Select Company to export:', df_selection.index)
    file_path = Path(__file__).parents[1] / f'Demo/docs1/{company}_report.pdf'
    with open(file_path, 'rb') as file:
        btn = st.download_button(
             label='Export to PDF',
             data=file,
             file_name=f'{company}_report.pdf')

elif authentication_status == False:
    st.error('Username/password is incorrect')

elif authentication_status == None:
    st.warning('Please enter your username and password')

# Improvements

# Provide 2 options:
# export en massse (all selection in one file) (MAX 10)
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