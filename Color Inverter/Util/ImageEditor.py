from PIL import Image as im
from PIL import ImageOps as imOps
from Util import DataManager

class Editor:

    path=""
    filename=""
    extension=""

    def __init__(self, path):
        self.path = path
        self.filename = DataManager.extractFilename(path)
        self.extension = DataManager.extractExtension(path)

    def invertColor(self):
        pic = im.open(self.path)
        if pic.mode == 'RGBA':
            r, g, b, a = pic.split()
            rgb_image = im.merge('RGB', (r, g, b))

            inverted_image = imOps.invert(rgb_image)

            r2, g2, b2 = inverted_image.split()

            final_transparent_image = im.merge('RGBA', (r2, g2, b2, a))

            final_transparent_image.save(DataManager.RESULT_FOLDER + "/" + self.filename + self.extension)

        else:
            inverted_image = imOps.invert(pic)
            inverted_image.save(DataManager.RESULT_FOLDER + "/" + self.filename + self.extension)