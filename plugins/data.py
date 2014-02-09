"""
Adds our json data to the template context.
"""

import json
import os.path


with open(os.path.join(os.path.dirname(__file__), '../templates/data.json')) as f:
    json_data = json.load(f)


def preBuildPage(site, page, context, data):
    context['data'] = json_data
    return context, data
