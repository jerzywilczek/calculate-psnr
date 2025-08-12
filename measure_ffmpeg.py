import os
import sys
import calculate
import subprocess

if __name__ == "__main__":
    args = sys.argv

    if len(args) != 5:
        print(f"usage: python {args[0]} input.nv12 output width height")
        exit()

    in_f = args[1]
    out_f = args[2]
    w = int(args[3])
    h = int(args[4])

    presets = [
        "ultrafast",
        "superfast",
        "veryfast",
        "faster",
        "fast",
        "medium",
        "slow",
        "slower",
        "veryslow",
        "placebo"
    ]

    for preset in presets:
        _ = subprocess.run([
                'ffmpeg',
                '-f',
                'rawvideo',
                '-pix_fmt',
                'nv12',
                '-s',
                f'{w}x{h}',
                '-r',
                '30',
                '-i',
                in_f,
                '-c:v',
                'libx264',
                '-preset',
                preset,
                '-x264-params',
                '"nal-hrd=cbr"',
                '-b:v',
                '8000k',
                '-maxrate',
                '10000k',
                '-bufsize',
                '8000k',
                'output.h264',
                '-y'
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        _ = subprocess.run([
                'ffmpeg',
                '-i',
                'output.h264',
                '-c:v',
                'rawvideo',
                '-pix_fmt',
                'nv12',
                out_f,
                '-y'
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        print(preset)
        calculate.print_psnr(w, h, in_f, out_f)

