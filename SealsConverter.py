import os, time
from difflib import Differ
from HandHistory import HandHistory
from NetworkConverter import NetworkConverter

def walk_hands(input_folder, output_folder, processed_folder, batch_count):
    '''
    This method walks all the hands in the directory and converts them
    '''

    files = []
    for (dirpath, dirnames, filenames) in os.walk(input_folder):
        # TODO: wanna recursively get into directories?
        files.extend(filenames)
        break

    count = 0
    for filename in files:
        part = 0
        full_path = input_folder + "/" + filename
        (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(full_path)
        #print "%s\nlast modified: %s\nsize: %s bytes\n\n" % (filename, time.ctime(mtime), size)
        f = open(full_path)
        hand_lines = []
        while True:
            line = f.readline().strip()
            if len(line) == 0:
                if len(hand_lines) > 0:
                    process_hand(hand_lines, output_folder, filename, part)
                    hand_lines = []
                    part += 1
                    time.sleep(5)
                break
            while len(line) > 0:
                hand_lines.append(line)
                line = f.readline().strip()
            if batch_count is not None:
                if count < batch_count:
                    hand_lines.extend(["", "", ""]) # adding some empty lines
                else:
                    process_hand(hand_lines, output_folder, filename, part)
                    hand_lines = []
                    part += 1
                    count = 0
                    time.sleep(5)
            else:
                process_hand(hand_lines, output_folder, filename, part)
                hand_lines = []
                part += 1
                time.sleep(2)
            # skip two empty lines
            f.readline()
            f.readline()
            count += 1
        f.close()
        os.rename(full_path, processed_folder + "/" + filename)

def monitor_hand(input_folder, start_time):
    pass

def process_hand(hand_lines, output_folder, filename, part):
    # print "\r\n".join(hand_lines)
    # print "\n"
    nc = NetworkConverter(hand_lines)
    fout_path = output_folder + "/" + filename + " - " + str(part) + ".txt"
    fout = open(fout_path, "w")
    fout.write(nc.processHandHistory())
    fout.close()
    print fout_path + " written"
    # hh = HandHistory(hand_lines)
    pass

def main():
    input_folder = "C:/swc_client-Windows v0.2.18/handhistories"
    output_folder = "C:/swc_client-Windows v0.2.18/converted_handhistories"
    processed_folder = "C:/swc_client-Windows v0.2.18/processed_handhistories"
    start_time = time.time()

    # monitor_hand(input_folder, start_time)
    walk_hands(input_folder, output_folder, processed_folder, 30)

if __name__ == "__main__":
    main()