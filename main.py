from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import logging
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
    for i in range(2, 9):
        unit = driver.find_element_by_xpath(f'//*[@id="units_home"]/tbody/tr[2]/td[{i}]')
        yield unit.get_attribute('id'), int(unit.text)


def get_pattern_gen():
    for k in range(1, 8):
        box = driver.find_element_by_xpath(f'//*[@id="content_value"]/div[2]/div/form[{form}]/table/tbody/tr[2]/td[{k}]'
                                           f'/input')
        yield box.get_attribute('name'), int(box.get_attribute('value'))


def compare_gens(units_gen, pattern_gen):
    count = 0
    for unit, pattern_unit in zip(units_gen, pattern_gen):
        try:
            count += unit[1] // pattern_unit[1]
        except ZeroDivisionError:
            pass

    return count


def counter():
    row_list = wait.until(ec.presence_of_all_elements_located((By.CLASS_NAME, 'farm_icon_a')))
    row_list = row_list[1:]

    click_rows = len(row_list)
    click_units = compare_gens(count_units(), get_pattern_gen())

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
    resources_dict = {}
    span = 1
    box = 2
    while box <= 10:
        x_path = f'//td[@class ="topAlign"][4]/table/tbody/tr[1]/td/table/tbody/tr/td[{box}]/span'
        if box == 10:
            x_path += f'[{span}]'
            if not span == 2:
                box = 8
            span += 1
        resource = wait.until(ec.presence_of_element_located((By.XPATH, x_path)))
        resources_dict.setdefault(resource.get_attribute('id'), int(resource.text))
        box += 2
    resources_dict.setdefault('getable_pop', resources_dict['pop_max_label'] - resources_dict['pop_current_label'])

    return resources_dict


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
    unit_box.send_keys(num)
    sleep()

    recruit_btn = wait.until(ec.presence_of_element_located((By.CLASS_NAME, 'btn-recruit')))
    recruit_btn.click()
    logging.info(f'Recruited {num} units type {unitType}')

    sleep()
    driver.get(url)


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
        time.sleep(round(random.uniform(1, 4), 2))


try:

    options = webdriver.ChromeOptions()
    options.add_argument('window-size=1500,1100')
    options.add_argument('headless')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    PATH = r'.\chromedriver.exe'
    driver = webdriver.Chrome(PATH, options=options)

    logging.basicConfig(filename='logs.log', level=logging.INFO,
                        format='%(asctime)s:%(levelname)s:%(message)s')
    
    driver.get('https://www.plemiona.pl/')     # <- type a link to your game server here
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
    logging.info('BOT started work')
    logging.info('Settings: user: {}, unit type {}, recruit {}, choice {}'
                 .format(userName, unitType, recruit_units, choice))

    # Bot running
    main()

except Exception as e:
    print(r'[error] ¯\_()_/¯')
    logging.error(e)
    driver.quit()

except KeyboardInterrupt:
    logging.warning('The program finished its operation')
    driver.quit()
