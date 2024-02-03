import pytest
from selenium import webdriver
from page_object.admin_panel.admin_panel import AdminPanel
from selenium.webdriver.common.by import By


class TestAdminPanel:

    def test_login_superuser(self, browser: webdriver, logout, PageAdminPanel: AdminPanel):
        browser.get("http://localhost:8082/api/unicorn/")
        PageAdminPanel.getLogin().send_keys('root')
        PageAdminPanel.getPassword().send_keys('fKXRA1FRYTA1lKfdg')
        PageAdminPanel.getLoginButton().click()
        assert "Permissions" in PageAdminPanel.getPermissionText().text

    # ToDo: Change cypress-username user to normal user
    @pytest.mark.skip(reason="Change cypress-username user to normal user")
    def test_login_normal_user(self, browser: webdriver, logout, PageAdminPanel: AdminPanel):
        browser.get("http://localhost:8082/api/unicorn/")
        PageAdminPanel.getLogin().send_keys('cypress-username')
        PageAdminPanel.getPassword().send_keys('cypress-password')
        PageAdminPanel.getLoginButton().click()
        assert "You don't have permission to view or edit anything." in PageAdminPanel.getPermissionText().text

    def test_login_with_valid_username_and_invalid_password(self, browser: webdriver, logout,
                                                            PageAdminPanel: AdminPanel):
        browser.get("http://localhost:8082/api/unicorn/")
        PageAdminPanel.getLogin().send_keys('cypress-username')
        PageAdminPanel.getPassword().send_keys('wrong')
        PageAdminPanel.getLoginButton().click()
        assert ("Please enter the correct username and password for a staff account. Note that both fields may be "
                "case-sensitive.") in PageAdminPanel.getErrorLogin().text

    def test_login_with_invalid_username_and_valid_password(self, browser: webdriver, logout,
                                                            PageAdminPanel: AdminPanel):
        browser.get("http://localhost:8082/api/unicorn/")
        PageAdminPanel.getLogin().send_keys('wrong')
        PageAdminPanel.getPassword().send_keys('cypress-password')
        PageAdminPanel.getLoginButton().click()
        assert ("Please enter the correct username and password for a staff account. Note that both fields may be "
                "case-sensitive.") in PageAdminPanel.getErrorLogin().text

    def test_login_with_invalid_username_and_invalid_password(self, browser: webdriver, logout,
                                                              PageAdminPanel: AdminPanel):
        browser.get("http://localhost:8082/api/unicorn/")
        PageAdminPanel.getLogin().send_keys('wrong')
        PageAdminPanel.getPassword().send_keys('wrong123123312')
        PageAdminPanel.getLoginButton().click()
        assert ("Please enter the correct username and password for a staff account. Note that both fields may be "
                "case-sensitive.") in PageAdminPanel.getErrorLogin().text

    def test_not_logged_main_page(self, browser: webdriver, logout, PageAdminPanel: AdminPanel):
        browser.get("http://localhost:8082")
        assert "Login via Active Directory" in PageAdminPanel.wait_for('//*[@id="root"]/div/div', By.XPATH).text

    def test_log_out_via_admin_panel(self, browser: webdriver, PageAdminPanel: AdminPanel):
        browser.get("http://localhost:8082/api/unicorn")
        PageAdminPanel.getButtonLogout().click()
        assert "Logged out" in PageAdminPanel.getLoggedOut().text
