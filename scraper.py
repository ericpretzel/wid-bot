from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import json

find_thumbnail = re.compile('src="(https:\\/\\/.+_full.jpg)"')
find_id = re.compile('"(\\d{17})"')
find_stats = re.compile('var stats = ({.+});')

# configure settings and open website
options = Options()
options.add_argument('--enable-javascript')
options.add_argument('--headless')

def get_stats(query):
    driver = webdriver.Chrome(options=options)

    # workaround for being detected as a bot
    # got this from https://stackoverflow.com/a/69766804
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    # find the steamID of the user
    driver.get(f'https://steamid.xyz/{query}')
    result = find_id.search(driver.page_source)
    if not result:
        raise Exception('Could not find user.')
    id = result.group(1)

    result = find_thumbnail.search(driver.page_source)
    if not result:
        raise Exception('Could not find user.')
    thumbnail = result.group(1)

    driver.get(f'https://csgostats.gg/player/{id}')
    result = find_stats.search(driver.page_source)
    if not result:
        raise Exception('Could not find user on csgostats.gg')

    stats = json.loads(result.group(1))
    stats['thumbnail'] = thumbnail

    driver.close()
    return stats