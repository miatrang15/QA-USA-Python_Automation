# 1. SELENIUM IMPORTS
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# 2. CLASS DEFINITION
class UrbanRoutesPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    # 3 LOCATORS
    FROM_FIELD = (By.ID, "from-input")
    TO_FIELD = (By.ID, "to-input")
    CALL_TAXI_BUTTON = (By.CLASS_NAME, "search-button")
    SUPPORTIVE_PLAN = (By.XPATH, "//div[contains(@class,'tcard') and .//div[text()='Supportive']]")
    PLAN_SELECTED = (By.CSS_SELECTOR, ".tcard.active")
    PHONE_FIELD = (By.ID, "phone")
    CONFIRMATION_FIELD = (By.ID, "code")
    PAYMENT_BUTTON = (By.CLASS_NAME, "payment-method")
    ADD_CARD_BUTTON = (By.CLASS_NAME, "add-card")
    CARD_NUMBER_FIELD = (By.ID, "card-number")
    CARD_CODE_FIELD = (By.ID, "card-code")
    LINK_CARD_BUTTON = (By.CLASS_NAME, "link-card")
    PAYMENT_METHOD_DISPLAY = (By.CLASS_NAME, "payment-method-text")
    COMMENT_FIELD = (By.ID, "comment")
    BLANKET_CHECKBOX = (By.ID, "blanket")
    HANDKERCHIEF_CHECKBOX = (By.ID, "handkerchief")
    ICE_CREAM_BUTTON = (By.XPATH, "//button[contains(text(), 'Add Ice Cream')]")
    ICE_CREAM_COUNTER = (By.CLASS_NAME, "ice-cream-count")
    ORDER_BUTTON = (By.CLASS_NAME, "order-button")
    CAR_MODAL = (By.ID, "car-modal")

    # 4. METHODS FOR SETTING AND GETTING ROUTE ADDRESSES
    def set_from(self, address):
        from_field = self.driver.find_element(*self.FROM_FIELD)
        from_field.clear()
        from_field.send_keys(address)

    def set_to(self, address):
        to_field = self.driver.find_element(*self.TO_FIELD)
        to_field.clear()
        to_field.send_keys(address)

    def get_from(self):
        from_field = self.driver.find_element(*self.FROM_FIELD)
        return from_field.get_attribute("value")

    def get_to(self):
        to_field = self.driver.find_element(*self.TO_FIELD)
        return to_field.get_attribute("value")

    # ACTION METHODS SECTION
    def set_addresses(self, from_address, to_address):
        from_field = self.wait.until(EC.presence_of_element_located(self.FROM_FIELD))
        to_field = self.wait.until(EC.presence_of_element_located(*self.TO_FIELD))
        from_field.clear()
        to_field.clear()
        from_field.send_keys(from_address)
        to_field.send_keys(to_address)

    def click_call_taxi(self):
        self.wait.until(EC.element_to_be_clickable(self.CALL_TAXI_BUTTON)).click()

    def select_supportive_plan(self):
        self.wait.until(EC.element_to_be_clickable(self.SUPPORTIVE_PLAN)).click()

    def enter_phone_number(self, number):
        phone_field = self.wait.until(EC.presence_of_element_located(self.PHONE_FIELD))
        phone_field.clear()
        phone_field.send_keys(number)

    def enter_sms_code(self, code):
        sms_field = self.wait.until(EC.presence_of_element_located(self.CONFIRMATION_FIELD))
        sms_field.clear()
        sms_field.send_keys(code)

    def open_card_form(self):
        self.wait.until(EC.element_to_be_clickable(self.PAYMENT_BUTTON)).click()
        self.wait.until(EC.element_to_be_clickable(self.ADD_CARD_BUTTON)).click()

    def enter_card_details(self, number, code):
        card_number_field = self.wait.until(EC.presence_of_element_located(self.CARD_NUMBER_FIELD))
        card_code_field = self.wait.until(EC.presence_of_element_located(self.CARD_CODE_FIELD))
        card_number_field.send_keys(number)
        card_code_field.send_keys(code + Keys.TAB)

    def link_card(self):
        self.wait.until(EC.element_to_be_clickable(self.LINK_CARD_BUTTON)).click()

    def leave_driver_comment(self, comment):
        comment_field = self.wait.until(EC.presence_of_element_located(self.COMMENT_FIELD))
        comment_field.send_keys(comment)

    def order_blanket_and_handkerchiefs(self):
        blanket_checkbox = self.wait.until(EC.element_to_be_clickable(self.BLANKET_CHECKBOX))
        handkerchief_checkbox = self.wait.until(EC.element_to_be_clickable(self.HANDKERCHIEF_CHECKBOX))
        blanket_checkbox.click()
        handkerchief_checkbox.click()

    def order_ice_cream(self, count):
        ice_cream_button = self.wait.until(EC.element_to_be_clickable(self.ICE_CREAM_BUTTON))
        for _ in range(count):
            ice_cream_button.click()

    def click_order(self):
        self.wait.until(EC.element_to_be_clickable(self.ORDER_BUTTON)).click()

    # 5. VERIFICATION METHODS SECTION

    def get_addresses(self):
        from_value = self.driver.find_element(*self.FROM_FIELD).get_attribute("value")
        to_value = self.driver.find_element(*self.TO_FIELD).get_attribute("value")
        return from_value, to_value

    def get_selected_plan_text(self):
        return self.driver.find_element(*self.PLAN_SELECTED).text

    def get_entered_phone_number(self):
        return self.driver.find_element(*self.PHONE_FIELD).get_attribute("value")

    def get_payment_method(self):
        return self.driver.find_element(*self.PAYMENT_METHOD_DISPLAY).text

    def get_driver_comment(self):
        return self.driver.find_element(*self.COMMENT_FIELD).get_attribute("value")

    def get_blanket_and_handkerchief_selection(self):
        blanket = self.driver.find_element(*self.BLANKET_CHECKBOX).get_property("checked")
        handkerchief = self.driver.find_element(*self.HANDKERCHIEF_CHECKBOX).get_property("checked")
        return blanket, handkerchief

    def get_ice_cream_count(self):
        return int(self.driver.find_element(*self.ICE_CREAM_COUNTER).text)

    def is_car_modal_displayed(self):
        return self.wait.until(EC.visibility_of_element_located(self.CAR_MODAL)).is_displayed()
