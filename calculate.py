import math
import numpy as np
import sys

def print_psnr(width: int, height: int, filename_a: str, filename_b: str):
    frame_len = width * height * 3 // 2
    mse = 0
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

                mse += ((frame_a - frame_b) ** 2).sum() / frame_a.shape[0]
                frame_count += 1

    mean_mse = mse / frame_count

    psnr = 20 * math.log10(255) - 10 * math.log10(mean_mse)

    print(f"processed {frame_count} frames, mean_mse is {mean_mse} and psnr is {psnr}")

if __name__ == '__main__':
    args = sys.argv

    if len(args) != 5:
        print(f'usage: python {args[0]} a b width height')
        sys.exit()

    (w, h) = (int(args[3]), int(args[4]))

    print_psnr(w, h, args[1], args[2])

