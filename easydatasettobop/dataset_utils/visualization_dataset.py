import json
import os

import cv2
import numpy as np

from easydatasettobop.dataset_utils.visualization_cv2 import VisualizeCV2


def visualize_dataset(args):
    path = args.path
    first_file = True
    visualization = VisualizeCV2()
    f = open(path + "/scene_gt.json")
    poses = json.load(f)
    f = open(path + "/scene_gt_info.json")
    infos = json.load(f)
    for file in sorted(os.listdir(path + "/rgb")):
        image_number = int(file.rstrip(".png"))
        if first_file:
            f = open(path + "/scene_camera.json")
            camera_k = json.load(f)[str(image_number)]["cam_K"]
            camera_k = np.array(camera_k).reshape((3, 3))
            print(camera_k)
            first_file = False
        object_poses = poses[str(image_number)]
        object_infos = infos[str(image_number)]
        detections = {}
        for pose in object_poses:
            detection = []
            object_pose = np.identity(4)
            object_pose[:3, :3] = np.array(pose["cam_R_m2c"]).reshape((3, 3))
            object_pose[:3, 3] = np.array(pose["cam_t_m2c"])
            print(object_pose)
            detection.append(object_pose)
            detections[f"obj_{pose['obj_id']:06d}"] = detection

        img_bgr = cv2.imread(path + "/rgb/" + file)
        for object_info in object_infos:
            bbox = object_info["bbox_obj"]
            img_bgr = cv2.rectangle(img=img_bgr, pt1=(int(bbox[0]), int(bbox[1])),
                                    pt2=(int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3])),
                                    color=(0, 0, 255), thickness=2)
        visualization.update(detections, img_bgr, camera_k)
        input()
        image_number += 1
