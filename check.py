from config import ALL_CARDS
import os

image_dir = 'images/'

for card in ALL_CARDS:
    if not os.path.isfile(image_dir+card['image']):
        print(card['image'])
