import arsenic
from arsenic import services, browsers
import structlog
import logging
import os
import config
import re
import json

# rank img takes the form:
# https://static.csstats.gg/images/ranks/{i}.png
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
# for searching web page source
find_nickname = re.compile(r'Nick Name\n<input type="text" onclick="this\.select\(\);" value="(.+)">')
find_thumbnail = re.compile(r'src="(https:\/\/.+_full.jpg)"')
find_id = re.compile(r'"(\d{17})"')
find_stats = re.compile(r'var stats = ({.+});')
find_premier_rank = re.compile(r'(\d+)\D+,(\d+)<')

# configure structlog so arsenic doesn't clog the hell out of stdout
# from https://github.com/HENNGE/arsenic/issues/35#issuecomment-451540986
logger = logging.getLogger('arsenic')
structlog.configure(logger_factory=lambda: logger)
logger.setLevel(logging.WARNING)

async def get_stats(query):
    """
    Retrieves stats for a user from https://csstats.gg.
    """
    service = services.Chromedriver(log_file=os.devnull)
    args=['--headless', '--disable-gpu', '--no-sandbox', 
    'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36']
    kwargs = {'goog:chromeOptions': dict(args=args)}
    browser = browsers.Chrome(**kwargs)

    async with arsenic.get_session(service, browser) as session:
        await session.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        await session.get(f'https://steamid.xyz/{query}')

        src = await session.get_page_source()
        result = find_nickname.search(src)
        nickname = result.group(1) if result else "?"

        result = find_id.search(src)
        user_id = result.group(1) if result else None

        result = find_thumbnail.search(src)
        thumbnail = result.group(1) if result else config.BASE_URL

        if user_id:
            await session.get(f"https://csstats.gg/player/{user_id}")
            src = await session.get_page_source()
        else:
            src = ""

        result = find_stats.search(src)
        stats = json.loads(result.group(1) if result else "{}")
        try:
            games_played = stats['totals']['overall']['games']
            csgo_rank = ranks[stats['rank']]
        except KeyError:
            games_played = "?"
            csgo_rank = "?"

        result = find_premier_rank.search(src)
        if result:
            premier_rank = f'{result.group(1)},{result.group(2)}'
        else:
            premier_rank = "?"

        stats = stats.get('overall', dict())
        stats['games'] = games_played
        stats['nickname'] = nickname
        stats['thumbnail'] = thumbnail
        stats['csgo_rank'] = csgo_rank
        stats['premier_rank'] = premier_rank
        return stats
