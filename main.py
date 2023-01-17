import os
import sys
import cv2
import qrcode
import platform
import webbrowser
import numpy as np
import matplotlib.pyplot as plt

from typing import Union


BASE_PATH: str   = os.path.dirname(os.path.abspath(__file__))
INPUT_PATH: str  = os.path.join(BASE_PATH, "input")
OUTPUT_PATH: str = os.path.join(BASE_PATH, "output")


def breaker(num: int = 50, char: str = "*") -> None:
    print("\n" + num*char + "\n")


def show_image(image, cmap: str = "gnuplot2", title: str=None) -> None:
    plt.figure()
    plt.imshow(image, cmap=cmap)
    plt.axis("off")
    if title: plt.title(title)
    if platform.system() == "Windows":
        figmanager = plt.get_current_fig_manager()
        figmanager.window.state("zoomed")
    plt.show()


def main():

    args_1: tuple = ("--mode", "-m")
    args_2: tuple = ("--data", "-d")
    args_3: tuple = ("--version", "-v")
    args_4: tuple = ("--box-size", "-bxs")
    args_5: tuple = ("--border", "-b")
    args_6: tuple = ("--background", "-bg")
    args_7: tuple = ("--foreground", "-fg")
    args_8: tuple = ("--save", "-s")
    args_9: tuple = ("--filename", "-f")

    mode: Union[str, None] = None
    data: Union[str, None] = None
    version: int = 1
    box_size: int = 10
    border: int = 4
    fg_color: list = "0,0,0"
    bg_color: list = "255,255,255"
    save: bool = True
    filename: Union[str, None] = None

    fg: list = []
    bg: list = []

    if args_1[0] in sys.argv: mode = sys.argv[sys.argv.index(args_1[0]) + 1]
    if args_1[1] in sys.argv: mode = sys.argv[sys.argv.index(args_1[1]) + 1]

    if args_2[0] in sys.argv: data = sys.argv[sys.argv.index(args_2[0]) + 1]
    if args_2[1] in sys.argv: data = sys.argv[sys.argv.index(args_2[1]) + 1]

    if args_3[0] in sys.argv: version = int(sys.argv[sys.argv.index(args_3[0]) + 1])
    if args_3[1] in sys.argv: version = int(sys.argv[sys.argv.index(args_3[1]) + 1])

    if args_4[0] in sys.argv: box_size = int(sys.argv[sys.argv.index(args_4[0]) + 1])
    if args_4[1] in sys.argv: box_size = int(sys.argv[sys.argv.index(args_4[1]) + 1])

    if args_5[0] in sys.argv: border = int(sys.argv[sys.argv.index(args_5[0]) + 1])
    if args_5[1] in sys.argv: border = int(sys.argv[sys.argv.index(args_5[1]) + 1])

    if args_6[0] in sys.argv: bg_color = sys.argv[sys.argv.index(args_6[0]) + 1]
    if args_6[1] in sys.argv: bg_color = sys.argv[sys.argv.index(args_6[0]) + 1]
        
    if args_7[0] in sys.argv: fg_color = sys.argv[sys.argv.index(args_7[0]) + 1]
    if args_7[1] in sys.argv: fg_color = sys.argv[sys.argv.index(args_7[0]) + 1]

    if args_8[0] in sys.argv or args_8[1] in sys.argv: save = True

    if args_9[0] in sys.argv: filename = sys.argv[sys.argv.index(args_9[0]) + 1]
    if args_9[1] in sys.argv: filename = sys.argv[sys.argv.index(args_9[1]) + 1]

    bg_color = (bg_color + ",").split(",")
    fg_color = (fg_color + ",").split(",")

    for i in range(3):
        if len(bg_color) == 3: 
            bg.append(int(bg_color[2-i]))
        else: 
            bg.append(int(bg_color[0]))
    
    for i in range(3):
        if len(fg_color) == 3: 
            fg.append(int(fg_color[2-i]))
        else: 
            fg.append(int(fg_color[0]))

    assert mode is not None, f"Please provide a value for mode (gen | scn)"

    if mode == "gen":
        assert data is not None, "Please provide a value for data"

        if data[-3:] == "txt":
            with open(os.path.join(INPUT_PATH, data), "r") as fp:
                data = fp.read()
            assert len(data) < 2000, "Data is too long to encode"

        qr = qrcode.QRCode(version=version, box_size=box_size, border=border)
        qr.add_data(data, optimize=0)
        qr.make(fit=True)
        image = qr.make_image(fill_color=tuple(fg), back_color=tuple(bg))

        if not save: show_image(image)
        else:
            num = len(os.listdir(OUTPUT_PATH)) - 1
            cv2.imwrite(os.path.join(OUTPUT_PATH, f"Code_{num + 1}.jpg"), np.array(image))

    else:
        assert filename in os.listdir(INPUT_PATH), f"{filename} not found in input directory"

        image = cv2.cvtColor(src=cv2.imread(os.path.join(INPUT_PATH, filename), cv2.IMREAD_COLOR), code=cv2.COLOR_BGR2RGB)

        qr_detector = cv2.QRCodeDetector()
        data, _, _ = qr_detector.detectAndDecode(image)

        if data != "":
            if data[:4] == "http":
                webbrowser.open_new(data)
            else:
                breaker()
                print(f"Data : \n\n{data}")
                breaker()
        else:
            breaker()
            print("No data detected")
            breaker()


if __name__ == "__main__":
    sys.exit(main() or 0)