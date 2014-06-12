import os
import urllib, urllib2

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
            if count > 0:
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
    url = "http://www.bitcoinpokerblog.com/handconverter/converthand.php"
    headers = {
        "User-Agent" : "Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0"
    }
    data = dict(ConversionRate=1, handhistory="\r\n".join(hand_lines))
    request = urllib2.Request(url, headers=headers, data=urllib.urlencode(data))
    response = urllib2.urlopen(request)
    print response.read()



def main():
    walk_hands()

if __name__ == "__main__":
    main()