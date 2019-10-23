import os
import sys
import argparse
import ast
import cv2
import torch
import numpy as np
from vidgear.gears import CamGear
import pandas
sys.path.insert(1, os.getcwd())
from SimpleHRNet import SimpleHRNet
from misc.visualization import draw_points, draw_skeleton, draw_points_and_skeleton, joints_dict




def main(camera_id, filename, hrnet_c, hrnet_j, hrnet_weights, hrnet_joints_set, image_resolution, single_person,
         max_batch_size, disable_vidgear, device, save_root):

#def main():
    if device is not None:
        device = torch.device(device)
    else:
        if torch.cuda.is_available() and True:
            torch.backends.cudnn.deterministic = True
            device = torch.device('cuda:0')
        else:
            device = torch.device('cpu')

    print(device)
    print('max_batch_size',max_batch_size)
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
            print('debug')
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
    num_of_frame = 0
    num_of_std = 0
    start = False
    flag = False
    root = os.path.join(save_root, 'sit_ups_v2_add_angle_hks')

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

        for i, pt in enumerate(pts):
            frame = draw_points_and_skeleton(frame, pt, joints_dict()[hrnet_joints_set]['skeleton'], person_index=i,
                                             points_color_palette='gist_rainbow', skeleton_color_palette='jet',
                                             points_palette_samples=10)

        # if not start:
        #     #print('pts', pts)
        #     angel = cal_angle(pts, 'start')
        #     start = True if angel <= 20 else False

        if not start:
            #text_ready = 'please ready'
            #cv2.putText(frame, text_ready, (50,50), cv2.FONT_HERSHEY_PLAIN, 2.0, (0, 0, 255), 2)
            angle_stg, angle_sew, angle_ewe = cal_angle(pts, 'start')
            print('angle_ewe ',angle_ewe )
            if angle_stg<=5 and angle_sew <= 90 and angle_ewe >= 120:
                start = True
            else:
                start = False
            #start = True if angel <= 5 else False

        # if start:
        #     #text_elbow_touch_knee = 'please elbow touch knee'
        #     cv2.putText(frame, text_elbow_touch_knee, (50, 50), cv2.FONT_HERSHEY_PLAIN, 2.0, (0, 0, 255), 2)



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
            angle_mke, angle_hks  = cal_angle(pts, 'stardard')
            print('angle_mke', angle_mke)
            print('angle_hks', angle_hks)
            # if angle_hks <= 50 and start and flag_elblow_over_knee:
            if start and angle_mke <= 90 and angle_hks <= 50:

                num_of_std += 1
                text = "count_{}".format(num_of_std)
                count(frame, text, num_of_frame, root, video)
                start = False
                flag = True

            elif angle_hks <= 60 and not start and not flag:
                print('True')
                text_error = 'fault wrong hands action'
                cv2.putText(frame, text_error, (330, 50), cv2.FONT_HERSHEY_PLAIN, 2.0, (0, 0, 255), 2)
                text = "count_{}".format(num_of_std)
                count(frame, text, num_of_frame, root, video)
                #print(type(frame))
            else:
                text = "count_{}".format(num_of_std)
                count(frame, text, num_of_frame, root, video)


        print('num_of_frame', num_of_frame)
        #print('pts', pts)
        num_of_frame += 1


def count(frame, text, num_of_frame, root, video):
    shape = frame.shape
    height = shape[0]
    width = shape[1]
    cv2.putText(frame, text, (int(width / 3), int(height / 15)), cv2.FONT_HERSHEY_PLAIN, 2.0, (0, 0, 255), 2)

    # cv2.imshow('frame.png', frame)
    # k = cv2.waitKey(1)
    # if k == 27:  # Esc button
    #     if False:
    #         video.release()
    #     else:
    #         video.stop()
    #     os._exit()

    #return frame
    cv2.imwrite(root + '/frames_{:0>4}.png'.format(num_of_frame), frame)


def cosine_theorem(p1, p2, p3):
    vec_p1_to_p2  = np.array((p1[0] - p2[0], p1[1] - p2[1]))
    vec_p1_to_p3  = np.array((p1[0] - p3[0], p1[1] - p3[1]))

    L_vec_p1_to_p2 = np.sqrt(vec_p1_to_p2.dot(vec_p1_to_p2))
    L_vec_p1_to_p3 = np.sqrt(vec_p1_to_p3.dot(vec_p1_to_p3))

    cos_angle = vec_p1_to_p2.dot(vec_p1_to_p3) / (L_vec_p1_to_p2 * L_vec_p1_to_p3)
    angle_rad = np.arccos(cos_angle)
    angle = angle_rad * 360 / 2 / np.pi

    return  angle

def cal_angle(pts, flag):
    ## knee
    left_knee_y = pts[0][13][0]
    left_knee_x = pts[0][13][1]

    right_knee_y = pts[0][14][0]
    right_knee_x = pts[0][14][1]
    knee_y = max(left_knee_y, right_knee_y)
    knee_x = max(left_knee_x, right_knee_x)

    ## hip
    left_hip_y = pts[0][11][0]
    left_hip_x = pts[0][11][1]

    right_hip_y = pts[0][12][0]
    right_hip_x = pts[0][12][1]
    hip_y = max(left_hip_y, right_hip_y)
    hip_x = max(left_hip_x, right_hip_x)

    ## shoulder
    left_shoulder_y = pts[0][5][0]
    left_shoulder_x = pts[0][5][1]

    right_shoulder_y = pts[0][6][0]
    right_shoulder_x = pts[0][6][1]
    shoulder_y = max(left_shoulder_y, right_shoulder_y)
    shoulder_x = max(left_shoulder_x, right_shoulder_x)

    ## elbow
    left_elbow_y = pts[0][7][0]
    left_elbow_x = pts[0][7][1]

    right_elbow_y = pts[0][8][0]
    right_elbow_x = pts[0][8][1]
    elbow_y = max(left_elbow_y, right_elbow_y)
    elbow_x = max(left_elbow_x, right_elbow_x)

    ## wrist
    left_wrist_y = pts[0][9][0]
    left_wrist_x = pts[0][9][1]

    right_wrist_y = pts[0][10][0]
    right_wrist_x = pts[0][10][1]
    wrist_y = max(left_wrist_y, right_wrist_y)
    wrist_x = max(left_wrist_x, right_wrist_x)

    ## ear
    left_ear_y = pts[0][3][0]
    left_ear_x = pts[0][3][1]

    right_ear_y = pts[0][4][0]
    right_ear_x = pts[0][4][1]
    ear_y = max(left_ear_y, right_ear_y)
    ear_x = max(left_ear_x, right_ear_x)
    if flag == 'start':

        ## angle of shoulder touching ground
        mid_point_x  = shoulder_x
        mid_point_y  = hip_y

        ## angle of shoudler touching ground
        angle_stg = cosine_theorem((hip_x, hip_y), (mid_point_x, mid_point_y), (shoulder_x, shoulder_y))

        ## angle of shoulder, wrist, elbow

        angle_sew = cosine_theorem((elbow_x, elbow_y),(shoulder_x, shoulder_y), (wrist_x, wrist_y))

        ## angle_of elbow, wrist , ear
        angle_ewe =  cosine_theorem((wrist_x, wrist_y), (ear_x, ear_y), (elbow_x, elbow_y))


        # vec_hip_to_mid = np.array((hip_x - mid_point_x, hip_y - mid_point_y))
        # vec_hip_to_shoulder = np.array((hip_x - shoulder_x, hip_y - shoulder_y))
        #
        # L_hip_to_mid = np.sqrt(vec_hip_to_mid.dot(vec_hip_to_mid))
        # L_hip_to_shoulder = np.sqrt(vec_hip_to_shoulder.dot(vec_hip_to_shoulder))
        #
        # cos_angle_stg = vec_hip_to_mid.dot(vec_hip_to_shoulder) / (L_hip_to_mid * L_hip_to_shoulder)
        #
        # angle_rad_stg = np.arccos(cos_angle_stg)
        # angle_shoulder_touch_ground = angle_rad_stg * 360 / 2 / np.pi


        ## angle of shoulder, wrist and elbow
        # vec_elbow_to_shoulder = np.array((elbow_x - shoulder_x, elbow_y - shoulder_y))
        # vec_elbow_to_wrist = np.array((elbow_x - wrist_x, elbow_y - wrist_y))
        #
        # L_elbow_to_shoulder = np.sqrt(vec_elbow_to_shoulder.dot(vec_elbow_to_shoulder))
        # L_elbow_to_wrist = np.sqrt(vec_elbow_to_wrist.dot(vec_elbow_to_wrist))
        #
        # cos_angle_sew = vec_elbow_to_shoulder.dot(vec_elbow_to_wrist) / (L_elbow_to_shoulder * L_elbow_to_wrist)
        # angle_rad_sew = np.arccos(cos_angle_sew)
        # angle_shoulder_elbow_wirst = angle_rad_sew* 360 / 2 / np.pi

        #print(angle_stg ,angle_sew ,angle_ewe)
        return angle_stg ,angle_sew ,angle_ewe

    elif flag == 'stardard':

        mid_point_x =  knee_x
        mid_point_y = elbow_y
        ## angle_of mid_point, knee, elblow

        angle_mke = cosine_theorem((knee_x, knee_y), (mid_point_x, mid_point_y), (elbow_x, elbow_y))

        ## angle of hip, knee ,shoulder
        angle_hks = cosine_theorem((hip_x, hip_y), (knee_x, knee_y), (shoulder_x, shoulder_y))







        L_both_knee = np.sqrt((left_knee_x - right_knee_x)**2 + (left_knee_y - right_knee_y)**2)
        L_knee_to_elblow = np.sqrt((knee_x - elbow_x)**2 + (knee_y - elbow_y)**2)


        flag_elblow_over_knee = True if L_knee_to_elblow <= 2.5*L_both_knee else False



        # vec_hip_to_knee = np.array((hip_x - knee_x, hip_y - knee_y))
        # vec_hip_to_shoulder = np.array((hip_x - shoulder_x, hip_y - shoulder_y))
        #
        # L_hip_to_knee = np.sqrt(vec_hip_to_knee.dot(vec_hip_to_knee))
        # L_hip_to_shoulder = np.sqrt(vec_hip_to_shoulder.dot(vec_hip_to_shoulder))
        #
        # cos_angle = vec_hip_to_shoulder.dot(vec_hip_to_knee) / (L_hip_to_shoulder * L_hip_to_knee)
        #
        # angle_rad = np.arccos(cos_angle)
        #
        # angle = angle_rad * 360 / 2 / np.pi
        #print(angle)

        return angle_mke, angle_hks


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--camera_id", "-d", help="open the camera with the specified id", type=int, default=0)
    parser.add_argument("--filename", "-f", help="open the specified video (overrides the --camera_id option)",
                        type=str, default=None)
    parser.add_argument("--hrnet_c", "-c", help="hrnet parameters - number of channels", type=int, default=48)
    parser.add_argument("--hrnet_j", "-j", help="hrnet parameters - number of joints", type=int, default=17)
    parser.add_argument("--hrnet_weights", "-w", help="hrnet parameters - path to the pretrained weights",
                        type=str, default="/mnt/simple-HRNet/pretrain_models/pytorch/pose_coco/pose_hrnet_w48_384x288.pth")
    parser.add_argument("--hrnet_joints_set",
                        help="use the specified set of joints ('coco' and 'mpii' are currently supported)",
                        type=str, default="coco")
    parser.add_argument("--image_resolution", "-r", help="image resolution", type=str, default='(384, 288)')
    parser.add_argument("--single_person",
                        help="disable the multiperson detection (YOLOv3 or an equivalen detector is required for"
                             "multiperson detection)",
                        action="store_true")
    parser.add_argument("--max_batch_size", help="maximum batch size used for inference", type=int, default=1)
    parser.add_argument("--disable_vidgear",
                        help="disable vidgear (which is used for slightly better realtime performance)",
                        action="store_true")  # see https://pypi.org/project/vidgear/
    parser.add_argument("--device", help="device to be used (default: cuda, if available)", type=str, default=None)
    parser.add_argument("--save_root", "-s", help="the path to save", type=str, default='/mnt/simple-HRNet/frames')
    args = parser.parse_args()
    main(**args.__dict__)
