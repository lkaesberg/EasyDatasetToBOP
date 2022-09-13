import json
from pathlib import Path
import pymeshlab

from easydatasettobop.bop_dataset_utils import misc
from easydatasettobop.bop_dataset_utils import inout


def convert_models(root_folder: Path, destination_folder: Path, ending: str):
    root_folder = root_folder / "models"
    destination_folder = destination_folder / "models"
    destination_folder.mkdir(exist_ok=True)
    count = 1
    convert_info = {}
    model_info = {}
    for file in root_folder.iterdir():
        if file.is_file() and file.suffix.lower() in [ending]:
            ms = pymeshlab.MeshSet()
            if ending == ".gltf":
                ms.load_new_mesh(file.as_posix(), load_in_a_single_layer=True)
            else:
                ms.load_new_mesh(file.as_posix())
            ms.meshing_poly_to_tri()
            ms.compute_texcoord_by_function_per_vertex()
            name = f"obj_{count:06d}"
            save_file = destination_folder / f"{name}.ply"
            ms.save_current_mesh(save_file.as_posix())
            model = inout.load_ply(save_file.as_posix())
            convert_info[file.stem] = (count, name)
            print(f"Converting model: {file.stem}")
            # Calculate 3D bounding box.
            ref_pt = list(map(float, model['pts'].min(axis=0).flatten()))
            size = list(map(float, (model['pts'].max(axis=0) - ref_pt).flatten()))
            diameter = misc.calc_pts_diameter(model['pts'])
            model_info[str(count)] = {"diameter": diameter,
                                      "min_x": ref_pt[0],
                                      "min_y": ref_pt[1],
                                      "min_z": ref_pt[2],
                                      "size_x": size[0],
                                      "size_y": size[1],
                                      "size_z": size[2],
                                      "symmetries_discrete": [],
                                      "symmetries_continuous": []}
            count += 1
    (destination_folder / "models_info.json").write_text(json.dumps(model_info))
    return convert_info
