from PIL import Image
import glob
import os

STEPS = 100
if (STEPS < 1):
  print("INVALID STEPS")
  exit()

RANGE = [1] if (STEPS == 1) else range(STEPS)
JUMP = 100 if (len(RANGE) == 1) else 100/(len(RANGE) - 1)

'''
1 -> 100
2 -> 0, 100
3 -> 0, 50, 100
4 -> 0, 33, 66, 100
5 -> 0, 25, 50, 75, 100
6 -> 0, 20, 40, 60, 80, 100
7 -> 0, 16, 33, 50, 67, 83, 100
'''

def open_images(path):
  return [Image.open(e) for e in glob.glob(path)]

def get_faded_image(factor, i1, i2):
  image1 = i1.getdata()
  image2 = i2.getdata()
  image_faded = [sum_vector(factor, x, y) for (x, y) in zip(image1, image2)]
  flattened = bytes([y for x in image_faded for y in x])
  print(f"image {factor + 1}/{STEPS} done")
  return Image.frombytes("RGB", (512, 512), flattened)

def sum_vector(factor, v1, v2):
  f2 = factor * JUMP / 100
  f1 = 1 - f2
  l1 = list(map(lambda x: x * f1, v1))
  l2 = list(map(lambda x: x * f2, v2))
  final = [(lambda x, y: round(x + y))(x, y) for (x, y) in zip(l1, l2)]
  return final

def get_image_name(n):
  return 'image{}.jpg'.format(n)

def fade_images(imagens):
  return [get_faded_image(factor, i1, i2) for factor in RANGE for i1, i2 in zip(imagens, imagens[1::])]
  # return [get_faded_image(i1, i2) for i1, i2 in zip(imagens, imagens[1::])]

def save_images(images, path):
  for c, i in enumerate(images): save_image(i, path, get_image_name(c))

def save_image(image, path, file_name):
  image.save(os.path.join(path, file_name))


def main():
  path_in = './in/*.*'
  path_out = './out/'

  print(f"NEED {STEPS} STEPS")
  print(f"JUMP IS {JUMP}")
  print(f"RANGE HAS {len(RANGE)} STEPS")
  # [(lambda x: print(round(x * JUMP)))(x) for x in RANGE]

  images = open_images(path_in)
  faded_images = fade_images(images)
  save_images(faded_images, path_out)


if __name__ == '__main__':
  main()
