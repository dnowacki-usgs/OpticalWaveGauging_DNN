#      ▄▄▌ ▐ ▄▌ ▄▄ •
# ▪     ██· █▌▐█▐█ ▀ ▪
# ▄█▀▄ ██▪▐█▐▐▌▄█ ▀█▄
# ▐█▌.▐▌▐█▌██▐█▌▐█▄▪▐█
# ▀█▄▀▪ ▀▀▀▀ ▀▪·▀▀▀▀
#
## predict_image.py
## A script to use a model on a single image for prediction
## modify config_test.json with relevant inputs
## Written by Daniel Buscombe,
## Northern Arizona University
## daniel.buscombe.nau.edu

# import libraries
import sys, getopt, os
import numpy as np
import json
import glob
import pandas as pd

os.environ["CUDA_VISIBLE_DEVICES"] = "0"  ##use CPU
from utils import *

# ==============================================================
## script starts here
if __name__ == "__main__":
    # image_path = 'snap_images/data/1513706400.cx.snap.jpg' #H = 0.4
    # image_path = 'snap_images/data/1516127400.cx.snap.jpg' #H = 1.85
    # image_path = 'snap_images/data/1516401000.cx.snap.jpg' #H = 2.33

    for prefix in [178]:#np.arange(160,178):
        prefix = str(prefix)
        ipaths = glob.glob(f"/Volumes/Argus/unk/snap/c1/{prefix}*jpg")

        with open(os.getcwd() + os.sep + "config" + os.sep + "config_test.json") as f:
            config = json.load(f)

        # config variables
        im_size = int(config["im_size"])
        category = config["category"]
        weights_path = config["weights_path"]
        samplewise_std_normalization = config["samplewise_std_normalization"]
        samplewise_center = config["samplewise_center"]

        IMG_SIZE = (im_size, im_size)
        # ==============================================================
        print("[INFO] Preparing model...")
        # load json and create model
        # call the utils.py function load_OWG_json
        OWG = load_OWG_json(weights_path)

        print("[INFO] Predicting ...")
        # call the utils.py function pred_1image
        preds = []
        for image_path in ipaths:
            try:
                pred_Y = pred_1image(
                    OWG, image_path, IMG_SIZE, samplewise_std_normalization, samplewise_center
                )
            except:
                preds.append(np.nan)
                continue

            print(image_path, pred_Y)

            preds.append(pred_Y)
            if not len(preds) % 100:
                print("****** ")
                print(len(preds))

        df = pd.DataFrame(
            {
                "time": [
                    pd.Timestamp(int(x.split("/")[-1].split(".")[0]), unit="s") for x in ipaths
                ],
                "path": ipaths,
                "H": preds,
            }
        ).to_csv(f"{prefix}_djn_output_Hs.csv", index=False)
