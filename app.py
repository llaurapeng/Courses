from get_data import setup
import streamlit as st
import os
import time

#start = st.button ('start')
delete = st.button ('Clear')

if delete: 
    st.session_state.clear()
    directory_path = '/Users/mqw/Desktop/Courses Project/courses'

    # Loop through all files and delete them
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)


#SET UP CHROME DRIVER-----------------------------------------------------

with st.spinner ('waiting to set up...'):
    set_up = setup()
    driver = set_up.driver()
    set_up.signin(driver)

st.success ('Done')


#ENTER CLASS------------------------------------------------------------------------
'''
input = st.text_input ('Enter a Class Name', placeholder = '', on_change = None)
input2 = st.text_input ('Enter a Instructor Name', placeholder = '',on_change = None)


set_up.search_course(driver, input, input2)

set_up.open_navig()
results = set_up.course_list()


for prof in results: 
    with st.spinner ('Wating for results:'):
        display = prof ['course'] + ' | ' + prof['full_name'] + ' | ' + prof['semester'] + '|' + prof['resp']
        with st.expander (display):
            #st.write (prof['ratings'])
            ratings_split = prof['ratings'].split ('-->')

            for x in ratings_split:
                st.write (x)
            

            #only wait if file is not already in courses folder
            if prof['pdf_name'] not in st.session_state:
                #st.write ('pdf not downloaded')
                set_up.wait (prof['pdf_name'])
                #GET THE REAL PDF NAME
                pdf_name = set_up.find_file_name (prof ['course'], prof ['full_name'], prof ['pdf_name'])
                print ('not already in session state')

                
            #print course evaluations comments

            set_up.print_pdf_read (st.session_state [prof['pdf_name']])

st.success ('Done')

'''
