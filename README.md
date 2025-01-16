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

# Monai airway Segmentation Module

This module helps you to integrate the airway segmentation models to Monai label and to the Slicer.

### Pretrained Models

The pre-trained model for the segmentation can be downloaded from the following links

- Upper airway segmentation (Pre-trained model): [Download Here](http://www.link.com)

### How to Use the App

Below are commands to start the airway segmentation models. Ensure that you specify the correct app and studies path according to your system.

```bash
monailabel start_server --app apps/radiology --studies datasets/Task09_Spleen/imagesTr --conf models airway_segmentation
```

This will start the MONAI Label server locally on your PC at https://localhost:800.

Next, follow these steps in Slicer:

1. Open the .nrrd upper airway volume file you have.
2. Navigate to the MONAI Label extension. If it's not installed, please refer to the installation instructions for MONAI Label in Slicer.
3. Enter 'https://localhost:8000' in the URL section and refresh to detect the MONAI Label server.
4. Once detected, you should see the details filling up in the Slicer module.
5. Go to the Inferencing section of the MONAI Label extension and click "Start" to begin the segmentation process.

The model may take a few minutes to run. Once the results are ready, you will see the segmentations displayed on the image.
