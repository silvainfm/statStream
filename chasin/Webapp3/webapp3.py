import pandas as pd
import streamlit as st
import pdfkit as pdf
import streamlit_authenticator as stauth
from pathlib import Path

# be able to select each company
# figure out the score filtering 
# and only show the company name the score and the notes 

st.set_page_config(page_title='Post-Show Dashboard', page_icon=':bar_chart:', layout='wide')

names = ['Chris', 'Nick', 'Franck', 'Michael']
usernames = ['cwolfe','nwolfe', 'fbrych', 'mmarlowe']
passwords = ['1968','1999', '1996', '2022']

hashed_passwords = stauth.hasher(passwords).generate()

authenticator = stauth.authenticate(names,usernames,hashed_passwords,
    'cookie_postshowchasing','keyY1963chasinGthEshoW',cookie_expiry_days=15)

name, authentication_status = authenticator.login('Login','main')

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
        return df

     # add if user gets overall or only one of the categories or 2...
    # use second df for exports with all of the data
    dfshow = get_data_from_excel('TotalShow')
    dfex = get_data_from_excel('TotalEx')
    newshow = get_data_from_excel('NewShow')
    newex = get_data_from_excel('NewEx')
    #ucaas = get_data_from_excel('Ucaas_Ccaas')
    #data_c = get_data_from_excel('DATA Center')
    #mobility = get_data_from_excel('Mobility')

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
        df_selection = newshow.query('(State == @state) & (mobility_ranking == @mobility_score) & (ucaas_ccaas_ranking == @ucaas_score) & (cyber_ranking == @cyber_score) & (DATA_Center_ranking == @data_score)')
    else:
        df_selection = dfshow.query('(State == @state) & (mobility_ranking == @mobility_score) & (ucaas_ccaas_ranking == @ucaas_score) & (cyber_ranking == @cyber_score) & (DATA_Center_ranking == @data_score)')

    if new == 'Yes':
        df1_selection = newex.query('(State == @state) & (mobility_ranking == @mobility_score) & (ucaas_ccaas_ranking == @ucaas_score) & (cyber_ranking == @cyber_score) & (DATA_Center_ranking == @data_score)')
    else: 
        df1_selection = dfex.query('(State == @state) & (mobility_ranking == @mobility_score) & (ucaas_ccaas_ranking == @ucaas_score) & (cyber_ranking == @cyber_score) & (DATA_Center_ranking == @data_score)')
    
    st.dataframe(df_selection)

    # CSV Download button 
    st.download_button(label = 'Export current selection to CSV', data = df1_selection.to_csv(), mime='text/csv')

    pdf_col_ucaas = ['Industry Sector - Job Title', 
     'Operating System', 
     'Cloud Service Provider', 
     'Current ERP',
     'IT Department Size - IT Security Team Size - Department Spend',
     'cyber',
     'cloud',
     'digital',
     'data',
     'software',
     'communication',
     'network',
     'consulting',
     'IT']
    
    # figure out if we want the user to be able to select the companies individually or just from the selection
    #company_bull = st.radio('Do you want to transfer the current selection to pdf or just one company?', ('Current Selection', '1 Company'))

    #if company_bull == 'Current Selection':
        #button_pdfy = st.button('Export selection to PDF')
        #if button_pdfy:
            #companies = df_selection['Company'].to_list()
            #for c in companies:
               # to_pdf(df1_selection, c, pdf_col_ucaas) 
    #else: 
       # company = st.text_input('Which company do you want to export to PDF?')
        #button_pdf = st.button('Export to PDF')
       # if button_pdf: 
          #  to_pdf(df1_selection, company, pdf_col_ucaas)


elif authentication_status == False:
    st.error('Username/password is incorrect')

elif authentication_status == None:
    st.warning('Please enter your username and password')
