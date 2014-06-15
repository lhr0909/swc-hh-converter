import re

class HandHistory:
    """
    Hand History dissection
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
        self.getPlayers(lines)

    def getPlayers(self, lines):
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

        self.getBlindsAndButton(lines[i:])

    def getBlindsAndButton(self, lines):
        button_regex = r"(\S+) has the dealer button"
        m = re.search(button_regex, lines[0])
        # most hand history uses seat # for button
        self.buttonSeat = self.players[m.group(1)][0]

        sb_regex = r"(\S+) posts small blind ([0-9.]+)"
        m = re.search(sb_regex, lines[1])
        self.smallBlind = (m.group(1), float(m.group(2)))

        bb_regex = r"(\S+) posts big blind ([0-9.]+)"
        m = re.search(bb_regex, lines[2])
        self.bigBlind = (m.group(1), float(m.group(2)))

        # TODO: deal with more than 1 bb / sb

        self.getHoleCards(lines[3:])

    def getHoleCards(self, lines):
        holeCards_regex = r"Dealt to (\S+) \[([^]]+)\]"
        m = re.search(holeCards_regex, lines[1])
        if m is not None:
            self.holeCards = (m.group(1), tuple(m.group(2).split(" ")))
        else:
            self.holeCards = None
        
        self.getPreflopActions(lines[2:])

    def getAction(self, line):
        return tuple(line.split(" ", 2))

    def getCommunityCards(self, line):
        commCards_regex = r"\[([^]]+)\]"
        m = re.search(commCards_regex, line)
        return tuple(m.group(1).split(" "))

    def getPreflopActions(self, lines):
        self.preflopActions = []
        i = 0
        while i < len(lines):
            if lines[i].startswith("**"):
                break
            else:
                self.preflopActions.append(self.getAction(lines[i]))
                i += 1

        if i < len(lines):
            self.flop = self.getCommunityCards(lines[i])
            self.getFlopActions(lines[i+1:])

    def getFlopActions(self, lines):
        self.flopActions = []
        i = 0
        while i < len(lines):
            if lines[i].startswith("**"):
                break
            else:
                self.flopActions.append(self.getAction(lines[i]))
                i += 1

        if i < len(lines):
            self.turn = self.getCommunityCards(lines[i])
            self.getTurnActions(lines[i+1:])

    def getTurnActions(self, lines):
        self.turnActions = []
        i = 0
        while i < len(lines):
            if lines[i].startswith("**"):
                break
            else:
                self.turnActions.append(self.getAction(lines[i]))
                i += 1

        if i < len(lines):
            self.river = self.getCommunityCards(lines[i])
            self.getRiverActions(lines[i+1:])

    def getRiverActions(self, lines):
        self.riverActions = []
        i = 0
        while i < len(lines):
            if lines[i].startswith("**"):
                break
            else:
                self.riverActions.append(self.getAction(lines[i]))
                i += 1

        if i < len(lines):
            self.getShowdown(lines[i+1:])

    def getShowdown(self, lines):
        print self.holeCards
        print self.preflopActions
        print self.flop
        print self.flopActions
        print self.turn
        print self.turnActions
        print self.river
        print self.riverActions
        print
        pass