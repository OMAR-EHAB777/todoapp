from selenium import webdriver

browser = webdriver.Firefox()
browser.get('http:///127.0.0.1:4444')

assert 'Django' in browser.titlepyth