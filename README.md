# EasyDatasetToBOP
Convert Datasets from the EasyDatasetGenerator to BOP Dataset Format

## Install
```
pip install easydatasettobop
```

## Usage
```
python -m easydatasettobop <path-to-easydataset-generator-root> -e <3d-file-format>
```
#### To visualize the dataset use:
```
python -m easydatasettobop <path-to-bop-train-set> -v
```

## Tips
If you use another 3D model file for creating the bop dataset, it must have the same name as the gltf file for the EasyDatasetGenerator