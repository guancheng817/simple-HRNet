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
            #multiperson=not single_person,
            multiperson=False,
            max_batch_size=args.max_batch_size,
            device=device
        )

        while True:
            if args.filename is not None or args.disable_vidgear:
                ret, frame = video.read()
                if not ret:
                    break
            else:
                frame = video.read()
                if frame is None:
                    break

            pts = model.predict(frame)

            for i, pt in enumerate(pts):
                frame = draw_points_and_skeleton(frame, pt, joints_dict()[args.hrnet_joints_set]['skeleton'], person_index=i,
                                                 points_color_palette='gist_rainbow', skeleton_color_palette='jet',
                                                 points_palette_samples=10)

            if has_display:
                cv2.imshow('frame.png', frame)
                k = cv2.waitKey(1)
                if k == 27:  # Esc button
                    if args.disable_vidgear:
                        video.release()
                    else:
                        video.stop()
                    break
            else:
                cv2.imwrite('frame.png', frame)



