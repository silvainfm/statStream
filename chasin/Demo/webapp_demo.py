from docxtpl import DocxTemplate
import docx
import pandas as pd
import streamlit as st
import streamlit_authenticator as stauth
from pathlib import Path
import base64
import os
import json
import pickle
import uuid
import re

# instead of creating the word docs in the app, have em ready in github folder
st.set_page_config(page_title='Demo Dashboard', page_icon=':bar_chart:', layout='wide')

names = ['demo_email']
usernames = ['demo']
passwords = ['demo_acct']

hashed_passwords = stauth.Hasher(passwords).generate()

authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
    'cOOkiE_poStSHowcHasINgAlL', 'keyY1969chasinGthEshoWsS', cookie_expiry_days=15)

name, authentication_status, username = authenticator.login('Login','main')

if authentication_status:
    # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/

    # ---- MAINPAGE ----
    st.title(':bar_chart: Demo Dashboard')
    st.markdown('##')

    # ---- READ EXCEL ----
    @st.cache
    def get_data_from_excel(sheet):
        path_excel = Path(__file__).parents[1] / 'Demo/webapp_demo.xlsx' # demo file 
        df = pd.read_excel(
            io = path_excel,
            engine = 'openpyxl',
            sheet_name = sheet)
        df = df.astype(str)
        df.set_index('Company', inplace=True)
        return df

    dfshow = get_data_from_excel('TotalShow')
    
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
    
    st.dataframe(df_selection)

    selected_indices = st.multiselect('Select rows:', df_selection.index)
    selected_rows = df_selection.loc[selected_indices]
    st.write('### Current Selection', selected_rows)

    # CSV Download buttons 
    st.download_button(
        label = 'Export current selection to Excel', 
        data = selected_rows.to_csv(), 
        file_name='selected_companies.csv', 
        mime='text/csv')

    st.download_button(
        label = 'Export all to Excel', 
        data = dfshow.to_csv(), 
        file_name='all_companies.csv', 
        mime='text/csv')

    keepcols = [
    'Job Title',
    'State',
    'Department Spend',
    'Industry Sector',
    'Employee Count',
    'Annual Sales',
    'Locations ',
    'IT Department Size',
    'IT Security Team Size',
    'Contact Center Seats',
    'Operating System',
    'Current ERP']


# transfers the variables in the df to word doc
    def to_docs(company,df1):
        df = df1[keepcols]
        to_docx = df.loc[[company]]
        compani = company
        state = to_docx['State'].iloc[0]
        job_title = to_docx['Job Title'].iloc[0]
        annual_spend = to_docx['Department Spend'].iloc[0]
        industry = to_docx['Industry Sector'].iloc[0]
        employees = to_docx['Employee Count'].iloc[0]
        revenue = to_docx['Annual Sales'].iloc[0]
        locations = to_docx['Locations '].iloc[0]
        it_count = to_docx['IT Department Size'].iloc[0]
        security_count = to_docx['IT Security Team Size'].iloc[0]
        contact_center = to_docx['Contact Center Seats'].iloc[0]
        op_s = to_docx['Operating System'].iloc[0]
        erp_v = to_docx['Current ERP'].iloc[0]

        context = {'company': compani,
        'state': state, 
        'annual_spend': annual_spend, 
        'job_title': job_title, 
        'industry': industry,
        'employees': employees, 
        'revenue': revenue, 
        'locations': locations, 
        'it_count': it_count, 
        'security_count': security_count,
        'contact_center': contact_center, 
        'op_s': op_s, 
        'erp_v': erp_v}
        

        # import the word template
        path = Path(__file__).parents[1] / 'Demo/demo_template.docx'
        doc = DocxTemplate(path)

        # link the variables
        doc.render(context)
        doc.save(f'{company}_report.docx')
    
        return doc


    def download_button(object_to_download, download_filename, button_text, pickle_it=False):
        """
        Generates a link to download the given object_to_download.

        Params:
        ------
        object_to_download:  The object to be downloaded.
        download_filename (str): filename and extension of file. e.g. mydata.csv,
        some_txt_output.txt download_link_text (str): Text to display for download
        link.
        button_text (str): Text to display on download button (e.g. 'click here to download file')
        pickle_it (bool): If True, pickle file.

        Returns:
        -------
        (str): the anchor tag to download object_to_download

        Examples:
     --------
        download_link(your_df, 'YOUR_DF.csv', 'Click to download data!')
        download_link(your_str, 'YOUR_STRING.txt', 'Click to download text!')

        """
        if pickle_it:
            try:
                object_to_download = pickle.dumps(object_to_download)
            except pickle.PicklingError as e:
                st.write(e)
                return None

        else:
            if isinstance(object_to_download, bytes):
                pass

            elif isinstance(object_to_download, pd.DataFrame):
                object_to_download = object_to_download.to_csv(index=False)

            # Try JSON encode for everything else
            else:
                object_to_download = json.dumps(object_to_download)

        try:
            # some strings <-> bytes conversions necessary here
            b64 = base64.b64encode(object_to_download.encode()).decode()

        except AttributeError as e:
            b64 = base64.b64encode(object_to_download).decode()

        button_uuid = str(uuid.uuid4()).replace('-', '')
        button_id = re.sub('\d+', '', button_uuid)

        custom_css = f""" 
            <style>
                #{button_id} {{
                    background-color: rgb(255, 255, 255);
                    color: rgb(38, 39, 48);
                    padding: 0.25em 0.38em;
                    position: relative;
                    text-decoration: none;
                    border-radius: 4px;
                    border-width: 1px;
                    border-style: solid;
                    border-color: rgb(230, 234, 241);
                    border-image: initial;

                }} 
                #{button_id}:hover {{
                    border-color: rgb(246, 51, 102);
                    color: rgb(246, 51, 102);
                }}
                #{button_id}:active {{
                    box-shadow: none;
                    background-color: rgb(246, 51, 102);
                    color: white;
                    }}
            </style> """

        dl_link = custom_css + f'<a download="{download_filename}" id="{button_id}" href="data:file/txt;base64,{b64}">{button_text}</a><br></br>'

        return dl_link


    # Store word docs in github and allow the user to download from there
    company = st.selectbox('Select Company to export:', df_selection.index)
    file_path = Path(__file__).parents[1] / f'Demo/docs/{company}_report.docx'
    with open(file_path, 'rb') as file:
        btn = st.download_button(
             label='Export to Word Doc',
             data=file,
             file_name=f'{company}_report.docx')

    #button_pdf = st.button('Export to Word doc')
    #if button_pdf: 
        #download_button(to_docs(company, df_selection), f'{company}_report.docx', 'Click here to download Word report')

elif authentication_status == False:
    st.error('Username/password is incorrect')

elif authentication_status == None:
    st.warning('Please enter your username and password')
