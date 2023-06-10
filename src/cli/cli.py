from docopt import docopt
from yaml   import safe_load

with open('./src/content/conf.yaml') as conf:
    usage: dict[str, any] = safe_load(conf)

def run(args: list[str]) -> None:
    args:   dict[str, any] = docopt(
        usage.get('usage'),
        argv    = args,
        help    = True, 
        version = usage.get('information').get('ver')
    )


    if args.get('<file_name>'):
        pass # execute Neu-file

    else:
        pass # open Neu-interpreter