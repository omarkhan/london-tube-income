import os.path
from glob import glob
from markdown import markdown


rendered = {}

for path in glob(os.path.join(os.path.dirname(__file__), '../markdown/*')):
    name, ext = os.path.splitext(os.path.basename(path))
    with open(path) as f:
        rendered[name] = markdown(f.read())


def preBuildPage(site, page, context, data):
    context['markdown'] = rendered
    return context, data
