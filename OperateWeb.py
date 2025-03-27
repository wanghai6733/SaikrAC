from selenium.webdriver.common.by import By
import re

class OperateWeb:
    def __init__(self, driver, web_element):
        self.driver = driver
        self.web_element = web_element

    def handle_single_choice(self, answer):
        answer = answer.upper()
        choice = -1
        if bool(re.match(r'^[A-Za-z]+$', answer)):
            choice = ord(answer) - ord('A')
        elif answer == "正确":
            choice = 0
        elif answer == "错误":
            choice = 1

        assert choice != -1, "Invalid answer:{}.".format(answer)

        self.web_element.find_elements(
            By.XPATH, './/label[@class="el-radio el-radio--large"]')[choice].click()

    def handle_fill_in_the_blank(self, answer):
        self.web_element.find_element(By.XPATH, './/input[@class="el-input__inner"]').send_keys(answer)
    
    def handle_reading(self,answer):
        questions = self.web_element.find_elements(By.XPATH, './/div[@class="material-detail-item"]')        
        for i, question in enumerate(questions):
            ans = answer[i]
            choice = -1
            choice = ord(ans) - ord('A')
            question.find_elements(By.XPATH, './/label[@class="el-radio el-radio--large"]')[choice].click()
            

    def handle_all(self, answer):
        # self.driver.execute_script("arguments[0].scrollIntoView();", self.web_element)

        is_fill = self.web_element.find_elements(By.XPATH, './/div[@class="question-fill"]')
        is_single = self.web_element.find_elements(By.XPATH, './div[@class="single-choice"]')
        is_reading = self.web_element.find_elements(By.XPATH, './/div[@class="material-detail"]')
        assert len(is_fill) + len(is_single) + len(is_reading) == 1, "The question type is not fill in the blank, single choice, or reading comprehension."
        
        if is_fill:
            self.handle_fill_in_the_blank(answer)
        elif is_single:
            self.handle_single_choice(answer)
        elif is_reading:
            self.handle_reading(answer)
        else:
            raise Exception("Unknown question type.")
            