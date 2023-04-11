"""
Split files in train and test folders
"""

# import torch
# import torch.nn as nn
# import torch.nn.functional as F
# import torch.optim as optim
# import torch.optim.lr_scheduler as lr_scheduler
# from torch.optim.lr_scheduler import _LRScheduler
# import torch.utils.data as data

# import torchvision.transforms as transforms
# import torchvision.datasets as datasets
# import torchvision.models as models

from sklearn import decomposition
from sklearn import manifold
from sklearn.metrics import confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay
import matplotlib.pyplot as plt
import numpy as np

import copy
from collections import namedtuple
import os
import random
import shutil
import time

"""Next, we'll set the random seeds for reproducability."""

SEED = 1234

random.seed(SEED)
np.random.seed(SEED)
# torch.manual_seed(SEED)
# torch.cuda.manual_seed(SEED)
# torch.backends.cudnn.deterministic = True



# # REPLACE THESE WITH YOUR OWN KAGGLE USERNAME AND KEY
# os.environ['KAGGLE_USERNAME'] = 'YOUR_KAGGLE_USERNAME_HERE'
# os.environ['KAGGLE_KEY'] = 'YOUR_KAGGLE_KEY_HERE'

# !pip install kaggle
# !kaggle datasets download veeralakrishna/200-bird-species-with-11788-images --unzip

# ROOT = 'data'

# datasets.utils.extract_archive('CUB_200_2011.tgz', ROOT)

"""To handle using custom datasets, torchvision provides a [`datasets.ImageFolder`](https://pytorch.org/vision/stable/datasets.html#torchvision.datasets.ImageFolder) class. 

`ImageFolder` expects data to be stored in the following way:

```
root/class_x/xxy.png
root/class_x/xxz.jpg

root/class_y/123.jpeg
root/class_y/nsdf3.png
root/class_y/asd932_.jpg
```

That is, each folder in the root directory is the name of a class, and within each of those folders are the images that correspond to that class. The images in the downloaded dataset are currently in the form of:

```
CUB_200_2011/images/class_a/image_1.jpg
CUB_200_2011/images/class_a/image_2.jpg

CUB_200_2011/images/class_b/image_1.jpg
CUB_200_2011/images/class_b/image_2.jpg

CUB_200_2011/images/class_c/image_1.jpg
CUB_200_2011/images/class_c/image_2.jpg
```

This means we could call `datasets.ImageFolder(root = '.data/CUB_200_2011/images)` and it would load all of the data. However, we want to split our data into train and test splits. This could be done with `data.random_split`, which we have used in the past to create our validation sets - but we will show how to manually create a `train` and `test` folder and store the relevant images in those folders. This way means that we only need to create a train/test split once and re-use it each time we re-run the notebook

We first set a `TRAIN_RATIO` which will decide what percentage of the images per class are used to make up the training set, with the remainder making up the test set. We create a `train` and `test` folder within the `CUB_200_2011` folder - after first deleting them if they already exist. Then, we get a list of all classes and loop through each class. For each class we get the image names, use the first `TRAIN_RATIO` of them for the training set and the remainder for the test set. We then copy - with `shutil.copyfile` - each of the images into their respective `train` or `test` folder. It is usually better to copy, rather than move, the images to create your custom splits just in case we accidentally mess up somewhere.

After running the below cell we have our training set as:

```
CUB_200_2011/images/train/class_a/image_1.jpg
CUB_200_2011/images/train/class_a/image_2.jpg

CUB_200_2011/images/train/class_b/image_1.jpg
CUB_200_2011/images/train/class_b/image_2.jpg

CUB_200_2011/images/train/class_b/image_1.jpg
CUB_200_2011/images/train/class_b/image_2.jpg
```

and our test set as:

```
CUB_200_2011/images/test/class_a/image_48.jpg
CUB_200_2011/images/test/class_a/image_49.jpg

CUB_200_2011/images/test/class_b/image_48.jpg
CUB_200_2011/images/test/class_b/image_49.jpg

CUB_200_2011/images/test/class_c/image_48.jpg
CUB_200_2011/images/test/class_c/image_49.jpg
```

This train/test split only needs to be created once and does not need to be created again on subsequent runs.

**Note:** `ImageFolder` will only load files that have image related extensions, i.e. jpg/jpeg/png, so if there was, for example, a `.txt` file in one of the class folders then it would not be loaded with the images. If we wanted more flexibility when deciding which files to load or not - such as not loading .png images or loading images with an esoteric format - then we could either use the `is_valid_file` argument of the `ImageFolder` class or use [`DatasetFolder`](https://pytorch.org/vision/stable/datasets.html#torchvision.datasets.DatasetFolder) and provide a list of valid extensions to the `extensions` argument.
"""

# from google.colab import drive
# drive.mount('/content/drive')

# !unzip -q /content/drive/MyDrive/Data_ml/maps/data_2.zip -d /content/drive/MyDrive/Data_ml/maps/

ROOT = '/Users/kar/Documents/maps/tiles/data'
TRAIN_RATIO = 0.85

data_dir = os.path.join(ROOT, 'images')
# images_dir = os.path.join(data_dir, 'images')
images_dir = ROOT
train_dir = os.path.join(ROOT,  'train')
test_dir = os.path.join(ROOT, 'test')

if os.path.exists(train_dir):
    shutil.rmtree(train_dir)
if os.path.exists(test_dir):
    shutil.rmtree(test_dir)

os.makedirs(train_dir)
os.makedirs(test_dir)

classes = os.listdir(data_dir)
classes.remove('.DS_Store')
print(classes)
#
for c in classes:

    class_dir = os.path.join(data_dir, c)
    # print(f'clas_dir={class_dir}')

    images = os.listdir(class_dir)
    # print(f'images={images}')

    n_train = int(len(images) * TRAIN_RATIO)
    print(f'len(images) = {len(images)}, n_train= {n_train}, {len(images)-n_train}')

    train_images = images[:n_train]
    test_images = images[n_train:]

    os.makedirs(os.path.join(train_dir, c), exist_ok=True)
    os.makedirs(os.path.join(test_dir, c), exist_ok=True)

    for image in train_images:
        if not image == '.DS_Store':
            image_src = os.path.join(class_dir, image)
            image_dst = os.path.join(train_dir, c, image)
            if not os.path.isdir(image_src):
                shutil.copyfile(image_src, image_dst)

    for image in test_images:
        if not image == '.DS_Store':
            image_src = os.path.join(class_dir, image)
            image_dst = os.path.join(test_dir, c, image)
            if not os.path.isdir(image_src):
                shutil.copyfile(image_src, image_dst)