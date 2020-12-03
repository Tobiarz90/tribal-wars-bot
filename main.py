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
    # print('List of rows:')
    # for i in row_list:
    #     print(i.get_attribute('class'))

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


def recruit(dict_res):
    values = recruitment.get(unitType)
    num = int(min(dict_res['wood'] / values[0],
                  dict_res['stone'] / values[1],
                  dict_res['iron'] / values[2],
                  dict_res['getable_pop'] / values[3]))
    print(f'I can recruit {num} units')

    if not num >= recruit_units:
        return

    # get new url based on what type of unit do you want to get
    url = driver.current_url
    pos = url.find('screen')
    driver.get(f'{url[:pos]}screen={values[4]}')
    sleep()

    unit_box = wait.until(ec.presence_of_element_located((By.XPATH, f'//input[@name="{unitType}"]')))
    print(unit_box.get_attribute('name'), end=' | ')
    print(unit_box.get_attribute('id'), end=' | ')
    print(unit_box.get_attribute('class'))
    unit_box.send_keys(num)
    sleep()

    recruit_btn = wait.until(ec.presence_of_element_located((By.CLASS_NAME, 'btn-recruit')))
    recruit_btn.click()
    print(f'I recruited {num} units type {unitType}')

    sleep()
    driver.get(url)


def what_time():
    current_time = datetime.datetime.now()
    return f'{current_time.hour}:{current_time.minute}:{current_time.second}'


def main():
    while True:
        result = counter()
        times_click = result[0]
        row_list = result[1]

        if times_click != 0 and len(row_list) != 0:
            villages_id(times_click, row_list)

        # check if I can recruit a unit
        recruit(count_resources())

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
    unitType = 'axe'    # <- set type of unit you want to recruit
    recruit_units = 15  # <- recruit when you can recruit at least n units
    choice = 'a'        # <- set which button bot have to click [a or b]

    # 'unit_type': [wood, stone, iron, population, building]
    recruitment = {'spear': [50, 30, 10, 1, 'barracks'],
                   'sword': [30, 30, 70, 1, 'barracks'],
                   'axe': [60, 30, 40, 1, 'barracks'],
                   'spy': [50, 50, 20, 2, 'stable'],
                   'light': [125, 100, 250, 4, 'stable'],
                   'heavy': [200, 150, 600, 6, 'stable']}

    if choice == 'a':
        form = 1
    elif choice == 'b':
        form = 2

    # Log in
    readiness()
    print(f'BOT started work at {what_time()}')

    # Bot running
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
