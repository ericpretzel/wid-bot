from pprint import pprint
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
import json

find_stats = re.compile('var stats = {.+};')

# configure settings and open website
options = Options()
options.add_argument('--enable-javascript')
options.add_argument('--headless')

driver = webdriver.Chrome(options=options)

# workaround for being detected as a bot
# got this from https://stackoverflow.com/a/69766804
driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

driver.get('https://csgostats.gg/player/76561198106229202')

result = find_stats.search(driver.page_source)
if not result:
    print("couldn't find stats!")
    exit()

stats = result.group(0)
stats = json.loads(stats[len('var stats = '):-1])

with open('output.txt', 'w') as f:
    pprint(stats, f)

driver.close()