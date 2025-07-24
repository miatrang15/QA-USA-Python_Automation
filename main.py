# 1. IMPORTS
import time
import data
import helpers
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pages import UrbanRoutesPage
from helpers import retrieve_phone_code

# 2. CLASS DEFINITION AND SETUP_CLASS

class TestUrbanRoutes:
    @classmethod
    def setup_class(cls):
        # do not modify - we need additional logging enabled in order to retrieve phone confirmation code
        options = Options()
        options.add_argument("--enable-logging")
        options.add_argument("--log-level=0")
        cls.driver = webdriver.Chrome(options=options)
        cls.page = UrbanRoutesPage(cls.driver)

        # Moved from previous project: check URL reachability
        if helpers.is_url_reachable(data.URBAN_ROUTES_URL):
            print("Connected to the Urban Routes server")
            cls.driver.get(data.URBAN_ROUTES_URL)
        else:
            print("Cannot connect to Urban Routes. Check the server is on and still running")

    def setUp(self):
        self.driver.get(data.URBAN_ROUTES_URL)

    def tearDown(self):
        # This runs after each individual test
        # Reset to fresh page state after each test
        self.driver.get(data.URBAN_ROUTES_URL)

        # 3.TEST FUNCTIONS

    def test_set_route(self):
            routes_page = UrbanRoutesPage(self.driver)
            address_from = "East 2nd Street, 601"
            address_to = "1300 1st St"

            routes_page.set_from(address_from)
            routes_page.set_to(address_to)

            assert routes_page.get_from() == address_from
            assert routes_page.get_to() == address_to

    def test_select_plan(self):
            self.page.set_addresses(data.ADDRESS_FROM, data.ADDRESS_TO)
            self.page.click_call_taxi()
            self.page.select_supportive_plan()
            selected = self.page.get_selected_plan_text()
            assert "Supportive" in selected

    def test_fill_phone_number(self):
        self.page.set_addresses(data.ADDRESS_FROM, data.ADDRESS_TO)
        print("Addresses set successfully")
        time.sleep(5)
        print("About to click call taxi")
        self.page.click_call_taxi()
        self.page.select_supportive_plan()
        time.sleep(5)
        self.page.enter_phone_number(data.PHONE_NUMBER)
        time.sleep(3)
        code = helpers.retrieve_phone_code()
        self.page.enter_sms_code(code)
        self.page.click_confirm_button()
        phone_value = self.page.get_entered_phone_number()
        assert phone_value == data.PHONE_NUMBER

    def test_fill_card(self):
            self.page.set_addresses(data.ADDRESS_FROM, data.ADDRESS_TO)
            self.page.click_call_taxi()
            self.page.select_supportive_plan()
            self.page.open_card_form()
            self.page.enter_card_details(data.CARD_NUMBER, data.CARD_CODE)
            self.page.link_card()
            payment_method = self.page.get_payment_method()
            assert payment_method == "Card"

    def test_comment_for_driver(self):
            self.page.set_addresses(data.ADDRESS_FROM, data.ADDRESS_TO)
            self.page.click_call_taxi()
            self.page.select_supportive_plan()
            self.page.leave_driver_comment(data.MESSAGE_FOR_DRIVER)
            comment = self.page.get_driver_comment()
            assert comment == data.MESSAGE_FOR_DRIVER

    def test_order_blanket_and_handkerchiefs(self):
            self.page.set_addresses(data.ADDRESS_FROM, data.ADDRESS_TO)
            self.page.click_call_taxi()
            self.page.select_supportive_plan()
            self.page.order_blanket_and_handkerchiefs()
            blanket, handkerchief = self.page.get_blanket_and_handkerchief_selection()
            assert blanket is True
            assert handkerchief is True

    def test_order_2_ice_creams(self):
            self.page.set_addresses(data.ADDRESS_FROM, data.ADDRESS_TO)
            self.page.click_call_taxi()
            self.page.select_supportive_plan()
            self.page.order_ice_cream(2)
            count = self.page.get_ice_cream_count()
            assert count == 2

    def test_car_search_model_appears(self):
        self.page.set_addresses(data.ADDRESS_FROM, data.ADDRESS_TO)
        self.page.click_call_taxi()
        self.page.select_supportive_plan()
        # Maybe just click order directly?
        self.page.click_order()
        assert self.page.is_car_modal_displayed()


    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
