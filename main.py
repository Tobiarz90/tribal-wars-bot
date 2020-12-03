from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import datetime
import time
import random


def readiness():
    user_name_input = wait.until(ec.presence_of_element_located((By.NAME, 'username')))
    user_name_input.send_keys(userName)

    pass_input = wait.until(ec.presence_of_element_located((By.NAME, 'password')))
    pass_input.send_keys(passWord)

    login_btn = wait.until(ec.presence_of_element_located((By.CLASS_NAME, 'btn-login')))
    login_btn.click()

    world_btn = wait.until(ec.presence_of_element_located((By.CLASS_NAME, 'world_button_active')))
    world_btn.click()

    af_btn = wait.until(ec.presence_of_element_located((By.ID, 'manager_icon_farm')))
    af_btn.click()


def sleep():
    time.sleep(round(random.uniform(1, 2), 2))


def count_units():
    units_dict = {}
    for i in range(2, 9):
        unit = driver.find_element_by_xpath(f'//*[@id="units_home"]/tbody/tr[2]/td[{i}]')
        units_dict.setdefault(unit.get_attribute('id'), int(unit.text))

    print('Units:', units_dict)
    return units_dict


def get_pattern_dict():
    pattern_units = {}
    for k in range(1, 8):
        box = driver.find_element_by_xpath(f'//*[@id="content_value"]/div[2]/div/form[{form}]/table/tbody/tr[2]/td[{k}]'
                                           f'/input')
        pattern_units.setdefault(box.get_attribute('name'), int(box.get_attribute('value')))

    print('Template:', pattern_units)
    return pattern_units


def compare_dicts(units_dict, pattern_dict):
    count = 0
    once = True
    for key in units_dict:
        if units_dict[key] >= pattern_dict[key]:
            if pattern_dict[key] != 0:
                units_division = units_dict[key] / pattern_dict[key]
                if once:
                    count = units_division
                    once = False
                else:
                    if units_division < count:
                        count = units_division
        else:
            return int(count)

    return int(count)


def counter():
    row_list = wait.until(ec.presence_of_all_elements_located((By.CLASS_NAME, 'farm_icon_a')))
    row_list = row_list[1:]
    print('List of rows:')
    for i in row_list:
        print(i.get_attribute('class'))

    click_rows = len(row_list)
    click_units = compare_dicts(count_units(), get_pattern_dict())
    print('\nClicks based on the number of rows:', click_rows, '\nClicks based on the number of units:', click_units)

    # how many times can I click
    if click_units < click_rows:
        return click_units, row_list
    else:
        return click_rows, row_list


def villages_id(count, rows):
    # row = village_id
    for j in range(count):
        row = rows[j].get_attribute('class')
        row = row[:18]
        print('Class name:', row)

        sleep()

        # find all villages with class name: row (e.g. farm_village_4856)
        btn = wait.until(ec.presence_of_all_elements_located((By.CLASS_NAME, str(row))))

        # btn[0] => A button
        # btn[1] => B button
        if choice == 'a':
            btn[0].click()
        elif choice == 'b':
            btn[1].click()


def count_resources():
    # get data from page
    resources = wait.until(ec.presence_of_all_elements_located((By.CLASS_NAME, 'res')))
    curent_population = wait.until(ec.presence_of_element_located((By.ID, 'pop_current_label')))
    max_pop = wait.until(ec.presence_of_element_located((By.ID, 'pop_max_label')))

    # get amount of population
    curent_population = int(curent_population.text)
    max_pop = int(max_pop.text)
    getable_pop = max_pop - curent_population   # getable -> dostępna

    resources_list = {product.get_attribute('id'): int(product.text) for product in resources}

    # assign population to resources_list
    resources_list.setdefault('curent_population', curent_population)
    resources_list.setdefault('max_pop', max_pop)
    resources_list.setdefault('getable_pop', getable_pop)

    print('Resources:', resources_list)
    return resources_list


def can_i_recruit(type_of_unit):
    # get necessary resources using count_resources() function
    dict_res = count_resources()
    wood = dict_res['wood']
    stone = dict_res['stone']
    iron = dict_res['iron']
    pop = dict_res['getable_pop']

    # if I can recruit then recruit
    term = wood >= 125 and stone >= 100 and iron >= 250 and pop >= 4
    if term:
        recruit(type_of_unit)


def recruit(unit_type):
    url = driver.current_url[:-7] + 'stable'
    sleep()
    driver.get(url)

    light_btn = wait.until(ec.presence_of_element_located((By.ID, f'{unit_type}_0_a')))
    print(f'Recruited {light_btn.text[1]} light cavalry at {what_time()}')
    sleep()
    light_btn.click()

    recruit_btn = wait.until(ec.presence_of_element_located((By.XPATH, '//*[@id="train_form"]/table/tbody/tr[4]/td['
                                                                       '2]/input')))
    sleep()
    recruit_btn.click()

    url = driver.current_url[:-6] + 'am_farm'
    sleep()
    driver.get(url)


def what_time():
    current_time = datetime.datetime.now()
    return f'{current_time.hour}:{current_time.minute}:{current_time.second}'


def main():
    result = counter()
    times_click = result[0]
    row_list = result[1]

    if times_click != 0 and len(row_list) != 0:
        villages_id(times_click, row_list)

    # check if I can recruit a unit
    can_i_recruit(unitType)

    driver.refresh()
    time.sleep(round(random.uniform(1, 3), 2))


try:

    options = webdriver.ChromeOptions()
    options.add_argument('window-size=1400,1000')
    PATH = r'.\chromedriver.exe'
    driver = webdriver.Chrome(PATH, options=options)
    driver.get(' ')     # <- type a link to your game server here
    wait = WebDriverWait(driver, 8)
    print('Launched...')

    # user settings
    userName = ' '      # <- type your username here
    passWord = ' '      # <- type your password here
    unitType = 'light'

    choice = 'a'        # <- set which button bot have to click [a or b]
    if choice == 'a':
        form = 1
    elif choice == 'b':
        form = 2

    # Log in
    readiness()
    print(f'BOT started work at {what_time()}')

    # Bot running
    while True:
        main()

except Exception as e:
    # End
    try:
        print(r'[error] ¯\_(ツ)_/¯')
        print(e)

        driver.quit()
        # send_email()

        print(f'The program finished its operation at {what_time()}')
    except Exception:
        pass
