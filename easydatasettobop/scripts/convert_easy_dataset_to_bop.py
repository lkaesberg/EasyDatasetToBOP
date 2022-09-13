import argparse
import sys
from pathlib import Path

from easydatasettobop.dataset_utils.camera import create_camera_info
from easydatasettobop.dataset_utils.models import convert_models
from easydatasettobop.dataset_utils.train import create_train


def get_arguments():
    parser = argparse.ArgumentParser("Convert EasyDataset to BOP Dataset")

    parser.add_argument('path', help="Path to the root of the EasyDatasetGenerator", type=str)
    parser.add_argument('-e', '--ending', help="Generate the .ply models from specified file format", type=str, default=".gltf")
    return parser.parse_args()


def main():
    args = get_arguments()
    path = Path(args.path)
    print(f"Path: {path}")
    if not path.exists():
        print("This folder doesnt exist!")
        sys.exit()

    save_path = path / f"bop_dataset"
    if save_path.exists():
        print("Dataset already generated!")
        sys.exit()
    save_path.mkdir(exist_ok=True)  # TODO remove exist_ok

    conversion_info = convert_models(path, save_path, args.ending)
    print(conversion_info)
    train_data_folder = path / "trainData"
    create_camera_info(train_data_folder, save_path)
    train_folder = save_path / "train"
    train_folder.mkdir(exist_ok=True)
    print("Create train files!")
    create_train(train_data_folder, train_folder, conversion_info)
    print("Finished!")


if __name__ == '__main__':
    main()
