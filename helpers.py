import os
from uninotes import app


def image_recover(note_id):
    for filename in os.listdir(app.config['UPLOAD_PATH']):
        if filename.endswith('.jpg'):
            return filename

    return 'default_cover.png'