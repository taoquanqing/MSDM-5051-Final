import streamlit as st
import pandas as pd
from st_aggrid import AgGrid
import re
from sort_algorithm_1 import *
import time

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
    uploaded_file = st.file_uploader(label="Please choose a file (first row will be taken as header)", type=["csv"],
                                     help='All functions will be implemented on this dataframe or on default '
                                          'dataframe if upload nothing.')
    default = st.button('Use default dataframe')
    if uploaded_file:
        # file_type = str(uploaded_file.name).split('.')[-1]
        st.session_state['df'] = pd.read_csv(uploaded_file, header=0)
        st.success("Upload successfully!")
    if default:
        try:
            st.session_state['df'] = pd.read_csv('TDCS_M06A_20190830_080000.csv',
                                                 names=['VehicleType', 'DerectionTime_O', 'GantryID_O',
                                                        'DerectionTime_D', 'GantryID_D', 'TripLength',
                                                        'TripEnd', 'TripInformation'])
        except:
            st.warning("No required CSV file!")
    if st.session_state['df'] is not None:
        df = st.session_state['df']
        i = st.slider('Slide to preview the data', 0, len(df)-10, 0)
        st.caption(f'{i+1}~{i+10} rows of dataframe:')
        AgGrid(df.iloc[i:i+10, :])


def search_file(df):
    df = df.astype(str)
    st.subheader('Search data')
    with st.form(key='search'):
        l, r = st.columns(2)
        col = l.selectbox("Specify a column", [i for i in df.columns])
        key = r.text_input(label='Keyword')
        submit_button = st.form_submit_button(label='Confirm')
        if submit_button:
            if key == '':
                st.warning('Keyword is empty!')
            else:
                res = df.loc[df[col].str.contains(key, flags=re.IGNORECASE), :]
                st.session_state['found'] = res
    if st.session_state['found'] is not None:
        res_copy = st.session_state['found']
        st.caption('%d rows are found.' % len(res_copy))
        i = st.slider('Slide to view the result', 0, len(res_copy) - 10, 0)
        st.caption(f'{i + 1}~{i + 10} rows of result:')
        AgGrid(res_copy.iloc[i:i + 10, :])

        st.download_button(
            label="Download result as CSV file",
            data=pd.DataFrame(res_copy).to_csv().encode('utf-8'),
            file_name='result.csv',
            mime='text/csv',
        )


def sort_file(df):
    st.subheader('Sort data')
    download = False
    with st.form(key='sort'):
        l0, r0 = st.columns(2)
        l1, r1 = st.columns(2)
        col = l0.selectbox("Specify a column", [i for i in df.columns])
        method_list = ['quick sort', 'merge sort', 'count sort', 'insertion sort',
                       'bubble sort', 'heap sort', 'BST sort', 'AVL sort']
        method = r0.selectbox("Choose a sort algorithm", method_list)
        subset = r1.selectbox('Subset', ['100%', '75%', '50%', '25%', '10%'])
        order = l1.selectbox('Order', ['ascend', 'descend'])
        submit_button = st.form_submit_button(label='start')
        if submit_button:
            subset_int = int(subset.split('%')[0])
            length = int(subset_int / 100 * len(df))
            arr = df.loc[:length, col].to_list()
            start = time.time()
            if method == method_list[0]:
                res = quick_sort(arr)
            elif method == method_list[1]:
                res = merge_sort(arr)
            elif method == method_list[2]:
                res = count_sort(arr)
            elif method == method_list[3]:
                res = insertion_sort(arr)
            elif method == method_list[4]:
                res = bubble_sort(arr)
            elif method == method_list[5]:
                res = heap_sort(arr)
            elif method == method_list[6]:
                res = BST_sort(arr)
            elif method == method_list[7]:
                res = AVL_sort(arr)
            elapse_time = time.time() - start
            if order == 'descend':
                res = res[::-1]

            # format the result
            st.caption('Elapsed time: %.5fs' % elapse_time)
            n = min(10, len(res))
            s = 'First %d data of result: ' % n
            for i in range(n):
                s += str(res[i]) + '&emsp;'
            st.markdown(s)
            with st.expander("See All the results"):
                st.write(res)
            download = True
    if download:
        st.download_button(
            label="Download result as CSV file",
            data=pd.DataFrame(res, columns=['result']).to_csv().encode('utf-8'),
            file_name='result.csv',
            mime='text/csv',
        )


if __name__ == '__main__':
    if 'found' not in st.session_state:
        st.session_state['found'] = None
    # initialize default dataframe
    if 'df' not in st.session_state:
        st.session_state['df'] = None
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
