import os
from HandHistory import HandHistory
from NetworkConverter import NetworkConverter

def walk_hands():
    input_folder = "C:/swc_client-Windows v0.2.18/handhistories"

    files = []
    for (dirpath, dirnames, filenames) in os.walk(input_folder):
        # TODO: wanna recursively get into directories?
        files.extend(filenames)
        break

    count = 0
    for filename in files:
        f = open(input_folder + "/" + filename)
        while True:
            hand_lines = []
            line = f.readline().strip()
            if len(line) == 0:
                break
            if count > 10:
                break
            while len(line) > 0:
                hand_lines.append(line)
                line = f.readline().strip()
            process_hand(hand_lines)
            # skip two empty lines
            f.readline()
            f.readline()
            count += 1
        f.close()

def process_hand(hand_lines):
    print "\r\n".join(hand_lines)
    # print "\n"
    # nc = NetworkConverter(hand_lines)
    # print nc.processHandHistory()
    hh = HandHistory(hand_lines)

def main():
    walk_hands()

if __name__ == "__main__":
    main()