import os
import pipes


def postBuild(site):
    command = 'coffee -c %s/static/js/*.coffee' % pipes.quote(site.paths['build'])
    os.system(command)
