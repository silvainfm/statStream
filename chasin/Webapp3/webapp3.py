import pandas as pd
import streamlit as st
import pdfkit as pdf
import streamlit_authenticator as stauth
from pathlib import Path

# be able to select each company
# figure out the score filtering 
# and only show the company name the score and the notes 

st.set_page_config(page_title='Post-Show Dashboard', page_icon=':bar_chart:', layout='wide')

names = ['Chris Wolfe', 'Nick Wolfe', 'Franck Brych', 'Michael M']
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

    # https://discuss.streamlit.io/t/how-to-take-text-input-from-a-user/187/3

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
     'IT',
     'Communication Systems Solutions - Business SMS and MMS',
     'Communication Systems Solutions - Cloud based phone systems (VOIP)',
     'Communication Systems Solutions - Contact Center Optimization',
     'Communication Systems Solutions - Contract Management',
     'Communication Systems Solutions - Contract Negotiations',
     'Communication Systems Solutions - Hosted PBX',
     'Communication Systems Solutions - Outsourced Consulting',
     'Communication Systems Solutions - Telecom Expense Management',
     'Communication Systems Solutions - Unified Communications',
     'Consulting / Outsourcing Solutions - Call Centers',
     'Consulting / Outsourcing Solutions - Digital Worker',
     'Consulting / Outsourcing Solutions - Vendor Evaluations',
     'Cybersecurity Solutions - Application Security - Vulnerability Assessment',
     'Cybersecurity Solutions - Application Security and WAF',
     'Cybersecurity Solutions - Cloud Security',
     'Cybersecurity Solutions - Critical Event Management',
     'Cybersecurity Solutions - Security Awareness Computer-Based Training for end-users',
     'Cybersecurity Solutions - Data Loss Protection',
     'Cybersecurity Solutions - Data Center Security',
     'Cybersecurity Solutions - Data Security',
     'Cybersecurity Solutions - DevOps Security',
     'Cybersecurity Solutions - Disaster / Backup Recovery',
     'Cybersecurity Solutions - Email Security',
     'Cybersecurity Solutions - Employee monitoring - Insider Threat Detection',
     'Cybersecurity Solutions - Encryption',
     'Cybersecurity Solutions - Endpoint detection & response (EDR)',
     'Cybersecurity Solutions - Extended Detection and Response (XDR)',
     'Cybersecurity Solutions - Endpoint prevention',
     'Cybersecurity Solutions - Fraud Prevention / Transaction Security',
     'Cybersecurity Solutions - Identity & Access Management',
     'Cybersecurity Solutions - Multi-factor authentication',
     'Cybersecurity Solutions - Zerotrust',
     'Cybersecurity Solutions - Industrial / IoT Security',
     'Cybersecurity Solutions - Managed Security Service Provider',
     'Cybersecurity Solutions - Mobile App Security',
     'Cybersecurity Solutions - Mobile Security',
     'Cybersecurity Solutions - Network Security - Firewall',
     'Cybersecurity Solutions - Network Security - Intrusion Prevention Systems',
     'Cybersecurity Solutions - Network Security - Monitoring & forensics',
     'Cybersecurity Solutions - Network Security - Unified Threat Management',
     'Cybersecurity Solutions - Outsourced Consulting',
     'Cybersecurity Solutions - Penetration Testing and Simulation',
     'Cybersecurity Solutions - Phishing',
     'Cybersecurity Solutions - Physical Security - Surveillance and Access Control',
     'Cybersecurity Solutions - Privileged Access Management',
     'Cybersecurity Solutions - Ransomware',
     'Cybersecurity Solutions - Risk & Compliance',
     'Cybersecurity Solutions - Security Incident Response',
     'Cybersecurity Solutions - Security Operations Center - SOC as a Service',
     'Cybersecurity Solutions - Security Rating / Benchmarking',
     'Cybersecurity Solutions - SIEM',
     'Cybersecurity Solutions - SOAR - Security Orchestration Automation and Response',
     'Cybersecurity Solutions - Third Party Cyber Risk Management',
     'Cybersecurity Solutions - Threat Intelligence',
     'Cybersecurity Solutions - User behavior monitoring',
     'Cybersecurity Solutions - Web Security',
     'Network Systems Solutions  - MPLS',
     'Network Systems Solutions  - SD-WAN',
     'Network Systems Solutions  - WAN',
     'Consulting / Outsourcing Solutions - APIs',
     'Consulting / Outsourcing Solutions - Cloud Enablement',
     'Consulting / Outsourcing Solutions - Cloud Workload and Migration',
     'Consulting / Outsourcing Solutions - Cybersecurity Services',
     'Consulting / Outsourcing Solutions - IT Service Management (ITSM)',
     'Consulting / Outsourcing Solutions - Technology Lifecycle Management',
     'Consulting / Outsourcing Solutions - Vendor Evaluations']

    # To PDF function
    def to_pdf(df, company, pdf_list):
        # loc the row of the company we want
        pdf1 = df.loc[df['Company'] == company]
        pdf1 = pdf1.set_index('Company Name - Website - State')
        pdf1 = pdf1[pdf_list]

        # transpose df
        pdf1 = pdf1.T

        # convert to html to then convert to pdf
        result = pdf1.to_html(f'{company}_ht.html', render_links = True) # look deeper into pandas tohtml to change the aspect 
        pdf_name = f'{company}_report.pdf'
        pdf.from_file([f'{company}_ht.html'], pdf_name)
        return result

    # figure out if we want the user to be able to select the companies individually or just from the selection
    # add a yes or no line for multiple or only a single company
    # add a multiple choice between the categories for ucaas and all... 
    company_bull = st.radio('Do you want to transfer the current selection to pdf or just one company?', ('Current Selection', '1 Company'))

    if company_bull == 'Current Selection':
        button_pdfy = st.button('Export selection to PDF')
        if button_pdfy:
            companies = df_selection['Company'].to_list()
            for c in companies:
                to_pdf(df1_selection, c, pdf_col_ucaas) 
    else: 
        company = st.text_input('Which company do you want to export to PDF?')
        button_pdf = st.button('Export to PDF')
        if button_pdf: 
            to_pdf(df1_selection, company, pdf_col_ucaas)


elif authentication_status == False:
    st.error('Username/password is incorrect')

elif authentication_status == None:
    st.warning('Please enter your username and password')
