import requests
from bs4 import BeautifulSoup

URL = 'https://wiki.multitheftauto.com/wiki/CreateBlipAttachedTo'


# Source: HTML result
def get_html():
    req = requests.request('GET', URL)
    html = req.text
    soup_html = BeautifulSoup(html, 'html.parser')



# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
