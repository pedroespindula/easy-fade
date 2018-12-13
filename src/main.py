from PIL import Image
import glob
import os
import itertools

STEPS = 60 # FPS
if (STEPS < 1):
  print("INVALID STEPS")
  exit()

RANGE = [1] if (STEPS == 1) else range(STEPS)
JUMP = 100 if (len(RANGE) == 1) else 100/(len(RANGE) - 1)
GIF_DURATION = 2000 / STEPS # GIF DURATION = 2 secs

'''
FADE PROGRESSION
(image 2 alpha factor)
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

def get_faded_image(step, image1, image2):
  # BLACK IMAGE: image2 = Image.frombytes("RGB", (512, 512), bytes([0,0,0]*(512 * 512)))
  if (step == 0):
    print(f"image 1/{STEPS} done")
    return image1
  if (STEPS == 1 or step == (STEPS - 1)):
    print(f"image {STEPS}/{STEPS} done")
    return image2

  image1_data = itertools.chain(*list(image1.getdata())) # flattened
  image2_data = itertools.chain(*list(image2.getdata())) # flattened
  result_image = [apply_factors(step, value1, value2) for (value1, value2) in zip(image1_data, image2_data)]

  print(f"image {step + 1}/{STEPS} done")

  return Image.frombytes("RGB", (512, 512), bytes(result_image))

def apply_factors(step, value1, value2):
  alpha2 = step * JUMP / 100
  alpha1 = 1 - alpha2
  return round(value1 * alpha1 + value2 * alpha2)


def get_image_name(n):
  return 'image{}.jpg'.format(n)


def fade_images(imagens):
  return [get_faded_image(step, i1, i2) for step in RANGE for i1, i2 in zip(imagens, imagens[1::])]


def save_images(images, path):
  for c, i in enumerate(images): save_image(i, path, get_image_name(c))


def save_image(image, path, file_name):
  image.save(os.path.join(path, file_name))


def save_gif(images, path):
  looped_images = images[:-1] + images[-1:0:-1]
  looped_images[0].save(path + 'image_fade.gif',
                 save_all=True,
                 append_images=looped_images[1:],
                 duration=GIF_DURATION,
                 loop=0)

def ensure_dirs(path_in, path_out):
  if not os.path.exists(path_in):
    print(path_in)
    print("Please add an in directory.")
    exit()
  if not os.path.exists(path_out):
    print("Creating out directory.")
    os.mkdir(path_out)

def main():
  path_in = '../in/'
  path_out = '../out/'

  ensure_dirs(path_in, path_out)

  ''' DEBUG
  print(f"NEED {STEPS} STEPS")
  print(f"JUMP IS {JUMP} {list(map(lambda x: x * JUMP, RANGE))}")
  print(f"RANGE HAS {len(RANGE)} STEPS")
  '''

  images = open_images(path_in + "*.*")
  faded_images = fade_images(images)
  save_images(faded_images, path_out)
  save_gif(faded_images, path_out)


if __name__ == '__main__':
  main()
