import pandas as pd
import streamlit as st
import streamlit_authenticator as stauth
from pathlib import Path
from docxtpl import DocxTemplate
import docx

# figure out the score filtering 

st.set_page_config(page_title='Post-Show Dashboard', page_icon=':bar_chart:', layout='wide')

names = ['Chris', 'Nick', 'Franck', 'Michael']
usernames = ['cwolfe','nwolfe', 'fbrych', 'mmarlowe']
passwords = ['1968','1999', '1996', '2022']

hashed_passwords = stauth.hasher(passwords).generate()

authenticator = stauth.authenticate(names,usernames,hashed_passwords,
    'cookie_postshowchasing','keyY1963chasinGthEshoW',cookie_expiry_days=15)

name,authentication_status = authenticator.login('Login','main')

if authentication_status:
    # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/

    # ---- MAINPAGE ----
    st.title(':bar_chart: Post-Show Dashboard')
    st.markdown('##')

    # ---- READ EXCEL ----
    @st.cache
    def get_data_from_excel(sheet):
        path_excel = Path(__file__).parents[1] / 'Webapp3/pdf_webapp.xlsx'
        df = pd.read_excel(
            io = path_excel,
            engine = 'openpyxl',
            sheet_name = sheet)
        df = df.astype(str)
        df.set_index('Company', inplace=True)
        return df

    # add if user gets overall or only one of the categories or 2...
    # use second df for exports with all of the data
    dfshow = get_data_from_excel('TotalShow')
    dfex = get_data_from_excel('TotalEx')
    newshow = get_data_from_excel('NewShow')
    newex = get_data_from_excel('NewEx')

    # ---- SIDEBAR ----
    st.sidebar.header('Please Filter Here:')
    
    new = st.sidebar.radio('Only companies new in this show?', ('Yes', 'No'))

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
    
    if new == 'Yes':
        df_selection = newshow.query('(State == @state) | (mobility_ranking == @mobility_score) | (ucaas_ccaas_ranking == @ucaas_score) | (cyber_ranking == @cyber_score) | (DATA_Center_ranking == @data_score)')
    else:
        df_selection = dfshow.query('(State == @state) | (mobility_ranking == @mobility_score) | (ucaas_ccaas_ranking == @ucaas_score) | (cyber_ranking == @cyber_score) | (DATA_Center_ranking == @data_score)')

    if new == 'Yes':
        df1_selection = newex.query('(State == @state) | (mobility_ranking == @mobility_score) | (ucaas_ccaas_ranking == @ucaas_score) | (cyber_ranking == @cyber_score) | (DATA_Center_ranking == @data_score)')
    else: 
        df1_selection = dfex.query('(State == @state) | (mobility_ranking == @mobility_score) | (ucaas_ccaas_ranking == @ucaas_score) | (cyber_ranking == @cyber_score) | (DATA_Center_ranking == @data_score)')
    
    # show the filtered dataframe
    st.dataframe(df_selection)
    
    # selecting rows feature and showing the selected rows for billing purposes
    selected_indices = st.multiselect('Select rows:', df_selection.index)
    selected_rows = df_selection.loc[selected_indices]
    st.write('### Selected Rows', selected_rows)

    # CSV Download buttons 
    export_choice = st.radio('Do you want to export the current selection or all companies to Excel?', ('Current Selection', 'All companies'))
    
    if export_choice == 'Current Selection':
        st.download_button(
            label = 'Export current selection to Excel', 
            data = df1_selection.to_csv(), 
            file_name='selected_companies.csv', 
            mime='text/csv')
    else:
        st.download_button(
            label = 'Export all companies to Excel', 
            data = df1_selection.to_csv(), 
            file_name='all_companies.csv', 
            mime='text/csv')

    # Store word docs in github and allow the user to download from there
    company = st.selectbox('Select Company to export:', df_selection.index)
    file_path = Path(__file__).parents[1] / f'Webapp3/docs/{company}_report.docx'
    with open(file_path, 'rb') as file:
        wrdbtn = st.download_button(
             label='Export to Word Doc',
             data=file,
             file_name=f'{company}_report.docx')
    
# add a multiple choice between the categories for ucaas and all... 

elif authentication_status == False:
    st.error('Username/password is incorrect')

elif authentication_status == None:
    st.warning('Please enter your username and password')
