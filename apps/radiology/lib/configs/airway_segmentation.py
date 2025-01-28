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

import logging
import os
from typing import Any, Dict, Optional, Union

import lib.infers
import lib.trainers
from monai.networks.nets import UNet
from monai.networks.layers import Norm
from monai.utils import optional_import

from monailabel.interfaces.config import TaskConfig
from monailabel.interfaces.tasks.infer_v2 import InferTask
from monailabel.interfaces.tasks.train import TrainTask
from monailabel.utils.others.generic import download_file, remove_file, strtobool

_, has_cp = optional_import("cupy")
_, has_cucim = optional_import("cucim")

logger = logging.getLogger(__name__)


class AirwaySegmentation(TaskConfig):
    def init(self, name: str, model_dir: str, conf: Dict[str, str], planner: Any, **kwargs):
        super().init(name, model_dir, conf, planner, **kwargs)

        # Labels
        conf_labels = self.conf.get("labels")
        self.labels = (
            {label: idx for idx, label in enumerate(conf_labels.split(","), start=1)}
            if conf_labels
            else {
                "airway": 1,
            }
        )

        # Model Files
        self.path = [
            os.path.join(self.model_dir, f"pretrained_{name}.pth"),  # pretrained
            os.path.join(self.model_dir, f"{name}.pth"),  # published
        ]

        # Remove pre-trained pt if user is using his/her custom labels.
        if conf_labels:
            remove_file(self.path[0])

        self.target_spacing = (1, 1, 1)  # target space for image
        # Setting ROI size - This is for the image padding
        self.roi_size = (128, 128, 16)

        # Network
        self.network = UNet(
        spatial_dims=3,
        in_channels=1,
        out_channels=2,
        channels=(16, 32, 64, 128, 256),
        strides=(2, 2, 2, 2),
        num_res_units=2,
        norm=Norm.BATCH,
    )

    def infer(self) -> Union[InferTask, Dict[str, InferTask]]:
        task: InferTask = lib.infers.AirwaySegmentation(
            path=self.path,
            network=self.network,
            roi_size=self.roi_size,
            target_spacing=self.target_spacing,
            labels=self.labels,
            preload=strtobool(self.conf.get("preload", "false")),
            config={"largest_cc": True if has_cp and has_cucim else False},
        )
        return task

    def trainer(self) -> Optional[TrainTask]:
        output_dir = os.path.join(self.model_dir, self.name)
        load_path = self.path[0] if os.path.exists(self.path[0]) else self.path[1]

        task: TrainTask = lib.trainers.Segmentation(
            model_dir=output_dir,
            network=self.network,
            roi_size=self.roi_size,
            target_spacing=self.target_spacing,
            load_path=load_path,
            publish_path=self.path[1],
            description="Train Segmentation Model",
            labels=self.labels,
        )
        return task
