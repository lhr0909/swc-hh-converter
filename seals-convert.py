import os
import urllib, urllib2
import re

class HandHistory:
    """
    Hand History class
    """
    def __init__(self, hand_lines):
        self.handNumber = self.getHandNumber(hand_lines[0])
        self.time = self.getTime(hand_lines[0])
        self.gameType = self.getGameType(hand_lines[1])
        self.limitType = self.getLimitType(hand_lines[1])
        self.getBlinds = self.getBlinds(hand_lines[1])
        self.tableName = self.getTableName(hand_lines[3])
        self.maxSeat = self.getMaxSeat(hand_lines[3])
        self.getHistory(hand_lines[4:])

    def getHandNumber(self, line):
        handNumber_regex = r"Hand \#([0-9]+-[0-9]+)"
        m = re.search(handNumber_regex, line)
        return m.group(1).replace("-", "")

    def getTime(self, line):
        time_regex = r"Hand \#[0-9]+-[0-9]+ - (.*)"
        m = re.search(time_regex, line)
        return m.group(1).replace("-", "/") + " ET"

    def getGameType(self, line):
        gameType_regex = r"Game: [NP]L ([HoldemOha']+)"
        m = re.search(gameType_regex, line)
        return m.group(1).replace("'", "")

    def getLimitType(self, line):
        limitType_regex = r"Game: ([NP])L [HoldemOha']+"
        m = re.search(limitType_regex, line)
        if m.group(1) == "N":
            return "No"
        elif m.group(1) == "P":
            return "Pot"
        return "Fixed"

    def getBlinds(self, line):
        blinds_regex = r"Blinds ([0-9.]+/[0-9.]+)"
        m = re.search(blinds_regex, line)
        return tuple(map(float, m.group(1).split("/")))

    def getTableName(self, line):
        tableName_regex = r"Table: (.*)"
        m = re.search(tableName_regex, line)
        return "SwC-" + m.group(1)

    def getMaxSeat(self, line):
        maxSeat_regex = r"([HU69max]{2,4})"
        m = re.search(maxSeat_regex, line)
        if m.group(1) == "HU":
            return 2
        elif m.group(1) == "6max":
            return 6
        elif m.group(1) == "9max":
            return 9
        return -1

    def getHistory(self, lines):
        self.players = dict()
        i = 0
        while i < len(lines):
            line = lines[i]
            if line.startswith("Seat"):
                player_regex = r"Seat ([0-9]): ([A-z0-9_]+) \(([0-9.]+)\)"
                m = re.search(player_regex, line)
                self.players[m.group(2)] = (int(m.group(1)), float(m.group(3)))
            else:
                # break out since we get all the players
                break
            i += 1

        print self.players



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
    hh = HandHistory(hand_lines)


def process_hand_bpb(hand_lines):
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