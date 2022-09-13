import json
import shutil
from pathlib import Path

import cv2
import numpy as np
from scipy.spatial.transform import Rotation


def copy_pictures(root_folder: Path, save_folder: Path, data_order):
    count = 1
    for number in data_order:
        shutil.copy(root_folder / f"image{number}.png", save_folder / f"{count:06d}.png")
        count += 1


def create_mask_images(root_folder: Path, save_folder: Path, data_order):
    count = 1
    for number in data_order:
        img = cv2.imread((root_folder / f"segmentation{number}.png").as_posix())
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_number = 0

        data = json.loads((root_folder / f"data{number}.json").read_text())
        scan_objects = data["scanObjectsData"]
        object_colors = []

        for scan_object in scan_objects:
            object_colors.append(scan_object["color"])

        for color in object_colors:
            split_image = img.copy()
            split_image[np.where(gray != color)] = 0
            split_image[np.where(gray == color)] = 255
            split_image[np.where(gray == color + 1)] = 255
            split_image[np.where(gray == color + 2)] = 255
            split_image[np.where(gray == color - 1)] = 255
            split_image[np.where(gray == color - 2)] = 255
            split_image_gray = cv2.cvtColor(split_image, cv2.COLOR_BGR2GRAY)
            nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(
                split_image_gray.astype(np.uint8), connectivity=4)
            sizes = stats[:, -1]
            max_label = 1
            if len(sizes) == 1:
                out_image = np.zeros(output.shape)
            else:
                max_size = sizes[1]
                for i in range(2, nb_components):
                    if sizes[i] > max_size:
                        max_label = i
                        max_size = sizes[i]

                out_image = np.zeros(output.shape)
                out_image[output == max_label] = 255
            cv2.imwrite((save_folder / f"{count:06d}_{img_number:06d}.png").as_posix(), out_image)
            img_number += 1
        count += 1


def get_translation_rotation(data):
    translation = data["translation"]
    translation = [translation["x"], translation["y"], translation["z"]]
    rotation = data["rotation"]
    rotation = [rotation["x"], rotation["y"], rotation["z"], rotation["w"]]
    rotation = Rotation.from_quat(rotation).as_matrix().flatten().tolist()
    return translation, rotation


def create_scene_camera(root_folder: Path, save_folder: Path, data_order):
    count = 1
    content = {}
    for number in data_order:
        data = json.loads((root_folder / f"data{number}.json").read_text())
        cam_info = data["cameraInformation"]
        translation, rotation = get_translation_rotation(cam_info)
        cam = [cam_info["fx"], cam_info["skew"], cam_info["cx"], 0.0, cam_info["fy"], cam_info["cy"], 0.0, 0.0, 1.0]
        content[str(count)] = {"cam_K": cam, "cam_R_w2c": rotation, "cam_t_w2c": translation,
                               "depth_scale": cam_info["depthScale"]}
        count += 1
    (save_folder / "scene_camera.json").write_text(json.dumps(content))


def create_scene_gt(root_folder: Path, save_folder: Path, data_order, conversion_info):
    count = 1
    content = {}
    for number in data_order:
        data = json.loads((root_folder / f"data{number}.json").read_text())
        objects_data = data["scanObjectsData"]
        objects = []
        for object_data in objects_data:
            translation, rotation = get_translation_rotation(object_data)
            if object_data["name"] in conversion_info:
                object_id = conversion_info[object_data["name"]][0]
            else:
                for object_name in conversion_info:
                    if object_name in object_data["name"]:
                        object_id = object_name
                        break
            objects.append({"cam_R_m2c": rotation, "cam_t_m2c": translation, "obj_id": object_id})
        content[str(count)] = objects
        count += 1
    (save_folder / "scene_gt.json").write_text(json.dumps(content))


def create_scene_gt_info(root_folder: Path, save_folder: Path, data_order):
    count = 1
    content = {}
    for number in data_order:
        data = json.loads((root_folder / f"data{number}.json").read_text())
        objects_data = data["scanObjectsData"]
        objects = []
        for object_data in objects_data:
            bbox_data = object_data["bbox"]
            width = bbox_data["width"]
            height = bbox_data["height"]
            bbox = [bbox_data["x"], bbox_data["y"], width, height]
            px_count_all = width * height
            px_count_valid = width * height
            px_count_visib = width * height
            visib_fract = 0
            if px_count_all > 0:
                visib_fract = px_count_visib / px_count_all
            objects.append(
                {"bbox_obj": bbox, "bbox_visib": bbox, "px_count_all": px_count_all, "px_count_valid": px_count_valid,
                 "px_count_visib": px_count_visib, "visib_fract": visib_fract})
        content[str(count)] = objects
        count += 1
    (save_folder / "scene_gt_info.json").write_text(json.dumps(content))


def create_train(root_folder: Path, save_folder: Path, conversion_info):
    data_folder = save_folder / "000000"
    rgb_folder = data_folder / "rgb"
    mask_folder = data_folder / "mask_visib"
    data_folder.mkdir(exist_ok=True)
    rgb_folder.mkdir(exist_ok=True)
    mask_folder.mkdir(exist_ok=True)
    data_order = []
    for file in root_folder.iterdir():
        if file.is_file() and file.suffix == ".json":
            data_order.append(file.stem.removeprefix("data"))
    copy_pictures(root_folder, rgb_folder, data_order)
    create_mask_images(root_folder, mask_folder, data_order)
    create_scene_gt(root_folder, data_folder, data_order, conversion_info)
    create_scene_gt_info(root_folder, data_folder, data_order)
    create_scene_camera(root_folder, data_folder, data_order)
