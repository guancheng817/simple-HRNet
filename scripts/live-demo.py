import os
import sys
import argparse
import ast
import cv2
import torch
import numpy as np
from vidgear.gears import CamGear

sys.path.insert(1, os.getcwd())

from SimpleHRNet import SimpleHRNet
from misc.visualization import draw_points, draw_skeleton, draw_points_and_skeleton, joints_dict


def main(camera_id, filename, hrnet_c, hrnet_j, hrnet_weights, hrnet_joints_set, image_resolution, single_person,
         max_batch_size, disable_vidgear, device, save_root, save_dir):
    if device is not None:
        device = torch.device(device)
    else:
        if torch.cuda.is_available() and True:
            torch.backends.cudnn.deterministic = True
            device = torch.device('cuda:0')
        else:
            device = torch.device('cpu')

    print(device)

    image_resolution = ast.literal_eval(image_resolution)
    has_display = 'DISPLAY' in os.environ.keys() or sys.platform == 'win32'
    has_display = False

    if filename is not None:
        video = cv2.VideoCapture(filename)
        assert video.isOpened()
    else:
        if disable_vidgear:
            video = cv2.VideoCapture(camera_id)
            assert video.isOpened()
        else:
            video = CamGear(camera_id).start()

    model = SimpleHRNet(
        hrnet_c,
        hrnet_j,
        hrnet_weights,
        resolution=image_resolution,
        multiperson=not single_person,
        max_batch_size=max_batch_size,
        device=device
    )

    num_of_std = 0
    num_of_frame = 0
    start = False
    root = os.path.join(save_root, 'test_v1')

    if not os.path.exists(root):
        os.mkdir(root)

    while True:

        if filename is not None or disable_vidgear:
            ret, frame = video.read()
            if not ret:
                break
        else:
            frame = video.read()
            if frame is None:
                break

        pts = model.predict(frame)
        if len(pts) == 0:
            continue

        for i, pt in enumerate(pts):
            frame = draw_points_and_skeleton(frame, pt, joints_dict()[hrnet_joints_set]['skeleton'], person_index=i,
                                             points_color_palette='gist_rainbow', skeleton_color_palette='jet',
                                             points_palette_samples=10)


        print('num of frame', num_of_frame)

        if not start:
            print('pts', pts)
            angel = cal_angle(pts)
            start = True if angel >= 150 else False
        if has_display:
            cv2.imshow('frame.png', frame)
            k = cv2.waitKey(1)
            if k == 27:  # Esc button
                if disable_vidgear:
                    video.release()
                else:
                    video.stop()
                break
        else:
            left_ear_height = pts[0][3][0]  # pts -> (y,x ,conf)
            right_ear_height = pts[0][4][0]
            avg_ear_height = (left_ear_height + right_ear_height) / 2

            left_writst_height = pts[0][9][0]
            right_writst_height = pts[0][10][0]
            avg_wrist_height = (left_writst_height + right_writst_height) / 2

            left_shoulder_height = pts[0][5][0]
            right_shoulder_height = pts[0][6][0]
            avg_shoulder_height = (left_shoulder_height + right_shoulder_height) / 2

            if avg_ear_height < avg_wrist_height:
                ear_wrist_diff = avg_wrist_height - avg_ear_height
                wrist_shoulder_diff = avg_shoulder_height - avg_wrist_height

                ratio = ear_wrist_diff / wrist_shoulder_diff

                if 0.5 <= ratio <= 2 and start:
                    text = "count:{}".format(num_of_std)
                    num_of_std+=1
                    count(frame, text, num_of_frame, root, video)
                    start = False
                else:
                    text = "count:{}".format(num_of_std)
                    count(frame, text, num_of_frame, root, video)
            else:
                text = "count:{}".format(num_of_std)
                count(frame, text, num_of_frame, root, video)



        num_of_frame += 1

def count(frame, text, num_of_frame, root, video):
    shape = frame.shape
    height = shape[0]
    width = shape[1]
    print(height)
    cv2.putText(frame, text, (int(width / 3), int(height / 15)), cv2.FONT_HERSHEY_PLAIN, 2.0, (0, 0, 255), 2)

    cv2.imshow('frame.png', frame)
    k = cv2.waitKey(1)
    if k == 27:  # Esc button
        if False:
            video.release()
        else:
            video.stop()
        os._exit()

    cv2.imwrite(root + '/frames_{:0>4}.png'.format(num_of_frame), frame)

def cal_angle(pts):

    left_writst_y = pts[0][9][0]
    left_writst_x = pts[0][9][1]
    right_writst_y = pts[0][10][0]
    right_writst_x = pts[0][10][1]


    left_shoulder_y = pts[0][5][0]
    left_shoulder_x = pts[0][5][1]
    right_shoulder_y = pts[0][6][0]
    right_shoulder_x = pts[0][6][1]

    left_elblow_y = pts[0][7][0]
    left_elblow_x = pts[0][7][1]
    right_elblow_y = pts[0][8][0]
    right_elblow_x = pts[0][8][1]

    if left_writst_y >= left_shoulder_y or right_writst_y >= right_shoulder_y:
        return 0

    vec_elbow_to_shoulder = np.array((left_elblow_x - left_shoulder_x, left_elblow_y - left_shoulder_y))
    vec_elbow_to_wrist = np.array((left_elblow_x - left_writst_x, left_elblow_y - left_writst_y))

    L_elbow_to_shoulder = np.sqrt(vec_elbow_to_shoulder.dot(vec_elbow_to_shoulder))
    L_elbow_to_wrist = np.sqrt(vec_elbow_to_wrist.dot(vec_elbow_to_wrist))

    cos_angle = vec_elbow_to_shoulder.dot(vec_elbow_to_wrist) / (L_elbow_to_shoulder * L_elbow_to_wrist)

    print(cos_angle)
    angle = np.arccos(cos_angle)
    angle2 = angle * 360 / 2 / np.pi
    print(angle2)
    #start = True if angle2 >= 150 else False
    return angle2

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--camera_id", "-d", help="open the camera with the specified id", type=int, default=0)
    parser.add_argument("--filename", "-f", help="open the specified video (overrides the --camera_id option)",
                        type=str, default=None)
    parser.add_argument("--hrnet_c", "-c", help="hrnet parameters - number of channels", type=int, default=48)
    parser.add_argument("--hrnet_j", "-j", help="hrnet parameters - number of joints", type=int, default=17)
    parser.add_argument("--hrnet_weights", "-w", help="hrnet parameters - path to the pretrained weights",
                        type=str, default="./weights/pose_hrnet_w48_384x288.pth")
    parser.add_argument("--hrnet_joints_set",
                        help="use the specified set of joints ('coco' and 'mpii' are currently supported)",
                        type=str, default="coco")
    parser.add_argument("--image_resolution", "-r", help="image resolution", type=str, default='(384, 288)')
    parser.add_argument("--single_person",
                        help="disable the multiperson detection (YOLOv3 or an equivalen detector is required for"
                             "multiperson detection)",
                        action="store_true")
    parser.add_argument("--max_batch_size", help="maximum batch size used for inference", type=int, default=16)
    parser.add_argument("--disable_vidgear",
                        help="disable vidgear (which is used for slightly better realtime performance)",
                        action="store_true")  # see https://pypi.org/project/vidgear/
    parser.add_argument("--device", help="device to be used (default: cuda, if available)", type=str, default=None)
    parser.add_argument("--save_root", "-s", help="the path to save", type=str, default='/mnt/simple-HRNet/frames')
    parser.add_argument("--save_dir", help="the dir to save", type=str)
    args = parser.parse_args()
    main(**args.__dict__)
