# Copyright (c) MONAI Consortium
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Callable, Sequence
from monai.inferers import Inferer, SlidingWindowInferer
from monai.transforms import (
    Activationsd,
    AsDiscreted,
    EnsureChannelFirstd,
    EnsureTyped,
    KeepLargestConnectedComponentd,
    LoadImaged,
    Orientationd,
    ScaleIntensityd,
    ScaleIntensityRanged,
    Spacingd,
    Lambdad,
    Transposed,
    CropForegroundd
)

from monailabel.interfaces.tasks.infer_v2 import InferType
from monailabel.tasks.infer.basic_infer import BasicInferTask
from monailabel.transform.post import Restored


class AirwaySegmentation(BasicInferTask):
    """
    This provides Inference Engine for pre-trained Segmentation (SegResNet) model.
    """

    def __init__(
        self,
        path,
        network=None,
        target_spacing=(1.0, 1.0, 1.0),
        type=InferType.SEGMENTATION,
        labels=None,
        dimension=3,
        description="A pre-trained model for volumetric (3D) Segmentation from upper airway MRI",
        **kwargs,
    ):
        super().__init__(
            path=path,
            network=network,
            type=type,
            labels=labels,
            dimension=dimension,
            description=description,
            load_strict=False,
            **kwargs,
        )
        self.target_spacing = target_spacing

    def print_shape(self, image):
        print("###################### input shape",image.shape)
        return image

    def pre_transforms(self, data=None) -> Sequence[Callable]:
        t = [
        LoadImaged(keys=["image"],
                reader="NrrdReader", image_only=True),
        EnsureChannelFirstd(keys=["image"]),
        ScaleIntensityRanged(
            keys=["image"],
            a_min=-57,  # Minimum intensity value of the input
            a_max=1000,  # Maximum intensity value of the input
            b_min=0.0,  # Minimum value after scaling
            b_max=1.0,  # Maximum value after scaling
            clip=True,),
        ]
        return t

    def inferer(self, data=None) -> Inferer:
        return SlidingWindowInferer(
            roi_size=self.roi_size,
            sw_batch_size=2,
        )

    def inverse_transforms(self, data=None):
        return []

    def binarize(self, label, threshold=0):
        binary_mask = (label < threshold)
        binary_mask[binary_mask > 0] = 1  # Set all non-zero pixels to 1
        return binary_mask

    def post_transforms(self, data=None) -> Sequence[Callable]:
        t = [
            EnsureTyped(keys="pred", device=data.get("device") if data else None),
            Lambdad(("pred"), self.binarize),
            Restored(keys="pred", ref_image="image"),
        ]
        return t
