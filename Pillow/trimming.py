import os
from PIL import Image


def trim_vertical(img_path, save_dir, newimgname, top):
    im = Image.open(img_path)
    # left upper riht lower
    savepath = os.path.join(save_dir, newimgname)
    im_crop = im.crop((0, top, im.size[0], im.size[1])).save(
        savepath, quality=95)


"""=======================================
メイン
========================================"""

if __name__ == '__main__':
    # main
    test2image = './../テスト画像/test-2.jpg'
    trim_vertical(test2image, "", "new.jpg", 82)
