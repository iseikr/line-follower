from line_detector import LineDetector

def main():
    ld = LineDetector("input-img.png", 6)
    dir = ld.getTurnDir()

    print dir
    return

main()
