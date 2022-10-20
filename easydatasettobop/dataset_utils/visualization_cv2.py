import cv2
import numpy as np
from scipy.spatial.transform import Rotation

bounding_boxes = {
    "obj_000001": [[0.15, 0.2, 0.15], [0, 0, 0]],
    "obj_000008": [[0.04, 0.015, 0.04], [0, 0, 0]],
    "obj_000004": [[0.035, 0.05, 0.035], [0, 0, 0]],
    "obj_000014": [[0.04, 0.045, 0.04], [0, 0, 0]],
    "obj_000020": [[0.06, 0.02, 0.08], [0, 0, 0]]
}


def draw_axis(frame, rotation_vector, translation_vector, camera_matrix, dist_coeffs=np.zeros((4, 1)), size=0.1):
    (points2D, _) = cv2.projectPoints(
        np.array([(0.0, 0.0, 0.0), (size, 0.0, 0.0), (0.0, size, 0.0), (0.0, 0.0, size)]),
        rotation_vector,
        translation_vector, camera_matrix, dist_coeffs)
    frame = cv2.line(frame, (int(points2D[0][0][0]), int(points2D[0][0][1])),
                     (int(points2D[1][0][0]), int(points2D[1][0][1])), (255, 0, 0), 4)
    frame = cv2.line(frame, (int(points2D[0][0][0]), int(points2D[0][0][1])),
                     (int(points2D[2][0][0]), int(points2D[2][0][1])), (0, 255, 0), 4)
    frame = cv2.line(frame, (int(points2D[0][0][0]), int(points2D[0][0][1])),
                     (int(points2D[3][0][0]), int(points2D[3][0][1])), (0, 0, 255), 4)
    return frame


def draw_3d_bounding_box(frame, rotation_vector, translation_vector, camera_matrix, length=0.02, height=0.05,
                         width=0.02, offset_x=0, offset_y=0, offset_z=0,
                         dist_coeffs=np.zeros((4, 1))):
    rotation_euler = Rotation.from_rotvec(rotation_vector[:, 0]).as_euler("xyz")
    rotation_euler[0] += offset_x
    rotation_euler[1] += offset_y
    rotation_euler[2] += offset_z
    rotation_vector = np.array([[x] for x in Rotation.from_euler("xyz", rotation_euler).as_rotvec()])
    (points2D, _) = cv2.projectPoints(
        np.array(
            [(width, length, height), (width, length, -height), (width, -length, height), (width, -length, -height),
             (-width, length, height), (-width, length, -height), (-width, -length, height),
             (-width, -length, -height)]),
        rotation_vector,
        translation_vector, camera_matrix, dist_coeffs)
    frame = cv2.line(frame, (int(points2D[0][0][0]), int(points2D[0][0][1])),
                     (int(points2D[1][0][0]), int(points2D[1][0][1])), (255, 0, 0), 4)
    frame = cv2.line(frame, (int(points2D[0][0][0]), int(points2D[0][0][1])),
                     (int(points2D[2][0][0]), int(points2D[2][0][1])), (255, 0, 0), 4)
    frame = cv2.line(frame, (int(points2D[3][0][0]), int(points2D[3][0][1])),
                     (int(points2D[1][0][0]), int(points2D[1][0][1])), (255, 0, 0), 4)
    frame = cv2.line(frame, (int(points2D[3][0][0]), int(points2D[3][0][1])),
                     (int(points2D[2][0][0]), int(points2D[2][0][1])), (255, 0, 0), 4)

    frame = cv2.line(frame, (int(points2D[4][0][0]), int(points2D[4][0][1])),
                     (int(points2D[5][0][0]), int(points2D[5][0][1])), (255, 0, 0), 4)
    frame = cv2.line(frame, (int(points2D[4][0][0]), int(points2D[4][0][1])),
                     (int(points2D[6][0][0]), int(points2D[6][0][1])), (255, 0, 0), 4)
    frame = cv2.line(frame, (int(points2D[7][0][0]), int(points2D[7][0][1])),
                     (int(points2D[5][0][0]), int(points2D[5][0][1])), (255, 0, 0), 4)
    frame = cv2.line(frame, (int(points2D[7][0][0]), int(points2D[7][0][1])),
                     (int(points2D[6][0][0]), int(points2D[6][0][1])), (255, 0, 0), 4)

    frame = cv2.line(frame, (int(points2D[0][0][0]), int(points2D[0][0][1])),
                     (int(points2D[4][0][0]), int(points2D[4][0][1])), (0, 255, 0), 4)
    frame = cv2.line(frame, (int(points2D[1][0][0]), int(points2D[1][0][1])),
                     (int(points2D[5][0][0]), int(points2D[5][0][1])), (0, 255, 0), 4)
    frame = cv2.line(frame, (int(points2D[2][0][0]), int(points2D[2][0][1])),
                     (int(points2D[6][0][0]), int(points2D[6][0][1])), (0, 255, 0), 4)
    frame = cv2.line(frame, (int(points2D[3][0][0]), int(points2D[3][0][1])),
                     (int(points2D[7][0][0]), int(points2D[7][0][1])), (0, 255, 0), 4)

    return frame


class VisualizeCV2:
    def __init__(self):
        pass

    def update(self, poses, image, camera_matrix):
        if not poses:
            cv2.imshow('Input', image)
            cv2.waitKey(1)
            return

        for obj_name in poses:
            pose = np.array(poses[obj_name][0])
            trans = pose[:3, 3]
            trans = trans / 100
            rot = pose[:3, :3]
            rot = Rotation.from_matrix(rot).as_rotvec()
            if obj_name in bounding_boxes:
                bounding_box = bounding_boxes[obj_name]
                image = draw_3d_bounding_box(image, np.array([[x] for x in rot]), np.array([[x] for x in trans]),
                                             camera_matrix, *bounding_box[0], *bounding_box[1])
            else:
                print(obj_name)
                image = draw_axis(image, np.array([[x] for x in rot]), np.array([[x] for x in trans]),
                                  camera_matrix)

        cv2.imshow('Input', image)
        cv2.waitKey(1)
