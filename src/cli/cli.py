from docopt import docopt
from yaml   import safe_load

with open('./src/content/conf.yaml') as conf:
    usage: dict[str, any] = safe_load(conf)

def run() -> None:
    args:  dict[str, any] = docopt(usage.get('usage'), help = usage.get('help'), version = usage.get('information').get('version'))

    if args['--version'] or args['-v']:
        print('test')