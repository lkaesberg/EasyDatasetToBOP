import argparse

from easydatasettobop.dataset_utils.visualization_dataset import visualize_dataset
from scripts.convert_easy_dataset_to_bop import convert_dataset


def get_arguments():
    parser = argparse.ArgumentParser("Convert EasyDataset to BOP Dataset")

    parser.add_argument('path', help="Path to the root of the EasyDatasetGenerator", type=str)
    parser.add_argument('-v', '--visualize', help="Visualize a converted dataset. Path of the train set (i.e. */bopdataset/train/000000)",
                        action="store_true")
    parser.add_argument('-e', '--ending', help="Generate the .ply models from specified file format", type=str,
                        default=".gltf")
    return parser.parse_args()


if __name__ == '__main__':
    args = get_arguments()
    if args.visualize:
        visualize_dataset(args)
    else:
        convert_dataset(args)
