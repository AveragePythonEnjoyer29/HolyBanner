import requests, sys
from random import shuffle, choice

local_verses = [
    ('Cast all your anxiety on him because he cares for you.', 'Peter 5:7'),
    ('Let the wicked forsake their ways and the unrighteous their thoughts. Let them turn to the LORD, and he will have mercy on them, and to our God, for he will freely pardon.', 'Isaiah 55:7'),
    ('Jesus said, “Father, forgive them, for they do not know what they are doing.” And they divided up his clothes by casting lots.', 'Luke 23:34'),
    ('Whoever conceals their sins does not prosper, but the one who confesses and renounces them finds mercy.', 'Proverbs 28:13 '),
    ('“Do not judge, and you will not be judged. Do not condemn, and you will not be condemned. Forgive, and you will be forgiven.', 'Luke 6:37'),
    ('For if you forgive other people when they sin against you, your heavenly Father will also forgive you. But if you do not forgive others their sins, your Father will not forgive your sins.', 'Matthew 6:14-15'),
    ('Whoever would foster love covers over an offense, but whoever repeats the matter separates close friends.', 'Proverbs 17:9')
]

def get_verse() -> tuple[str, str]:
    """
    get_verse() -> verse, reference

    Returns a random verse

    :returns tuple[str, str]: (verse, reference)
    """

    # placeholder verse
    verse = (
        'In the beginning God created the heavens and the earth.', 
        'Genesis 1:1'
    )

    try:
        with requests.Session() as sess:
            # for some reason the API blocks the requests library
            # so we spoof some headers

            sess.headers = {
                "accept": (
                    "text/html,"
                    "application/xhtml+xml,"
                    "application/xml;q=0.9,"
                    "image/avif,"
                    "image/webp,"
                    "image/apng,"
                    "*/*;q=0.8,"
                    "application/signed-exchange;v=b3;q=0.9"
                ),

                "accept-encoding": "gzip, deflate",
                "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
                "cache-control": "max-age=0",
                "sec-fetch-dest": "document",
                "sec-fetch-mode": "navigate",
                "sec-fetch-site": "none",
                "sec-fetch-user": "?1",
                "sec-gpc": "1",
                "dnt": "1",
                "upgrade-insecure-requests": "1",
                "user-agent": (
                    "Mozilla/5.0 "
                    "(Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 "
                    "(KHTML, like Gecko) "
                    "Chrome/100.0.4896.79 "
                    "Safari/537.36"
                )
            }

            resp = sess.get('https://bible-api.com/?random=verse').json()
            verse = resp['text'].rstrip().strip(), resp['reference']
        
    except Exception: 
        # on errors (such as no internet or api ratelimit)
        # we pick a random local verse

        shuffle(local_verses)
        verse = choice(local_verses)
    
    return verse

if __name__ == '__main__':
    if not '--noclear' in sys.argv:
        print('\033c', end='')

    try:
        verse, reference = get_verse()

        # might look confusing, but all this does is put space between the left side and the reference
        spaces = ' ' * int((len(verse) - len(reference)) - len(verse) / 6)

        print(verse.capitalize())
        print(spaces + reference)

        exit(0)
    except KeyboardInterrupt:
        exit(0)

    except Exception as exc:
        print('Exception occurred!')
        print(str(exc).rstrip())

        exit(1)