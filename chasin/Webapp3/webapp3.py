import pandas as pd
import streamlit as st
import streamlit_authenticator as stauth
from pathlib import Path
from docxtpl import DocxTemplate
import docx

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
        df_selection = newshow.query('(State == @state) | (mobility_ranking == @mobility_score) | (ucaas_ccaas_ranking == @ucaas_score) | (cyber_ranking == @cyber_score) | (DATA_Center_ranking == @data_score)')
    else:
        df_selection = dfshow.query('(State == @state) | (mobility_ranking == @mobility_score) | (ucaas_ccaas_ranking == @ucaas_score) | (cyber_ranking == @cyber_score) | (DATA_Center_ranking == @data_score)')

    if new == 'Yes':
        df1_selection = newex.query('(State == @state) | (mobility_ranking == @mobility_score) | (ucaas_ccaas_ranking == @ucaas_score) | (cyber_ranking == @cyber_score) | (DATA_Center_ranking == @data_score)')
    else: 
        df1_selection = dfex.query('(State == @state) | (mobility_ranking == @mobility_score) | (ucaas_ccaas_ranking == @ucaas_score) | (cyber_ranking == @cyber_score) | (DATA_Center_ranking == @data_score)')
    
    st.dataframe(df_selection)

    # CSV Download button 
    st.download_button(label = 'Export current selection to CSV', data = df1_selection.to_csv(), mime='text/csv')

    keepcols = ['Company',
    'Job Title',
    'State',
    'Department Spend',
    'Attendee Location',
    'Industry Sector',
    'Key Products or Services',
    'Employee Count',
    'Annual Sales',
    'Locations ',
    'IT Department Size',
    'IT Security Team Size',
    'Contact Center Seats',
    'Operating System',
    'Current ERP',
    'Cloud Service Provider',
    'Cybersecurity Responsibility',
    'Cyber Initiatives',
    'Cybersecurity Solutions',
    'cyber',
    'Cloud Solutions Responsibility',
    'Cloud Initiatives',
    'Which Cloud Solutions',
    'cloud',
    'Digital Responsibility',
    'Digital Initiatives',
    'Digital Solutions',
    'digital',
    'Data Management Responsibility',
    'Data Management Initiatives',
    'Data Management Solutions',
    'data',
    'Software / Application Development Responsibility',
    'Development Initiatives',
    'Software / Application Development Solutions',
    'software',
    'Communication Systems Responsibility',
    'Communication Initiatives',
    'Communication Systems Solutions',
    'communication',
    'Network Systems Responsibility',
    'Network Initiatives',
    'Network Systems Solutions',
    'network',
    'Consulting / Outsourcing Responsibility',
    'Consulting Initiatives',
    'Consulting / Outsourcing Solutions',
    'consulting',
    'IT Leadership, Talent Management and Training Responsibility',
    'Leadership Initiatives',
    'IT Leadership, Talent Management and Training Solutions',
    'IT']

# transfers the variables in the df to word doc
    def to_docs(company,df1):
        df = df1[keepcols]
        to_docx = df.loc[df['Company'] == company]
        compani = company
        state = to_docx['State'].iloc[0]
        job_title = to_docx['Job Title'].iloc[0]
        annual_spend = to_docx['Department Spend'].iloc[0]
        industry = to_docx['Industry Sector'].iloc[0]
        key_products = to_docx['Key Products or Services'].iloc[0]
        employees = to_docx['Employee Count'].iloc[0]
        revenue = to_docx['Annual Sales'].iloc[0]
        locations = to_docx['Locations '].iloc[0]
        it_count = to_docx['IT Department Size'].iloc[0]
        security_count = to_docx['IT Security Team Size'].iloc[0]
        contact_center = to_docx['Contact Center Seats'].iloc[0]
        op_s = to_docx['Operating System'].iloc[0]
        erp_v = to_docx['Current ERP'].iloc[0]
        cloud_sp = to_docx['Cloud Service Provider'].iloc[0]
        cyber_res = to_docx['Cybersecurity Responsibility'].iloc[0]
        cyber_in = to_docx['Cyber Initiatives'].iloc[0]
        cyber_sol = to_docx['Cybersecurity Solutions'].iloc[0]
        cyber = to_docx['cyber'].iloc[0]
        cloud_res = to_docx['Cloud Solutions Responsibility'].iloc[0]
        cloud_in = to_docx['Cloud Initiatives'].iloc[0]
        cloud_sol = to_docx['Which Cloud Solutions'].iloc[0]
        cloud = to_docx['cloud'].iloc[0]
        digital_res = to_docx['Digital Responsibility'].iloc[0]
        digital_in = to_docx['Digital Initiatives'].iloc[0]
        digital_sol = to_docx['Digital Solutions'].iloc[0]
        digital = to_docx['digital'].iloc[0]
        data_res = to_docx['Data Management Responsibility'].iloc[0]
        data_in = to_docx['Data Management Initiatives'].iloc[0]
        data_sol = to_docx['Data Management Solutions'].iloc[0]
        data = to_docx['data'].iloc[0]
        soft_res = to_docx['Software / Application Development Responsibility'].iloc[0]
        soft_in = to_docx['Development Initiatives'].iloc[0]
        soft_sol = to_docx['Software / Application Development Solutions'].iloc[0]
        soft  = to_docx['software'].iloc[0]
        coms_res = to_docx['Communication Systems Responsibility'].iloc[0]
        coms_in = to_docx['Communication Initiatives'].iloc[0]
        coms_sol = to_docx['Communication Systems Solutions'].iloc[0]
        coms = to_docx['communication'].iloc[0]
        network_res = to_docx['Network Systems Responsibility'].iloc[0]
        network_in = to_docx['Network Initiatives'].iloc[0]
        network_sol = to_docx['Network Systems Solutions'].iloc[0]
        network = to_docx['network'].iloc[0]
        consult_res = to_docx['Consulting / Outsourcing Responsibility'].iloc[0]
        consult_in = to_docx['Consulting Initiatives'].iloc[0]
        consult_sol = to_docx['Consulting / Outsourcing Solutions'].iloc[0]
        consulting = to_docx['consulting'].iloc[0]
        it_res = to_docx['IT Leadership, Talent Management and Training Responsibility'].iloc[0]
        it_in = to_docx['Leadership Initiatives'].iloc[0]
        it_sol = to_docx['IT Leadership, Talent Management and Training Solutions'].iloc[0]
        it = to_docx['IT'].iloc[0]

        context = {'company': compani,
        'state': state, 
        'annual_spend': annual_spend, 
        'job_title': job_title, 
        'industry': industry,
        'key_products': key_products, 
        'employees': employees, 
        'revenue': revenue, 
        'locations': locations, 
        'it_count': it_count, 
        'security_count': security_count,
        'contact_center': contact_center, 
        'op_s': op_s, 
        'erp_v': erp_v, 
        'cloud_sp': cloud_sp, 
        'cyber_res': cyber_res, 
        'cyber_in': cyber_in, 
        'cyber_sol': cyber_sol, 
        'cyber': cyber, 
        'cloud_res': cloud_res, 
        'cloud_in': cloud_in, 
        'cloud_sol': cloud_sol, 
        'cloud': cloud, 
        'digital_res': digital_res, 
        'digital_in': digital_in, 
        'digital_sol': digital_sol, 
        'digital': digital, 
        'data_res': data_res, 
        'data_in': data_in, 
        'data_sol': data_sol, 
        'data': data, 
        'soft_res': soft_res, 
        'soft_in': soft_in, 
        'soft_sol': soft_sol, 
        'soft': soft,
        'coms_res': coms_res, 
        'coms_in': coms_in, 
        'coms_sol': coms_sol, 
        'coms': coms, 
        'network_res': network_res, 
        'network_in': network_in, 
        'network_sol': network_sol, 
        'network': network, 
        'consult_res': consult_res, 
        'consult_in': consult_in, 
        'consult_sol': consult_sol, 
        'consulting': consulting, 
        'it_res': it_res, 
        'it_in': it_in, 
        'it_sol': it_sol, 
        'IT': it}

        # import the word template
        path = path_excel = Path(__file__).parents[1] / 'Webapp3/Template.docx'
        doc = DocxTemplate(path)

        # link the variables
        doc.render(context)
        doc.save(f'{company}_report.docx')
    
        return doc.save(f'{company}_report.docx')


    # figure out if we want the user to be able to select the companies individually or just from the selection
    # add a yes or no line for multiple or only a single company
    # add a multiple choice between the categories for ucaas and all... 

elif authentication_status == False:
    st.error('Username/password is incorrect')

elif authentication_status == None:
    st.warning('Please enter your username and password')
