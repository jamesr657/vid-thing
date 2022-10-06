from selenium import webdriver
import undetected_chromedriver as uc

# from undetected-chromedriver import
from bs4 import BeautifulSoup as bs
import requests


def get_webpage_data(url, webdriver_path):
    """
    Function to return the html for a given webpage

    Args:
        url:            [str] The URL to get data from.
        webdriver_path: [str] The location for the wedriver file.

    Returns:
        something, still need to figure it out.

    """

    # driver = webdriver.Chrome(webdriver_path)
    driver = uc.Chrome(webdriver_path)
    # window_size = driver.execute_script(
    #     """
    #     return [window.outerWidth - window.innerWidth + arguments[0],
    #       window.outerHeight - window.innerHeight + arguments[1]];
    #     """,
    #     800,
    #     600,
    # )
    # driver.set_window_size(*window_size)

    driver.get(url)
    content = driver.page_source

    return content
