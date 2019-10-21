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

# parser = argparse.ArgumentParser()
# parser.add_argument("--camera_id", "-d", help="open the camera with the specified id", type=int, default=0)
# parser.add_argument("--filename", "-f", help="open the specified video (overrides the --camera_id option)",
#                     type=str, default=None)
# parser.add_argument("--hrnet_c", "-c", help="hrnet parameters - number of channels", type=int, default=48)
# parser.add_argument("--hrnet_j", "-j", help="hrnet parameters - number of joints", type=int, default=17)
# parser.add_argument("--hrnet_weights", "-w", help="hrnet parameters - path to the pretrained weights",
#                     type=str, default="/mnt/simple-HRNet/pretrain_models/pytorch/pose_coco/pose_hrnet_w48_384x288.pth")
# parser.add_argument("--hrnet_joints_set",
#                     help="use the specified set of joints ('coco' and 'mpii' are currently supported)",
#                     type=str, default="coco")
# parser.add_argument("--image_resolution", "-r", help="image resolution", type=str, default='(384, 288)')
# parser.add_argument("--single_person",
#                     help="disable the multiperson detection (YOLOv3 or an equivalen detector is required for"
#                          "multiperson detection)",
#                     action="store_true")
# parser.add_argument("--max_batch_size", help="maximum batch size used for inference", type=int, default=16)
# parser.add_argument("--disable_vidgear",
#                     help="disable vidgear (which is used for slightly better realtime performance)",
#                     action="store_true")  # see https://pypi.org/project/vidgear/
# parser.add_argument("--device", help="device to be used (default: cuda, if available)", type=str, default=None)
# parser.add_argument("--save_root", "-s", help="the path to save", type=str, default='/mnt/simple-HRNet/frames')
# args = parser.parse_args()



# def main(camera_id, filename, hrnet_c, hrnet_j, hrnet_weights, hrnet_joints_set, image_resolution, single_person,
#          max_batch_size, disable_vidgear, device, save_root):

class sitUps(object):
    # def __init__(self):
    #     self.error_box_text = ' '
    #     #self.args = args
    #     #self.main()

    def main(self, args):
        if args.device is not None:
            device = torch.device(args.device)
        else:
            if torch.cuda.is_available() and True:
                torch.backends.cudnn.deterministic = True
                device = torch.device('cuda:0')
            else:
                device = torch.device('cpu')

        print(device)

        image_resolution = ast.literal_eval(args.image_resolution)
        has_display = 'DISPLAY' in os.environ.keys() or sys.platform == 'win32'
        has_display = False
        if args.filename is not None:
            video = cv2.VideoCapture(args.filename)
            assert video.isOpened()
        else:
            if args.disable_vidgear:
                video = cv2.VideoCapture(args.camera_id)
                assert video.isOpened()
            else:
                video = CamGear(args.camera_id).start()

        model = SimpleHRNet(
            args.hrnet_c,
            args.hrnet_j,
            args.hrnet_weights,
            resolution=image_resolution,
            #multiperson=not args.single_person,
            multiperson= False,
            max_batch_size=args.max_batch_size,
            device=device
        )
        num_of_frame = 0
        self.num_of_std = 0
        self.error_box_text = ' '
        start = False
        flag = False
        root = os.path.join(args.save_root, 'sit_ups_v3')

        if not os.path.exists(root):
            os.mkdir(root)

        while True:
            if args.filename is not None or args.disable_vidgear:
                ret, self.frame = video.read()
                if not ret:
                    break
            else:
                self.frame = video.read()
                if self.frame is None:
                    break

            pts = model.predict(self.frame)

            for i, pt in enumerate(pts):
                self.frame = draw_points_and_skeleton(self.frame, pt, joints_dict()[args.hrnet_joints_set]['skeleton'], person_index=i,
                                                 points_color_palette='gist_rainbow', skeleton_color_palette='jet',
                                                 points_palette_samples=10)

            if not start:
                self.text_ready = 'please ready'
                angel = self.cal_angle(pts, 'start')
                start = True if angel <= 5 else False
                self.state_box_text = self.text_ready

            elif start:
                self.text_elbow_touch_knee = 'please elbow touch knee'
                self.state_box_text = self.text_elbow_touch_knee

            if has_display:
                cv2.imshow('frame.png', self.frame)
                k = cv2.waitKey(1)
                if k == 27:  # Esc button
                    if args.disable_vidgear:
                        video.release()
                    else:
                        video.stop()
                    break
            else:
                angle  = self.cal_angle(pts, 'stardard')
                if angle <= 50 and start:
                    self.text = "count_{}".format(self.num_of_std)
                    self.frame = self.count(self.frame, self.text , num_of_frame, root, video)
                    self.num_of_std += 1
                    #print(type(frame))

                    start = False
                    flag = True
                elif angle <= 50 and not start and not flag:

                    self.text_error = 'fault wrong hands action'
                    self.error_box_text = self.text_error

                else:
                    self.text = "count_{}".format(self.num_of_std)
                    self.frame = self.count(self.frame, self.text, num_of_frame, root, video)

            yield (self.state_box_text, self.error_box_text, self.frame, self.num_of_std)

            self.error_box_text = ' '
            num_of_frame += 1


    def count(self, frame, text, num_of_frame, root, video):
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
        #cv2.imwrite(root + '/frames_{:0>4}.png'.format(num_of_frame), frame)
        return frame


        #


    def cal_angle(self, pts, flag):
        left_knee_y = pts[0][13][0]
        left_knee_x = pts[0][13][1]

        right_knee_y = pts[0][14][0]
        right_knee_x = pts[0][14][1]
        knee_y = max(left_knee_y, right_knee_y)
        knee_x = max(left_knee_x, right_knee_x)

        left_hip_y = pts[0][11][0]
        left_hip_x = pts[0][11][1]

        right_hip_y = pts[0][12][0]
        right_hip_x = pts[0][12][1]
        hip_y = max(left_hip_y, right_hip_y)
        hip_x = max(left_hip_x, right_hip_x)

        left_shoulder_y = pts[0][5][0]
        left_shoulder_x = pts[0][5][1]

        right_shoulder_y = pts[0][6][0]
        right_shoulder_x = pts[0][6][1]
        shoulder_y = max(left_shoulder_y, right_shoulder_y)
        shoulder_x = max(left_shoulder_x, right_shoulder_x)

        if flag == 'start':
            mid_point_x  = shoulder_x
            mid_point_y  = hip_y
            vec_hip_to_mid = np.array((hip_x - mid_point_x, hip_y - mid_point_y))
            vec_hip_to_shoulder = np.array((hip_x - shoulder_x, hip_y - shoulder_y))

            L_hip_to_mid = np.sqrt(vec_hip_to_mid.dot(vec_hip_to_mid))
            L_hip_to_shoulder = np.sqrt(vec_hip_to_shoulder.dot(vec_hip_to_shoulder))

            cos_angle = vec_hip_to_mid.dot(vec_hip_to_shoulder) / (L_hip_to_mid * L_hip_to_shoulder)

            angle_rad = np.arccos(cos_angle)
            angle = angle_rad * 360 / 2 / np.pi
            #print(angle)
            return angle

        elif flag == 'stardard':
            vec_hip_to_knee = np.array((hip_x - knee_x, hip_y - knee_y))
            vec_hip_to_shoulder = np.array((hip_x - shoulder_x, hip_y - shoulder_y))

            L_hip_to_knee = np.sqrt(vec_hip_to_knee.dot(vec_hip_to_knee))
            L_hip_to_shoulder = np.sqrt(vec_hip_to_shoulder.dot(vec_hip_to_shoulder))

            cos_angle = vec_hip_to_shoulder.dot(vec_hip_to_knee) / (L_hip_to_shoulder * L_hip_to_knee)

            angle_rad = np.arccos(cos_angle)

            angle = angle_rad * 360 / 2 / np.pi
            #print(angle)

            return angle

#main(args)

# if __name__ == '__main__':
#     parser = argparse.ArgumentParser()
#     parser.add_argument("--camera_id", "-d", help="open the camera with the specified id", type=int, default=0)
#     parser.add_argument("--filename", "-f", help="open the specified video (overrides the --camera_id option)",
#                         type=str, default=None)
#     parser.add_argument("--hrnet_c", "-c", help="hrnet parameters - number of channels", type=int, default=48)
#     parser.add_argument("--hrnet_j", "-j", help="hrnet parameters - number of joints", type=int, default=17)
#     parser.add_argument("--hrnet_weights", "-w", help="hrnet parameters - path to the pretrained weights",
#                         type=str, default="/mnt/simple-HRNet/pretrain_models/pytorch/pose_coco/pose_hrnet_w48_384x288.pth")
#     parser.add_argument("--hrnet_joints_set",
#                         help="use the specified set of joints ('coco' and 'mpii' are currently supported)",
#                         type=str, default="coco")
#     parser.add_argument("--image_resolution", "-r", help="image resolution", type=str, default='(384, 288)')
#     parser.add_argument("--single_person",
#                         help="disable the multiperson detection (YOLOv3 or an equivalen detector is required for"
#                              "multiperson detection)",
#                         action="store_true")
#     parser.add_argument("--max_batch_size", help="maximum batch size used for inference", type=int, default=16)
#     parser.add_argument("--disable_vidgear",
#                         help="disable vidgear (which is used for slightly better realtime performance)",
#                         action="store_true")  # see https://pypi.org/project/vidgear/
#     parser.add_argument("--device", help="device to be used (default: cuda, if available)", type=str, default=None)
#     parser.add_argument("--save_root", "-s", help="the path to save", type=str, default='/mnt/simple-HRNet/frames')
#     args = parser.parse_args()
#     main(**args.__dict__)
