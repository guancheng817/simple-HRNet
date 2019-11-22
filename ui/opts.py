import argparse

def parse_opts():
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
    parser.add_argument("--max_batch_size", help="maximum batch size used for inference", type=int, default=128)
    parser.add_argument("--disable_vidgear",
                        help="disable vidgear (which is used for slightly better realtime performance)",
                        action="store_true")  # see https://pypi.org/project/vidgear/
    parser.add_argument("--device", help="device to be used (default: cuda, if available)", type=str, default=None)
    parser.add_argument("--save_root", "-s", help="the path to save", type=str, default='/mnt/simple-HRNet/frames')
    parser.add_argument("--save_dir", help="the path to dir for saving", type=str, default='sit_ups_v1')
    parser.add_argument("--stg", help="angle of the shoulder touches ground", type=int, default=5)
    parser.add_argument("--sew", help="angle of shoulder,elbow and wrist", type=int, default=90)
    parser.add_argument("--raise_feet", help="angle of raise feet", type=int, default=10)
    parser.add_argument("--hks", help="angle of hip, knee and shoulder ", type=int, default=70)
    parser.add_argument("--ratio_distance", help="the ratio between x_distance_elblow_knee and x_distance_ankle_knee", type=int, default=0.35)
    parser.add_argument("--timer", help="time of count", type=int, default=240)

    args = parser.parse_args()

    return args
