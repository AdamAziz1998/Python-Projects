def email_box(driver, email):
    xpath = '//*[@id="session_key"]'
    text_box = driver.find_element_by_xpath(xpath)
    text_box.send_keys(email)
    
def password_box(driver, password):
    xpath = '//*[@id="session_password"]'
    text_box = driver.find_element_by_xpath(xpath)
    text_box.send_keys(password)

def try_sign_in(driver, email, password):
    email_box(email)
    
    password_box(password)
    
    sign_in_button = driver.find_element_by_class_name('sign-in-form__submit-button')
    
    sign_in_button.click()

#still need to check for captcha
#still need to deal with any popups
#...