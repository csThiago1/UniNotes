import os
from uninotes import app


def image_recover(note_id):
    for filename in os.listdir(app.config['UPLOAD_PATH']):
        if f'cover{note_id}' in filename:
            return filename

    return 'default_cover.png'

def image_delete(note_id):
    for filename in os.listdir(app.config['UPLOAD_PATH']):
        if filename != 'default_cover.png':
            os.remove(app.config['UPLOAD_PATH'] + filename)