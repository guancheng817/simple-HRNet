import os
import sys
import argparse
import ast
import cv2
import torch
from vidgear.gears import CamGear
sys.path.insert(1, os.getcwd())
from SimpleHRNet import SimpleHRNet
from misc.visualization import draw_points, draw_skeleton, draw_points_and_skeleton, joints_dict
import time
import numpy as np
class sitUps(object):
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
        has_display =False
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
        root = os.path.join(args.save_root, 'sit_ups_v4')

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
                self.text_ready = '请双肩着地，双手抱头'
                angle_stg, angle_sew, angle_hma_start = self.cal_angle(pts, 'start')
                if angle_stg <= 5 and angle_sew <= 90 and angle_hma_start <= 10:
                    start = True
                else:
                    start = False
                self.state_box_text = self.text_ready

            elif start:
                self.text_elbow_touch_knee = '请双手爆头坐起肘部触膝'
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
                ratio_between_distance, angle_hks, angle_hma_standard, x_diff_elbow_knee, avg_conf = self.cal_angle(pts, 'stardard')
                if avg_conf < 0.2:
                    start = False
                    self.text = "count_{}".format(self.num_of_std)
                    self.count(self.frame, self.text, num_of_frame, root, video)
                    num_of_frame += 1
                    continue

                raise_feet = False if np.absolute(angle_hma_start - angle_hma_standard) <= 5 else True
                if angle_hks <= 70 and start and (ratio_between_distance or x_diff_elbow_knee < 0) and not raise_feet:
                    self.text = "count_{}".format(self.num_of_std)
                    self.count(self.frame, self.text , num_of_frame, root, video)
                    self.num_of_std += 1
                    start = False
                    flag = True
                elif angle_hks <= 70 and (ratio_between_distance or x_diff_elbow_knee < 0) and not raise_feet and not start and not flag:
                    self.text_error = '犯规，手部动作不规范'
                    self.error_box_text = self.text_error
                    self.text = "count_{}".format(self.num_of_std)
                    self.count(self.frame, self.text, num_of_frame, root, video)
                else:
                    self.text = "count_{}".format(self.num_of_std)
                    self.count(self.frame, self.text, num_of_frame, root, video)

            #yield (self.state_box_text, self.error_box_text, self.frame, self.num_of_std)
            #print('time', time.time() - start_time)
            self.error_box_text = ' '
            print('pts', pts)
            #print('num_of_frame',num_of_frame)
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
        cv2.imwrite(root + '/frames_{:0>4}.png'.format(num_of_frame), frame)


    def cosine_theorem(self, p1, p2, p3):
        vec_p1_to_p2 = np.array((p1[0] - p2[0], p1[1] - p2[1]))
        vec_p1_to_p3 = np.array((p1[0] - p3[0], p1[1] - p3[1]))

        L_vec_p1_to_p2 = np.sqrt(vec_p1_to_p2.dot(vec_p1_to_p2))
        L_vec_p1_to_p3 = np.sqrt(vec_p1_to_p3.dot(vec_p1_to_p3))
        # if L_vec_p1_to_p3 == 0 or L_vec_p1_to_p2 == 0:
        #     return 0.0
        cos_angle = vec_p1_to_p2.dot(vec_p1_to_p3) / (L_vec_p1_to_p2 * L_vec_p1_to_p3)
        angle_rad = np.arccos(cos_angle)
        angle = angle_rad * 360 / 2 / np.pi

        return angle

    def x_distance(self, p1, p2):
        return np.absolute(p1 - p2)

    def cal_angle(self, pts, flag):
        try:
            ## knee
            left_knee_y = pts[0][13][0]
            left_knee_x = pts[0][13][1]
            left_knee_conf = pts[0][13][2]

            right_knee_y = pts[0][14][0]
            right_knee_x = pts[0][14][1]
            right_knee_conf = pts[0][14][2]

            knee_y = max(left_knee_y, right_knee_y)
            # knee_x = max(left_knee_x, right_knee_x)
            # knee_y = (left_knee_y + right_knee_y) / 2
            knee_x = (left_knee_x + right_knee_x) / 2

            ## hip
            left_hip_y = pts[0][11][0]
            left_hip_x = pts[0][11][1]

            right_hip_y = pts[0][12][0]
            right_hip_x = pts[0][12][1]
            hip_y = max(left_hip_y, right_hip_y)
            hip_x = max(left_hip_x, right_hip_x)

            # hip_y = (left_hip_y + right_hip_y) / 2
            # hip_x = (left_hip_x + right_hip_x) / 2

            ## shoulder
            left_shoulder_y = pts[0][5][0]
            left_shoulder_x = pts[0][5][1]

            right_shoulder_y = pts[0][6][0]
            right_shoulder_x = pts[0][6][1]
            shoulder_y = max(left_shoulder_y, right_shoulder_y)
            shoulder_x = max(left_shoulder_x, right_shoulder_x)

            # shoulder_y = (left_shoulder_y + right_shoulder_y)/ 2
            # shoulder_x = (left_shoulder_x + right_shoulder_x)/ 2

            ## elbow
            left_elbow_y = pts[0][7][0]
            left_elbow_x = pts[0][7][1]

            right_elbow_y = pts[0][8][0]
            right_elbow_x = pts[0][8][1]

            elbow_y = max(left_elbow_y, right_elbow_y)
            elbow_x = min(left_elbow_x, right_elbow_x)

            # elbow_y = (left_elbow_y+right_elbow_y)/ 2
            # elbow_x = (left_elbow_x+ right_elbow_x)/ 2

            ## wrist
            left_wrist_y = pts[0][9][0]
            left_wrist_x = pts[0][9][1]

            right_wrist_y = pts[0][10][0]
            right_wrist_x = pts[0][10][1]
            wrist_y = max(left_wrist_y, right_wrist_y)
            wrist_x = max(left_wrist_x, right_wrist_x)

            # wrist_y = (left_wrist_y+ right_wrist_y)/ 2
            # wrist_x = (left_wrist_x+ right_wrist_x)/ 2

            ## ear
            left_ear_y = pts[0][3][0]
            left_ear_x = pts[0][3][1]

            right_ear_y = pts[0][4][0]
            right_ear_x = pts[0][4][1]
            ear_y = max(left_ear_y, right_ear_y)
            ear_x = max(left_ear_x, right_ear_x)
            # ear_y = (left_ear_y + right_ear_y)/ 2
            # ear_x = (left_ear_x + right_ear_x)/ 2

            ## ankle
            left_ankle_y = pts[0][15][0]
            left_ankle_x = pts[0][15][1]
            left_ankle_conf = pts[0][15][2]

            right_ankle_y = pts[0][16][0]
            right_ankle_x = pts[0][16][1]
            right_ankle_conf = pts[0][16][2]

            ankle_y = max(left_ankle_y, right_ankle_y)
            # ankle_x = max(left_ankle_x, right_ankle_x)
            ankle_x = (left_ankle_x + right_ankle_x) / 2

            if flag == 'start':

                ## angle of shoulder touching ground
                mid_point_shoulder_hip_x = shoulder_x
                mid_point_shoulder_hip_y = hip_y

                ## angle of shoudler touching ground
                angle_stg = self.cosine_theorem((hip_x, hip_y), (mid_point_shoulder_hip_x, mid_point_shoulder_hip_y),
                                           (shoulder_x, shoulder_y))

                ## angle of shoulder, wrist, elbow

                angle_sew = self.cosine_theorem((elbow_x, elbow_y), (shoulder_x, shoulder_y), (wrist_x, wrist_y))

                ## angle_of elbow, wrist , ear
                angle_ewe = self.cosine_theorem((wrist_x, wrist_y), (ear_x, ear_y), (elbow_x, elbow_y))

                ## angle of ankle, hip of start
                mid_point_ankle_hip_x = hip_x
                mid_point_ankle_hip_y = ankle_y
                angle_hma_start = self.cosine_theorem((ankle_x, ankle_y), (hip_x, hip_y),
                                                 (mid_point_ankle_hip_x, mid_point_ankle_hip_y))

                return angle_stg, angle_sew, angle_hma_start

            elif flag == 'stardard':

                mid_point_x = knee_x
                mid_point_y = elbow_y

                ## angle of hip, knee ,shoulder
                angle_hks = self.cosine_theorem((hip_x, hip_y), (knee_x, knee_y), (shoulder_x, shoulder_y))

                ## the distance
                x_distance_ankle_knee = self.x_distance(knee_x, ankle_x)
                x_distance_elblow_knee = self.x_distance(elbow_x, knee_x)

                if x_distance_elblow_knee <= 0.25 * x_distance_ankle_knee:
                    ratio_between_distance = True
                else:
                    ratio_between_distance = False
                #print('x_distance_ankle_knee', x_distance_ankle_knee)
                #print('x_distance_elblow_knee', x_distance_elblow_knee)

                ## angle of ankle, hip of standard
                mid_point_ankle_hip_x = hip_x
                mid_point_ankle_hip_y = ankle_y
                angle_hma_standard = self.cosine_theorem((ankle_x, ankle_y), (hip_x, hip_y),
                                                    (mid_point_ankle_hip_x, mid_point_ankle_hip_y))

                if hip_x > knee_x:
                    x_diff_elbow_knee = elbow_x - knee_x
                else:
                    x_diff_elbow_knee = knee_x - elbow_x


                ### confidence of ankle,knee
                #avg_conf = (left_knee_conf + right_knee_x + left_ankle_conf + right_ankle_conf) / 4
                avg_conf = (left_ankle_conf + right_ankle_conf) / 2
                return ratio_between_distance, angle_hks, angle_hma_standard, x_diff_elbow_knee, avg_conf
        except IndexError as e:
            print('视频中没有人物出现，请把摄像头对准人')