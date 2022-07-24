#!/home/developer/Downloads/selenium-automation/python-selenium-basic/venv/bin/python3.8
from datetime import date, datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys
import subprocess
from creds import DoneDone, Harvest, Sk, Knysys, ALI, Crontab
from helpers import get_progress_report_email_subject, get_progress_report_body_template, have_network_connection, \
    show_netflix


def harvest_sign_in(driver, task_id):
    # Task reference generation
    task_ref = task_id if task_id[0] == '#' else f'#{task_id}'
    # set_progress_report_template(driver, task_ref)
    sign_in_time = get_sign_in_time(driver)
    if not sign_in_time:
        return 'No tracking until you sign in.'
    time.sleep(5)
    driver.get(Harvest().web_link_ali)
    time.sleep(5)

    try:
        email = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, 'email'))
        )
        email.send_keys(HV_EMAIL)
        password = driver.find_element(By.ID, 'password')
        password.send_keys(HV_PWD)
        driver.find_element(By.ID, 'log-in').send_keys(Keys.RETURN)
    except Exception as e:
        print(e)
        driver.quit()

    driver.get(DoneDone().web_link_ali)
    time.sleep(5)

    try:
        dd_email_field = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, 'txtEmail'))
        )
        dd_email_field.send_keys(DD_EMAIL)
        dd_pwd_field = driver.find_element(By.ID, 'txtPassword')
        dd_pwd_field.send_keys(DD_PWD)
        driver.find_element(By.XPATH, '//*[@id="btnSubmit"]').send_keys(Keys.RETURN)

        task_tab = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/div[1]/ul[1]/li[2]/a/span'))
        )
        task_tab.click()
    except Exception as e:
        print(e)
        return e

    # driver.get(DoneDone().web_link_ali)
    time.sleep(5)

    # Task reference find
    driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[2]/div[1]/div/div/input').send_keys(task_ref)
    time.sleep(2)

    # Task reference click
    driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[3]/table/tr[2]/td[2]/a/div[1]').click()
    time.sleep(2)

    # Harvest iframe Handling
    driver.find_element(By.XPATH, '/html/body/div[1]/div/div[3]/div/main/div/div/div[2]/div[1]/div/div/i').click()
    time.sleep(4)

    iframe = driver.find_element(By.XPATH, '//iframe[@class="harvest-iframe"]')
    driver.switch_to.frame(iframe)
    driver.find_element(By.XPATH, '//*[@id="root"]/div/button[1]').click()
    time.sleep(5)

    # Switching window
    window_before = driver.window_handles[0]
    window_after = driver.window_handles[1]
    driver.switch_to.window(window_after)
    driver.find_element(By.CLASS_NAME, 'account').click()
    time.sleep(5)
    driver.switch_to.window(window_before)
    time.sleep(2)
    iframe = driver.find_element(By.XPATH, '//iframe[@class="harvest-iframe"]')
    driver.switch_to.frame(iframe)
    time.sleep(2)
    driver.find_element(By.XPATH, '//*[@id="root"]/div/div/form/div[5]/div[1]/button').click()
    time.sleep(3)

    # Editing time to harvest
    time_to_edit = str(datetime.now() - sign_in_time).rsplit(':', 1).pop(0)
    driver.get(Harvest().web_link_ali)
    time.sleep(3)
    driver.find_element(By.XPATH, '//span[contains(text(), "Stop")]').click()
    time.sleep(3)
    driver.find_element(By.XPATH, '//button[@title="Edit entry"]').click()

    time_edit_field = WebDriverWait(driver, 7).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="new-entry-dialog"]/div/form/div[3]/input'))
    )

    time.sleep(3)
    time_edit_field.clear()

    time_edit_field.send_keys(time_to_edit)
    time.sleep(2)

    driver.find_element(By.XPATH, '//button[contains(text(), "Update entry")]').click()
    time.sleep(3)

    task_start_button = WebDriverWait(driver, 7).until(
        EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "Start")]'))
    )

    task_start_button.click()
    time.sleep(5)

    driver.close()

    return "Congratulation, You have saved your precious five minutes!!!"


def harvest_sign_out(driver, sign_out=None):
    # Harvest tracking stop
    driver.get(Harvest().web_link_ali)
    email = driver.find_element(By.ID, 'email')
    email.send_keys(HV_EMAIL)
    password = driver.find_element(By.ID, 'password')
    password.send_keys(HV_PWD)
    driver.find_element(By.ID, 'log-in').send_keys(Keys.RETURN)
    time.sleep(3)
    driver.find_element(By.XPATH, '//span[contains(text(), "Stop")]').click()
    time.sleep(5)

    if sign_out:
        from skpy import Skype
        # Getting total time from harvest on tasks.
        total_time = driver.find_element(By.XPATH, '//*[@id="day-view-entries"]/tfoot/tr/td[2]').text

        # Skype connection.
        sk = Skype(Sk().email, Sk().password)

        # Sending message of total time for the day to the project manager.
        contact = sk.contacts[Sk().br_adeel_ref]
        msg = f'Date: {datetime.strftime(date.today(), "%B %dth, %Y")}\nMy total time for the day:\t{total_time}'
        contact.chat.sendMsg(msg)

        # Last task reference get and update in the bashrc file for later use.
        last_task_ref_obj = driver.find_elements(By.CLASS_NAME, 'remote-entry-data').pop().text
        last_task_ref_id = last_task_ref_obj.split(':').pop(0)
        cron_updated = update_crontab(last_task_ref_id)
        cron_update_status = "Crontab has been updated successfully!" if cron_updated else "Crontab not updated!"
    else:
        cron_update_status = "Crontab will update at the time of Sign Out."
    driver.close()
    return "Assalam o Alaikum, Take care!", cron_update_status


def lunch_end(driver):
    driver.get(Harvest().web_link_ali)
    email = driver.find_element(By.ID, 'email')
    email.send_keys(HV_EMAIL)
    password = driver.find_element(By.ID, 'password')
    password.send_keys(HV_PWD)
    time.sleep(2)
    driver.find_element(By.ID, 'log-in').send_keys(Keys.RETURN)
    time.sleep(2)
    driver.find_elements(By.XPATH, '//span[contains(text(), "Start")]')[-1].click()
    time.sleep(5)
    driver.close()
    return "Task timing continued !"


def get_sign_in_time(driver):
    driver.get(Knysys().portal_link)
    try:
        email = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, 'login'))
        )
        email.send_keys(Knysys.email)
        password = driver.find_element(By.ID, 'password')
        password.send_keys(Knysys.password)
        driver.find_element(By.XPATH, '/html/body/div/div/form/div[3]/button').send_keys(Keys.RETURN)
        time.sleep(5)

        attendance = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="oe_main_menu_placeholder"]/ul[1]/li[6]/a/span'))
        )
        attendance.click()

        all_records = WebDriverWait(driver, 7).until(
            EC.presence_of_element_located(
                (By.XPATH, '/html/body/div[2]/div[2]/div[1]/div/div[1]/div[2]/div/div[2]/div[2]/span[1]'))
        )
        all_records.click()

        time.sleep(2)
        is_signed_in = driver.find_element(By.XPATH,
                                           '/html/body/div[2]/div[2]/div[2]/div/div[1]/div/table/tbody/tr[1]/td[3]')

        is_signed_in = True if is_signed_in.text == 'Sign In' else False

        sign_in_time = None
        if is_signed_in:
            sign_in_field = driver.find_element(
                By.XPATH, '/html/body/div[2]/div[2]/div[2]/div/div[1]/div/table/tbody/tr[1]/td[2]')

            sign_in_text = sign_in_field.text
            sign_in_time = datetime.strptime(sign_in_text, "%m/%d/%Y %H:%M:%S")

        return sign_in_time

    except Exception as e:
        print(e)
        driver.quit()
        return e


def set_progress_report_template(driver, task_ref):
    driver.get(Knysys().gmail_link)
    try:
        sign_in_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//a[contains(text(), "Sign in")]'))
        )
        sign_in_button.click()
        email_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="identifierId"]'))
        )
        email_field.send_keys(Sk().email)
        next_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="identifierNext"]/div/button/span'))
        )
        next_button.click()

        pwd_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input'))
        )
        pwd_field.send_keys(Sk().password)
        next_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="passwordNext"]/div/button/span'))
        )
        next_button.click()

        compose_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id=":ku"]/div/div'))
        )
        compose_button.click()

        to_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id=":qt"]'))
        )
        to_field.send_keys(ALI().email)

        cc = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id=":nm"]'))
        )
        cc.click()

        cc_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id=":qu"]'))
        )
        cc_field.send_keys(ALI().cc_emails)
        subject_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id=":qb"]'))
        )
        subject, _date = get_progress_report_email_subject(project='ALI')
        subject_field.send_keys(subject)

        email_body = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id=":rh"]'))
        )
        body_template = get_progress_report_body_template(_date, task_ref=task_ref)
        email_body.send_keys(body_template)

    except Exception as e:
        print(e)
        driver.quit()
        return e


def update_crontab(last_task_ref_id):
    if not last_task_ref_id:
        return False
    grep_line_nos_cmd = "grep -n 'lastTaskRef='"
    _cron_file_path = Crontab().user_cron_path
    awk_first_line_cmd = "awk -F: '{ print $1 } NR==1{exit}'"
    get_ref_line_number_bash_cmd = "%s %s | %s;" % (grep_line_nos_cmd, _cron_file_path, awk_first_line_cmd)

    p = subprocess.Popen(get_ref_line_number_bash_cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         stderr=subprocess.DEVNULL, universal_newlines=True)
    p.stdin.flush()

    for line in p.stdout.readlines():
        line_number = line.strip('\n') if line.strip('\n').isdigit() else False
        if line_number:
            replace_task_ref_bash_cmd = f"sed -i '{line_number}s/.*/lastTaskRef={last_task_ref_id}/' {_cron_file_path}"

            p1 = subprocess.Popen(replace_task_ref_bash_cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                  stderr=subprocess.DEVNULL, universal_newlines=True)
            p1.stdin.flush()
            if not p1.stderr:
                return True


if __name__ == "__main__":
    if not have_network_connection():
        show_netflix()
        sys.exit("No internet connection found!")
    HV_EMAIL = Harvest().email
    HV_PWD = Harvest().password
    DD_EMAIL = DoneDone().email
    DD_PWD = DoneDone().password

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    _driver = webdriver.Chrome(options=chrome_options, service=Service(ChromeDriverManager().install()))
    if len(sys.argv) == 1:
        print('What are you doing?\nPlease add one the commands below\n["sign-in", "stop", "continue", "sign-out"]')
    else:
        if sys.argv[1] == "sign-in":
            conditions_for_sign_in_with_cron = [(sys.argv[1] == "sign-in"), (len(sys.argv) == 3)]
            if all(conditions_for_sign_in_with_cron):
                t_id = sys.argv[2]
            else:
                t_id = input('Please enter your task id:\n')

            _driver.maximize_window()
            status = harvest_sign_in(_driver, t_id)
            print(status)
        elif len(sys.argv) == 2:
            _driver.maximize_window()
            if sys.argv[1] == "stop":
                status = harvest_sign_out(_driver)
                print(status)
            elif sys.argv[1] == "continue":
                status = lunch_end(_driver)
                print(status)
            elif sys.argv[1] == "sign-out":
                status, status_1 = harvest_sign_out(_driver, sign_out=True)
                print(status, status_1)
            else:
                print('Required arguments missing!')
