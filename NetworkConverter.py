import urllib, urllib2

class NetworkConverter:
    """
    A converter that converts a SwC hand to full tilt format by submitting them to bitcoinpokerblog
    gg UncleGravy
    """

    def __init__(self, hand_lines):
        self.lines = hand_lines

    def processHandHistory(self):
        url = "http://www.bitcoinpokerblog.com/handconverter/converthand.php"
        headers = {
            "User-Agent" : "Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0"
        }
        data = dict(ConversionRate=1, handhistory="\r\n".join(self.lines))
        request = urllib2.Request(url, headers=headers, data=urllib.urlencode(data))
        response = urllib2.urlopen(request)

        # take out header before returning
        return "\r\n".join(response.read().split("\r\n")[6:])