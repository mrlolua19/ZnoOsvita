import time
import fastrand
import math
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

url = 'https://zno.osvita.ua/ukraine-history/tag-u_skladi_rechi_pospolitoyi_v_xvii_st/'
service = Service(executable_path='C:\Program Files (x86)\Chromium\chromedriver.exe')

Hspent = int(input("Please enter hours spent: "))
Mspent = int(input("Please enter minutes spent: "))
PercInput = int(input("Please enter the goal in percents: "))

cor = False
while cor == False:
    if  100 >= PercInput >= 0:
        cor = True
    else:
        PercInput = int(input("Wrong percentage, please enter the correct goal: "))



def RepNum(Hspent, Mspent, score):
    x = driver.find_element(By.XPATH, f'//*[@id="wrap"]/div/div[1]/div[1]/strong')
    Total = int(x.text)
    Pcorrect = math.ceil(score*100/Total)
    x = driver.find_element(By.XPATH, f'//*[@id="wrap"]/div/div[1]/div[3]/strong')
    driver.execute_script("arguments[0].textContent = arguments[1];", x, f'{Pcorrect}%')
    x = driver.find_element(By.XPATH, f'//*[@id="wrap"]/div/div[1]/div[2]/strong')
    driver.execute_script("arguments[0].textContent = arguments[1];", x, f'{score}')
    x = driver.find_element(By.XPATH, f'//*[@id="wrap"]/div/div[1]/div[4]/strong')
    if Hspent != 0:
        driver.execute_script("arguments[0].textContent = arguments[1];", x, f'{Hspent} год. {Mspent} хв.')
    else:
        driver.execute_script("arguments[0].textContent = arguments[1];", x, f'{Mspent} хв.')


def IsMultiQ(id): ## 1/0 for single choice, 2/1/0 for triple choice, 4/2/0 for matching
    q = driver.find_element(By.XPATH, f'//*[@id="q{id}"]')
    try:
        q.find_element(By.PARTIAL_LINK_TEXT, 'Завдання на встановлення')
        return 2
    except NoSuchElementException:
        try:
            q.find_element(By.PARTIAL_LINK_TEXT, 'Завдання з вибором тр')
            return 1
        except NoSuchElementException:
            return 0





options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ['enable-automation'])
driver = webdriver.Chrome(service=service, options = options)


driver.get(url)
questions_container = driver.find_element(By.ID, 'tasks-numbers')
question_elements = questions_container.find_elements(By.CSS_SELECTOR, 'span.number')
question_count = len(question_elements)

if question_count > 0:
    last_question = question_elements[-1]
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 3);")
    last_question.click()


driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 3);")
driver.find_element(By.XPATH, f'//*[@id="q_form_{question_count}"]/div[7]/div[2]/span').click()

questions_container = driver.find_element(By.ID, 'tasks-numbers')
question_elements = questions_container.find_elements(By.CSS_SELECTOR, 'span.number')


totCorScore = 0
FullScore = int(WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, f'//*[@id="wrap"]/div/div[1]/div[1]/strong'))).text)
NeededScore = math.ceil((PercInput/100)*FullScore) - 1


Qnumber = 1
for i in range(question_count):
    Type = IsMultiQ(Qnumber)
    ranNumber = fastrand.pcg32randint(1, 100)
    question_elements = driver.find_elements(By.CSS_SELECTOR, 'span.number')
    question_element = question_elements[i]
    if Type > 0:
        if ranNumber > 80:
            driver.execute_script("arguments[0].classList.add('bad');", question_element)
        elif 50 < ranNumber < 70:
            driver.execute_script("arguments[0].classList.add('good');", question_element)
            totCorScore += Type
        else:
            driver.execute_script("arguments[0].classList.add('super');", question_element)
            totCorScore += 2*Type
    else:
        if ranNumber > 80:
            driver.execute_script("arguments[0].classList.add('bad');", question_element)
        else:
            driver.execute_script("arguments[0].classList.add('super');", question_element)
            totCorScore += 1
    
    question_element = questions_container.find_element(By.CSS_SELECTOR, 'span.number')
    Qnumber += 1
    time.sleep(0.01) ## to look smooth xD

while totCorScore != NeededScore:
    if totCorScore < NeededScore:
        while (totCorScore < NeededScore):
            QNumber = fastrand.pcg32randint(1, len(question_elements))
            question_element = question_elements[QNumber-1]
            class_name = question_element.get_attribute('class')
            while 'super' in class_name:
                QNumber = fastrand.pcg32randint(1, len(question_elements))
                question_element = question_elements[QNumber-1]
                class_name = question_element.get_attribute('class')
            Type = IsMultiQ(QNumber)
            if 'bad' in class_name:
                driver.execute_script("arguments[0].classList.remove('bad');", question_element)
                if Type < 1:
                    driver.execute_script("arguments[0].classList.add('super');", question_element)
                    totCorScore += 1
                elif QNumber < 3:
                    driver.execute_script("arguments[0].classList.add('good');", question_element)
                    totCorScore += Type
                else:
                    driver.execute_script("arguments[0].classList.add('super');", question_element)
                    totCorScore += 2*Type
            if 'good' in class_name:
                driver.execute_script("arguments[0].classList.remove('good');", question_element)
                driver.execute_script("arguments[0].classList.add('super');", question_element)
                totCorScore += 2*Type
        if totCorScore == NeededScore:
                break

    if totCorScore > NeededScore:
        while (totCorScore > NeededScore):
            QNumber = fastrand.pcg32randint(1, len(question_elements))
            question_element = question_elements[QNumber-1]
            class_name = question_element.get_attribute('class')
            while 'bad' in class_name:
                QNumber = fastrand.pcg32randint(1, len(question_elements))
                question_element = question_elements[QNumber-1]
                class_name = question_element.get_attribute('class')
            Type = IsMultiQ(QNumber)
            if 'good' in class_name:
                driver.execute_script("arguments[0].classList.remove('good');", question_element)
                driver.execute_script("arguments[0].classList.add('bad');", question_element)
                totCorScore -= Type
            elif 'super' in class_name:
                driver.execute_script("arguments[0].classList.remove('super');", question_element)
                if Type < 1:
                    driver.execute_script("arguments[0].classList.add('bad');", question_element)
                    totCorScore -= 1
                elif QNumber < 3:
                    driver.execute_script("arguments[0].classList.add('good');", question_element)
                    totCorScore -= Type
                else:
                    driver.execute_script("arguments[0].classList.add('bad');", question_element)
                    totCorScore -= 2*Type
            if totCorScore == NeededScore:
                break




RepNum(Hspent, Mspent, totCorScore)



time.sleep(38888888)
driver.quit()
