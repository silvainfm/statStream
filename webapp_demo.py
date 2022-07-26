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
names = ['demo_email', 'rick_sanchez', 'nick']
usernames = ['demo','rsanchez', 'nwolfe']
passwords = ['demo_acct', 'morty', 'fred']

admin_names = ['demo_email', 'nick']
admin_usernames = ['demo', 'nwolfe']
admin_passwords = ['demo_acct', 'fred']

hashed_passwords = stauth.Hasher(passwords).generate()

authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
    'cOOkiE_poStSHowcHasINgAlL', 'keyY1969chasinGthEshoWsS', cookie_expiry_days=0)

# path_image = Path(__file__) / 'chasetek.jpg' # demo file 
st.image('images/Statstorm.png', width = 400)

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
        options=dfshow['State'].unique())

    mobility_score = st.sidebar.radio('Are you selling Mobility Solutions?',
        ['Yes', 'No'])
    if mobility_score == 'Yes':
        mob = '1'
    else:
        mob ='0'

    ucaas_score = st.sidebar.radio('Are you selling Ucaas/Ccaas solutions?',
        ['Yes', 'No'])
    if ucaas_score == 'Yes':
        uca = '1'
    else:
        uca ='0'

    cyber_score = st.sidebar.radio('Are you selling Cybersecurity solutions?',
        ['Yes', 'No'])
    if cyber_score == 'Yes':
        cyb = '1'
    else:
        cyb ='0'

    data_score = st.sidebar.radio('Are you selling the Data Center?',
        ['Yes', 'No'])
    if data_score == 'Yes':
        data = '1'
    else:
        data ='0'
    

    df_selection = dfshow.query('(State == @state)')
    #  & ((mobility_ranking == @mob) | (ucaas_ccaas_ranking == @uca) | (cyber_ranking == @cyb) | (DATA_Center_ranking == @data))
    df1_selection = dfex.query('(State == @state)')
    # & ((mobility_ranking == @mob) | (ucaas_ccaas_ranking == @uca) | (cyber_ranking == @cyb) | (DATA_Center_ranking == @data))

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
            file_name='selected_companies.csv', 
            mime='text/csv')
    else:
        st.download_button(
            label = 'Export all companies to Excel', 
            data = dfex.to_csv(), 
            file_name='all_companies.csv', 
            mime='text/csv')

    def to_docs_contC1(compani, df):
        to_docx_c = df.loc[df['Company'] == compani]
        companie = to_docx_c['Company'].iloc[0]
        attendee = to_docx_c['C1 Full Name'].iloc[0]
        job_title_c = to_docx_c['C1 Title'].iloc[0]
        email = to_docx_c['C1 Primary Email'].iloc[0]
        email1 = to_docx_c['C1 Email 1'].iloc[0]
        email2  = to_docx_c['C1 Email 2'].iloc[0]
        linkedin = to_docx_c['C1 LI Profile URL'].iloc[0]
        cell = to_docx_c['C1 Phone 1'].iloc[0]
        phone2 = to_docx_c['C1 Phone 2'].iloc[0]
        attendee2 = to_docx_c['C2 Full Name'].iloc[0]
        job_title_c2 = to_docx_c['C2 Title'].iloc[0]
        email_2 = to_docx_c['C2 Primary Email'].iloc[0]
        email1_2 = to_docx_c['C2 Email 1'].iloc[0]
        email2_2 = to_docx_c['C2 Email 2'].iloc[0]
        linkedin_2 = to_docx_c['C2 LI Profile URL'].iloc[0]
        cell2 = to_docx_c['C2 Phone 1'].iloc[0]
        phone2_2 = to_docx_c['C2 Phone 2'].iloc[0]
        website_c = to_docx_c['Website'].iloc[0]
        phone = to_docx_c['Company Phone 1'].iloc[0]
        address = to_docx_c['HQ Address'].iloc[0]
        state_c = to_docx_c['State'].iloc[0]
        annual_spend_c = to_docx_c['Department Spend'].iloc[0]
        industry_c = to_docx_c['Industry Sector'].iloc[0]
        key_products_c = to_docx_c['Key Products or Services'].iloc[0]
        employees_c = to_docx_c['Employee Count'].iloc[0]
        revenue_c = to_docx_c['Annual Sales'].iloc[0]
        locations_c = to_docx_c['Locations '].iloc[0]
        it_count_c = to_docx_c['IT Department Size'].iloc[0]
        security_count_c = to_docx_c['IT Security Team Size'].iloc[0]
        contact_center_c = to_docx_c['Contact Center Seats'].iloc[0]
        op_s_c = to_docx_c['Operating System'].iloc[0]
        erp_v_c = to_docx_c['Current ERP'].iloc[0]
        cloud_sp_c = to_docx_c['Cloud Service Provider'].iloc[0]
        cyber_res = to_docx_c['Cybersecurity Responsibility'].iloc[0]
        cyber_in = to_docx_c['Cyber Initiatives'].iloc[0]
        cyber_sol = to_docx_c['Cybersecurity Solutions'].iloc[0]
        cyber = to_docx_c['cyber'].iloc[0]
        cloud_res = to_docx_c['Cloud Solutions Responsibility'].iloc[0]
        cloud_in = to_docx_c['Cloud Initiatives'].iloc[0]
        cloud_sol = to_docx_c['Which Cloud Solutions'].iloc[0]
        cloud = to_docx_c['cloud'].iloc[0]
        digital_res = to_docx_c['Digital Responsibility'].iloc[0]
        digital_in = to_docx_c['Digital Initiatives'].iloc[0]
        digital_sol = to_docx_c['Digital Solutions'].iloc[0]
        digital = to_docx_c['digital'].iloc[0]
        data_res = to_docx_c['Data Management Responsibility'].iloc[0]
        data_in = to_docx_c['Data Management Initiatives'].iloc[0]
        data_sol = to_docx_c['Data Management Solutions'].iloc[0]
        data = to_docx_c['data'].iloc[0]
        soft_res = to_docx_c['Software / Application Development Responsibility'].iloc[0]
        soft_in = to_docx_c['Development Initiatives'].iloc[0]
        soft_sol = to_docx_c['Software / Application Development Solutions'].iloc[0]
        soft  = to_docx_c['software'].iloc[0]
        coms_res = to_docx_c['Communication Systems Responsibility'].iloc[0]
        coms_in = to_docx_c['Communication Initiatives'].iloc[0]
        coms_sol = to_docx_c['Communication Systems Solutions'].iloc[0]
        coms = to_docx_c['communication'].iloc[0]
        network_res = to_docx_c['Network Systems Responsibility'].iloc[0]
        network_in = to_docx_c['Network Initiatives'].iloc[0]
        network_sol = to_docx_c['Network Systems Solutions'].iloc[0]
        network = to_docx_c['network'].iloc[0]
        consult_res = to_docx_c['Consulting / Outsourcing Responsibility'].iloc[0]
        consult_in = to_docx_c['Consulting Initiatives'].iloc[0]
        consult_sol = to_docx_c['Consulting / Outsourcing Solutions'].iloc[0]
        consulting = to_docx_c['consulting'].iloc[0]
        it_res = to_docx_c['IT Leadership, Talent Management and Training Responsibility'].iloc[0]
        it_in = to_docx_c['Leadership Initiatives'].iloc[0]
        it_sol = to_docx_c['IT Leadership, Talent Management and Training Solutions'].iloc[0]
        it = to_docx_c['IT'].iloc[0]

        context_c = {'attendee': attendee,
        'job_title': job_title_c,
        'email': email,
        'email1': email1,
        'email2': email2,
        'phone': phone,
        'cell': cell,
        'phone2': phone2,
        'linkedin': linkedin,
        'attendee2': attendee2,
        'job_title_c2': job_title_c2,
        'email_2': email_2,
        'email1_2': email1_2,
        'email2': email2_2,
        'phone2_2': phone2_2,
        'cell2': cell2,
        'linkedin2': linkedin_2,
        'website': website_c,
        'company': companie,
        'address' : address,
        'state': state_c, 
        'annual_spend': annual_spend_c,
        'industry': industry_c,
        'key_products': key_products_c, 
        'employees': employees_c, 
        'revenue': revenue_c, 
        'locations': locations_c, 
        'it_count': it_count_c, 
        'security_count': security_count_c,
        'contact_center': contact_center_c, 
        'op_s': op_s_c, 
        'erp_v': erp_v_c, 
        'cloud_sp': cloud_sp_c, 
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
        doc_c = DocxTemplate('Template_contact_table.docx')

        # link the variables
        doc_c.render(context_c)
        result_path = f'{compani}_report.docx'
        doc_c.save(result_path) 

        return doc_c

    def pdf_conversion(company):
        result_path = f'{company}_report.docx'
        pdf_path = result_path.replace('.docx', '.pdf')
        convert(result_path, pdf_path)
        pdf = pdf_path
        return pdf

    # Store word docs in github and allow the user to download from there
    company = st.selectbox('Select Company to export:', dfshow.index)
    file_path = f'docs1/{company}_report.pdf'
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
## https://medium.com/@theprasadpatil/how-to-create-a-pdf-report-from-excel-using-python-b882c725fcf6
