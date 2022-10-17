from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
import selenium.webdriver.support.ui as ui
import sys
import time
from datetime import datetime

PATH = "C:\\Program Files (x86)\\chromedriver.exe"
class_id = sys.argv[1]
a = 1

def delete_overlay():
    try:
        element = driver.find_element_by_class_name('t-overlay')
        driver.execute_script("""
        var element = arguments[0];
        element.parentNode.removeChild(element);
        """, element)
    except:
        pass

# driver = webdriver.Chrome(PATH)
driver = webdriver.Firefox(executable_path="C:\\Program Files (x86)\\geckodriver.exe")
driver.get('https://im.aua.am')
username_field = driver.find_element(By.ID, "UserName")
username_field.send_keys("samvel.topuzyan@gmail.com")
password_field = driver.find_element(By.ID, "Password")
password_field.send_keys("Samvel2002")
btn = driver.find_element(By.ID, "btnLogin")
btn.send_keys(Keys.RETURN)
driver.get('https://im.aua.am/Student/ClassRegistration')

while True:
    try:
        tms = time.time()
        # delete_overlay()
        link = ui.WebDriverWait(driver, 15).until(lambda browser: browser.find_element_by_css_selector(f'a[onclick="ViewDetails({class_id},true)"]'))
        link.click()
        capacity_num = int(ui.WebDriverWait(driver, 15).until(lambda driver: driver.find_element(By.XPATH, '//label[text()="Capacity"]/following-sibling::div').text))
        registered_num = int(ui.WebDriverWait(driver, 15).until(lambda driver: driver.find_element(By.XPATH, '//label[text()="Registered"]/following-sibling::div').text))

        if tms % 10 < 3:
            try:
                print("Write")
                f = open(f'routine_{class_id}.log', 'a+')
                f.write(f"[{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')}] Capacity: {capacity_num}, Registered: {registered_num}\n")
                f.close()
            except:
                pass

        if registered_num < capacity_num:
            # delete_overlay()

            registration_link = driver.find_element(By.XPATH, '//div[@class="aua_form"]//a[text()="Add to My Classes"]')
            registration_link.click()

            while True:
                try:
                    driver.find_element(By.XPATH, '//div[@id="wndConfirm"]//input[@value="Yes"]').click()
                    break
                except:
                    pass

            success = False
            try:
                driver.find_element(By.XPATH, '//span[text()="Error"]')
                # delete_overlay()

                driver.find_element(By.XPATH, '//div[@id="wndMessage"]//span[@class="t-icon t-close"]').click()
                driver.find_element(By.XPATH, '//div[@id="wndClassDetails"]//span[@class="t-icon t-close"]').click()
            except:
                success = True

            if success:
                try:
                    print("Success")
                    f = open(f'action_{class_id}.log', 'a+')
                    f.write(f"[{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')}] Clicking Register\n")
                    f.close()
                except:
                    pass
                driver.quit()
                sys.exit(0)
        else:
            driver.find_element(By.CLASS_NAME, 't-close').click()
    except Exception as e:
        print(str(e))
        driver.quit()

        driver = webdriver.Firefox(executable_path="C:\\Program Files (x86)\\geckodriver.exe")
        driver.get('https://im.aua.am')
        username_field = driver.find_element(By.ID, "UserName")
        username_field.send_keys("samvel.topuzyan@gmail.com")
        password_field = driver.find_element(By.ID, "Password")
        password_field.send_keys("Samvel2002")
        btn = driver.find_element(By.ID, "btnLogin")
        btn.send_keys(Keys.RETURN)
        driver.get('https://im.aua.am/Student/ClassRegistration')
