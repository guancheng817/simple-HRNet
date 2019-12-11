import os
import sys
import argparse
import ast
import cv2
import torch
import vidgear
from vidgear.gears import CamGear
sys.path.insert(1, os.getcwd())
from SimpleHRNet import SimpleHRNet
from misc.visualization import draw_points, draw_skeleton, draw_points_and_skeleton, joints_dict
import time
import numpy as np
import time
import math

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
        options = {"CAP_PROP_FRAME_WIDTH ": 320, "CAP_PROP_FRAME_HEIGHT": 240, "CAP_PROP_FPS ": 1000}
        image_resolution = ast.literal_eval(args.image_resolution)
        has_display = 'DISPLAY' in os.environ.keys() or sys.platform == 'win32'
        video_writer = None

        if args.filename is not None:
            video = cv2.VideoCapture(args.filename)
            assert video.isOpened()
        else:
            #if True:
            if args.disable_vidgear:
                video = cv2.VideoCapture(args.camera_id)
                video.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
                video.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
                video.set(cv2.CAP_PROP_FPS, args.fps)
                #video.set(cv2.CAP_PROP_FRAME_COUNT, 60)
                assert video.isOpened()
            else:
                video = CamGear(source=args.camera_id, **options).start()
        print('fps', video.get(cv2.CAP_PROP_FPS))
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
        cnt = 0
        start_time = time.time()
        while True:
            cnt+=1
            if args.filename is not None or args.disable_vidgear:
                ret, frame = video.read()
                if not ret:
                    break
            else:
                frame = video.read()
                if frame is None:
                    break
            end_time = time.time()
            if (math.floor(end_time*1000) - math.floor(start_time*1000)) >= 1000:
                #frame_rate = 1 / (time.time() - start_time)
                #print('frame_rate', cnt)
                start_time = end_time
                cnt = 0
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

            if args.save_video:
                if video_writer is None:
                    fourcc = cv2.VideoWriter_fourcc(*args.video_format)  # video format
                    video_writer = cv2.VideoWriter('output.avi', fourcc, args.video_framerate,
                                                   (frame.get().shape[1], frame.get().shape[0]))
                video_writer.write(frame)

        if args.save_video:
            video_writer.release()



