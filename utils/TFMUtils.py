# coding: utf-8
import time as thetime, random, time, re, xml.etree.ElementTree as xml, xml.parsers.expat, binascii, base64, hashlib
import urllib
from datetime import datetime

class TFMUtils:
    @staticmethod
    def getTFMLangues(langueID):	
        if langueID == 0:
            return ["EN"]
        elif langueID == 1:
            return ["FR"]
        elif langueID == 2:
            return ["FR"]
        elif langueID == 3:
            return ["BR"]
        elif langueID == 4:
            return ["ES"]
        elif langueID == 5:
            return ["CN"]
        elif langueID == 6:
            return ["TR"]
        elif langueID == 7:
            return ["VK"]
        elif langueID == 8:
            return ["PL"]
        elif langueID == 9:
            return ["HU"]
        elif langueID == 10:
            return ["NL"]
        elif langueID == 11:
            return ["RO"]
        elif langueID == 12:
            return ["ID"]
        elif langueID == 13:
            return ["DE"]
        elif langueID == 14:
            return ["E2"]
        elif langueID == 15:
            return ["AR"]
        elif langueID == 16:
            return ["PH"]
        elif langueID == 17:
            return ["LT"]
        elif langueID == 18:
            return ["JP"]
        elif langueID == 19:
            return ["CH"]
        elif langueID == 20:
            return ["FI"]
        elif langueID == 21:
            return ["CZ"]
        elif langueID == 22:
            return ["SK"]
        elif langueID == 23:
            return ["HR"]
        elif langueID == 24:
            return ["BU"]
        elif langueID == 25:
            return ["LV"]
        elif langueID == 26:
            return ["HE"]
        elif langueID == 27:
            return ["IT"]
        elif langueID == 29:
            return ["ET"]
        elif langueID == 30:
            return ["AZ"]
        elif langueID == 31:
            return ["PT"]
        else:
            return ["EN"]

    @staticmethod
    def toHex(number):
        hexBytes = "0123456789abcdef"
        result = ""
        for x in range(0, 4):
            result += hexBytes[(number >> ((3 - x) * 8 + 4)) & 15]
            result += hexBytes[(number >> ((3 - x) * 8)) & 15]
            return result[6:]

    @staticmethod
    def getPass(password):
        salt = [-9, 25, -92, -37, -117, 18, 112, -95, -5, -108, 40, -83, -107, 73, -92, -102, 46, -52, 49, -118, -79, -56, -72, 63, -69, -98, -118, -22, 46, -16, -22, -111]
        password = hashlib.sha256(password.encode('ISO8859_1')).hexdigest()
        passBytes = []
        passBytes.extend(map(lambda x: ord(password[x]), range(0, len(password))))
        passBytes.extend(map(lambda x: salt[x] + x, range(0, len(salt))))
        return base64.b64encode(binascii.unhexlify(hashlib.sha256(binascii.unhexlify("".join(map(lambda x: TFMUtils.toHex(passBytes[x]), range(0, len(passBytes)))))).hexdigest()))

    @staticmethod
    def getBytes(*values):
        result = ""
        for value in values:
            result += str(chr(value))
        return result.getBytes()

    @staticmethod
    def getTime():
        return int(long(str(time.time())[:10]))

    @staticmethod
    def checkValidXML(XML):
        if re.search("ENTITY", XML) and re.search("<html>", XML):
            return False
        else:
            try:
                parser = xml.parsers.expat.ParserCreate()
                parser.Parse(XML)
                return True
            except Exception, e:
                return False

    @staticmethod
    def getHoursDiff(endTimeMillis):
        startTime = TFMUtils.getTime()
        startTime = datetime.fromtimestamp(float(startTime))
        endTime = datetime.fromtimestamp(float(endTimeMillis))
        result = endTime - startTime
        seconds = (result.microseconds + (result.seconds + result.days * 24 * 3600) * 10 ** 6) / float(10 ** 6)
        hours = int(int(seconds) / 3600) + 1
        return hours

    @staticmethod
    def getSecondsDiff(endTimeMillis):
        return int(long(str(thetime.time())[:10]) - endTimeMillis)

    @staticmethod
    def getRandomChars(size = 6, chars = "ABCDEF123456789"):
        return "".join((random.choice(chars) for x in range(size)))

    @staticmethod
    def getVideoID(url):
        search = re.findall("youtube\.com/watch\?v=(.+)", url)
        if search:
            videoID = search[0]

    @staticmethod
    def calculateTime(time):
        diff = int(time) - TFMUtils.getTime()
        diffSeconds = diff / 1000 % 60
        diffMinutes = diff / (60 * 1000) % 60
        diffHours = diff / (60 * 60 * 1000) % 24
        diffDays = diff / (24 * 60 * 60 * 1000)
        return diffDays <= 0 and diffHours <= 0 and diffMinutes <= 0 and diffSeconds <= 0

    @staticmethod
    def getDiffDays(time):
        diff = time - TFMUtils.getTime()
        return diff / (24 * 60 * 60)

    @staticmethod
    def parsePlayerName(playerName):
        return "*" + playerName[1:].lower().capitalize() if playerName.startswith("*") else playerName.lower().capitalize()

    @staticmethod
    def joinWithQuotes(list):
        return "\"" + "\", \"".join(list) + "\""

    @staticmethod    
    def getMusicDuration(musicName):
        urllib.urlopen("http://tools.miceice.com.br/ice3/info.php?file=").read()
