import json
from pathlib import Path


def create_camera_file(cx, cy, depth_scale, fx, fy, height, width, home_path: Path):
    (home_path / "camera.json").write_text(
        json.dumps(
            {"cx": cx, "cy": cy, "depth_scale": depth_scale, "fx": fx, "fy": fy, "height": height, "width": width},
            indent=2))


def create_camera_info(root_folder: Path, save_folder: Path):
    for file in root_folder.iterdir():
        if file.is_file() and file.suffix == ".json":
            data = json.loads(file.read_text())
            camera_info = data["cameraInformation"]
            create_camera_file(camera_info["cx"], camera_info["cy"], camera_info["depthScale"], camera_info["fx"],
                               camera_info["fy"], camera_info["height"], camera_info["width"], save_folder)
            break
