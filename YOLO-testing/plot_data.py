import matplotlib.pyplot as plt
from PIL import Image
import pandas as pd
import numpy as np
from matplotlib import patches

IMG_SIZE = (1920, 1080)
# Different x_coord calc strategy cuz PIL image plotting is different
# Than ultralytics' standard

if __name__ == "__main__":
    pic = np.array(Image.open("testing.jpg"))
    data = pd.read_csv("base_val_dataset_labels.csv")

    data = data[data["filename"] == "gss1.jpg"]
    row = data.iloc[0]
    print(data)

    x: tuple[int, int] = (row['xmin'], row['xmax'])
    y: tuple[int, int] = (row['ymin'], row['ymax'])
    width = x[1] - x[0] #/ IMG_SIZE[0]
    height = y[1] - y[0] #/ IMG_SIZE[1]
    x_coord = x[0]  #/ IMG_SIZE[0]
    y_coord = y[0] #/ IMG_SIZE[1]

    figure, axis = plt.subplots()
    rect = patches.Rectangle((x_coord, y_coord), width, height, linewidth=1, edgecolor='r', facecolor='none')
    axis.imshow(pic)
    axis.add_patch(rect)
    plt.show()





