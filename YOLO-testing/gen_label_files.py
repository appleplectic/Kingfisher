import pandas as pd

PATH = "sar-dataset/labels/val"
IMG_SIZE = (1920, 1080)

def main():
    data = pd.read_csv("base_val_dataset_labels.csv")

    for idx in data.index.to_list():
        row: pd.Series = data.iloc[idx]
        filename = row['filename'].replace(".jpg", ".txt")
        x: tuple[int, int] = (row['xmin'], row['xmax'])
        y: tuple[int, int] = (row['ymin'], row['ymax'])
        width = (x[1] - x[0]) / IMG_SIZE[0]
        height = (y[1] - y[0]) / IMG_SIZE[1]
        x_coord = round((x[1] + x[0]) / 2) / IMG_SIZE[0]
        y_coord = round((y[1] + y[0]) / 2) / IMG_SIZE[1]
        with open(PATH + "/" + filename, "a") as f:
            f.write(f"0 {x_coord} {y_coord} {width} {height}\n")

if __name__ == "__main__":
    main()
