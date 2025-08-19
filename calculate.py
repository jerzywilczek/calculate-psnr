import math
import numpy as np
import sys

def print_psnr(width: int, height: int, filename_a: str, filename_b: str):
    frame_len = width * height * 3 // 2
    mse_y = 0
    mse_uv = 0
    frame_count = 0
    with open(filename_a, 'rb') as a:
        with open(filename_b, 'rb') as b:
            while True:
                frame_a = a.read(frame_len)
                frame_b = b.read(frame_len)

                if len(frame_a) < frame_len or len(frame_b) < frame_len:
                    break

                frame_a = np.frombuffer(frame_a, dtype=np.uint8)
                frame_b = np.frombuffer(frame_b, dtype=np.uint8)

                a_y = frame_a[:(frame_len * 2 // 3)]
                b_y = frame_b[:(frame_len * 2 // 3)]

                a_uv = frame_a[(frame_len * 2 // 3):]
                b_uv = frame_b[(frame_len * 2 // 3):]



                mse_y += ((a_y - b_y) ** 2).sum() / a_y.shape[0]
                mse_uv += ((a_uv - b_uv) ** 2).sum() / a_uv.shape[0]
                frame_count += 1

    mean_mse_y = mse_y / frame_count
    mean_mse_uv = mse_uv / frame_count

    psnr_y = 20 * math.log10(255) - 10 * math.log10(mean_mse_y)
    psnr_uv = 20 * math.log10(255) - 10 * math.log10(mean_mse_uv)

    print(f"processed {frame_count} frames, mean_mse_y is {mean_mse_y}")
    print(f"psnr for y is {psnr_y} and for uv is {psnr_uv}")

if __name__ == '__main__':
    args = sys.argv

    if len(args) != 5:
        print(f'usage: python {args[0]} a b width height')
        sys.exit()

    (w, h) = (int(args[3]), int(args[4]))

    print_psnr(w, h, args[1], args[2])

