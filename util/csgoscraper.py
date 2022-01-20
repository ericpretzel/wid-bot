from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import json

# rank img takes the form:
# https://static.csgostats.gg/images/ranks/{i}.png
# this converts the number to the rank's actual name
ranks = {
    1: 'Silver I',
    2: 'Silver II',
    3: 'Silver III',
    4: 'Silver IV',
    5: 'Silver Elite',
    6: 'Silver Elite Master',
    7: 'Gold Nova I',
    8: 'Gold Nova II',
    9: 'Gold Nova III',
    10: 'Gold Nova Master',
    11: 'Master Guardian I',
    12: 'Master Guardian II',
    13: 'Master Guardian Elite',
    14: 'Distinguished Master Guardian',
    15: 'Legendary Eagle',
    16: 'Legendary Eagle Master',
    17: 'Supreme Master First Class',
    18: 'The Global Elite'
}
find_nickname = re.compile('Nick Name\\n<input type="text" onclick="this\\.select\\(\\);" value="(.+)">')
find_thumbnail = re.compile('src="(https:\\/\\/.+_full.jpg)"')
find_id = re.compile('"(\\d{17})"')
find_stats = re.compile('var stats = ({.+});')

# configure settings
options = Options()
options.add_argument('--enable-javascript')
options.add_argument('--headless')

"""
Retrieves stats for a user from https://csgostats.gg.
"""
def get_stats(query):
    driver = webdriver.Chrome(options=options)

    # workaround for being detected as a bot
    # got this from https://stackoverflow.com/a/69766804
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    # find the steamID of the user
    driver.get(f'https://steamid.xyz/{query}')

    result = find_nickname.search(driver.page_source)
    nickname = result.group(1)

    result = find_id.search(driver.page_source)
    id = result.group(1)

    result = find_thumbnail.search(driver.page_source)
    thumbnail = result.group(1)

    driver.get(f'https://csgostats.gg/player/{id}')
    result = find_stats.search(driver.page_source)

    current_rank = driver.find_element(By.XPATH, '//*[@id="content-wrapper"]/div[3]/div[1]/div/div[2]/div[1]/img').get_attribute('src')
    current_rank = ranks[int(current_rank[current_rank.rindex('/')+1:-4])]

    best_rank = driver.find_element(By.XPATH, '//*[@id="content-wrapper"]/div[3]/div[1]/div/div[2]/div[1]/div/img').get_attribute('src')
    best_rank = ranks[int(best_rank[best_rank.rindex('/')+1:-4])]

    stats = json.loads(result.group(1))
    games_played = stats['totals']['overall']['games']
    stats = stats['overall']
    stats['games'] = games_played
    stats['nickname'] = nickname
    stats['thumbnail'] = thumbnail
    stats['current_rank'] = current_rank
    stats['best_rank'] = best_rank

    driver.close()
    return stats