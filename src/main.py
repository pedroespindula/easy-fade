from PIL import Image
import glob
import os


def open_images(path):
  return [Image.open(e) for e in glob.glob(path)]

def get_faded_image(i1, i2):
  pass

def get_image_name(n):
  return 'image{}.jpg'.format(n)

def fade_images(imagens):
  return [get_faded_image(i1, i2) for (i1, i2) in zip(imagens, imagens[1::])]

def save_images(images, path):
  for c, i in enumerate(images): save_image(i, path, get_image_name(c))

def save_image(image, path, file_name):
  image.save(os.path.join(path, file_name))


def main():
  path_in = '../in/*.*'
  path_out = '../out/'


  images = open_images(path_in)
  faded_images = fade_images(images)
  save_images(faded_images, path_out)


if __name__ == '__main__':
  main()
