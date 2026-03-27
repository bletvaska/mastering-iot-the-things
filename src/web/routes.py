import json
from machine import reset

from microdot import Microdot, send_file, Response
from microdot.utemplate import Template

from models.settings import Settings
from constants import SETTINGS_FILE

app = Microdot()
Template.initialize(template_dir='www/templates')
Response.default_content_type = 'text/html'


@app.route('/static/<path:path>')
async def static(request, path):
    if '..' in path:
        # directory traversal is not allowed
        return 'Not found', 404
    return send_file(f'/www/static/{path}', max_age=86400)


@app.route('/')
async def index(request):
    return Template('base.html').render()

#
# @app.route('/settings')
# async def write_settings(request):
#     settings = Settings()
#     with open(SETTINGS_FILE, 'w') as file:
#         json.dump(settings.model_dump(), file)
#     return 'settings have been written'
#
#
# @app.route('/reboot')
# async def reboot(request):
#     reset()
