from bs4 import BeautifulSoup

tag = BeautifulSoup('<b id="boldest" required>bold</b>', 'html.parser').b

print(tag.attrs)