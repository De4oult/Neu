from docopt import docopt
from yaml   import safe_load

with open('./content/conf.yaml') as conf:
    usage = safe_load(conf)

args = docopt(usage)
print(args)