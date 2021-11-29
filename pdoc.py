"""
Nicholas Johnston
A01242666
"""
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


class EmployeeProcessor:

    def __init__(self, file_name):
        """
        Initialize an OrderProcessor object using a file name, with an empty order list to start.

        :param file_name: str
        """
        self._file_name = file_name
        self._employee_list = []

    def create_employee_list(self):
        """
        Build and return an employee list. Reads

        :return: Order list
        """
        data = pd.read_excel(self._file_name,
                             usecols=['Employee Name', 'Employer Name', 'Date', 'Salary', 'Vacation Pay'])
        dict_data = data.to_dict()

        for i in range(len(dict_data.get('Employee Name'))):
            employee = Employee()
            employee.employee_name = dict_data.get('Employee Name').get(i)
            employee.employer = dict_data.get('Employer Name').get(i)
            employee.date = dict_data.get('Date').get(i)
            employee.salary = dict_data.get('Salary').get(i)
            employee.vacation_pay = dict_data.get('Vacation Pay').get(i)
            self._employee_list.append(employee)

        return self._employee_list


class Employee:
    def __init__(self):
        self._employee_name = ""
        self._employer = ""
        self._date = ""
        self._salary = 0
        self._vacation_pay = 0

    @property
    def employee_name(self):
        return self._employee_name

    @employee_name.setter
    def employee_name(self, name):
        self._employee_name = name

    @property
    def employer(self):
        return self._employer

    @employer.setter
    def employer(self, value):
        self._employer = value

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        self._date = value

    @property
    def salary(self):
        return self._salary

    @salary.setter
    def salary(self, value):
        self._salary = value

    @property
    def vacation_pay(self):
        return self._vacation_pay

    @vacation_pay.setter
    def vacation_pay(self, value):
        self._vacation_pay = value


def start_driver(website):
    return website


def process_website(employees):
    # get element
    driver = webdriver.Firefox()
    driver.get(
        "https://www.canada.ca/en/revenue-agency/services/e-services/e-services-businesses/payroll-deductions-online"
        "-calculator.html")
    tax_website = start_driver(driver)

    assert "Payroll Deductions Online Calculator - Canada.ca" in driver.title
    for employee in employees:
        elem = tax_website.find_element(By.PARTIAL_LINK_TEXT, "calculation")
        elem.click()
        time.sleep(3)
        elem2 = tax_website.find_element(By.ID, "welcome_button_next")
        elem2.click()
        name_input = tax_website.find_element(By.ID, "employeeName")
        name_input.send_keys(employee.employee_name)
        employer_name = tax_website.find_element(By.ID, "employerName")
        employer_name.send_keys(employee.employer)
    assert "No results found." not in driver.page_source
    driver.close()


def main():
    employee_processor = EmployeeProcessor('payroll_list.xlsx')
    employee_list = employee_processor.create_employee_list()
    process_website(employee_list)


if __name__ == '__main__':
    main()
