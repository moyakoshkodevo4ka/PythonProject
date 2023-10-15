import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

import time
import random
import pyautogui as pag
import pyperclip
from pathlib import Path
root_dir = Path(__file__).parent.parent.parent.resolve()  # directory of source root

# pag.FAILSAFE = False

search_attribute_model_data_by_names = (1110, 346)  # координаты search-attribute-model-data-by-names в Network/Fetch/XHR
copy = (1206, 487)  # координаты кнопки copy
node_js_fetch = (1420, 612)
clear_network_log = (1091, 141)


def first_login(phone_number: str):
    options = uc.ChromeOptions()

    # options.add_argument("--headless")
    options.add_argument("start-maximized")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")

    driver = uc.Chrome(use_subprocess=True, options=options)

    # login page
    # driver.get("https://seller.ozon.ru/app/")
    driver.get("https://seller.ozon.ru/app/registration/signin")
    # time.sleep(120)
    print('Пройдите проверку на человека. После этого введите в консоль 1')
    code = input()
    assert code == '1'
    time.sleep(random.uniform(1.5, 2.5))

    # driver.save_screenshot('datadome_undetected_webddriver.png')
    time.sleep(random.uniform(1.5, 2.5))  # время поиска кнопки Войти
    # click on login button
    buttons = driver.find_elements(By.TAG_NAME, 'button')
    for button in buttons:
        text = button.find_element(By.TAG_NAME, 'span').text
        if text == 'Войти':
            button.click()
            time.sleep(random.uniform(5.5, 7.7))  # время ввода телефона
            break

    # input phone number
    driver.find_element(By.TAG_NAME, 'input').send_keys(phone_number)
    time.sleep(random.uniform(1.5, 2.5))  # ожидание после ввода номера перед нажатием Войти

    # click on login button
    buttons = driver.find_elements(By.TAG_NAME, 'button')
    for button in buttons:
        text = button.find_element(By.TAG_NAME, 'span').text
        if text == 'Войти':
            button.click()
            time.sleep(random.uniform(1.5, 2.5))
            break

    """
    # input code
    print("Введите код подтверждения с вашего телефона")
    code = input()
    driver.find_element(By.TAG_NAME, 'input').send_keys(code)
    time.sleep(1)
    print('Авторизация по номеру прошла успешно!\n')

    # email authorization
    buttons = driver.find_elements(By.TAG_NAME, 'button')
    for button in buttons:
        text = button.find_element(By.TAG_NAME, 'span').text
        if text == 'Войти':
            button.click()
            time.sleep(1)
            break

    print("Введите код подтверждения с вашего email")
    code = input()
    driver.find_element(By.TAG_NAME, 'input').send_keys(code)
    time.sleep(1)
    print('Авторизация по email прошла успешно!\n')
    time.sleep(1)
    """


    print('Перейдите в раздел Товары и цены/Добавить товары. После этого введите в консоль 1')
    code = input()
    assert code == '1'
    time.sleep(random.uniform(10, 12))

    finder(driver=driver, num_scrolls=5)

    time.sleep(random.uniform(3.5, 7.5))

    driver.quit()


def scroll(driver):
    # Прокрутка вниз
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # Пауза, пока загрузится страница.
    time.sleep(random.uniform(0.4, 0.5))


def copy_NodeJS_fetch_using_mouse():
    """
    копирует Node.js fetch в буфер
    """

    time.sleep(random.uniform(0.1, 0.2))

    # перемещаемся на search-attribute-model-data-by-names и тыкаем
    # start_pos = pag.position()
    pag.moveTo(search_attribute_model_data_by_names[0], search_attribute_model_data_by_names[1],
               duration=random.uniform(0.2, 0.3))
    time.sleep(random.uniform(0.2, 0.3))
    pag.click(search_attribute_model_data_by_names[0], search_attribute_model_data_by_names[1], 1, button='right')
    time.sleep(random.uniform(0.2, 0.3))

    # перемещаемся на copy
    # start_pos = mouse.get_position()
    pag.moveTo(copy[0], copy[1],
               duration=random.uniform(0.2, 0.3))
    time.sleep(random.uniform(0.2, 0.3))

    # перемещаемся на Node-js fetch
    pag.moveTo(node_js_fetch[0], node_js_fetch[1],
               duration=random.uniform(0.2, 0.3))
    time.sleep(random.uniform(0.2, 0.3))
    pag.click(node_js_fetch[0], node_js_fetch[1], 1, button='left')
    time.sleep(random.uniform(0.2, 0.3))


def clear_logs():
    """
    чистит предыдущие выводы
    """
    time.sleep(random.uniform(0.1, 0.2))

    pag.moveTo(clear_network_log[0], clear_network_log[1],
               duration=random.uniform(0.2, 0.3))
    time.sleep(random.uniform(0.2, 0.3))
    pag.click(clear_network_log[0], clear_network_log[1], 1, button='left')
    time.sleep(random.uniform(0.2, 0.3))


def save_from_buffer():
    """
    сохраняет инфу из буфера
    """
    path = Path(root_dir)
    path /= Path('bert_ozon/Parsing/collecting_data/fetches_from_buffer/buffer_example.txt')
    file = open(path, 'a')
    file.write(pyperclip.paste() + '\n')
    file.close()


def finder(driver, num_scrolls=10):
    """
    собирает информацию о продуктах из категории
    """

    # products = ['Рюкзак женский', 'Чехол для чемодана', 'Медицинская сумка', 'Чемодан детский', 'Женский Саквояж дорожный', 'Рюкзак спортивный', 'Бьюти-кейс дорожный', 'Органайзер для сумки/рюкзака', 'Мужской Несессер', 'Женский Клатч']
    products = load_third_categories()

    # find search line
    search_line = driver.find_element(By.TAG_NAME, 'input')
    for product in products:

        # чистим предыдущие выводы
        clear_logs()

        # вставляем в поиск продукт
        time.sleep(random.uniform(0.2, 0.3))
        search_line.send_keys(product)
        time.sleep(random.uniform(0.2, 0.3))

        # копируем Node.js fetch о товаре в буфер
        copy_NodeJS_fetch_using_mouse()

        # сохраняем из буфера
        save_from_buffer()

        # чистим строку поиска
        time.sleep(random.uniform(0.2, 0.3))
        search_line.clear()
        time.sleep(random.uniform(0.2, 0.3))

        for i in range(num_scrolls):
            # чистим предыдущие выводы
            clear_logs()

            # скролим 1 раз
            scroll(driver=driver)

            # копируем Node.js fetch о товаре в буфер
            copy_NodeJS_fetch_using_mouse()

            # сохраняем из буфера
            save_from_buffer()

            # чистим строку поиска
            time.sleep(random.uniform(0.2, 0.3))
            search_line.clear()
            time.sleep(random.uniform(0.2, 0.3))


def load_third_categories():
    path = Path(root_dir)
    path /= Path('bert_ozon/data/example/example.txt')

    data = []
    with open(path, 'r') as file:
        for line in file:
            data.append(line[:-1])
    return data


if __name__ == '__main__':
    # phone_number = '917 544 50 19'
    phone_number = '925 358 88 64'
    # phone_number = "925 128 59 48"
    first_login(phone_number)

