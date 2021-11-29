"""
Nicholas Johnston
A01242666
"""
import time

from selenium import webdriver
from selenium.webdriver.common.by import By


def get_employee_info():
    return []


def start_driver(website):
    website = website.get(
        "https://www.canada.ca/en/revenue-agency/services/e-services/e-services-businesses/payroll-deductions-online-calculator.html")
    assert "Payroll Deductions Online Calculator - Canada.ca" in website.title
    return website


def process_website(tax_site, employees):
    # get element
    driver = webdriver.Firefox()
    # for employee in employees:


if __name__ == '__main__':
    driver = webdriver.Firefox()
    tax_website = start_driver(driver)
    employees = get_employee_info()
    process_website(driver, employees)

    elem = driver.find_element(By.PARTIAL_LINK_TEXT, "calculation")
    elem.click()
    time.sleep(3)
    elem2 = driver.find_element(By.ID, "welcome_button_next")
    elem2.click()
    elem.clear()
    elem.send_keys("pycon")
    # elem.send_keys(Keys.RETURN)
    assert "No results found." not in driver.page_source
    driver.close()
