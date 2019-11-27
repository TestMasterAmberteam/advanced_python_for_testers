from time import sleep
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement


def hide_element(driver, id):
    driver.execute_script(f'document.getElementById("{id:3d}").setAttribute("opacity", 0)')


def show_element(driver, id):
    driver.execute_script(f'document.getElementById("{id}").setAttribute("opacity", 1)')


driver = webdriver.Chrome()
driver.maximize_window()
driver.get('file:///D:/jsabak/Documents/Konferencje/WarszawQA%202019-11/algorytm.svg')
driver.execute_script(f'document.getElementById("svg8").setAttribute("height", "auto")')
driver.execute_script(f'document.getElementById("svg8").setAttribute("width", "100% ")')
hide_element(driver, 'pobierz')
hide_element(driver, 'przetworz')
hide_element(driver, 'zapisz')
hide_element(driver, 'folderB')
hide_element(driver, 'fileB1')
hide_element(driver, 'fileB2')
hide_element(driver, 'fileB3')
hide_element(driver, 'czasy')
# pobierz
input('Next')
show_element(driver, 'pobierz')
input('Next')
# przetwórz
show_element(driver, 'przetworz')
input('Next')
# zapisz
show_element(driver, 'zapisz')
input('Next')
# folderB
show_element(driver, 'folderB')
sleep(1)
# fileB1
show_element(driver, 'fileB1')
sleep(1)
# fileB2
show_element(driver, 'fileB2')
sleep(1)
# fileB3
show_element(driver, 'fileB3')
input('Next')
# czasy
show_element(driver, 'czasy')

