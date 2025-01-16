<!--
Copyright (c) MONAI Consortium
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-->

# Monai Label Airway Segmentation Module for Slicer

This module helps you to integrate the airway segmentation models to Monai label and to the Slicer.

## Pretrained Models

The pre-trained model for the segmentation can be downloaded from the following links

- Upper airway segmentation (Pre-trained model): [Download Here](http://www.subinek.com)

## How to Use the App

1.  download and unzip this folder.

2.  You may have to download the data and dataset folders from Monai. follow these steps

```bash
    # install MONAI Label
    pip install monailabel

    # download Task MSD dataset
    monailabel datasets --download --name Task09_Spleen --output
    # Monai label server won't run without a dataset folder
```

3.  After unzipping run the following commands in your conda evirnment to initialize the monai label server.
    Below are commands to start the airway segmentation models. Ensure that you specify the correct app and studies path according to your system.

```bash
    monailabel start_server --app apps/radiology --studies datasets/Task09_Spleen/imagesTr --conf models airway_segmentation
```

This will start the MONAI Label server locally on your PC at https://localhost:8000.

4. Next, follow these steps in Slicer:

   1. Open the .nrrd upper airway volume file you have.
   2. Navigate to the MONAI Label extension. If it's not installed, please refer to the installation instructions for MONAI Label in Slicer.
   3. Enter 'https://localhost:8000' in the URL section and refresh to detect the MONAI Label server.
   4. Once detected, you should see the details filling up in the Slicer module.
   5. Go to the Inferencing section of the MONAI Label extension and click "Start" to begin the segmentation process.

The model may take a few minutes to run. Once the results are ready, you will see the segmentations displayed on the image.

## Note

This module consists of two custom python files located in the app folder. After installing the MONAI radiology app, you can just place these files into the app/radiology folder if you are already familiear with the Monai label.

```
- File 1: `apps/radiology/lib/configs/airway_segmentation.py`
- File 2: `apps/radiology/lib/infers/airway_segmentation.py`
```

## Citation

Please cite the following papers when using the code:

1. S Erattakulangara, Exploring Advanced MRI Airway Segmentation Techniques for Voice Analysis: A Comparative Study of 3DUNet, 2DUNet, 3D Transfer Learning UNet, and 3D Transformer UNet
