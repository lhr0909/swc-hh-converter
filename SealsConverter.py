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
        f = open(full_path)
        hand_lines = []
        while True:
            line = f.readline().strip()
            if len(line) == 0:
                if len(hand_lines) > 0:
                    process_hand(hand_lines, output_folder, filename, part, "w")
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
                    process_hand(hand_lines, output_folder, filename, part, "w")
                    hand_lines = []
                    part += 1
                    count = 0
                    time.sleep(5)
            else:
                process_hand(hand_lines, output_folder, filename, part, "w")
                hand_lines = []
                part += 1
                time.sleep(2)
            # skip two empty lines
            f.readline()
            f.readline()
            count += 1
        f.close()
        os.rename(full_path, processed_folder + "/" + filename)

def monitor_hand(start_flag, input_folder, output_folder, start_time, timeout):
    tracking_files = set()
    file_lines = dict()
    while not start_flag.empty():
        for (dirpath, dirnames, filenames) in os.walk(input_folder):
            # TODO: wanna recursively get into directories?
            for filename in filenames:
                full_path = input_folder + "/" + filename
                (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(full_path)
                if mtime > start_time:
                    # add new hand files into our tracking files
                    tracking_files.add(filename)
                    print "added %s to track" % filename
            # find diff and convert them
            for filename in tracking_files:
                full_path = input_folder + "/" + filename
                f = open(full_path, "r")
                lines = f.readlines()
                start_line = 0
                if filename not in file_lines:
                    start_line = 0
                else:
                    start_line = file_lines[filename]
                new_lines = map(lambda x: x.strip(), lines[start_line:])
                print "\n".join(new_lines)
                # update line count here
                file_lines[filename] = len(lines)
                process_hand(new_lines, output_folder, filename, None, "a")
            break
        tracking_files = set()
        start_time = time.time()
        time.sleep(timeout)

def process_hand(hand_lines, output_folder, filename, part, file_mode):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    # print "\r\n".join(hand_lines)
    # print "\n"
    nc = NetworkConverter(hand_lines)
    fout_path = ""
    if part is not None:
        fout_path = output_folder + "/" + filename + " - " + str(part) + ".txt"
    else:
        fout_path = output_folder + "/" + filename
    fout = open(fout_path, file_mode)
    fout.write(nc.processHandHistory())
    fout.close()
    print fout_path + " written"
    # hh = HandHistory(hand_lines)

def main():
    input_folder = "C:/swc_client-Windows v0.2.18/handhistories"
    output_folder = "C:/swc_client-Windows v0.2.18/converted_handhistories"
    processed_folder = "C:/swc_client-Windows v0.2.18/processed_handhistories"
    start_time = time.time()

    monitor_hand(input_folder, output_folder, start_time, 5)
    # walk_hands(input_folder, output_folder, processed_folder, 30)

if __name__ == "__main__":
    main()