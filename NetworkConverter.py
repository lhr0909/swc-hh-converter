import urllib, urllib2, time

class NetworkConverter:
    """
    A converter that converts a SwC hand to full tilt format by submitting them to bitcoinpokerblog
    gg UncleGravy
    """

    def __init__(self, hand_lines):
        self.lines = hand_lines
        if not self.haxCheck():
            self.lines = []

    def haxCheck(self):
        for line in self.lines:
            hax_regex = r"Dealt to (\S+) \[([^]]+)\]"
            m = re.search(hax_regex, line)
            if m is None:
                continue
            else:
                if m.group(1) != "lhr0909":
                    return False
                else:
                    return True

    def processHandHistory(self):
        url = "http://www.bitcoinpokerblog.com/handconverter/converthand.php"
        headers = {
            "User-Agent" : "Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0"
        }
        data = dict(SealsName="", ConversionRate=1, handhistory="\r\n".join(self.lines))
        request = urllib2.Request(url, headers=headers, data=urllib.urlencode(data))
        trying = True
        while trying:
            try:
                response = urllib2.urlopen(request)
                trying = False
            except:
                print "error occured, retrying.."
                time.sleep(5)
                trying = True

        # take out header before returning
        return "\r\n".join(response.read().split("\r\n")[6:])