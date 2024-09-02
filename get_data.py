from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType

import driver
import streamlit as st
import pdfplumber
import os
import time


class setup:
    
    curr_dir = os.getcwd()
    dir = curr_dir + '/courses'


    def __init__(self):
        '''
        curr_dir = os.getcwd()
        dir = curr_dir + '/courses'
        

        chrome_options = Options()
        chrome_options.add_experimental_option ('prefs', {
        'download.default_directory': f'{dir}',
        "download.prompt_for_download": False,   
        "profile.content_settings.exceptions.automatic_downloads.*.setting": 1 
        })
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--no-sandbox")  # Optional: For certain environments
        chrome_options.add_argument("--disable-dev-shm-usage")  # Optional: For certain environments
        # Specify the path to your ChromeDriver

        path = curr_dir + '/chromedriver'
        st.write (path)
        service = Service(path)

        self.driver = webdriver.Chrome (service = service, options = chrome_options)

        
        '''

        options = webdriver.ChromeOptions()
        #options.add_argument('--headless')
        #ptions.add_argument('--disable-gpu')
        #options.add_argument('--window-size=1920,1200')
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                                  options=options)
  
        self.driver.get ('https://eval-duke.evaluationkit.com/Respondent')
    
    #SIGN IN ----------------------------------------------------------------------
    def signin (self): 
        username = 'lp244'
        password = 'Dolphinldp2004!'
        self.driver.find_element (By.ID, 'j_username').send_keys (username)
        self.driver.find_element (By.ID, 'j_password').send_keys (password)
        self.driver.find_element (By.ID, 'Submit').click()

        print ('success')

        self.driver.get ('https://eval-duke.evaluationkit.com/Report/Public/Results?Course=Writing+101&Instructor=&TermId=&Year=&AreaId=&QuestionKey=780869-0&Search=true')



    #SEARCH FOR COURSE----------------------------------------------------------------------
    def search_course (self, course_val, instructor):

        if course_val == '':
            course = '&Search=true'
        else: 
            course = course_val
            course = course.replace (' ', '+')


        if instructor == '':
            instructor = '&Search=true'
        else:
            instructor = instructor.replace (' ', '+')


        self.url = f'https://eval-duke.evaluationkit.com/Report/Public/Results?Course={course}&Instructor={instructor}'

        course_field = self.driver.find_element(By.CSS_SELECTOR, '.Course').send_keys(course)
        instructor_field = self.driver.find_element(By.ID, 'Instructor').send_keys (instructor)

        self.driver.find_element (By.CSS_SELECTOR, '.btn.btn-primary.sr-search-btn-results').click()
        self.driver.get (self.url)

    
    #OPEN NAVIGATION ----------------------------------------------------------------------
    def open_navig (self):
        divs = self.driver.find_elements (By.CSS_SELECTOR, '.sr-dataitem.panel.panel-default')

        for index, div in enumerate (divs):
            try: 
                expand2 = div.find_element (By.CSS_SELECTOR, '.accordion-toggle.getQuestions.collapsed')
                expand2.click()
            except:
                print ('Navigtion Not Found')

    #GET THE COURSE LIST----------------------------------------------------------------------
    def course_list (self):

        self.pdf_names = []
        self.results = []
        wait = False

        self.divs = self.driver.find_elements (By.CSS_SELECTOR, '.sr-dataitem.panel.panel-default')

        for index, div in enumerate (self.divs):

            info = {}
            #get the course information
            div_text = div.text

            #get the average rating scores
            col_text = div.find_elements (By.CLASS_NAME, 'sr-question-template')
        
            ratings = ''
         
            #goes through each rating and assigns to ratings
            for x in col_text:
                #st.write (x.text)
                ratings+= x.text + '-->'

            #create a list with all the strings--------------
            ind = div_text.split ('\n')

            #format the professor name--------------------
            name  = ind [2].split (',')
            first_name = name [1]
            first_name = first_name.strip()
            last_name = name [0]
            full_name = first_name + ' ' + last_name 

            #format download name---------------------
            course = ind [0].replace (' ','')
            course = course.replace ('/','')
            
            long_course = ind [1].replace (' ','')
            long_course= long_course.replace ('/','')
        
            link_name = course + long_course + '_'
            end = first_name + last_name  + '.pdf'
            link_name = link_name.upper()
            pdf_name = link_name + end

    
            #ONLY DOWNLOAD if file not in session state-------------------------   
            
            #DOWNLOAD IF PDF NAME IS IN SESSION STATE
            #pdf name is added to session state so that it means it is already downloaded

            if pdf_name not in st.session_state:
                button = div.find_element (By.CSS_SELECTOR, '.sr-pdf.btn.btn-default.btn-sm')
                button.click()

            else:
                print ('File already downloaded')


            #add values into a dictionary---------------------
            
            info ['course'] = ind[0]
            info ['long_course'] = ind[1]
            info ['full_name'] = full_name
            info ['semester'] = ind [3]
            info ['resp'] = ind [5]
            info ['ratings'] = ratings
            info ['pdf_name'] = link_name + end
            self.pdf_names.append (info ['pdf_name'])
            self.results.append (info)

        return self.results
    

    #WAIT FOR THE FILE TO SHOW UP IN THE DIRECTORY
    #Checks 
    def wait (self,file, timeout = 20):
        
        #get the file path
        #directory = f'/Users/mqw/Desktop/Courses Project/courses/{file}'
        directory = f'{dir}/{file}'

        #files = os.listdir (directory) #list files in the directory
        start_time = time.time()

        while True:
            if os.path.isfile (directory):
                #return true if the path exits and is a file
                return True
            #If the file doesn't exist then wait for the file to be downloaded
            if time.time()-start_time > timeout:
                #st.write ('Timed Out To Find File')
                return False
            
    #goes through all files in the directory to see if name of class and first name is in the file name
    def find_file_name (self, name, first_name, pdf_name):
        curr_dir = os.getcwd()
        dir = curr_dir + '/courses'


        directory = f'{dir}'
        # List all files in the directory

        for filename in os.listdir (directory):
            if name in filename or first_name in filename:
                file_path = os.path.join(directory, filename)
                st.session_state [pdf_name] = file_path
                return file_path
            
    
    #PRINT THE FILE IN THE DIRECTORY
    def print_pdf_read(self, pdf_name):
        curr_dir = os.getcwd()
        dir = curr_dir + '/courses'
        directory = f'{dir}'

        #st.write (pdf_name)

        pdf_path = os.path.join(directory, pdf_name)

        try: 
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    tables = page.extract_tables()
                    st.write (text)
                        
        except: 
            #self.results ['text'] = 'No file'
            st.write ('No File Was Found')



            




            
