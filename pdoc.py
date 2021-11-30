"""
Nicholas Johnston
A01242666
"""
import sys
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


class EmployeeProcessor:
    """
    Reads file with Pandas

    :return employee list
    """
    def __init__(self, file_name):
        """
        Initialize an OrderProcessor object using a file name, with an empty order list to start.

        :param file_name: str
        """
        self._file_name = file_name
        self._employee_list = []

    def create_employee_list(self):
        """
        Build and return an employee list

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
    """
    Employee class with property methods
    """
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


def process_website(employees):
    """
    Instantiates
    :param employees: list of employee objects
    """
    chrome_options = webdriver.ChromeOptions()
    # TODO: add path for where downloads should go
    prefs = {"download.default_directory": "/Users/enjay/Downloads"}
    chrome_options.add_experimental_option("prefs", prefs)
    driver = None
    # Instantiate driver
    # TODO: add your path where chromedriver resides
    # ex: /Users/user/Downloads/chromedriver
    try:
        chrome_driver = "/Users/enjay/Downloads/chromedriver2"
        if chrome_driver == "":
            raise ValueError
        driver = webdriver.Chrome(executable_path=chrome_driver, chrome_options=chrome_options)
    except ValueError:
        print("Must enter path of ChromeDriver: Line 111")
        exit()
    # Get website
    driver.get(
        "https://www.canada.ca/en/revenue-agency/services/e-services/e-services-businesses/payroll-deductions-online"
        "-calculator.html")
    # Sleep to give time for website to load (pry better way  to check if it's loaded)
    time.sleep(3)
    # Assert we're on the correct page
    assert "Payroll Deductions Online Calculator - Canada.ca" in driver.title
    # Click on initial page " I accept " button
    initial_accept = driver.find_element(By.PARTIAL_LINK_TEXT, "calculation")
    initial_accept.click()
    time.sleep(3)
    # Next page just need to preess neext
    next1 = driver.find_element(By.ID, "welcome_button_next")
    next1.click()
    time.sleep(3)
    # jurisdiction/pay period can reside outside of loop
    # because next calculation button at end select these values again
    employment_province = Select(driver.find_element(By.ID, "jurisdiction"))
    employment_province.select_by_visible_text("British Columbia")
    pay_period = Select(driver.find_element(By.ID, "payPeriodFrequency"))
    pay_period.select_by_value("SEMI_MONTHLY")
    # Start processing employees into input page
    for employee in employees:
        # Input Name
        name_input = driver.find_element(By.ID, "employeeName")
        name_input.send_keys(employee.employee_name)
        # Input Employer
        employer_name = driver.find_element(By.ID, "employerName")
        employer_name.send_keys(employee.employer)
        # Extract pandas Timestamp object
        employee_date = pd.Timestamp.date(employee.date)
        # Input Date
        # Year
        date_paid_year = Select(driver.find_element(By.ID, "datePaidYear"))
        date_paid_year.select_by_value(str(employee_date.year))
        # Month
        date_paid_month = Select(driver.find_element(By.ID, "datePaidMonth"))
        date_paid_month.select_by_value(str(employee_date.month))
        # Day
        date_paid_day = Select(driver.find_element(By.ID, "datePaidDay"))
        date_paid_day.select_by_value(str(employee_date.day))
        # Finish form
        next2 = driver.find_element(By.ID, "payrollDeductionsStep1_button_next")
        next2.click()
        time.sleep(3)
        # Input Salary
        salary_input = driver.find_element(By.ID, "incomeAmount")
        salary_input.send_keys(employee.salary)
        # Input Vacation Pay
        vp_input = driver.find_element(By.ID, "vacationPay")
        vp_input.send_keys(employee.vacation_pay)
        # Finish form
        next3 = driver.find_element(By.ID, "payrollDeductionsStep2a_button_next")
        next3.click()
        # Calculate taxes
        calculate_button = driver.find_element(By.ID, "payrollDeductionsStep3_button_calculate")
        calculate_button.click()
        # Save result
        save_result = driver.find_element(By.ID, "payrollDeductionsResults_button_generateResultsPdf")
        save_result.click()
        # Go to next calculation
        next_calculation = driver.find_element(By.ID, "payrollDeductionsResults_button_nextCalculationButton")
        next_calculation.click()
        time.sleep(2)
    # Close driver (closes website)
    driver.close()


def main():
    employee_processor = EmployeeProcessor(sys.argv[2])
    employee_list = employee_processor.create_employee_list()
    process_website(employee_list)


if __name__ == '__main__':
    main()
