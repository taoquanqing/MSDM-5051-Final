import streamlit as st
import pandas as pd
from st_aggrid import AgGrid
import re
from io import StringIO

st.set_page_config(
# Basic setting
# Must be declared in the beginning.
    page_title="Group12",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "Welcome to our app! Developed by *TAO Quanqing*, *HU Xinyu*, and *XIAO Jun*."
    }
)
st.header("Data Inquiry System")


def load_file():
    uploaded_file = st.file_uploader(label="Please choose a file", type=["csv"],
                                   help='All functions will be implemented on this dataframe or on default '
                                        'dataframe if nothing is uploaded.')
    if not uploaded_file:
        st.write("First 10 rows of default dataframe 'TDCS_M06A_20190830_080000.csv'")
    if uploaded_file:
        # file_type = str(uploaded_file.name).split('.')[-1]
        st.session_state['df'] = pd.read_csv(uploaded_file, names=['VehicleType', 'DerectionTime_O', 'GantryID_O',
                                                                 'DerectionTime_D', 'GantryID_D', 'TripLength',
                                                                 'TripEnd', 'TripInformation'])
        st.success("Upload successfully!")
        st.write('First 10 rows of uploaded dataframe')
    AgGrid(st.session_state['df'].head(10))




def search_file(df):


    df = df.astype(str)
    st.subheader('Search data')
    with st.form(key='search'):
        left, mid, right = st.columns(3)
        col = left.selectbox("Specify a column", [i for i in df.columns])
        key = mid.text_input(label='Keyword')
        row_num = right.number_input(label='Number of rows to show', value=0, min_value=0, max_value=200, help=
                                  'If input zero all the rows will be returned')
        submit_button = st.form_submit_button(label='Confirm')
        if submit_button:
            if key == '':
                st.warning('Keyword is empty!')
            res = df.loc[df[col].str.contains(key, flags=re.IGNORECASE), :]
            st.write('Result contains %d rows.' % len(res))
            if row_num == 0:
                st.table(res)
            elif row_num <= len(res):
                st.write('First %d rows of result:' % row_num)
                st.table(res.head(row_num))
            else:
                st.write('Number of rows to show is out of range of index.')
                st.table(res)


def sort_file(df):
    st.subheader('Sort data')
    with st.form(key='sort'):
        col = st.selectbox("Specify a column", [i for i in df.columns])
        method = st.selectbox("Choose a sort algorithm", ['quick sort', 'merge sort', 'counting sort'])
        order = st.selectbox('Order', ['descend', 'ascend'])
        submit_button = st.form_submit_button(label='start')
        if submit_button:
            st.error('This is an error', icon="🚨")


# @st.cache
# def convert_df(df):
#     # IMPORTANT: Cache the conversion to prevent computation on every rerun
#     return df.to_csv().encode('utf-8')


if __name__ == '__main__':
    # initialize default dataframe
    if 'df' not in st.session_state:
        default_data = pd.read_csv('TDCS_M06A_20190830_080000.csv', names=['VehicleType', 'DerectionTime_O', 'GantryID_O',
                                                                           'DerectionTime_D', 'GantryID_D', 'TripLength',
                                                                           'TripEnd', 'TripInformation'])
        st.session_state['df'] = default_data
    init_data = True
    # initialize default state of the page
    if 'func' not in st.session_state:
        st.session_state['func'] = 'Load'
    st.session_state['func'] = st.sidebar.selectbox('Choose a module', ['Load', 'Search', 'Sort'])
    if st.session_state['func'] == 'Load':
        load_file()
    elif st.session_state['func'] == 'Search':
        search_file(st.session_state['df'])
    else:
        sort_file(st.session_state['df'])
