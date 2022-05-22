#coding: utf-8
import os, sys, ConfigParser, random, traceback, time, smtplib, sqlite3, logging, threading, json, struct

# Compiler Files
sys.dont_write_bytecode = True

# Modules
from modules import *

# Utils
from utils import *

# Library
from subprocess import Popen, PIPE
from datetime import datetime
from email.mime.text import MIMEText
from twisted.internet import reactor, protocol

class Client(ClientHandler):
    def __init__(this):
    
        # String
        this.Username = ""
        this.Langue = ""
        this.realLangue = ""
        this.MouseColor = "78583a"
        this.ShamanColor = "78583a"
        this.roomName = ""
        this.shopItems = ""
        this.shamanItems = ""
        this.playerLook = "1;0,16,0,32,0,0,0,0,0"
        this.shamanLook = "0,0,0,0,0,0,0,0,0,0"
        this.lastMessage = ""
        this.modoPwetLangue = "all"
        this.silenceMessage = ""
        this.marriage = ""
        this.tribeName = ""
        this.emailAddress = ""
        this.tempEmailAddress = ""
        this.lastEmailCode = ""
        this.currentMusicName = ""
        this.tradeName = ""
        this.mouseName = ""
        this.captcha = ""

        # Integer
        this.lastPacketID = random.randint(0, 99)
        this.langueByte = 0
        this.playerScore = 0
        this.playerCode = 0
        this.privLevel = 0
        this.playerID = 0
        this.playerAvatar = 0
        this.TitleNumber = 0
        this.TitleStars = 0
        this.posX = 0
        this.posY = 0
        this.playerX = 0
        this.playerY = 0
        this.velX = 0
        this.velY = 0
        this.playerStartTime = 0
        this.firstCount = 0
        this.cheeseCount = 0
        this.shamanCheeses = 0
        this.shopCheeses = 1000
        this.shopFraises = 1000
        this.shamanSaves = 0
        this.hardModeSaves = 0
        this.divineModeSaves = 0
        this.bootcampCount = 0
        this.shamanType = 0
        this.regDate = 0
        this.banHours = 0
        this.shamanLevel = 1
        this.shamanExp = 0
        this.shamanExpNext = 1
        this.ambulanceCount = 0
        this.bubblesCount = 0
        this.lastOn = 0
        this.silenceType = 0
        this.gender = 0
        this.lastDivorceTimer = 0
        this.tribeCode = 0
        this.tribeRank = 0
        this.tribeJoined = 0
        this.tribePoints = 0
        this.defilantePoints = 0
        this.lastGameMode = 0
        this.currentPlace = 0
        this.iceCoins = 0
        this.iceTokens = 0
        this.shamanSymbol = 0
        this.equipedShamanSymbol = 0
        this.pet = 0
        this.petEnd = 0

        # Bool
        this.isClosed = False
        this.validatingVersion = True
        this.isGuest = False
        this.isDead = False
        this.hasCheese = False
        this.hasEnter = False
        this.isSync = False
        this.isMovingRight = False
        this.isMovingLeft = False
        this.isJumping = False
        this.isShaman = False
        this.isAfk = False
        this.isVoted = False
        this.qualifiedVoted = False
        this.modMute = False
        this.RTotem = False
        this.UTotem = False
        this.LoadCountTotem = False
        this.modoPwet = False
        this.canResSkill = False
        this.canShamanRespawn = False
        this.isOpportunist = False
        this.desintegration = False
        this.sendMusic = True        
        this.canMeep = False
        this.sendMusic = True
        this.isCafe = False
        this.canSkipMusic = False
        this.isHidden = False
        this.isTeleport = False
        this.isFly = False
        this.isSpeed = False
        this.isNewPlayer = False
        this.isVampire = False
        this.isSuspect = False
        this.isTrade = False
        this.tradeConfirm = False
        this.canUseConsumable = True
        this.runLuaAsBot = False

        # Others
        this.Cursor = Cursor
        this.TFMUtils = TFMUtils

        # Nonetype
        this.room = None
        this.awakeTimer = None
        this.resSkillsTimer = None
        this.skipMusicTimer = None
        this.playMusicTimer = None
        this.consumablesTimer = None

        # List Arguments
        this.STotem = [0, ""]
        this.Totem = [0, ""]
        this.survivorStats = [0, 0, 0, 0]
        this.racingStats = [0, 0, 0, 0]
        this.marriageInivite = []
        this.tribeData = ["", "", 0, None]
        this.tribeInvite = []
        this.mulodromePos = []
        this.canLogin = [False, False]
        this.AntiBots = [0, False, 0, 0]

        # DDos Atack
        this.can = this
        this.can.Loop_Decoded = False

        # List
        this.cheeseTitleList = []
        this.firstTitleList = []
        this.shamanTitleList = []
        this.shopTitleList = []
        this.bootcampTitleList = []
        this.hardModeTitleList = []
        this.divineModeTitleList = []
        this.specialTitleList = []
        this.titleList = []
        this.clothes = []
        this.shopBadges = []
        this.shopNatal = []
        this.friendsList = []
        this.ignoredsList = []
        this.ignoredMarriageInvites = []
        this.ignoredTribeInvites = []
        this.chats = []
        this.voteBan = []
        this.equipedConsumables = []
        this.consumablesShop = []

        # Dict
        this.playerSkills = {}
        this.playerConsumables = {}
        this.tradeConsumables = {}

    def getPing():
          _command = "ping "+this.ipAddress[0]
          _result = str(Popen(_command, stdout=PIPE, stderr=PIPE, shell=True).communicate()).split("\\n")
          _line_content = _result[len(_result)-2];
          return _line_content.split(",")[0].split(" = ")[1].replace("ms","")

    def sendRemovePoup63(this):
            this.sendPacket([29, 22], struct.pack("!l", 63), True)
    def sendRemovePoup62(this):
            this.sendPacket([29, 22], struct.pack("!l", 62), True) 
    def sendRemovePoup(this, id):
            this.sendPacket([29, 22], struct.pack("!l", id), True)

    def chatEnable(this):
        this.chatdisabled = False       
    def defineNotLibCn(this):
        this.libCn = False
    def sendBlueTeam(this):
        this.isBlue = False
    def sendRedTeam(this):
        this.isRed = False

    def connectionMade(this):
        this.ipAddress = this.transport.getPeer()
        this.ipAddress = this.ipAddress.host
        this.server = this.factory

        this.parsePackets = ParsePackets(this, this.server)
        this.parseCommands = ParseCommands(this, this.server)
        this.shopModule = ShopModule(this, this.server)
        this.ModoPwet = ModoPwet(this, this.server)
        this.skillModule = SkillModule(this, this.server)
        this.tribulle = Tribulle(this, this.server)

        # Bot
        this.shop = shop(this, this.server)
        this.vipInfo = vipInfo(this, this.server)
        this.spinTheWheel = spinTheWheel(this, this.server)
        this.consumablesShop = consumablesShop(this, this.server)

        if this.server.getIPPermaBan(this.ipAddress) or this.ipAddress in this.server.tempIPBanList:
            this.transport.loseConnection()
            return

        if this.server.connectedCounts.has_key(this.ipAddress):
            this.server.connectedCounts[this.ipAddress] += 1
        else:
            this.server.connectedCounts[this.ipAddress] = 1

        if this.server.connectedCounts[this.ipAddress] >= 5:
            this.server.tempIPBanList.append(this.ipAddress)
            this.server.sendOutput("DDoS Attack Blocked in IP: "+this.ipAddress+".")
            this.server.sendModMessage(7, "Ataque DDoS bloqueado no IP: <V>"+this.ipAddress+"<BL>.")
            this.server.disconnectIPAddress(this.ipAddress)
            del this.server.connectedCounts[this.ipAddress]
            this.transport.loseConnection()
                
    def connectionLost(this, remove=True):
        this.isClosed = True
        
        if this.server.connectedCounts.has_key(this.ipAddress):
            count = this.server.connectedCounts[this.ipAddress] - 1
            if count <= 0:
                del this.server.connectedCounts[this.ipAddress]
            else:
                this.server.connectedCounts[this.ipAddress] = count

            if this.isTrade:
                this.cancelTrade(this.tradeName)

            if this.server.players.has_key(this.Username) and remove:
                del this.server.players[this.Username]

            if this.server.chatMessages.has_key(this.Username):
                del this.server.chatMessages[this.Username]

            for client in this.server.players.values():
                if this.Username in client.friendsList and client.Username in this.friendsList:
                    client.tribulle.sendFriendDisconnected(this.Username)

            if not this.tribeName == "":
                this.tribulle.sendTribeMemberDisconnected()

            if this.privLevel >= 5:
                this.sendStaffLogin(True)

            try:
                if this.server.clientAvatarKeys.has_key(this.Username):
                    del this.server.avatarKeys[this.server.clientAvatarKeys[this.Username]]
                    del this.server.clientAvatarKeys[this.Username]
            except:
                pass

        if not this.Username == "":
            if not this.isGuest:
                this.updateDatabase()

        if this.room != None:
            this.room.removeClient(this)

    def sendPacket(this, identifiers, packet=None, newProtocol=False):
        data = None
        identifiers = "".join(map(chr, identifiers))
        if not newProtocol:
            packetData = chr(1).join(map(str, [identifiers] + packet))

        length = len(identifiers + packet) if newProtocol else (len(packetData) + 6)
        p = ByteArray()
        if length <= 0xFF:
            p.writeByte(1).writeUnsignedByte(length)
        elif length <= 0xFFFF:
            p.writeByte(2).writeUnsignedShort(length)
        elif length <= 0xFFFFFF:
            p.writeByte(3).writeByte((length >> 16) & 0xFF).writeByte((length >> 8) & 0xFF).writeByte(length & 0xFF)

        if not p.toByteArray() == "":
            if newProtocol:
                p.writeBytes(identifiers + packet)
            else:
                p.writeBytes(chr(1) + chr(1)).writeShort(len(packetData)).writeBytes(packetData).writeShort(0)

        if not this.isClosed:
            this.transport.write(str(p.toByteArray()))

        if this.server.VERBOSE:
            if len(packet) < 20000: 
                this.server.sendOutput("SEND: "+str(identifiers)+" : "+repr(packet))
            else:
                this.server.sendOutput("SEND: "+str(identifiers)+" : [Long Packet]")
 
    def parseString(this, packet):
        p = ByteArray(packet)
        if packet == "" or packet == " " or packet == "\x00":
            #Check socket
            os.system("iptables -I INPUT -s %s -j DROP" % (this.ipAddress))
            this.server.sendModMessage(5, "<R>Loop attack closed, sent to %s" % (this.ipAddress))
            this.server.tempIPBanList.append(this.ipAddress)
            this.transport.loseConnection()
            #Check socket
            this.can.Loop_Decoded = True
        if this.validatingVersion:
            C = p.readUnsignedShort()
            CC = p.readUnsignedByte()
            if this.server.VERBOSE:
                this.server.sendOutput("RECV: "+str(C)+" -> "+str(CC)+" : "+repr(packet))

            if C == 28 and CC == 1:
                version = p.readShort()
                validVersion = "1."+str(version)
                ckey = p.readUTF()
                if not ckey == this.server.CKEY:
                    this.server.sendOutput("WARNING: CKEY Error, CKEY: ("+ckey+")")
                    this.transport.loseConnection()

                if not validVersion == this.server.Version:
                    this.server.sendOutput("WARNING: Wrong SWF Version, Right Version: ("+validVersion+")")
                    this.transport.loseConnection()

                if ckey == this.server.CKEY and validVersion == this.server.Version:
                    this.validatingVersion = False
                    this.sendCorrectVersion()
                    this.BotTimerKick = reactor.callLater(1, this.getReturnValues, 1)
        else:
            try:

                if packet == "":
                    this.server.tempIPBanList.append(this.ipAddress)
                    this.transport.loseConnection()
                else:
                    checkPacketID = (this.lastPacketID % 99)
                    checkPacketID += 0 if checkPacketID == 0 else 1
                    packetID = p.readUnsignedByte()

                    this.lastPacketID = packetID

                    C = p.readUnsignedByte()
                    CC = p.readUnsignedByte()
                    if C != 0 and CC != 0:
                        this.parsePackets.parsePacket(C, CC, packet[3:])
                        if this.server.VERBOSE:
                           this.server.sendOutput("RECV: "+str(C)+" -> "+str(CC)+" : "+repr(packet))

            except Exception as ERROR:
                c = open("./errors.log", "a")
                c.write("\n" + "=" * 40 + "\n")
                c.write("- Time: %s\n- IP: %s\n- Player: %s\n- Error: \n" %(this.server.getHours(), this.ipAddress, this.Username))
                traceback.print_exc(file=c)
                c.close()

    def loginPlayer(this, playerName, password, startRoom):    
        if this.server.connectedCounts[this.ipAddress] >= 3:
            this.sendPlayerBan(0, "Permanent Ban", True)
            this.transport.loseConnection()
        playerName = "Tourist" if playerName == "" else playerName
        if password == "":
            playerName = this.server.checkAlreadyExistingGuest("*" + playerName)
            startRoom = chr(3) + "[Tutorial] " + playerName
            this.isGuest = True

        if not this.canLogin[0] and not this.canLogin[1] or this.ipAddress in this.server.tempIPBanList:
            this.transport.loseConnection()
            return

        if not this.isGuest:
            if playerName in this.server.userPermaBanCache:
                this.sendPermaBan()
                this.transport.loseConnection()
                return

        if not this.isGuest:
            if playerName in this.server.userTempBanCache:
                banInfo = this.server.getTempBanInfo(playerName)
                timeCalc = TFMUtils.getHoursDiff(int(banInfo[0]))
                if timeCalc <= 0:
                    this.server.removeTempBan(playerName)
                else:
                    this.sendPlayerBanLogin(timeCalc, (banInfo[1]))
                    this.transport.loseConnection()
                    return

        if len(playerName) < 3 or len(playerName) > 12:
            reactor.callLater(5, lambda: this.sendPacket(Identifiers.send.Login_Result, chr(2), True))
        elif this.server.checkConnectedAccount(playerName):
            this.sendPacket(Identifiers.send.Login_Result, chr(1), True)
        else:
            if not this.isGuest:
                this.Cursor.execute("select * from Users where Username = ? and Password = ?", [playerName, password])
                rs = this.Cursor.fetchone()
                if rs:
                    this.privLevel = rs["PrivLevel"]
                    this.playerID = rs["PlayerID"]
                    this.playerAvatar = rs["avatar"]
                    this.TitleNumber = rs["TitleNumber"]
                    this.firstCount = rs["FirstCount"]
                    this.cheeseCount = rs["CheeseCount"]
                    this.shamanCheeses = rs["ShamanCheeses"]
                    this.shopCheeses = rs["ShopCheeses"]
                    this.shopFraises = rs["ShopFraises"]
                    this.shamanSaves = rs["ShamanSaves"]
                    this.hardModeSaves = rs["HardModeSaves"]
                    this.divineModeSaves = rs["DivineModeSaves"]
                    this.bootcampCount = rs["BootcampCount"]
                    this.shamanType = rs["ShamanType"]
                    this.shopItems = rs["ShopItems"]
                    this.shamanItems = rs["ShamanItems"]
                    this.clothes = rs["Clothes"].split("|")
                    this.playerLook = rs["Look"]
                    this.shamanLook = rs["ShamanLook"]
                    this.MouseColor = rs["MouseColor"]
                    this.ShamanColor = rs["ShamanColor"]
                    this.regDate = rs["RegDate"]
                    this.shopBadges = rs["Badges"].split(",")
                    this.cheeseTitleList = rs["CheeseTitleList"].split(",")
                    this.firstTitleList = rs["FirstTitleList"].split(",")
                    this.shamanTitleList = rs["ShamanTitleList"].split(",")
                    this.shopTitleList = rs["ShopTitleList"].split(",")
                    this.bootcampTitleList = rs["BootcampTitleList"].split(",")
                    this.hardModeTitleList = rs["HardModeTitleList"].split(",")
                    this.divineModeTitleList = rs["DivineModeTitleList"].split(",")
                    this.specialTitleList = rs["SpecialTitleList"].split(",")
                    this.banHours = rs["BanHours"]
                    level = rs["ShamanLevel"].split("/")
                    this.shamanLevel = int(level[0])
                    this.shamanExp = int(level[1])
                    this.shamanExpNext = int(level[2])
                    
                    for skill in rs["Skills"].split(";"):
                        values = skill.split(":")
                        if len(values) >= 2:
                            this.playerSkills[int(values[0])] = int(values[1])

                    this.lastOn = rs["LastOn"]
                    this.friendsList = rs["FriendsList"].split(",")
                    this.ignoredsList = rs["IgnoredsList"].split(",")
                    this.gender = rs["Gender"]
                    this.lastDivorceTimer = rs["LastDivorceTimer"]
                    this.marriage = rs["Marriage"]
                    
                    tribeInfo = rs["TribeInfo"].split("#")
                    if len(tribeInfo) == 3:
                        this.tribeCode = int(tribeInfo[0])
                        this.tribeRank = int(tribeInfo[1])
                        this.tribeJoined = int(tribeInfo[2])
                        this.tribeData = this.server.getTribeInfo(this.tribeCode)
                        this.tribeName = this.tribeData[0]

                    this.emailAddress = rs["Email"]
                    survivor = rs["SurvivorStats"].split(",")
                    racing = rs["RacingStats"].split(",")
                    this.survivorStats = [int(survivor[0]), int(survivor[1]), int(survivor[2]), int(survivor[3])]
                    this.racingStats = [int(racing[0]), int(racing[1]), int(racing[2]), int(racing[3])]
                    this.iceCoins = rs["IceCoins"]
                    this.iceTokens = rs["IceTokens"]

                    for consumable in rs["Consumables"].split(";"):
                        values = consumable.split(":")
                        if len(values) >= 2:
                            this.playerConsumables[int(values[0])] = int(values[1])

                    for EquipedConsumables in rs["EquipedConsumables"].split(","):
                        consumable.split(":")
                    this.shamanSymbol = rs["ShamanSymbol"]
                    this.equipedShamanSymbol = rs["EquipedSymbol"]

                    totem = this.server.getTotemData(playerName)
                    if len(totem) == 2:
                        this.STotem = [int(totem[0]), totem[1]]

                    this.modMute = playerName in this.server.userMuteCache

                    this.shopModule.checkGiftsAndMessages(rs["LastReceivedGifts"], rs["LastReceivedMessages"])

                else:
                    reactor.callLater(5, lambda: this.sendPacket(Identifiers.send.Login_Result, chr(2), True))
                    return

            this.Username = playerName
            this.playerCode = this.server.generatePlayerCode()
            this.Cursor.execute("insert into LoginLog (Username, IP) select ?, ? where not exists (select 1 from LoginLog where Username = ? and IP = ?)", [playerName, this.ipAddress, playerName, this.ipAddress])

            this.clothes = filter(None, this.clothes)
            this.shopBadges = filter(None, this.shopBadges)
            this.friendsList = filter(None, this.friendsList)
            this.ignoredsList = filter(None, this.ignoredsList)
            this.shopTitleList = filter(None, this.shopTitleList)
            this.firstTitleList = filter(None, this.firstTitleList)
            this.cheeseTitleList = filter(None, this.cheeseTitleList)
            this.shamanTitleList = filter(None, this.shamanTitleList)
            this.specialTitleList = filter(None, this.specialTitleList)
            this.bootcampTitleList = filter(None, this.bootcampTitleList)
            this.hardModeTitleList = filter(None, this.hardModeTitleList)
            this.divineModeTitleList = filter(None, this.divineModeTitleList)

            if this.MouseColor == "":
                this.MouseColor = "78583a"

            if this.ShamanColor == "":
                this.ShamanColor = "fade55" if this.shamanSaves >= 1 else "95d9d6"

            for name in ["cheese", "first", "shaman", "shop", "bootcamp", "hardmode", "divinemode"]:
                this.checkAndRebuildTitleList(name)

            this.shopModule.checkAndRebuildBadges()

            this.sendCompleteTitleList()

            for title in this.titleList:
                if str(title).split(".")[0] == str(this.TitleNumber):
                    this.TitleStars = int(str(title).split(".")[1])

            this.server.players[this.Username] = this
            this.skillModule.sendShamanSkills(False)
            this.skillModule.sendExp(this.shamanLevel, this.shamanExp, this.shamanExpNext)
            this.sendLogin()
            this.sendPlayerIdentification()
            this.shopModule.sendShamanItems()
            if not this.emailAddress == "":
                this.shopModule.sendCanGift()

            this.sendTimeStamp()
            if this.privLevel == 2:
                this.checkVip()

            if not this.emailAddress == "":
                this.sendPacket(Identifiers.send.Email_Confirmed, chr(1), True)

            this.tribulle.sendPlayerInfo()
            this.tribulle.sendFriendList(None)
            this.tribulle.sendIgnoredsList()
            this.tribulle.sendTribe(False)

            for client in this.server.players.values():
                if this.Username in client.friendsList and client.Username in this.friendsList:
                    client.tribulle.sendFriendConnected(this.Username)

            if not this.tribeName == "":
                this.tribulle.sendTribeMemberConnected()

            if this.privLevel >= 5:
                this.sendStaffLogin(False)

            if this.shamanSaves >= 1:
                this.sendShamanType(this.shamanType, (this.shamanSaves >= 2 and this.hardModeSaves >= 3))

            this.sendInventoryConsumables()

            if not startRoom == "" and not startRoom == "801":
                this.enterRoom(this.server.checkRoom(startRoom, this.Langue))
            else:
                this.enterRoom(this.server.recommendRoom(this.Langue))                

            this.resSkillsTimer = reactor.callLater(600, setattr, this, "canResSkill", True)
            
            this.sendMessage("<br><N>«<J>Welcome<N>»<br><N>To play music /play or /stop to stop.<br><N>«<font color='#07C1AB'> Type it <N>/commands<font color='#07C1AB'>, to see the list of commands.</font><N> »<br><N>Version 1.373<br>")
        
    def createAccount(this, playerName, password):
        this.server.lastPlayerID += 1
        this.server.setServerSetting("Last Player ID", str(this.server.lastPlayerID))
        id = this.server.lastPlayerID
        this.sendNewConsumable(0, 10)
        this.Cursor.execute("insert into Users (Username, Password, PlayerID, PrivLevel, TitleNumber, FirstCount, CheeseCount, ShamanCheeses, ShopCheeses, ShopFraises, ShamanSaves, HardModeSaves, DivineModeSaves, BootcampCount, ShamanType, ShopItems, ShamanItems, Clothes, Look, ShamanLook, MouseColor, ShamanColor, RegDate, Badges, CheeseTitleList, FirstTitleList, ShamanTitleList, ShopTitleList, SpecialTitleList, BootcampTitleList, HardModeTitleList, DivineModeTitleList, BanHours, ShamanLevel, Skills, LastOn, FriendsList, IgnoredsList, Gender, LastDivorceTimer, Marriage, TribeInfo, Email, LastReceivedGifts, LastReceivedMessages, SurvivorStats, RacingStats, VipTime, IceCoins, IceTokens, Consumables, EquipedConsumables) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", [playerName, password, id, 1, 0, 1000, 1000, 1000, this.server.initialCheeses, this.server.initialFraises, 0, 0, 0, 1000, 0, "", "", "", "1;0,0,0,0,0,0,0,0,0", "0,0,0,0,0,0,0,0,0,0", "78583a", "95d9d6", TFMUtils.getTime(), "", "", "", "", "", "", "", "", "", 0, "32/275/10", "", 0, "", "", 0, 0, "", "", "", "", "", "0,0,0,0", "0,0,0,0", 0, 0, 0, "0:10", ""])

    def checkAndRebuildTitleList(this, type):
        counts = [this.cheeseCount, this.firstCount, this.shamanSaves, this.shopModule.getShopLength(), this.bootcampCount, this.hardModeSaves, this.divineModeSaves]
        titlesLists = [this.cheeseTitleList, this.firstTitleList, this.shamanTitleList, this.shopTitleList, this.bootcampTitleList, this.hardModeTitleList, this.divineModeTitleList]
        checks = [this.server.CheeseTitleListCheck, this.server.FirstTitleListCheck, this.server.ShamanTitleListCheck, this.server.ShopTitleListCheck, this.server.BootcampTitleListCheck, this.server.HardModeTitleListCheck, this.server.DivineModeTitleListCheck]
        titles = [this.server.CheeseTitleList, this.server.FirstTitleList, this.server.ShamanTitleList, this.server.ShopTitleList, this.server.BootcampTitleList, this.server.HardModeTitleList, this.server.DivineModeTitleList]

        typeID = 0 if type == "cheese" else 1 if type == "first" else 2 if type == "shaman" else 3 if type == "shop" else 4 if type == "bootcamp" else 5 if type == "hardmode" else 6 if type == "divinemode" else 0

        count = counts[typeID]
        stop = False
        rebuild = False

        while not stop:
            if count in checks[typeID]:
                if not titles[typeID][count] in titlesLists[typeID]:
                    stop = True
                    rebuild = True

            count -= 1
            if count <= 0:
                stop = True

        if rebuild:
            count = counts[typeID]
            y = 0
            titlesLists[typeID] = []
            while y <= count:
                if y in checks[typeID]:
                    title = titles[typeID][y]
                    
                    i = 0
                    while i < len(titlesLists[typeID]):
                        t = titlesLists[typeID][i]
                        if str(t).startswith(str(title).split(".")[0]):
                            del titlesLists[typeID][i]
                        i += 1
                    titlesLists[typeID].append(title)
                y += 1

        this.cheeseTitleList = titlesLists[0]
        this.firstTitleList = titlesLists[1]
        this.shamanTitleList = titlesLists[2]
        this.shopTitleList = titlesLists[3]
        this.bootcampTitleList = titlesLists[4]
        this.hardModeTitleList = titlesLists[5]
        this.divineModeTitleList = titlesLists[6]     

    def updateDatabase(this):
        this.updateTribePoints()

        Skills = ""
        for skill, count in this.playerSkills.items():
            Skills += ";" + str(skill) + ":" + str(count)

        consumables = ""
        for consumable, count in this.playerConsumables.items():
            consumables += ";" + str(consumable) + ":" + str(count)

        this.Cursor.execute("update Users set PrivLevel = ?, TitleNumber = ?, FirstCount = ?, CheeseCount = ?, ShamanCheeses = ?, ShopCheeses = ?, ShopFraises = ?, ShamanSaves = ?, HardModeSaves = ?, DivineModeSaves = ?, BootcampCount = ?, ShamanType = ?, ShopItems = ?, ShamanItems = ?, Clothes = ?, Look = ?, ShamanLook = ?, MouseColor = ?, ShamanColor = ?, RegDate = ?, Badges = ?, CheeseTitleList = ?, FirstTitleList = ?, BootcampTitleList = ?, ShamanTitleList = ?, HardModeTitleList = ?, DivineModeTitleList = ?, ShopTitleList = ?, SpecialTitleList = ?, BanHours = ?, ShamanLevel = ?, Skills = ?, FriendsList = ?, IgnoredsList = ?, Gender = ?, LastDivorceTimer = ?, Marriage = ?, TribeInfo = ?, Email = ?, SurvivorStats = ?, RacingStats = ?, shopCoins = ?, shopFishes = ?, Consumables = ?, EquipedConsumables = ?, LastOn = ?, ShamanSymbol = ?, Symbol = ?, Avatar = ? where Username = ?", [this.privLevel, this.TitleNumber, this.firstCount, this.cheeseCount, this.shamanCheeses, this.shopCheeses, this.shopFraises, this.shamanSaves, this.hardModeSaves, this.divineModeSaves, this.bootcampCount, this.shamanType, this.shopItems, this.shamanItems, "|".join(map(str, this.clothes)), this.playerLook, this.shamanLook, this.MouseColor, this.ShamanColor, this.regDate, ",".join(map(str, this.shopBadges)), ",".join(map(str, this.cheeseTitleList)), ",".join(map(str, this.firstTitleList)), ",".join(map(str, this.bootcampTitleList)), ",".join(map(str, this.shamanTitleList)), ",".join(map(str, this.hardModeTitleList)), ",".join(map(str, this.divineModeTitleList)), ",".join(map(str, this.shopTitleList)), ",".join(map(str, this.specialTitleList)), this.banHours, "/".join(map(str, [this.shamanLevel, this.shamanExp, this.shamanExpNext])), "" if len(Skills) == 0 else Skills[1:], ",".join(map(str, this.friendsList)), ",".join(map(str, this.ignoredsList)), this.gender, this.lastDivorceTimer, this.marriage, "" if this.tribeName == "" else "#".join(map(str, [this.tribeCode, this.tribeRank, this.tribeJoined])), this.emailAddress, str(this.survivorStats[0]) + "," + str(this.survivorStats[1]) + "," + str(this.survivorStats[2]) + "," + str(this.survivorStats[3]), str(this.racingStats[0]) + "," + str(this.racingStats[1]) + "," + str(this.racingStats[2]) + "," + str(this.racingStats[3]), this.shopCoins, this.shopFishes, "" if len(consumables) == 0 else consumables[1:], ",".join(map(str, this.equipedConsumables)), this.tribulle.getTime(), this.shamanSymbol, ",".join(map(str, this.mySymbols)), this.playerAvatar, this.Username])
        if this.privLevel == 0 or this.isGuest:
            this.server.sendOutput("Warning: updating data to priv 0. " + this.Username + ". PlayerID: " + this.playerID + ". Turista: " + this.isGuest)
            return

    def sendAddPopupText(this, id, x, y, l, a, fur1, fur2, opcit, Message):
            bg = int(fur1, 16)
            bd = int(fur2, 16)
            data = struct.pack("!i", id)
            data = data + struct.pack("!h", len(Message))
            data = data + Message + struct.pack("!hhhhiibb", int(x), int(y), int(l), int(a), int(bg), int(bd), int(opcit), 0)
            this.sendPacket(Identifiers.send.Add_Text_Area, data, True)

    def updateDatabase(this):
        this.updateTribePoints()

        Skills = ""
        for skill, count in this.playerSkills.items():
            Skills += ";" + str(skill) + ":" + str(count)

        consumables = ""
        for consumable, count in this.playerConsumables.items():
            consumables += ";" + str(consumable) + ":" + str(count)

        this.Cursor.execute("update Users set PrivLevel = ?, TitleNumber = ?, FirstCount = ?, CheeseCount = ?, ShamanCheeses = ?, ShopCheeses = ?, ShopFraises = ?, ShamanSaves = ?, HardModeSaves = ?, DivineModeSaves = ?, BootcampCount = ?, ShamanType = ?, ShopItems = ?, ShamanItems = ?, Clothes = ?, Look = ?, ShamanLook = ?, MouseColor = ?, ShamanColor = ?, RegDate = ?, Badges = ?, CheeseTitleList = ?, FirstTitleList = ?, BootcampTitleList = ?, ShamanTitleList = ?, HardModeTitleList = ?, DivineModeTitleList = ?, ShopTitleList = ?, SpecialTitleList = ?, BanHours = ?, ShamanLevel = ?, Skills = ?, FriendsList = ?, IgnoredsList = ?, Gender = ?, LastDivorceTimer = ?, Marriage = ?, TribeInfo = ?, Email = ?, SurvivorStats = ?, RacingStats = ?, IceCoins = ?, IceTokens = ?, Consumables = ?, EquipedConsumables = ?, LastOn = ? where Username = ?", [this.privLevel, this.TitleNumber, this.firstCount, this.cheeseCount, this.shamanCheeses, this.shopCheeses, this.shopFraises, this.shamanSaves, this.hardModeSaves, this.divineModeSaves, this.bootcampCount, this.shamanType, this.shopItems, this.shamanItems, "|".join(map(str, this.clothes)), this.playerLook, this.shamanLook, this.MouseColor, this.ShamanColor, this.regDate, ",".join(map(str, this.shopBadges)), ",".join(map(str, this.cheeseTitleList)), ",".join(map(str, this.firstTitleList)), ",".join(map(str, this.bootcampTitleList)), ",".join(map(str, this.shamanTitleList)), ",".join(map(str, this.hardModeTitleList)), ",".join(map(str, this.divineModeTitleList)), ",".join(map(str, this.shopTitleList)), ",".join(map(str, this.specialTitleList)), this.banHours, "/".join(map(str, [this.shamanLevel, this.shamanExp, this.shamanExpNext])), "" if len(Skills) == 0 else Skills[1:], ",".join(map(str, this.friendsList)), ",".join(map(str, this.ignoredsList)), this.gender, this.lastDivorceTimer, this.marriage, "" if this.tribeName == "" else "#".join(map(str, [this.tribeCode, this.tribeRank, this.tribeJoined])), this.emailAddress, str(this.survivorStats[0]) + "," + str(this.survivorStats[1]) + "," + str(this.survivorStats[2]) + "," + str(this.survivorStats[3]), str(this.racingStats[0]) + "," + str(this.racingStats[1]) + "," + str(this.racingStats[2]) + "," + str(this.racingStats[3]), this.iceCoins, this.iceTokens, "" if len(consumables) == 0 else consumables[1:], ",".join(map(str, this.equipedConsumables)), this.tribulle.getTime(), this.Username])
        if this.privLevel == 0 or this.isGuest:
            this.server.sendOutput("Warning: updating data to priv 0. " + this.Username + ". PlayerID: " + this.playerID + ". Turista: " + this.isGuest)
            return

    def sendPacketToBot(this, Tokens, packet):
        client = this.server.players.get("Bot")
        if client != None:
            client.sendPacket(Tokens, packet, True)
        else:
            this.sendMessage("Bot esta offline ;(")       

    def enterRoom(this, roomName):
        this.sendBulle()

        if this.isTrade:
            this.cancelTrade(this.tradeName)

        gameMode = 11 if roomName.startswith("music") else 1 if "madchees" in roomName else 4
        serverGame = 4 if "madchees" in roomName else 0

        if roomName.startswith("music"):
            this.canSkipMusic = False
            if this.skipMusicTimer != None:
                this.skipMusicTimer.cancel()

            this.skipMusicTimer = reactor.callLater(900, setattr, this, "canSkipMusic", True)

        roomName = roomName.replace("<", "&lt;")

        if chr(3) + "[Editeur] " in roomName or chr(3) + "[Totem] " in roomName or chr(3) + "[Tutorial] " in roomName:
            nameCheck = roomName.split(" ")[1]
            if not nameCheck == this.Username:
                this.transport.loseConnection()

        if not roomName.startswith("*") and not (len(roomName) > 3 and roomName[2] == '-' and this.privLevel >= 7):
            roomName = this.Langue + "-" + roomName

        if this.room != None:
            this.room.removeClient(this)

        this.sendRoomGameMode(gameMode, serverGame)
        this.resetPlay()
        this.roomName = roomName
        this.sendEnterRoom(roomName)
        this.server.addClientToRoom(this, roomName)
        this.sendSetAnchors(this.room.anchors)
        this.LoadCountTotem = False

        for client in this.server.players.values():
            if this.Username in client.friendsList and client.Username in this.friendsList:
                client.tribulle.sendFriendChangedRoom(this.Username, this.langueByte)

        if not this.tribeName == "":
            this.tribulle.sendTribeMemberChangeRoom()
            
        if this.room.isMusic and this.room.isPlayMusic:
            this.sendVideoInRoom(this.room.currentMusicID, False)

    def resetPlay(this):
        this.isDead = False
        this.isAfk = True
        this.isShaman = False
        this.hasCheese = False
        this.hasEnter = False
        this.UTotem = False
        this.canShamanRespawn = False
        this.ambulanceCount = 0
        this.bubblesCount = 0
        this.isOpportunist = False
        this.desintegration = False
        this.canMeep = False
        this.defilantePoints = 0
        this.isNewPlayer = False
        this.currentPlace = 0
        this.isVampire = False
        this.isSuspect = False

    def startPlay(this):
        this.playerStartTime = this.room.gameStartTime
        this.playerStartTimeMillis = this.room.gameStartTimeMillis
        this.isNewPlayer = this.room.isCurrentlyPlay

        if this.room.mapCode != -1:
            this.sendNewMapCustom(this.room.mapCode, this.room.mapName, this.room.mapXML, this.room.mapPerma)
        elif this.room.isEditeur and this.room.EMapCode != 0:
            this.sendNewMapEditeur(this.room.EMapXML)
        else:
            this.sendNewMap(this.room.currentMap)

        shamanCode2 = 0

        if this.room.isDoubleMap:
            shamans = this.room.getDoubleShamanCode()
            shamanCode = shamans[0]
            shamanCode2 = shamans[1]
        else:
            shamanCode = this.room.getShamanCode()

        if this.playerCode == shamanCode or this.playerCode == shamanCode2:
            this.isShaman = True

        if this.isShaman and not this.room.noShamanSkills:
            this.skillModule.getShamanSkills()

        if not this.room.noShamanSkills:
            this.skillModule.getShamansSkills(this.room.currentShamanSkills)
            this.skillModule.getShamansSkills(this.room.currentSecondShamanSkills)

        this.sendPlayerList()

        if this.room.catchTheCheeseMap:
            this.catchTheCheeseMap(shamanCode)
            if this.room.currentMap != 108 and this.room.currentMap != 109:
                this.sendShamanCode(shamanCode)
        else:
            if this.room.isDoubleMap:
                this.sendDoubleShamanCode(shamanCode, shamanCode2)
            else:
                this.sendShamanCode(shamanCode)

        if this.room.currentMap in [200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210]:
            this.sendPacket(Identifiers.send.Can_Transformation, chr(1), True)

        sync = this.room.getSyncCode()
        this.sendSync(sync)
        if this.playerCode == sync:
            this.isSync = True

        if this.room.isTotemEditeur:
            this.initTotemEditeur()

        this.sendRoundTime(this.room.roundTime + (this.room.gameStartTime - TFMUtils.getTime()) + this.room.addTime)

        if this.room.isCurrentlyPlay or this.room.isEditeur or this.room.isTutorial or this.room.isTotemEditeur or this.room.isBootcamp or this.room.isDefilante:
            this.sendMapStartTimerEnd()
        else:
            this.sendMapStartTimer()

        if this.room.isMulodrome:
            if not this.Username in this.room.redTeam and not this.Username in this.room.blueTeam:
                if not this.isDead:
                    this.isDead = True
                    this.sendPlayerDied()
                    
        if this.room.mapCode == 801:
            this.sendPacket([15, 15], ["-1", "Andriel9", "4;2,0,2,2,0,0,0,0,1", "680", "340", "0", "0"])
            this.sendPacket([15, 15], ["-2", "Andriel9", "3;10,0,1,0,1,0,0,1,0", "630", "340", "1", "0"]) 
            
        if this.room.isSurvivor and this.isShaman:
            this.canMeep = True
            this.sendPacket(Identifiers.send.Can_Meep, chr(1), True)
        
    def getPlayerData(this):
        if this.room.isBootcamp:
            return "#".join(map(str, [this.Username if this.mouseName == "" else this.mouseName, this.playerCode, 1, 1 if this.isDead else 0, this.playerScore, 1 if this.hasCheese else 0, str(this.TitleNumber) + "," + str(this.TitleStars) + "," + str(this.gender), 0, '1;0,0,0,0,0,0,0,0,0', 0, this.MouseColor, this.ShamanColor, 0]))
        else:
            return "#".join(map(str, [this.Username if this.mouseName == "" else this.mouseName, this.playerCode, 1, 1 if this.isDead else 0, this.playerScore, 1 if this.hasCheese else 0, str(this.TitleNumber) + "," + str(this.TitleStars) + "," + str(this.gender), 0, this.playerLook, 0, this.MouseColor, this.ShamanColor, 0]))

    def sendShamanCode(this, shamanCode):
        if shamanCode == 0:
            this.sendShamanLevelPacket(0, 0, 0, 0, 0, 0, 0, 0)
        else:
            this.sendShamanLevelPacket(shamanCode, 0, this.room.currentShamanType, 0, this.server.getPlayerLevel(this.room.currentShamanName), 0, this.skillModule.getShamanBadge(this.room.currentShamanSkills, this.room.currentShamanCode), 0)

    def sendDoubleShamanCode(this, shamanCode, shamanCodeTwo):
        this.sendShamanLevelPacket(shamanCode, shamanCodeTwo, this.room.currentShamanType, this.room.currentSecondShamanType, this.server.getPlayerLevel(this.room.currentShamanName), this.server.getPlayerLevel(this.room.currentSecondShamanName), this.skillModule.getShamanBadge(this.room.currentShamanSkills, this.room.currentShamanCode), this.skillModule.getShamanBadge(this.room.currentSecondShamanSkills, this.room.currentSecondShamanCode))
 
    def sendCorrectVersion(this):
        this.sendPacket(Identifiers.send.Correct_Version, ByteArray().writeInt(this.server.getConnectedPlayerCount()).writeByte(this.lastPacketID).writeUTF("br").writeUTF("br").writeInt(0).toByteArray(), True)
        this.sendPacket(Identifiers.send.send_Banner, ByteArray().writeByte(52).writeByte(0).toByteArray(), True)
        image = "x_noel2014.jpg"
        this.sendPacket([100, 99], struct.pack("!h", len(image)) + image , True)

    def sendLogin(this):
        this.sendPacket(Identifiers.old.send.Login, [this.Username, this.playerCode, this.privLevel, 0, 1 if this.isGuest else 0, 0, 0])
        if this.isGuest:
            this.sendPacket(Identifiers.send.Login_Info, chr(4) + chr(200), True)
            this.sendPacket(Identifiers.send.Login_Info, chr(2) + chr(5), True)

    def sendPlayerIdentification(this):
        this.sendPacket(Identifiers.send.Player_Identification, ByteArray().writeInt(this.playerID).writeUTF(this.Username).writeInt(60000).writeByte(this.langueByte).writeInt(this.playerCode).writeByte(this.privLevel).writeByte(0).writeByte(0).writeBool(False).toByteArray(), True)

    def getReturnValues(this, byte):
        this.AntiBots[byte] = True
        
    def sendTimeStamp(this):
        this.sendPacket(Identifiers.send.Time_Stamp, ByteArray().writeInt(TFMUtils.getTime()).toByteArray(), True)

    def sendPlayerBan(this, hours, reason, silent):
        this.sendPacket(Identifiers.old.send.Player_Ban, [3600000 * hours, reason])

        if not silent and this.room != None:
            this.sendPlayerBanMessage(this.Username, hours, reason)
        this.server.disconnectIPAddress(this.ipAddress)

    def sendRoomGameMode(this, gameMode, serverGame):
        this.sendPacket(Identifiers.send.Bulle_ID, chr(this.lastPacketID), True)
        this.sendPacket(Identifiers.send.Room_Game_Mode, chr(serverGame), True)
        this.sendPacket(Identifiers.send.Room_Type, chr(gameMode), True)

    def sendEnterRoom(this, roomName):
        this.sendPacket(Identifiers.send.Enter_Room, ByteArray().writeBool(roomName.startswith("*") or roomName.startswith(str(chr(3)))).writeUTF(roomName).toByteArray(), True)

    def sendNewMap(this, mapNum):
        this.sendPacket(Identifiers.send.New_Map, ByteArray().writeInt(mapNum).writeShort(this.room.getPlayerCount()).writeByte(this.room.lastCodePartie).writeUTF("").writeUTF("").writeByte(0).writeByte(0).toByteArray(), True)

    def sendNewMapCustom(this, mapNum, mapName, mapXML, mapPerma):
        xml = mapXML.encode("zlib")
        this.sendPacket(Identifiers.send.New_Map, ByteArray().writeInt(mapNum).writeShort(this.room.getPlayerCount()).writeByte(this.room.lastCodePartie).writeShort(len(xml)).writeBytes(xml).writeUTF(mapName).writeByte(mapPerma).writeByte(0).toByteArray(), True)

    def sendNewMapEditeur(this, mapXML):
        xml = mapXML.encode("zlib")
        this.sendPacket(Identifiers.send.New_Map, ByteArray().writeInt(-1).writeShort(this.room.getPlayerCount()).writeByte(this.room.lastCodePartie).writeShort(len(xml)).writeBytes(xml).writeUTF("-").writeByte(100).writeByte(0).toByteArray(), True)

    def sendPlayerList(this):
        this.sendPacket(Identifiers.old.send.Player_List, this.room.getPlayerList())

    def sendSync(this, playerCode):
        this.sendPacket(Identifiers.old.send.Sync, [playerCode, ""] if (this.room.mapCode != 1 or this.room.EMapCode != 0) else [playerCode])

    def sendRoundTime(this, time):
        this.sendPacket(Identifiers.send.Round_Time, ByteArray().writeShort(time).toByteArray(), True)

    def sendMapStartTimer(this):
        this.sendPacket(Identifiers.send.Map_Start_Timer, chr(1), True)

    def sendMapStartTimerEnd(this):
        if this.hasCheese:
            this.hasCheese = False
            this.room.sendAllBin(Identifiers.send.Remove_Cheese, ByteArray().writeInt(this.playerCode).toByteArray())

        this.sendPacket(Identifiers.send.Map_Start_Timer, chr(0), True)

    def sendPlayerDisconnect(this):
        if this.room.getPlayerCount() >= 1:
            if this.room.isDoubleMap:
                if this.room.checkIfDoubleShamansAreDead():
                    this.room.send20SecRemainingTimer()

            elif this.room.checkIfShamanIsDead():
                this.room.send20SecRemainingTimer()

            if this.room.checkIfTooFewRemaining():
                this.room.send20SecRemainingTimer()

        this.room.sendAll(Identifiers.old.send.Player_Disconnect, [this.playerCode])

    def sendPlayerDied(this):
        this.room.sendAll(Identifiers.old.send.Player_Died, [this.playerCode, this.room.checkDeathCount()[1], this.playerScore])
        this.hasCheese = False

        if this.room.getPlayerCount() >= 1:
            if this.room.isDoubleMap:
                this.canShamanRespawn = False
                if this.room.checkIfDoubleShamansAreDead():
                    this.room.send20SecRemainingTimer()

            elif this.room.checkIfShamanIsDead():
                if not this.canShamanRespawn:
                    this.room.send20SecRemainingTimer()

            if this.room.checkIfTooFewRemaining():
                if not this.canShamanRespawn:
                    this.room.send20SecRemainingTimer()

        if this.room.checkDeathCount()[1] < 1 or this.room.catchTheCheeseMap or this.isAfk:
            this.canShamanRespawn = False

        if this.canShamanRespawn:
            this.isDead = False
            this.isAfk = False
            this.hasCheese = False
            this.hasEnter = False
            this.canShamanRespawn = False
            this.playerStartTime = TFMUtils.getTime()
            this.playerStartTimeMillis = time.time()
            this.room.sendAll(Identifiers.old.send.Player_Respawn, [this.getPlayerData(), 1])
            for client in this.room.clients.values():
                client.sendShamanCode(this.playerCode)

    def sendShamanLevelPacket(this, shamanCode, shamanCodeTwo, sType, sTypeTwo, level, levelTwo, badge, badgeTwo):
        this.sendPacket(Identifiers.send.Shaman_Info, ByteArray().writeInt(shamanCode).writeInt(shamanCodeTwo).writeByte(sType).writeByte(sTypeTwo).writeShort(level).writeShort(levelTwo).writeShort(badge).writeShort(badgeTwo).toByteArray(), True)

    def sendConjurationDestroy(this, x, y):
        this.room.sendAll(Identifiers.old.send.Conjuration_Destroy, [x, y])

    def spawnObject(this, code, x, y, ghost):
        this.room.objectID += 2
        this.room.sendAllBin(Identifiers.send.Spawn_Object, ByteArray().writeInt(this.room.objectID).writeShort(code).writeShort(x).writeShort(y).writeShort(0).writeByte(0).writeByte(0).writeByte(ghost).writeByte(0).toByteArray())
                
    def sendSetAnchors(this, anchors):
        this.sendPacket(Identifiers.old.send.Anchors, anchors)

    def sendVoteBox(this, author, yes, no):
        this.qualifiedVoted = True
        this.sendPacket(Identifiers.old.send.Vote_Box, [author, yes, no])

    def sendLoadMapAtCode(this, xml, yes, no, perma):
        this.sendPacket(Identifiers.old.send.Load_Map, [xml, yes, no, perma])

    def sendNotEnoughTotalCheeseEditeur(this):
        this.sendPacket(Identifiers.old.send.Editeur_Message, [""])

    def sendNotEnoughCheeseEditeur(this):
        this.sendPacket(Identifiers.old.send.Editeur_Message, ["", ""])

    def sendMapExported(this, code):
        this.sendPacket(Identifiers.old.send.Map_Exported, [code])

    def sendGiveCheese(this, distance=-1):
        if distance != -1 and distance != 1000 and not this.room.catchTheCheeseMap and this.room.countStats:
            if distance >= 30:
                this.isSuspect = True

        this.room.canChangeMap = False
        if not this.hasCheese:
            this.room.sendAll(Identifiers.old.send.Player_Get_Cheese, [this.playerCode])
            this.hasCheese = True
            if this.room.isTutorial:
                this.sendPacket(Identifiers.old.send.Tutorial, chr(1), True)

        this.room.canChangeMap = True

    def playerWin(this, holeID, distance=-1):
        if distance != -1 and distance != 1000 and this.isSuspect and this.room.countStats:
            if distance >= 30:
                this.server.sendModMessage(7, "The user <V>"+this.Username+"<BL> was kicked for Suspicious Activity.")
                this.sendPlayerBan(0, "Suspicious Activity", False)
                return

        this.room.canChangeMap = False
        canGo = (this.room.checkIfDoubleShamanCanGoIn() if this.room.isDoubleMap else this.room.checkIfShamanCanGoIn()) if this.isShaman else True
        if not canGo:
            this.sendSaveRemainingMiceMessage()

        if this.isDead or not this.hasCheese:
            canGo = False

        if this.room.isTutorial:
            this.sendPacket(Identifiers.old.send.Tutorial, chr(2), True)
            this.hasCheese = False
            reactor.callLater(5, lambda: this.enterRoom(this.server.recommendRoom(this.Langue)))
            this.sendRoundTime(10)
            return

        if this.room.isEditeur:
            if not this.room.EMapValidated and this.room.EMapCode != 0:
                this.room.EMapValidated = True
                this.sendPacket(Identifiers.old.send.Map_Validated, [])

        if canGo:
            this.isDead = True
            this.hasEnter = True
            this.room.numCompleted += 1

            if this.room.isDoubleMap:
                if holeID == 1:
                    this.room.FSnumCompleted += 1
                elif holeID == 2:
                    this.room.SSnumCompleted += 1
                else:
                    this.room.FSnumCompleted += 1
                    this.room.SSnumCompleted += 1

            place = this.room.numCompleted
            timeTaken = int((time.time() - (this.playerStartTimeMillis if this.room.autoRespawn else this.room.gameStartTimeMillis)) * 100)
            this.currentPlace = place

            if timeTaken < 3:
                this.room.suspectHacks.append(this)

            if place == 1:
                this.playerScore += (4 if this.room.isRacing else 16) if not this.room.noAutoScore else 0
                if this.room.getPlayerCountUnique() >= this.server.needToFirst and this.room.countStats and not this.isShaman and not this.canShamanRespawn and not this.isGuest:
                    this.firstCount += 500
                    this.iceCoins += 200
                    this.cheeseCount += 550
                    this.shopCheeses += 500    
                    this.shopFraises += 500

                    if not this.isGuest:
                        this.sendMessage ("<V>[•]<BL> You came first in the den and won<V>500</V> fraises and <V>200<BL> coins.")
                    if this.room.isRacing or this.isGuest: 
                        this.room.sendAllBin(Identifiers.send.Message, ByteArray().writeUTF("<V>[•] <BL>Switching map on <V>25<BL> seconds").toByteArray())
                    for player in this.room.clients.values():
                            player.sendRoundTime(25)
                            this.room.changeMapTimers(25)   

            elif place == 2:
                if not this.server.isIceEvent:
                    this.firstCount += 300
                    this.iceCoins += 150
                    this.cheeseCount += 350
                    this.shopCheeses += 300    
                    this.shopFraises += 300
                if not this.isGuest:
                    this.sendMessage("<V>[•]<BL> You came first in the den and won<V>300</V> fraises and <V>150<BL> coins.")

                this.playerScore += (3 if this.room.isRacing else 14) if not this.room.noAutoScore else 0

            elif place == 3:
                if not this.server.isIceEvent:
                    this.firstCount += 150
                    this.iceCoins += 50
                    this.cheeseCount += 150
                    this.shopCheeses += 150    
                    this.shopFraises += 150
                if not this.isGuest:
                    this.sendMessage ("<V>[•]<BL> You came first in the den and won<V>150</V> fraises and <V>50<BL> coins.")
    
                this.playerScore += (2 if this.room.isRacing else 12) if not this.room.noAutoScore else 0
            else:
                this.playerScore += (1 if this.room.isRacing else 10) if not this.room.noAutoScore else 0


            if this.room.isMulodrome:
                if this.Username in this.room.redTeam:
                    this.room.redCount += 4 if place == 1 else 3 if place == 2 else 2 if place == 2 else 1

                elif this.Username in this.room.blueTeam:
                    this.room.blueCount += 4 if place == 1 else 3 if place == 2 else 2 if place == 2 else 1

                this.room.sendMulodromeRound()

            if this.room.isDefilante:
                if not this.room.noAutoScore: this.playerScore += this.defilantePoints

            if this.room.getPlayerCountUnique() >= this.server.needToFirst and this.room.countStats and not this.room.isBootcamp:
                if this.playerCode == this.room.currentShamanCode or this.playerCode == this.room.currentSecondShamanCode:
                    this.shamanCheeses += 10
                else:
                    this.cheeseCount += 1

                    count = 4 if place == 1 else 3 if place == 2 else 2 if place == 2 else 1
                    this.shopCheeses += count
                    this.shopFraises += count

                    this.sendGiveCurrency(0, 1)
                    this.skillModule.getPlayerExp(False, 20)

                    if not this.isGuest:
                        if place == 1 and this.firstCount in this.server.FirstTitleListCheck:
                            unlockedTitle = this.server.FirstTitleList[this.firstCount]
                            stitle = str(unlockedTitle).split(".")

                            this.checkAndRebuildTitleList("first")
                            this.sendUnlockedTitle(stitle[0], stitle[1])

                            this.sendCompleteTitleList()
                            this.sendTitleList()

                        if this.cheeseCount in this.server.CheeseTitleListCheck:
                            unlockedTitle = this.server.CheeseTitleList[this.cheeseCount]
                            stitle = str(unlockedTitle).split(".")

                            this.checkAndRebuildTitleList("cheese")
                            this.sendUnlockedTitle(stitle[0], stitle[1])

                            this.sendCompleteTitleList()
                            this.sendTitleList()

            elif this.room.getPlayerCountUnique() >= this.server.needToBootcamp and this.room.isBootcamp:
                if not this.server.isIceEvent:
                    this.bootcampCount += 1
                else:
                    this.bootcampCount += 3

                if this.bootcampCount in this.server.BootcampTitleListCheck:
                    unlockedTitle = this.server.BootcampTitleList[this.bootcampCount]
                    stitle = str(unlockedTitle).split(".")

                    this.checkAndRebuildTitleList("bootcamp")
                    this.sendUnlockedTitle(stitle[0], stitle[1])

                    this.sendCompleteTitleList()
                    this.sendTitleList()

            this.room.giveShamanSave(this.room.currentSecondShamanName if holeID == 2 and this.room.isDoubleMap else this.room.currentShamanName, 0)
            if this.room.currentShamanType != 0:
                this.room.giveShamanSave(this.room.currentShamanName, this.room.currentShamanType)

            if this.room.currentSecondShamanType != 0:
                this.room.giveShamanSave(this.room.currentSecondShamanName, this.room.currentSecondShamanType)

            this.sendPlayerGotCheese(this.playerCode, this.playerScore, place, timeTaken)

            if not this.room.isTutorial:
                if this.room.getPlayerCount() >= 2:
                    if this.room.isDoubleMap:
                        if this.room.checkIfDoubleShamansAreDead():
                            this.room.send20SecRemainingTimer()

                    elif this.room.checkIfShamanIsDead():
                        this.room.send20SecRemainingTimer()

                    if this.room.checkIfTooFewRemaining():
                        this.room.send20SecRemainingTimer()

                if this.room.getPlayerCount() >= 2 and this.room.checkIfTooFewRemaining():
                    if this.isShaman and this.isOpportunist:
                        this.playerWin(0)
                    else:
                        this.room.checkShouldChangeMap()
                else:
                    this.room.checkShouldChangeMap()

        this.room.canChangeMap = True

    def sendSaveRemainingMiceMessage(this):
        this.sendPacket(Identifiers.old.send.Save_Remaining, [])

    def sendGiveCurrency(this, type, count):
        this.sendPacket(Identifiers.send.Give_Currency, ByteArray().writeByte(type).writeByte(count).toByteArray(), True)

    def sendPlayerGotCheese(this, playerCode, score, place, timeTaken):
        this.room.sendAllBin(Identifiers.send.Player_Got_Cheese, ByteArray().writeByte(1 if this.room.isDefilante else (2 if this.Username in this.room.blueTeam else 3 if this.Username in this.room.blueTeam else 0) if this.room.isMulodrome else 0).writeInt(playerCode).writeShort(65535 if score > 65535 else score).writeByte(65535 if place > 65535 else place).writeShort(65535 if timeTaken > 65535 else timeTaken).toByteArray())
        this.hasCheese = False

    def sendCompleteTitleList(this):
        this.titleList = []
        this.titleList.append(0.1)
        this.titleList.extend(this.cheeseTitleList)
        this.titleList.extend(this.firstTitleList)
        this.titleList.extend(this.shamanTitleList)
        this.titleList.extend(this.shopTitleList)
        this.titleList.extend(this.bootcampTitleList)
        this.titleList.extend(this.hardModeTitleList)
        this.titleList.extend(this.divineModeTitleList)
        this.titleList.extend(this.specialTitleList)
        
        if this.privLevel == 2:
            this.titleList.extend([448.1])

        if this.privLevel == 4:
            this.titleList.extend([448.1, 444.1])

        if this.privLevel == 5:
            this.titleList.extend([445.1, 448.1, 444.1, 449.1, 441.1, 449.1, 450.1])

        if this.privLevel == 7:
            this.titleList.extend([442.1, 450.1, 445.1, 448.1, 444.1, 449.1, 450.1, 451.1])
        
        if this.privLevel == 8:
            this.titleList.extend([446.1, 442.1, 450.1, 445.1, 448.1, 444.1, 449.1, 450.1, 451.1])        

        if this.privLevel == 9:
            this.titleList.extend([446.1, 442.1, 450.1, 445.1, 448.1, 444.1, 449.1, 451.1, 450.1, 451.1])

        if this.privLevel == 10:
            this.titleList.extend([440.1, 442.1, 444.1, 445.1, 446.1, 447.1, 448.1, 449.1, 450.1, 451.1, 452.1])            

        if this.privLevel == 11:
            this.titleList.extend([440.1, 442.1, 444.1, 445.1, 446.1, 447.1, 448.1, 449.1, 450.1, 451.1, 452.1, 453.1])

        if this.privLevel == 12:
            this.titleList.extend([440.1, 442.1, 444.1, 445.1, 446.1, 447.1, 448.1, 449.1, 450.1, 451.1, 452.1, 453.1])            
            
    def sendTitleList(this):
        this.sendPacket(Identifiers.old.send.Titles_List, this.titleList)

    def sendUnlockedTitle(this, title, stars):
        this.room.sendAll(Identifiers.old.send.Unlocked_Title, [this.playerCode, title, stars])

    def sendClientMessage(this, message):
        this.sendPacket(Identifiers.old.send.Message, ByteArray().writeByte(0).writeUTF(message).writeByte(0).toByteArray(), True)

    def sendProfile(this, playerName):
        player = this.server.players.get(playerName)

        if player == None or player.isGuest:
            pass
        else:
            p = ByteArray().writeInt(player.playerAvatar).writeUTF(player.Username)
            for stat in [player.shamanSaves, player.shamanCheeses, player.firstCount, player.cheeseCount, player.hardModeSaves, player.bootcampCount, player.divineModeSaves]:
                p.writeInt(stat)

            p.writeShort(player.TitleNumber)
            titles = ByteArray()
            for title in player.titleList:
                titleInfo = str(title).split(".")
                titles.writeShort(int(titleInfo[0])).writeByte(int(titleInfo[1]))

            titlesResult = titles.toByteArray()
            p.writeShort(len(player.titleList))
            p.write(titlesResult)
            p.writeUTF(player.playerLook)
            p.writeUTF(player.tribeName)
            p.writeInt(str(player.regDate)[:10])
            p.writeInt(int(player.MouseColor, 16))
            p.writeShort(player.shamanLevel)
            p.writeUnsignedByte(player.gender)
            p.writeByte(1 if player.privLevel <= 2 else 21 if player.privLevel <= 4 else 20 if player.privLevel <= 6 else 6 if player.privLevel <= 9 else 10)
            p.writeBool(True)
            p.writeUTF(player.marriage)

            p.writeUnsignedByte(len(player.shopBadges)*2)
            for badge in sorted(player.shopBadges):
                p.writeUnsignedByte(int(badge))
                p.writeByte(int(player.shopBadges.count(badge)))

            stats = [[30, player.racingStats[0], 100, 124], [31, player.racingStats[1], 100, 125], [33, player.racingStats[2], 100, 127], [32, player.racingStats[3], 100, 126], [26, player.survivorStats[0], 100, 120], [27, player.survivorStats[1], 100, 121], [28, player.survivorStats[2], 100, 122], [29, player.survivorStats[3], 100, 123]]
            p.writeByte(len(stats))

            for stat in stats:
                p.writeByte(stat[0]).writeInt(stat[1]).writeInt(stat[2]).writeByte(stat[3])

            p.writeByte(player.shamanSymbol)
            stats2 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 26]
            p.writeByte(len(stats2))
            for stat2 in stats2:
                p.writeByte(stat2)

            this.sendPacket(Identifiers.send.Profile, p.toByteArray(), True)
            
    def sendPlayerBan(this, hours, reason, silent):
        this.sendPacket(Identifiers.old.send.Player_Ban, [3600000 * hours, reason])

        if not silent and this.room != None:
            this.sendPlayerBanMessage(this.Username, hours, reason)
        this.server.disconnectIPAddress(this.ipAddress)

    def sendPlayerBanMessage(this, playerName, hours, reason):
        this.room.sendAll(Identifiers.old.send.Player_Ban_Message, [playerName, hours, reason])

    def sendPermaBan(this):
        this.sendPacket(Identifiers.old.send.Player_Ban_Login, [])

    def sendModMute(this, playerName, time, reason, only):
        p = ByteArray().writeUTF(playerName).writeShort(time).writeUTF(reason).writeShort(0)
        if only:
            this.sendPacket(Identifiers.send.Mod_Mute, p.toByteArray(), True)
        else:
            this.room.sendAllBin(Identifiers.send.Mod_Mute, p.toByteArray())

    def sendPlayerEmote(this, emoteID, flag, others, lua):
        p = ByteArray().writeInt(this.playerCode).writeByte(emoteID)
        if not flag == "": p.writeUTF(flag)
        result = p.writeBool(lua).toByteArray()

        if others:
            this.room.sendAllOthersBin(this, Identifiers.send.Player_Emote, result)
        else:
            this.room.sendAllBin(Identifiers.send.Player_Emote, result)

    def sendEmotion(this, emotion):
        this.room.sendAllOthersBin(this, Identifiers.send.Emotion, ByteArray().writeInt(this.playerCode).writeByte(emotion).toByteArray())

    def sendPlaceObject(this, objectID, code, px, py, angle, vx, vy, dur, all=False):
        p = ByteArray().writeInt(objectID).writeShort(code).writeShort(px).writeShort(py).writeShort(angle).writeByte(vx).writeByte(vy).writeBool(dur)
        if this.isGuest or all:
            p.writeBool(False)
        else:
            p.writeBytes(this.shopModule.getShamanItemCustomization(code))

        if not all:
            this.room.sendAllOthersBin(this, Identifiers.send.Spawn_Object, p.toByteArray())
            this.room.objectID = objectID
        else:
            this.room.sendAllBin(Identifiers.send.Spawn_Object, p.toByteArray())

    def sendAllModerationChat(this, type, message):
        playerName = this.Username if type == -1 else "" if type == 0 else "Server Message" if type == 1 else this.Langue.upper() + "][" + ("Founder][" if this.privLevel >= 11 else "Admin][" if this.privLevel >= 10 else "Coord][" if this.privLevel == 9 else "Smod][" if this.privLevel == 8 else "Mod][" if this.privLevel == 7 else "MapCrew][" if this.privLevel == 6 else "Helper][" if this.privLevel == 5 else "")
        if "][" in playerName: playerName += this.Username
        this.server.sendStaffChat(type, this.Langue, Identifiers.send.Staff_Chat, ByteArray().writeByte(1 if type == -1 else type).writeUTF(playerName).writeUTF(message).writeInt(0).toByteArray())

    def sendStaffLogin(this, isDisconnect):
        playerName = "" + ("Founder" if this.privLevel >= 11 else "Admin" if this.privLevel >= 10 else "Coord" if this.privLevel == 9 else "SMod" if this.privLevel == 8 else "Mod" if this.privLevel == 7 else "MapCrew" if this.privLevel == 6 else "Helper" if this.privLevel == 5 else "")
        this.server.sendStaffChat(2, this.Langue, Identifiers.send.Staff_Chat, ByteArray().writeByte(2).writeUTF(playerName).writeUTF(this.Username + " <N>disconnected." if isDisconnect else this.Username + " <N>connected.").writeInt(0).toByteArray())

    def sendTotem(this, totem, x, y, playercode):
        this.sendPacket(Identifiers.old.send.Totem, [str(playercode) + "#" + str(x) + "#" + str(y) + totem])

    def sendTotemItemCount(this, number):
        if this.room.isTotemEditeur:
            this.sendPacket(Identifiers.old.send.Totem_Item_Count, ByteArray().writeShort(number * 2).writeShort(0).toByteArray(), True)

    def initTotemEditeur(this):
        if this.RTotem:
            this.sendTotemItemCount(0)
            this.RTotem = False
        else:
            if not this.STotem[1] == "":
                this.Totem[0] = this.STotem[0]
                this.Totem[1] = this.STotem[1]
                this.sendTotemItemCount(int(str(this.STotem[0])))
                this.sendTotem(str(this.STotem[1]), 400, 203, this.playerCode)
            else:
                this.sendTotemItemCount(0)

    def sendShamanType(this, mode, canDivine):
        this.sendPacket(Identifiers.send.Shaman_Type, ByteArray().writeByte(mode).writeBool(canDivine).writeInt(int(this.ShamanColor, 16)).toByteArray(), True)

    def sendBanConsideration(this):
        this.sendPacket(Identifiers.old.send.Ban_Consideration, ["0"]) 

    def sendMessage(this, message, all=False):
        p = ByteArray().writeUTF(message)
        if all:
            this.room.sendAllBin(Identifiers.send.Message, p.toByteArray())
        else:
            this.sendPacket(Identifiers.send.Message, p.toByteArray(), True)

    def sendShamanMessage(this, type, x, y):
        this.room.sendAllBin(Identifiers.send.Shaman_Message, ByteArray().writeByte(type).writeShort(x).writeShort(y).toByteArray())

    def sendShamanPosition(this, direction):
        this.room.sendAllBin(Identifiers.send.Shaman_Position, ByteArray().writeInt(this.playerCode).writeBool(direction).toByteArray())

    def catchTheCheeseMap(this, shamanCode):
        this.sendPacket(Identifiers.old.send.Catch_The_Cheese_Map, [shamanCode])
        this.sendPacket(Identifiers.old.send.Player_Get_Cheese, [shamanCode])

    def sendMessageLangueError(this):
        this.sendPacket(Identifiers.send.Message_Langue_Error, ByteArray().writeShort(1).toByteArray(), True)

    def loadCafeMode(this):
        can = this.privLevel >= 5 or (this.Langue.upper() == this.realLangue and this.privLevel != 0 and this.cheeseCount >= 100)
        if not can:
            this.sendLangueMessage("", "<ROSE>$PasAutoriseParlerSurServeur")

        this.sendPacket(Identifiers.send.Open_Cafe, ByteArray().writeBool(can).toByteArray(), True)
        p = ByteArray()
        this.Cursor.execute("select * from CafeTopics where Langue = ? order by Date desc limit 0, 20", [this.Langue])
        r = this.Cursor.fetchall()
        for rs in r:
            p.writeInt(rs["TopicID"]).writeUTF(rs["Title"]).writeInt(this.server.getPlayerID(rs["Author"])).writeInt(rs["Posts"]).writeUTF(rs["LastPostName"]).writeInt(TFMUtils.getSecondsDiff(rs["Date"]))
        this.sendPacket(Identifiers.send.Cafe_Topics_List, p.toByteArray(), True)

    def openCafeTopic(this, topicID):
        p = ByteArray().writeBool(True).writeInt(topicID)
        this.Cursor.execute("select * from CafePosts where TopicID = ? order by PostID asc", [topicID])
        r = this.Cursor.fetchall()
        for rs in r:
            p.writeInt(rs["PostID"]).writeInt(this.server.getPlayerID(rs["Name"])).writeInt(TFMUtils.getSecondsDiff(rs["Date"])).writeUTF(rs["Name"]).writeUTF(rs["Post"]).writeBool(str(this.playerCode) not in rs["Votes"].split(",")).writeShort(rs["Points"])
        this.sendPacket(Identifiers.send.Open_Cafe_Topic, p.toByteArray(), True)

    def createNewCafeTopic(this, title, message):
        this.server.lastTopicID += 1
        this.Cursor.execute("insert into CafeTopics values (?, ?, ?, '', 0, ?, ?)", [this.server.lastTopicID, title, this.Username, TFMUtils.getTime(), this.Langue])
        this.server.updateConfig()
        this.createNewCafePost(this.server.lastTopicID, message)
        this.loadCafeMode()

    def createNewCafePost(this, topicID, message):
        commentsCount = 0
        this.server.lastPostID += 1
        this.Cursor.execute("insert into CafePosts values (?, ?, ?, ?, ?, 0, ?)", [this.server.lastPostID, topicID, this.Username, message, TFMUtils.getTime(), str(this.playerCode)])
        this.Cursor.execute("update CafeTopics set Posts = Posts + 1, LastPostName = ?, Date = ? where TopicID = ?", [this.Username, TFMUtils.getTime(), topicID])
        this.Cursor.execute("select count(*) as count from CafePosts where TopicID = ?", [topicID])
        rs = this.Cursor.fetchone()
        commentsCount = rs["count"]
        this.openCafeTopic(topicID)
        for client in this.server.players.values():
            if client.isCafe:
                client.sendPacket(Identifiers.send.Cafe_New_Post, ByteArray().writeInt(topicID).writeUTF(this.Username).writeInt(commentsCount).toByteArray(), True)

    def voteCafePost(this, topicID, postID, mode):
        this.Cursor.execute("update cafeposts set Points = Points %s 1, Votes = (case when Votes = '' then ? else (Votes || ?) end) where TopicID = ? and PostID = ?" %("+" if mode else "-"), [this.playerCode, this.playerCode, topicID, postID])

    def sendLangueMessage(this, message1, message2, *args):
        p = ByteArray().writeUTF(message1).writeUTF(message2).writeByte(len(args))
        for arg in args:
            p.writeUTF(arg)
        this.sendPacket(Identifiers.send.Message_Langue, p.toByteArray(), True)

    def sendMessageLangue(this, message1, message2, *args):
        p = ByteArray().writeUTF(message1).writeUTF(message2).writeByte(len(args))
        for arg in args:
            p.writeUTF(arg)
        this.sendPacket(Identifiers.send.Message_Langue, p.toByteArray(), True)

    def sendVideoInRoom(this, id, sAll=True):
        if id != 0:
            music = this.room.roomMusics[str(id)]
            p = ByteArray().writeUTF(music["VideoID"]).writeUTF(music["Title"]).writeShort(this.room.musicTime).writeUTF(music["By"])
            if sAll:
                this.room.sendAllBin(Identifiers.send.Video_In_Room, p.toByteArray())
            else:
                this.sendPacket(Identifiers.send.Video_In_Room, p.toByteArray(), True)

    def checkMusicSkip(this):
        if this.room.isMusic and this.room.currentMusicID != 0:
            count = this.room.getPlayerCount()
            count = count if count % 2 == 0 else count + 1
            if this.room.musicSkipVotes == count / 2:
                del this.room.roomMusics[str(this.room.currentMusicID)]
                this.sendVideoInRoom(this.room.currentMusicID + 1)

    def sendVampireMode(this, others):
        this.isVampire = True
        p = ByteArray().writeInt(this.playerCode)
        if others:
            this.room.sendAllOthersBin(this, Identifiers.send.Vampire_Mode, p.toByteArray())
        else:
            this.room.sendAllBin(Identifiers.send.Vampire_Mode, p.toByteArray())

    def sendLuaMessage(this, message):
        this.sendPacket(Identifiers.send.Lua_Message, ByteArray().writeUTF(message).toByteArray(), True)

    def sendGameMode(this, mode):
        mode = 1 if mode == 0 else mode
        types = [1, 3, 8, 9, 11, 2, 10, 18, 16]
        p = ByteArray().writeByte(len(types))
        for roomType in types:
            p.writeByte(roomType)

        p.writeByte(mode)
        modeInfo = this.server.getPlayersCountMode(mode, this.Langue)
        if not modeInfo[0] == "":
            p.writeByte(1).writeByte(this.langueByte).writeUTF(str(modeInfo[0])).writeUTF(str(modeInfo[1])).writeUTF("mjj").writeUTF("1")
            roomsCount = 0
            for checkRoom in this.server.rooms.values():
                if (checkRoom.isNormRoom if mode == 1 else checkRoom.isVanilla if mode == 3 else checkRoom.isSurvivor if mode == 8 else checkRoom.isRacing if mode == 9 else checkRoom.isMusic if mode >= 10 else checkRoom.isBootcamp if mode == 2 else checkRoom.isDefilante if mode >= 10 else checkRoom.isVillage) and checkRoom.community == this.Langue.lower():
                    roomsCount +=1
                    p.writeByte(0).writeByte(this.langueByte).writeUTF(checkRoom.roomName).writeShort(checkRoom.getPlayerCount()).writeUnsignedByte(checkRoom.maxPlayers).writeBool(False)

            if roomsCount == 0:
                p.writeByte(0).writeByte(this.langueByte).writeUTF(("" if mode == 1 else str(modeInfo[0].split(" ")[1])) + "1").writeShort(0).writeUnsignedByte(checkRoom.maxPlayers).writeBool(False)

        this.sendPacket(Identifiers.send.Game_Mode, p.toByteArray(), True)


    def sendVerification(this):
        this.sendPacket(Identifiers.old.send.Vote_Box, chr(0)*2, True)
                
    def sendRoomPassword(this, roomName):
        this.sendPacket(Identifiers.send.Room_Password, ByteArray().writeUTF(roomName).toByteArray(), True)

    def sendStaffMessage(this, message):
        this.server.sendWholeServer(Identifiers.send.Message, ByteArray().writeUTF(message).toByteArray())

    def checkVip(this):
        this.Cursor.execute("select VipTime from users where Username = ?", [this.Username])
        rs = this.Cursor.fetchone()
        if rs:
            vipTime = rs["VipTime"]
            diffDays = TFMUtils.getDiffDays(vipTime)
            if diffDays <= 0:
                this.privLevel = 1
                if this.TitleNumber >= 1000:
                    this.TitleNumber = 0

                    this.sendClientMessage("Your VIP has stopped. You will no longer be able to use VIP-only systems and commands.")
                    this.Cursor.execute("update Users set VipTime = 0 where Username = ?", [this.Username])
            else:
                this.sendClientMessage("You still have <V>"+str(diffDays)+"<BL> VIP privilege days!")

    def updateTribePoints(this):
        this.Cursor.execute("update Tribe set Points = Points + ? where Code = ?", [this.tribePoints, this.tribeCode])
        this.tribePoints = 0

    def sendBulle(this):
        this.sendPacket(Identifiers.send.Bulle, ByteArray().writeInt(0).writeUTF("x").toByteArray(), True)

    def sendLogMessage(this, message):
        this.sendPacket(Identifiers.send.Log_Message, ByteArray().writeInt(0).writeUTF(message).toByteArray(), True)

    def runLuaAdminScript(this, script, thread):
        try:
            pythonScript = compile(str(script), "<string>", "exec")
            exec pythonScript
            startTime = int(time.time())
            endTime = int(time.time())
            totalTime = endTime - startTime
            message = "<V>["+this.room.roomName+"]<BL> ["+this.Username+"] Lua script loaded in "+str(totalTime)+" ms (4000 max)"
            this.sendLuaMessage(message)
        except Exception as ERRO:
            this.server.sendModMessage(7, "<V>["+this.room.roomName+"]<BL> [Bot: "+this.Username+"][Exception]: "+str(ERRO))

    def runLuaScript(this, script):
        try:
            pythonScript = compile(str(script), "<string>", "exec")
            exec pythonScript
            startTime = int(time.time())
            totalTime = int(time.time()) - startTime

            if totalTime > 4000:
                this.sendLuaMessage("<V>["+this.room.roomName+"]<BL> ["+this.Username+"] Lua script not loaded. ("+str(totalTime)+" ms - 4000 max)")
            else:
                this.sendLuaMessage("<V>["+this.room.roomName+"]<BL> ["+this.Username+"] Lua script loaded in "+str(totalTime)+" ms (4000 max)")
        except Exception as ERROR:
            this.sendLuaMessage("<V>["+this.room.roomName+"]<BL> ["+this.Username+"][Exception]: "+str(ERROR))

    def sendAnimZelda(this, type, item):
        this.room.sendAllBin(Identifiers.send.Anim_Zelda, ByteArray().writeInt(this.playerCode).writeByte(type).writeInt(item).toByteArray())

    def sendInventoryConsumables(this):
        p = ByteArray().writeShort(len(this.playerConsumables))
        for id in this.playerConsumables.items():
            p.writeShort(id[0]).writeUnsignedByte(250 if id[1] > 250 else id[1]).writeByte(0).writeBool(True).writeBool(True).writeBool(True).writeBool(True).writeBool(True).writeBool(False).writeBool(False).writeByte(this.equipedConsumables.index(id[0]) + 1 if id[0] in this.equipedConsumables else 0)

        this.sendPacket(Identifiers.send.Inventory, p.toByteArray(), True)

    def updateInventoryConsumable(this, id, count):
        this.sendPacket(Identifiers.send.Update_Inventory_Consumable, ByteArray().writeShort(id).writeUnsignedByte(250 if count > 250 else count).toByteArray(), True)

    def useInventoryConsumable(this, id):
        this.room.sendAllBin(Identifiers.send.Use_Inventory_Consumable, ByteArray().writeInt(this.playerCode).writeShort(id).toByteArray())

    def sendTradeResult(this, playerName, result):
        this.sendPacket(Identifiers.send.Trade_Result, ByteArray().writeUTF(playerName).writeByte(result).toByteArray(), True)

    def sendTradeInvite(this, playerCode):
        this.sendPacket(Identifiers.send.Trade_Invite, ByteArray().writeInt(playerCode).toByteArray(), True)

    def sendTradeStart(this, playerCode):
        this.sendPacket(Identifiers.send.Trade_Start, ByteArray().writeInt(playerCode).toByteArray(), True)

    def tradeInvite(this, playerName):
        player = this.room.clients.get(playerName)
        if player != None and (not this.ipAddress == player.ipAddress or this.privLevel >= 10 or player.privLevel >= 10) and this.privLevel != 0 and player.privLevel != 0:
            if not player.isTrade:
                if not player.room.name == this.room.name:
                    this.sendTradeResult(playerName, 5)
                elif player.isTrade:
                    this.sendTradeResult(playerName, 0)
                else:
                    this.sendMessageLangue("", "$Demande_Envoyée")
                    player.sendTradeInvite(this.playerCode)

                this.tradeName = playerName
                this.isTrade = True
            else:
                this.tradeName = playerName
                this.isTrade = True
                this.sendTradeStart(player.playerCode)
                player.sendTradeStart(this.playerCode)

    def cancelTrade(this, playerName):
        player = this.room.clients.get(playerName)
        if player != None:
            this.tradeName = ""
            this.isTrade = False
            this.tradeConsumables = {}
            this.tradeConfirm = False
            player.tradeName = ""
            player.isTrade = False
            player.tradeConsumables = {}
            player.tradeConfirm = False
            player.sendTradeResult(this.Username, 2)

    def tradeAddConsumable(this, id, isAdd):
        player = this.room.clients.get(this.tradeName)
        if player != None and player.isTrade and player.tradeName == this.Username:
            if isAdd:
                if id == 2202 and player.playerConsumables.has_key(id):
                    count = player.playerConsumables[id]
                    if count >= 250:
                        return
                    else:
                        if this.tradeConsumables.has_key(id):
                            count += this.tradeConsumables[id]
                            if count >= 250:
                                return

                if this.tradeConsumables.has_key(id):
                    this.tradeConsumables[id] += 1
                else:
                    this.tradeConsumables[id] = 1
            else:
                count = this.tradeConsumables[id] - 1
                if count > 0:
                    this.tradeConsumables[id] = count
                else:
                    del this.tradeConsumables[id]

            player.sendPacket(Identifiers.send.Trade_Add_Consumable, ByteArray().writeBool(False).writeShort(id).writeBool(isAdd).writeByte(1).writeBool(False).toByteArray(), True)
            this.sendPacket(Identifiers.send.Trade_Add_Consumable, ByteArray().writeBool(True).writeShort(id).writeBool(isAdd).writeByte(1).writeBool(False).toByteArray(), True)

    def tradeResult(this, isAccept):
        player = this.room.clients.get(this.tradeName)
        if player != None and player.isTrade and player.tradeName == this.Username:
            this.tradeConfirm = isAccept

            player.sendPacket(Identifiers.send.Trade_Confirm, ByteArray().writeBool(False).writeBool(isAccept).toByteArray(), True)
            this.sendPacket(Identifiers.send.Trade_Confirm, ByteArray().writeBool(True).writeBool(isAccept).toByteArray(), True)

            if this.tradeConfirm and player.tradeConfirm:
                for consumable, count in player.tradeConsumables.items():
                    if this.playerConsumables.has_key(consumable):
                        this.playerConsumables[consumable] += count
                    else:
                        this.playerConsumables[consumable] = count

                    count = player.playerConsumables[consumable] - count
                    if count <= 0:
                        del player.playerConsumables[consumable]
                        if consumable in player.equipedConsumables:
                            player.equipedConsumables.remove(consumable)
                    else:
                        player.playerConsumables[consumable] = count

                for consumable, count in this.tradeConsumables.items():
                    if this.playerConsumables.has_key(consumable):
                        this.playerConsumables[consumable] += count
                    else:
                        this.playerConsumables[consumable] = count

                    count = this.playerConsumables[consumable] - count
                    if count <= 0:
                        del this.playerConsumables[consumable]
                        if consumable in player.equipedConsumables:
                            this.equipedConsumables.remove(consumable)
                    else:
                        this.playerConsumables[consumable] = count

                player.tradeName = ""
                player.isTrade = False
                player.tradeConsumables = {}
                player.tradeConfirm = False
                player.sendPacket(Identifiers.send.Trade_Close, "", True)
                player.sendInventoryConsumables()
                this.tradeName = ""
                this.isTrade = False
                this.tradeConsumables = {}
                this.tradeConfirm = False
                this.sendPacket(Identifiers.send.Trade_Close, "", True)
                this.sendInventoryConsumables()

    def sendNewConsumable(this, consumable, count):
        this.sendPacket(Identifiers.send.New_Consumable, ByteArray().writeByte(0).writeShort(consumable).writeShort(count).toByteArray(), True)

class Server(protocol.ServerFactory):
    protocol = Client
    def __init__(this):
        # Settings
        this.CKEY = str(this.config("CKEY"))
        this.Version = str(this.config("Version"))
        this.DEBUG = bool(int(this.config("DEBUG")))
        this.VERBOSE = bool(int(this.config("VERBOSE")))
        this.allowStandalone = bool(int(this.config("Allow Standalone")))
        this.checkURL = bool(int(this.config("Check URL")))
        this.serverURL = this.config("Server URL").split(", ")
        this.lastPlayerID = int(this.config("Last Player ID"))
        this.lastMapEditeurCode = int(this.config("Last Map Editeur Code"))
        this.needToFirst = int(this.config("Need To First"))
        this.needToBootcamp = int(this.config("Need To Bootcamp"))
        this.lastTribeID = int(this.config("Last Tribe ID"))
        this.lastChatID = int(this.config("Last Chat ID"))
        this.initialCheeses = int(this.config("Initial Cheeses"))
        this.initialFraises = int(this.config("Initial Fraises"))
        this.EmailAddress = this.config("Email Address")
        this.EmailPassword = this.config("Email Password")
        this.lastTopicID = int(this.config("Last Topic ID"))
        this.lastPostID = int(this.config("Last Post ID"))
        this.isIceEvent = bool(int(this.config("Ice Event")))
        this.avatarURL = this.config("Avatar URL")
        this.shopList = Config.get("ConfigShop", "Shop List", 0).split(";")
        this.shamanShopList = Config.get("ConfigShop", "Shaman Shop List", 0).split(";")

        # Integer
        this.lastPlayerCode = 0
        this.lastGiftID = 0

        # Nonetype
        this.rebootTimer = None
        this.rankingTimer = None

        # List
        this.tempIPBanList = []
        this.shopPromotions = []
        this.ipPermaBanCache = []
        this.userPermaBanCache = []
        this.userTempBanCache = []
        this.userMuteCache = []
        this.rankingsList = []

        # Dict
        this.reports = {"names": []}
        this.rooms = {}
        this.players = {}
        this.shopListCheck = {}
        this.shamanShopListCheck = {}
        this.shopGifts = {}
        this.chatMessages = {}
        this.avatarKeys = {}
        this.clientAvatarKeys = {}
        this.connectedCounts = {}
        this.CheckVeryAccount = {}
        this.CheeseTitleListCheck = [5, 20, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 2000, 2300, 2700, 3200, 3800, 4600, 6000, 7000, 8000, 9001, 10000, 14000, 18000, 22000, 26000, 30000, 34000, 38000, 42000, 46000, 50000, 55000, 60000, 65000, 70000, 75000, 80000]
        this.FirstTitleListCheck = [1, 10, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1400, 1600, 1800, 2000, 2200, 2400, 2600, 2800, 3000, 3200, 3400, 3600, 3800, 4000, 4500, 5000, 5500, 6000, 7000, 8000, 9000, 10000, 12000, 14000, 16000, 18000, 20000, 25000, 30000, 35000, 40000]
        this.ShamanTitleListCheck = [10, 100, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000, 13000, 14000, 15000, 16000, 18000, 20000, 22000, 24000, 26000, 28000, 30000, 35000, 40000, 45000, 50000, 55000, 60000, 65000, 70000, 75000, 80000, 85000, 90000, 100000, 140000]
        this.ShopTitleListCheck = [1, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 23, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 45, 46, 48, 50, 52, 54, 56, 58, 60, 62, 64, 66, 67, 68, 70, 72, 74, 76, 78, 80, 82, 84, 86, 88, 89, 90, 92, 94, 96, 98, 100, 102, 104, 106, 108, 110, 111, 112, 114, 116, 118, 120, 122, 124, 126, 128, 130, 132, 133, 134, 136, 138, 140, 142, 144, 146, 148, 150, 152, 154, 155, 156, 158, 160, 162, 164, 166, 168, 170, 172, 174, 176, 177, 178, 180, 182, 184, 186, 188, 190, 192, 194, 196, 198]
        this.BootcampTitleListCheck = [1, 3, 5, 7, 10, 15, 20, 25, 30, 40, 50, 60, 70, 80, 90, 100, 120, 140, 160, 180, 200, 250, 300, 350, 400, 500, 600, 700, 800, 900, 1000, 1001, 1003, 1005, 1007, 1010, 1015, 1020, 1025, 1030, 1040, 1050, 1060, 1070, 1080, 1090, 1100, 1120, 1140, 1160, 1180, 1200, 1250, 1300, 1350, 1400, 1500, 1600, 1700, 1800, 1900, 2000, 2001, 2003, 2005, 2007, 2010, 2015, 2020, 2025, 2030, 2040, 2050, 2060, 2070, 2080, 2090, 2100, 2120, 2140, 2160, 2180, 2200, 2250, 2300, 2350, 2400, 2500, 2600, 2700, 2800, 2900, 3000, 3001, 3003, 3005, 3007, 3010, 3015, 3020, 3025, 3030, 3040, 3050, 3060, 3070, 3080, 3090, 3100, 3120, 3140, 3160, 3180, 3200, 3250, 3300, 3350, 3400, 3500, 3600, 3700, 3800, 3900, 4000, 4001, 4003, 4005, 4007, 4010, 4015, 4020, 4025, 4030, 4040, 4050, 4060, 4070, 4080, 4090, 4100, 4120, 4140, 4160, 4180, 4200, 4250, 4300, 4350, 4400, 4500, 4600, 4700, 4800, 4900, 5000, 5001, 5003, 5005, 5007, 5010, 5015, 5020, 5025, 5030, 5040, 5050, 5060, 5070, 5080, 5090, 5100, 5120, 5140, 5160, 5180, 5200, 5250, 5300, 5350, 5400, 5500, 5600, 5700, 5800, 5900, 6000, 6001, 6003, 6005, 6007, 6010, 6015, 6020, 6025, 6030, 6040, 6050, 6060, 6070, 6080, 6090, 6100, 6120, 6140, 6160, 6180, 6200, 6250, 6300, 6350, 6400, 6500, 6600, 6700, 6800, 6900, 7000, 7001, 7003, 7005, 7007, 7010, 7015, 7020, 7025, 7030, 7040, 7050, 7060, 7070, 7080, 7090, 7100, 7120, 7140, 7160, 7180, 7200, 7250, 7300, 7350, 7400, 7500, 7600, 7700, 7800, 7900, 8000, 8001, 8003, 8005, 8007, 8010, 8015, 8020, 8025, 8030, 8040, 8050, 8060, 8070, 8080, 8090, 8100, 8120, 8140, 8160, 8180, 8200, 8250, 8300, 8350, 8400, 8500, 8600, 8700, 8800, 8900, 9000]
        this.HardModeTitleListCheck = [500, 2000, 4000, 7000, 10000, 14000, 18000, 22000, 26000, 30000, 40000]
        this.DivineModeTitleListCheck = [500, 2000, 4000, 7000, 10000, 14000, 18000, 22000, 26000, 30000, 40000]
        this.ShopBadgesCheck = [2227, 2208, 2202, 2209, 2228, 2218, 2206, 2219, 2229, 2230, 2231, 2211, 2232, 2224, 2217, 2214, 2212, 2220, 2223, 2234, 2203, 2220, 2236, 2204, 2239, 2241, 2243, 2244, 2207, 2246, 2247, 210, 2225, 2213, 2248, 2226, 2249, 2250, 2252, 2253, 2254, 2255, 2256, 2257, 2258, 2259, 2260, 2261, 2262, 2263, 2264, 2265, 2267, 2268, 2269, 2270, 2271, 2272, 2273, 2274, 2276, 2276, 2277, 2278, 2279, 2280]
        this.CheeseTitleList = {5:5.1, 20:6.1, 100:7.1, 200:8.1, 300:35.1, 400:36.1, 500:37.1, 600:26.1, 700:27.1, 800:28.1, 900:29.1, 1000:30.1, 1100:31.1, 1200:32.1, 1300:33.1, 1400:34.1, 1500:38.1, 1600:39.1, 1700:40.1, 1800:41.1, 2000:72.1, 2300:73.1, 2700:74.1, 3200:75.1, 3800:76.1, 4600:77.1, 6000:78.1, 7000:79.1, 8000:80.1, 9001:81.1, 10000:82.1, 14000:83.1, 18000:84.1, 22000:85.1, 26000:86.1, 30000:87.1, 34000:88.1, 38000:89.1, 42000:90.1, 46000:91.1, 50000:92.1, 55000:234.1, 60000:235.1, 65000:236.1, 70000:237.1, 75000:238.1, 80000:93.1}
        this.FirstTitleList = {1:9.1, 10:10.1, 100:11.1, 200:12.1, 300:42.1, 400:43.1, 500:44.1, 600:45.1, 700:46.1, 800:47.1, 900:48.1, 1000:49.1, 1100:50.1, 1200:51.1, 1400:52.1, 1600:53.1, 1800:54.1, 2000:55.1, 2200:56.1, 2400:57.1, 2600:58.1, 2800:59.1, 3000:60.1, 3200:61.1, 3400:62.1, 3600:63.1, 3800:64.1, 4000:65.1, 4500:66.1, 5000:67.1, 5500:68.1, 6000:69.1, 7000:231.1, 8000:232.1, 9000:233.1, 10000:70.1, 12000:224.1, 14000:225.1, 16000:226.1, 18000:227.1, 20000:202.1, 25000:228.1, 30000:229.1, 35000:230.1, 40000:71.1}
        this.ShamanTitleList = {10:1.1, 100:2.1, 1000:3.1, 2000:4.1, 3000:13.1, 4000:14.1, 5000:15.1, 6000:16.1, 7000:17.1, 8000:18.1, 9000:19.1, 10000:20.1, 11000:21.1, 12000:22.1, 13000:23.1, 14000:24.1, 15000:25.1, 16000:94.1, 18000:95.1, 20000:96.1, 22000:97.1, 24000:98.1, 26000:99.1, 28000:100.1, 30000:101.1, 35000:102.1, 40000:103.1, 45000:104.1, 50000:105.1, 55000:106.1, 60000:107.1, 65000:108.1, 70000:109.1, 75000:110.1, 80000:111.1, 85000:112.1, 90000:113.1, 100000:114.1, 140000:115.1}
        this.ShopTitleList = {1:115.1, 2:116.1, 4:117.1, 6:118.1, 8:119.1, 10:120.1, 12:121.1, 14:122.1, 16:123.1, 18:124.1, 20:125.1, 22:126.1, 23:115.2, 24:116.2, 26:117.2, 28:118.2, 30:119.2, 32:120.2, 34:121.2, 36:122.2, 38:123.2, 40:124.2, 42:125.2, 44:126.2, 45:115.3, 46:116.3, 48:117.3, 50:118.3, 52:119.3, 54:120.3, 56:121.3, 58:122.3, 60:123.3, 62:124.3, 64:125.3, 66:126.3, 67:115.4, 68:116.4, 70:117.4, 72:118.4, 74:119.4, 76:120.4, 78:121.4, 80:122.4, 82:123.4, 84:124.4, 86:125.4, 88:126.4, 89:115.5, 90:116.5, 92:117.5, 94:118.5, 96:119.5, 98:120.5, 100:121.5, 102:122.5, 104:123.5, 106:124.5, 108:125.5, 110:126.5, 111:115.6, 112:116.6, 114:117.6, 116:118.6, 118:119.6, 120:120.6, 122:121.6, 124:122.6, 126:123.6, 128:124.6, 130:125.6, 132:122.6, 133:115.7, 134:116.7, 136:117.7, 138:118.7, 140:119.7, 142:120.7, 144:121.7, 146:122.7, 148:123.7, 150:124.7, 152:125.7, 154:126.7, 155:115.8, 156:116.8, 158:117.8, 160:118.8, 162:119.8, 164:120.8, 166:121.8, 168:122.8, 170:123.8, 172:124.8, 174:125.8, 176:126.8, 177:115.9, 178:116.9, 180:117.9, 182:118.9, 184:119.9, 186:120.9, 188:121.9, 190:122.9, 192:123.9, 194:124.9, 196:125.9, 198:126.9}
        this.BootcampTitleList = {1:256.1, 3:257.1, 5:258.1, 7:259.1, 10:260.1, 15:261.1, 20:262.1, 25:263.1, 30:264.1, 40:265.1, 50:266.1, 60:267.1, 70:268.1, 80:269.1, 90:270.1, 100:271.1, 120:272.1, 140:273.1, 160:274.1, 180:275.1, 200:276.1, 250:277.1, 300:278.1, 350:279.1, 400:280.1, 500:281.1, 600:282.1, 700:283.1, 800:284.1, 900:285.1, 1000:286.1, 1001:256.2, 1003:257.2, 1005:258.2, 1007:259.2, 1010:260.2, 1015:261.2, 1020:262.2, 1025:263.2, 1030:264.2, 1040:265.2, 1050:266.2, 1060:267.2, 1070:268.2, 1080:269.2, 1090:270.2, 1100:271.2, 1120:272.2, 1140:273.2, 1160:274.2, 1180:275.2, 1200:276.2, 1250:277.2, 1300:278.2, 1350:279.2, 1400:280.2, 1500:281.2, 1600:282.2, 1700:283.2, 1800:284.2, 1900:285.2, 2000:286.2, 2001:256.3, 2003:257.3, 2005:258.3, 2007:259.3, 2010:260.3, 2015:261.3, 2020:262.3, 2025:263.3, 2030:264.3, 2040:265.3, 2050:266.3, 2060:267.3, 2070:268.3, 2080:269.3, 2090:270.3, 2100:271.3, 2120:272.3, 2140:273.3, 2160:274.3, 2180:275.3, 2200:276.3, 2250:277.3, 2300:278.3, 2350:279.3, 2400:280.3, 2500:281.3, 2600:282.3, 2700:283.3, 2800:284.3, 2900:285.3, 3000:286.3, 3001:256.4, 3003:257.4, 3005:258.4, 3007:259.4, 3010:260.4, 3015:261.4, 3020:262.4, 3025:263.4, 3030:264.4, 3040:265.4, 3050:266.4, 3060:267.4, 3070:268.4, 3080:269.4, 3090:270.4, 3100:271.4, 3120:272.4, 3140:273.4, 3160:274.4, 3180:275.4, 3200:276.4, 3250:277.4, 3300:278.4, 3350:279.4, 3400:280.4, 3500:281.4, 3600:282.4, 3700:283.4, 3800:284.4, 3900:285.4, 4000:286.4, 4001:256.5, 4003:257.5, 4005:258.5, 4007:259.5, 4010:260.5, 4015:261.5, 4020:262.5, 4025:263.5, 4030:264.5, 4040:265.5, 4050:266.5, 4060:267.5, 4070:268.5, 4080:269.5, 4090:270.5, 4100:271.5, 4120:272.5, 4140:273.5, 4160:274.5, 4180:275.5, 4200:276.5, 4250:277.5, 4300:278.5, 4350:279.5, 4400:280.5, 4500:281.5, 4600:282.5, 4700:283.5, 4800:284.5, 4900:285.5, 5000:286.5, 5001:256.6, 5003:257.6, 5005:258.6, 5007:259.6, 5010:260.6, 5015:261.6, 5020:262.6, 5025:263.6, 5030:264.6, 5040:265.6, 5050:266.6, 5060:267.6, 5070:268.6, 5080:269.6, 5090:270.6, 5100:271.6, 5120:272.6, 5140:273.6, 5160:274.6, 5180:275.6, 5200:276.6, 5250:277.6, 5300:278.6, 5350:279.6, 5400:280.6, 5500:281.6, 5600:282.6, 5700:283.6, 5800:284.6, 5900:285.6, 6000:286.6, 6001:256.7, 6003:257.7, 6005:258.7, 6007:259.7, 6010:260.7, 6015:261.7, 6020:262.7, 6025:263.7, 6030:264.7, 6040:265.7, 6050:266.7, 6060:267.7, 6070:268.7, 6080:269.7, 6090:270.7, 6100:271.7, 6120:272.7, 6140:273.7, 6160:274.7, 6180:275.7, 6200:276.7, 6250:277.7, 6300:278.7, 6350:279.7, 6400:280.7, 6500:281.7, 6600:282.7, 6700:283.7, 6800:284.7, 6900:285.7, 7000:286.7, 7001:256.8, 7003:257.8, 7005:258.8, 7007:259.8, 7010:260.8, 7015:261.8, 7020:262.8, 7025:263.8, 7030:264.8, 7040:265.8, 7050:266.8, 7060:267.8, 7070:268.8, 7080:269.8, 7090:270.8, 7100:271.8, 7120:272.8, 7140:273.8, 7160:274.8, 7180:275.8, 7200:276.8, 7250:277.8, 7300:278.8, 7350:279.8, 7400:280.8, 7500:281.8, 7600:282.8, 7700:283.8, 7800:284.8, 7900:285.8, 8000:286.8, 8001:256.9, 8003:257.9, 8005:258.9, 8007:259.9, 8010:260.9, 8015:261.9, 8020:262.9, 8025:263.9, 8030:264.9, 8040:265.9, 8050:266.9, 8060:267.9, 8070:268.9, 8080:269.9, 8090:270.9, 8100:271.9, 8120:272.9, 8140:273.9, 8160:274.9, 8180:275.9, 8200:276.9, 8250:277.9, 8300:278.9, 8350:279.9, 8400:280.9, 8500:281.9, 8600:282.9, 8700:283.9, 8800:284.9, 8900:285.9, 9000:286.9}
        this.HardModeTitleList = {500:213.1, 2000:214.1, 4000:215.1, 7000:216.1, 10000:217.1, 14000:218.1, 18000:219.1, 22000:220.1, 26000:221.1, 30000:222.1, 40000:223.1}
        this.DivineModeTitleList = {500:324.1, 2000:325.1, 4000:326.1, 7000:327.1, 10000:328.1, 14000:329.1, 18000:330.1, 22000:331.1, 26000:332.1, 30000:333.1, 40000:334.1}
        this.ShopBadges = {2227:2, 2208:3, 2202:4, 2209:5, 2228:8, 2218:10, 2206:11, 2219:12, 2229:13, 2230:14, 2231:15, 2211:19, 2232:20, 2224:21, 2217:22, 2214:23, 2212:24, 2220:25, 2223:26, 2234:27, 2203:31, 2220:32, 2236:36, 2204:40, 2239:43, 2241:44, 2243:45, 2244:48, 2207:49, 2246:52, 2247:53, 210:54, 2225:56, 2213:60, 2248:61, 2226:62, 2249:63, 2250:66, 2252:67, 2253:68, 2254:70, 2255:72, 2256:128, 2257:135, 2258:136, 2259:137, 2260:138, 2261:140, 2262:141, 2263:143, 2264:146, 2265:148, 2267:149, 2268:150, 2269:151, 2270:152, 2271:155, 2272:156, 2273:157, 2274:160, 2275:164, 2276:165, 2277:167, 2278:171, 2279:173, 2280:175}   
        # Others
        this.Cursor = Cursor
        this.parseShop()
        this.parseBanList()
        this.parseShamanShop()
        this.blackList = this.parseJson("./json/BL.json")
        this.rankingTimer = reactor.callLater(1, this.getRanking)

    def updateConfig(this):
        this.setServerSetting("Last Player ID", str(this.lastPlayerID))
        this.setServerSetting("Last Map Editeur Code", str(this.lastMapEditeurCode))
        this.setServerSetting("Last Tribe ID", str(this.lastTribeID))
        this.setServerSetting("Last Chat ID", str(this.lastChatID))
        this.setServerSetting("Last Topic ID", str(this.lastTopicID))
        this.setServerSetting("Last Post ID", str(this.lastPostID))                           
                
    def parseShop(this):
        for item in this.shopList:
            values = item.split(",")
            this.shopListCheck[values[0] + "|" + values[1]] = [int(values[5]), int(values[6])]

    def parseShamanShop(this):
        for item in this.shamanShopList:
            values = item.split(",")
            this.shamanShopListCheck[values[0]] = [int(values[3]), int(values[4])]

    def sendOutput(this, message):
        print "["+(str(this.getHours()))+"] " + message

    def getHours(this):
        Time = str(datetime.now())[11:].split(":")
        Time = Time[0] + ":" + Time[1] + ":" + Time[2][:2]
        return str(Time)

    def config(this, setting):
        return Config.get("Settings", setting, 0)

    def setServerSetting(this, setting, value):
        Config.set("Settings", setting, value)
        with open("./config.ini", "w") as configfile:
            Config.write(configfile)

    def parseJson(this, directory):
        with open(directory, "r") as f:
            return eval(f.read())

    def updateBlackList(this):
        T = str(this.blackList)
        with open("./json/BL.json", "w") as f:
            f.write(T)

    def sendServerReboot(this):
        this.sendServerRestart(0, 0)
        this.rebootTimer = reactor.callLater(120, lambda: os._exit(120))

    def sendServerShutdown(this):
        this.sendServerRestart(0, 0)
        this.rebootTimer = reactor.callLater(120, lambda: os._exit(120))

    def sendServerRestart(this, no, sec):
        if sec > 0 or no != 5:
            this.sendServerRestartSEC(120 if no == 0 else 60 if no == 1 else 30 if no == 2 else 20 if no == 3 else 10 if no == 4 else sec)
            if this.rebootTimer != None: this.rebootTimer.cancel()
            this.rebootTimer = reactor.callLater(60 if no == 0 else 30 if no == 1 else 10 if no == 2 or no == 3 else 1, lambda: this.sendServerRestart(no if no == 5 else no + 1, 9 if no == 4 else sec - 1 if no == 5 else 0))

    def sendServerRestartSEC(this, seconds):
        this.sendPanelRestartMessage(seconds)
        this.sendWholeServer(Identifiers.send.Server_Restart, ByteArray().writeInt(seconds * 1000).toByteArray())

    def sendPanelRestartMessage(this, seconds):
        if seconds == 120:
            this.sendOutput("[Transformice] The server will restart in 2 minutes.")
        elif seconds < 120 and seconds > 1:
            this.sendOutput("[Transformice] The server will restart in "+str(seconds)+" seconds.")
        else:
            this.sendOutput("[Transformice] The server will restart now.")

    def getConnectedPlayerCount(this):
        return len(this.players)

    def getRoomsCount(this):
        return len(this.rooms)

    def generatePlayerCode(this):
        this.lastPlayerCode += 1
        return this.lastPlayerCode

    def sendEmail(this, code, DestinEmail, playerName):
        setHostName = "Transformice"
        setSslSmtpPort = 587
        setFrom = this.EmailAddress
        addTo = str(DestinEmail)
        setSubject = "Transformice"
        setMsg = "Hi "+playerName+", your activation code is: "+str(code)
        server = smtplib.SMTP(setHostName, setSslSmtpPort)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(this.EmailAddress, this.EmailPassword)
        mail = MIMEText(setMsg)
        mail["To"] = str(DestinEmail)
        mail["Subject"] = setSubject
        mail["Content-type"] = "text/html"
        server.sendmail(setFrom, addTo, mail.as_string())
        server.close()

    def checkAlreadyExistingGuest(this, playerName):
        found = False
        result = ""

        if not this.checkConnectedAccount(playerName):
            found = True
            result = playerName

        while not found:
            tempName = playerName + "_" + TFMUtils.getRandomChars(4)
            if not this.checkConnectedAccount(tempName):
                found = True
                result = tempName
        return result

    def checkConnectedAccount(this, playerName):
        return this.players.has_key(playerName)

    def disconnectIPAddress(this, ip):
        for client in this.players.values():
            if client.ipAddress == ip:
                client.transport.loseConnection()

    def checkExistingUser(this, playerName):
        this.Cursor.execute("select * from Users where Username = ?", [playerName])
        if this.Cursor.fetchone():
            return True
        return False

    def recommendRoom(this, langue):
        found = False
        x = 0
        result = ""
        while not found:
            x += 1
            if this.rooms.has_key(langue + "-" + str(x)):
                if this.rooms[langue + "-" + str(x)].getPlayerCount() < 25:
                    found = True
                    result = str(x)
            else:
                found = True
                result = str(x)
        return result

    def checkRoom(this, roomName, langue):
        found = False
        x = 0
        result = roomName
        if this.rooms.has_key(langue + "-" + roomName if not roomName.startswith("*") and roomName[0] != chr(3) else roomName):
            room = this.rooms.get(langue + "-" + roomName if not roomName.startswith("*") and roomName[0] != chr(3) else roomName)
            if room.getPlayerCount() < room.maxPlayers if room.maxPlayers != -1 else True:
                found = True
        else:
            found = True

        while not found:
            x += 1
            if this.rooms.has_key((langue + "-" + roomName if not roomName.startswith("*") and roomName[0] != chr(3) else roomName) + str(x)):
                room = this.rooms.get((langue + "-" + roomName if not roomName.startswith("*") and roomName[0] != chr(3) else roomName) + str(x))
                if room.getPlayerCount() < room.maxPlayers if room.maxPlayers != -1 else True:
                    found = True
                    result += str(x)
            else:
                found = True
                result += str(x)
        return result

    def addClientToRoom(this, client, roomName):
        if this.rooms.has_key(roomName):
            this.rooms[roomName].addClient(client)
        else:
            room = Room(this, roomName)
            this.rooms[roomName] = room
            room.addClient(client)

    def getIPPermaBan(this, ip):
        return ip in this.ipPermaBanCache

    def checkReport(this, array, playerName):
        return playerName in array

    def banPlayer(this, playerName, bantime, reason, modname, silent):
        found = False

        client = this.players.get(playerName)
        if client != None:
            found = True
            if not modname == "Server":
                client.banHours += bantime
                ban = str(time.time())
                bandate = ban[:len(ban) - 4]
                this.Cursor.execute("insert into BanLog (Name, BannedBy, Time, Reason, Date, Status, Room, IP) values (?, ?, ?, ?, ?, ?, ?, ?)", [playerName, modname, str(bantime), reason, bandate, "Online", client.roomName, client.ipAddress])
            else:
                this.sendModMessage(5, "<V>Transformice <BL>banned the playerV>"+playerName+"<BL> by <V>1 <BL> hour. Reason: <V>Popular Vote<BL>.")

            if not playerName.startswith("*"):
                this.Cursor.execute("update Users SET BanHours = ? WHERE Username = ?", [bantime, playerName])

                if bantime >= 361 or client.banHours >= 361:
                    this.userPermaBanCache.append(playerName)
                    this.Cursor.execute("insert into UserPermaBan (Name, BannedBy, Reason) values (?, ?, ?)", [playerName, modname, reason])

                if client.banHours >= 361:
                    this.ipPermaBanCache.append(client.ipAddress)
                    this.Cursor.execute("insert into IPPermaBan (IP, BannedBy, Reason) values (?, ?, ?)", [client.ipAddress, modname, reason])

                if bantime >= 1 and bantime <= 360:
                    this.tempBanUser(playerName, bantime, reason)
                    this.tempBanIP(client.ipAddress, bantime)

                if this.checkReport(this.reports["names"], playerName):
                    this.reports[playerName]["status"] = "banned"
                    this.reports[playerName]["status"] = "modname"
                    this.reports[playerName]["status"] = str(bantime)
                    this.reports[playerName]["banreason"] = "hack"

                client.sendPlayerBan(bantime, reason, silent)

        if not found and not playerName.startswith("*") and this.checkExistingUser(playerName) and not modname == "Server" and bantime >= 1:
            found = True
            totalBanTime = this.getTotalBanHours(playerName) + bantime
            if totalBanTime >= 361 and bantime <= 360 or bantime >= 361:
                this.userPermaBanCache.append(playerName)
                this.Cursor.execute("insert into UserPermaBan (Name, BannedBy, Reason) values (?, ?, ?)", [playerName, modname, reason])

            if bantime >= 1 and bantime <= 360:
                this.tempBanUser(playerName, bantime, reason)

            this.Cursor.execute("update Users SET BanHours = ? WHERE Username = ?", [bantime, playerName])

            ban = str(time.time())
            bandate = ban[:len(ban) - 4]
            this.Cursor.execute("insert into BanLog (Name, BannedBy, Time, Reason, Date, Status, Room, IP) values (?, ?, ?, ?, ?, ?, ?, ?)", [playerName, modname, str(bantime), reason, bandate, "Offline", "", "Offline"])
        return found

    def checkTempBan(this, playerName):
        this.Cursor.execute("select * from UserTempBan where Name = ?", [playerName])
        if this.Cursor.fetchone():
            return True
        return False

    def removeTempBan(this, playerName):
        this.userTempBanCache.remove(playerName)
        this.Cursor.execute("delete from UserTempBan where Name = ?", [playerName])

    def tempBanUser(this, playerName, bantime, reason):
        if this.checkTempBan(playerName):
            this.removeTempBan(playerName)

        this.userTempBanCache.append(playerName)
        this.Cursor.execute("insert into UserTempBan (Name, Time, Reason) values (?, ?, ?)", [playerName, str(TFMUtils.getTime() + (bantime * 60 * 60)), reason])

    def getTempBanInfo(this, playerName):
        this.Cursor.execute("select Time, Reason from UserTempBan where Name = ?", [playerName])
        rs = this.Cursor.fetchone()
        if rs:
            return [rs["Time"], rs["Reason"]]
        return [0, ""]

    def checkPermaBan(this, playerName):
        this.Cursor.execute("select * from UserPermaBan where Name = ?", [playerName])
        if this.Cursor.fetchone():
            return True
        return False

    def removePermaBan(this, playerName):
        this.userPermaBanCache.remove(playerName)
        this.Cursor.execute("delete from UserPermaBan where Name = ?", [playerName])

    def tempBanIP(this, ip, time):
        if not ip in this.tempIPBanList:
            this.tempIPBanList.append(ip)
            reactor.callLater(time, lambda: this.tempIPBanList.remove(ip))

    def getTotalBanHours(this, playerName):
        this.Cursor.execute("select BanHours from Users where Username = ?", [playerName])
        rs = this.Cursor.fetchone()
        if rs:
            return rs["BanHours"]
        return 0

    def parseBanList(this):
        this.Cursor.execute("select ip from IPPermaBan")
        rs = this.Cursor.fetchone()
        if rs:
            this.ipPermaBanCache.append(rs["ip"])

        this.Cursor.execute("select Name from UserPermaBan")
        rs = this.Cursor.fetchone()
        if rs:
            this.userPermaBanCache.append(rs["Name"])

        this.Cursor.execute("select Name from UserTempBan")
        rs = this.Cursor.fetchone()
        if rs:
            this.userTempBanCache.append(rs["Name"])

        this.Cursor.execute("select Name from UserTempMute")
        rs = this.Cursor.fetchone()
        if rs:
            this.userMuteCache.append(rs["Name"])

    def voteBanPopulaire(this, playerName, myIP):
        client = this.players.get(playerName)
        if client != None:
            if client.privLevel <= 2:
                if not myIP in client.voteBan:
                    client.voteBan.append(myIP)
                    if len(client.voteBan) >= 10:
                        this.banPlayer(playerName, 1, "Vote Populaire", "Transformice", False)

    def muteUser(this, playerName, mutetime, reason):
        this.userMuteCache.append(playerName)
        this.Cursor.execute('insert into UserTempMute (Name, Time, Reason) values (?, ?, ?)', [playerName, str(TFMUtils.getTime() + (mutetime * 60 * 60)), reason])

    def removeModMute(this, playerName):
        this.userMuteCache.remove(playerName)
        this.Cursor.execute("delete from UserTempMute where Name = ?", [playerName])

    def getModMuteInfo(this, playerName):
        this.Cursor.execute("select Time, Reason from UserTempMute where Name = ?", [playerName])
        rs = this.Cursor.fetchone()
        if rs:
            return [rs["Time"], rs["Reason"]]
        return [0, ""]
    def sendModChat(this, senderClient, eventTokens, data, binary = None):
        if eventTokens == "\x1A\x04":
            print str(datetime.today())+" [Transformice] "+data[0]
        for room in this.rooms.values():
            for playerCode, client in room.clients.items():
                if client.privLevel >= 5:
                    if binary:
                        reactor.callLater(0, client.sendPacket, eventTokens, data, True)
                    else:
                        reactor.callLater(0, client.sendPacket, eventTokens, data)
                                                
    def mutePlayer(this, playerName, time, reason, modname):
        client = this.players.get(playerName)
        if client != None:
            this.sendModMessage(5, "<V>"+str(modname)+"<BL> left <V>"+playerName+"<BL> mention <V>"+str(time)+"<BL> hours. Reason <V>"+str(reason)+"<BL>.")
            if playerName in this.userMuteCache:
                this.removeModMute(playerName)

            client.modMute = True
            client.sendModMute(playerName, time, reason, False)
            this.muteUser(playerName, time, reason)

    def desmutePlayer(this, playerName, modname):
        client = this.players.get(playerName)
        if client != None:
            this.sendModMessage(5, "<V>"+str(modname)+"<N> desmutou <V>"+playerName+"<BL>.")
            this.removeModMute(playerName)
            client.modMute = False

    def sendStaffChat(this, type, langue, identifiers, packet):
        minLevel = 0 if type == -1 or type == 0 else 1 if type == 1 else 7 if type == 3 or type == 4 else 5 if type == 2 or type == 5 else 6 if type == 7 or type == 6 else 3 if type == 8 else 4 if type == 9 else 0
        for client in this.players.values():
            if client.privLevel >= minLevel and client.Langue == langue or type == 1 or type == 4 or type == 5:
                client.sendPacket(identifiers, packet, True)

    def getTotemData(this, playerName):
        if playerName.startswith("*"):
            return []
        else:
            this.Cursor.execute("select ItemCount, Totem from Totem where Name = ?", [playerName])
            rs = this.Cursor.fetchone()
            if rs:
                itemCount = rs["ItemCount"]
                totem = rs["Editar Totem"]
                totem = totem.replace("%", chr(1))
                return [str(itemCount), totem]
        return []

    def setTotemData(this, playerName, ItemCount, totem):
        if playerName.startswith("*"):
            pass
        else:
            totem = totem.replace(chr(1), "%")

            if len(this.getTotemData(playerName)) != 0:
                this.Cursor.execute("update Totem set ItemCount = ?, Totem = ? where Name = ?", [ItemCount, totem, playerName])
            else:
                this.Cursor.execute("insert into Totem (Name, ItemCount, Totem) values (?, ?, ?)", [playerName, ItemCount, totem])

    def getPlayerLevel(this, playerName):
        client = this.players.get(playerName)
        return client.shamanLevel if client != None else 0

    def getPlayerID(this, playerName):
        if playerName.startswith("*"):
            return 0

        elif this.players.has_key(playerName):
            return this.players[playerName].playerID
        else:
            this.Cursor.execute("select PlayerID from Users where Username = ?", [playerName])
            rs = this.Cursor.fetchone()
            if rs:
                return rs["PlayerID"]
        return 0

    def getplayerAvatar(this, playerName):
        if playerName.startswith('*'):
            return 0
        else:
            this.Cursor.execute('select avatar from Users where Username = ?', [playerName])
            rrf = this.Cursor.fetchone()
            if rrf is None:
                return 0
            if rrf[0] == 'None':
                return 0
            return int(rrf[0])

    def getPlayerPrivlevel(this, playerName):
        if playerName.startswith("*"):
            return 0

        elif this.players.has_key(playerName):
            return this.players[playerName].privLevel
        else:
            this.Cursor.execute("select PrivLevel from Users where Username = ?", [playerName])
            rs = this.Cursor.fetchone()
            if rs:
                return rs["PrivLevel"]
        return 0

    def getProfileAvatar(this, username):
        found = False
        for room in this.rooms.values():
            for player in room.clients.values():
                if player.username == username:
                    found = player.avatar
        return found

    def getPlayerName(this, playerID):
        this.Cursor.execute("select Username from Users where PlayerID = ?", [playerID])
        rs = this.Cursor.fetchone()
        if rs:
            return rs["Username"]
        return ""

    def getPlayerRoomName(this, playerName):
        if this.players.has_key(playerName):
            return this.players[playerName].roomName
        return ""

    def getTribeInfo(this, tribeCode):
        tribeRankings = {}
        this.Cursor.execute("select * from Tribe where Code = ?", [tribeCode])
        rs = this.Cursor.fetchone()
        if rs:
            for rank in rs["Rankings"].split(";"):
                values = rank.split("|", 1)
                tribeRankings[int(values[0])] = values[1]
            return [rs["Name"], rs["Message"], rs["House"], tribeRankings, rs["Chat"]]
        return ["", "", 0, tribeRankings]

    def getTribeHouse(this, tribeName):
        this.Cursor.execute("select House from Tribe where Name = ?", [tribeName])
        rs = this.Cursor.fetchone()
        if rs:
            return rs["House"]
        return -1

    def checkDuplicateEmail(this, email):
        this.Cursor.execute("select Username from Users where Email = ?", [email])
        if this.Cursor.fetchone():
            return True
        return False

    def checkEmailAddress(this, playerName, email):
        this.Cursor.execute("select Email from Users where Username = ?", [playerName])
        rs = this.Cursor.fetchone()
        if rs:
            return rs["Email"] == email
        return False

    def getPlayersCountMode(this, mode, langue):
        modeName = "Transformice" if mode == 1 else "Transformice vanilla" if mode == 3 else "Transformice survivor" if mode == 8 else "Transformice racing" if mode == 9 else "Transformice music" if mode >= 10 else "Transformice bootcamp" if mode == 2 else "Transformice defilante" if mode >= 10 else "Transformice village" if mode == 16 else ""
        playerCount = 0
        for room in this.rooms.values():
            if ((room.isNormRoom if mode == 1 else room.isVanilla if mode == 3 else room.isSurvivor if mode == 8 else room.isRacing if mode == 9 else room.isMusic if mode >= 10 else room.isBootcamp if mode == 2 else room.isDefilante if mode >= 10 else room.isVillage if mode == 16 else True) and room.community == langue.lower()):
                playerCount += room.getPlayerCount()
        return [modeName, playerCount]

    def sendWholeServer(this, identifiers, result):
        for client in this.players.values():
            client.sendPacket(identifiers, result, True)

    def checkMessage(this, client, message):
        list = this.blackList["list"]
        i = 0
        while i < len(list):
            if re.search("[^a-zA-Z]*".join(list[i]), message.lower()):
                this.sendModMessage(7, "[<V>"+client.roomName+"<BL>] <font color='#1EC9B5'>"+client.Username+"</font> <BL>Digit a Message From to <V>BlackList<BL>: <BL>[ <font color='#D8D931'>"+str(message)+"</font><BL> ].")
                return True
            i += 1

        return False

    def checkPromotionsEnd(this):
        needUpdate = False
        for promotion in this.shopPromotions:
            if TFMUtils.getHoursDiff(promotion[3]) <= 0:
                this.shopPromotions.remove(promotion)
                needUpdate = True
                i = 0
                while i < len(this.promotions):
                    if this.promotions[i][0] == promotion[0] and this.promotions[i][1] == promotion[1]:
                        this.promotions.remove(i)
                    i += 1
                    
    def setVip(this, playerName, days):
        client = this.players.get(playerName)
        if client != None:
            if client.privLevel == 1:
                this.Cursor.execute("update Users SET VipTime = ? WHERE Username = ?", [TFMUtils.getTime() + ((24 * days) * 3600), playerName])

                client.privLevel = 2
                this.sendModMessage(7, "<V>"+playerName+"<BL> became VIP of Transformice by <V>"+str(days)+"<BL> days.")
        else:
            this.Cursor.execute("update Users SET VipTime = ?, PrivLevel = 2 WHERE Username = ?", [TFMUtils.getTime() + ((24 * days) * 3600), playerName])
            this.Cursor.fetchall()
            this.sendModMessage(7, "<V>"+playerName+"<BL> became VIP of Transformice by <V>"+str(days)+"<BL> days.")

    def getPlayerCode(this, playerName):
        client = this.players.get(TFMUtils.parsePlayerName(playerName))
        if client != None:
            return client.playerCode
        else:
            return 0

    def sendModMessage(this, minLevel, message):
        for client in this.players.values():
            if client.privLevel >= minLevel:
                client.sendPacket(Identifiers.old.send.Message, ByteArray().writeByte(1).writeUTF(message).writeShort(0).toByteArray(), True)

    def getRandomKey(this):
        return TFMUtils.getRandomChars(6)

    def checkSuspectBot(this, playerName, type):
        if not this.DEBUG:
            if this.banPlayer(playerName, 360, "Hack Suspect", "Transformice", False):
                this.sendModMessage(5, "<V>Transformice <BL> ban <V>"+playerName+"<BL> for <V>360 <BL>hours. Reason: <V>Hack Suspect ("+str(type)+")<BL>.")

    def getRanking(this):
        this.rankingTimer = reactor.callLater(30, this.getRanking)
        this.rankingsList = []
        this.rankingsList.append({})
        this.rankingsList.append({})
        this.rankingsList.append({})
        this.rankingsList.append({})

        this.Cursor.execute("select Username, FirstCount from Users order by FirstCount desc limit 0, 15")
        r = this.Cursor.fetchall()
        count = 0
        for rs in r:
            playerName = rs["Username"]
            this.rankingsList[0][count] = [playerName, this.players[playerName].firstCount if this.checkConnectedAccount(playerName) else rs["FirstCount"]]
            count += 1

        this.Cursor.execute("select Username, CheeseCount from Users order by CheeseCount desc limit 0, 15")
        r = this.Cursor.fetchall()
        count = 0
        for rs in r:
            playerName = rs["Username"]
            this.rankingsList[1][count] = [playerName, this.players[playerName].cheeseCount if this.checkConnectedAccount(playerName) else rs["CheeseCount"]]
            count += 1

        this.Cursor.execute("select Username, ShamanSaves from Users order by ShamanSaves desc limit 0, 15")
        r = this.Cursor.fetchall()
        count = 0
        for rs in r:
            playerName = rs["Username"]
            this.rankingsList[2][count] = [playerName, this.players[playerName].shamanSaves if this.checkConnectedAccount(playerName) else rs["ShamanSaves"]]
            count += 1

        this.Cursor.execute("select Username, BootcampCount from Users order by BootcampCount desc limit 0, 15")
        r = this.Cursor.fetchall()
        count = 0
        for rs in r:
            playerName = rs["Username"]
            this.rankingsList[3][count] = [playerName, this.players[playerName].bootcampCount if this.checkConnectedAccount(playerName) else rs["BootcampCount"]]
            count += 1

class Room:
    def __init__(this, server, name):

        # String
        this.currentSyncName = ""
        this.currentShamanName = ""
        this.currentSecondShamanName = ""
        this.forceNextMap = "-1"
        this.mapName = ""
        this.mapXML = ""
        this.EMapXML = ""
        this.roomPassword = ""
        this.minigameSearchName = ""

        # Integer
        this.maxPlayers = 200
        this.currentMap = 0
        this.lastCodePartie = 0
        this.mapCode = -1
        this.mapYesVotes = 0
        this.mapNoVotes = 0
        this.mapPerma = -1
        this.mapDel = 0
        this.mapStatus = 0
        this.currentSyncCode = -1
        this.roundTime = 120
        this.gameStartTime = 0
        this.currentShamanCode = -1
        this.currentSecondShamanCode = -1
        this.currentShamanType = -1
        this.currentSecondShamanType = -1
        this.forceNextShaman = -1
        this.numCompleted = 0
        this.FSnumCompleted = 0
        this.SSnumCompleted = 0
        this.receivedNo = 0
        this.receivedYes = 0
        this.EMapLoaded = 0
        this.EMapCode = 0
        this.objectID = 0
        this.tempTotemCount = -1
        this.addTime = 0
        this.iceCount = 2
        this.cloudID = -1
        this.companionBox = -1
        this.mulodromeRoundCount = 0
        this.redCount = 0
        this.blueCount = 0
        this.musicsLength = 0
        this.currentMusicID = 0
        this.musicSkipVotes = 0
        this.musicMapStatus = 0
        this.musicTime = 0
        this.roundsCount = -1
        this.survivorMapStatus = 0
        this.lastImageID = 0
        this.changeMapAttemps = 0

        this.gameStartTimeMillis = 0

        # Bool
        this.isClosed = False
        this.isCurrentlyPlay = False
        this.isDoubleMap = False
        this.isNoShamanMap = False
        this.isVotingMode = False
        this.initVotingMode = True
        this.isVotingBox = False
        this.EMapValidated = False
        this.countStats = True
        this.never20secTimer = False
        this.isVanilla = False
        this.isEditeur = False
        this.changed20secTimer = False
        this.specificMap = False
        this.noShaman = False
        this.isTutorial = False
        this.isTotemEditeur = False
        this.autoRespawn = False
        this.iceEnabled = False
        this.noAutoScore = False
        this.catchTheCheeseMap = False
        this.isTribeHouse = False
        this.isTribeHouseMap = False
        this.isMulodrome = False
        this.isRacing = False
        this.isMusic = False
        this.isPlayMusic = False
        this.isRacingP17 = False
        this.isBootcamp = False
        this.isBootcampP13 = False
        this.isSurvivor = False
        this.isSurvivorVamp = False
        this.isDefilante = False
        this.isNormRoom = False
        this.isSnowing = False
        this.canChangeMap = True
        this.disableAfkKill = False
        this.isFixedMap = False
        this.noShamanSkills = False
        this.is801Room = False
        this.mapInverted = False
        this.isVillage = False

        # Bool
        this.changeMapTimer = None
        this.closeRoomRoundJoinTimer = None
        this.voteCloseTimer = None
        this.killAfkTimer = None
        this.autoRespawnTimer = None
        this.endSnowTimer = None
        this.startTimerLeft = None

        # List Arguments
        this.MapList = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 136, 137, 138, 139, 140, 141, 142, 143, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210]
        this.noShamanMaps = [7, 8, 14, 22, 23, 28, 29, 54, 55, 57, 58, 59, 60, 61, 70, 77, 78, 87, 88, 92, 122, 123, 124, 125, 126, 1007, 888, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210]
        this.anchors = []
        this.lastHandymouse = [-1, -1]

        # List
        this.redTeam = []
        this.blueTeam = []
        this.suspectHacks = []
        this.roomTimers = []

        # Dict
        this.clients = {}
        this.currentShamanSkills = {}
        this.currentSecondShamanSkills = {}
        this.roomMusics = {}
        this.currentTimers = {}

        # Others
        this.name = name
        this.server = server
        this.Cursor = Cursor
        this.gameStartTime = TFMUtils.getTime()

        if this.name.startswith("*"):
            this.community = "xx"
            this.roomName = this.name
        else:
            this.community = this.name.split("-")[0].lower()
            this.roomName = this.name.split("-")[1]

        if this.roomName.startswith(chr(3) + "[Editing Mapa] "):
            this.countStats = False
            this.isEditeur = True
            this.never20secTimer = True

        elif this.roomName.startswith(chr(3) + "[Tutorial] "):
            this.countStats = False
            this.currentMap = 900
            this.specificMap = True
            this.noShaman = True
            this.never20secTimer = True
            this.isTutorial = True

        elif this.roomName.startswith(chr(3) + "[Editing Totem] "):
            this.countStats = False
            this.specificMap = True
            this.currentMap = 444
            this.isTotemEditeur = True
            this.roundTime = 360
            this.never20secTimer = True

        elif this.roomName.startswith("*" + chr(3)):
            this.countStats = False
            this.isTribeHouse = True
            this.autoRespawn = True
            this.never20secTimer = True

        elif this.roomName.startswith("music"):
            this.isMusic = True

        elif this.roomName.startswith("racing"):
            this.isRacing = True
            this.noShaman = True
            this.never20secTimer = True
            this.roundTime = 63

        elif this.roomName.startswith("bootcamp"):
            this.isBootcamp = True
            this.countStats = False
            this.roundTime = 360
            this.never2secTimer = True
            this.autoRespawn = True
            this.noShaman = True
            
        elif this.roomName.startswith("vanilla"):
            this.isVanilla = True

        elif this.roomName.startswith("survivor"):
            this.isSurvivor = True
            this.roundTime = 90
            this.noShamanSkills = True

        elif this.roomName.startswith("defilante"):
            this.isDefilante = True
            this.noShaman = True
            this.countStats = False
            this.noAutoScore = True

        elif this.roomName.startswith("village"):
            this.isVillage = True
            this.roundTime = 0
            this.never20secTimer = True
            this.autoRespawn = True
            this.countStats = False
            this.noShaman = True
            this.isFixedMap = True

        elif this.roomName in ("801", "*801"):
            this.is801Room = True
            this.roundTime = 0
            this.never20secTimer = True
            this.autoRespawn = True
            this.countStats = False
            this.noShaman = True
            this.isFixedMap = True
        else:
            this.isNormRoom = True

        if this.name.startswith("#"):
            this.minigameSearchName = this.name[1:]

        if this.name.startswith("*#"):
            this.minigameSearchName = this.name[2:]

        this.mapChange()

    def startTimer(this):
        for client in this.clients.values():
            client.sendMapStartTimerEnd()

    def mapChange(this):
    #Unex   
        if this.changeMapTimer:
            try:this.changeMapTimer.cancel()
            except:this.changeMapTimer = None

        if not this.canChangeMap:
            this.changeMapAttemps += 1
            if this.changeMapAttemps < 5:
                this.changeMapTimer = reactor.callLater(1, this.mapChange)
                return

        for timer in this.roomTimers:
            timer.cancel()

        this.roomTimers = []

        if this.voteCloseTimer:
            try:this.voteCloseTimer.cancel()
            except:this.voteCloseTimer = None
        if this.killAfkTimer:
            try:this.killAfkTimer.cancel()
            except:this.killAfkTimer = None
        if this.autoRespawnTimer:
            try:this.autoRespawnTimer.cancel()
            except:this.autoRespawnTimer = None
        if this.startTimerLeft:
            try:this.startTimerLeft.cancel()
            except:this.startTimerLeft = None

        if this.initVotingMode:
            if not this.isVotingBox and (this.mapPerma == 0 and this.mapCode != -1) and this.getPlayerCount() >= 2:
                this.isVotingMode = True
                this.isVotingBox = True
                this.voteCloseTimer = reactor.callLater(8, this.closeVoting)
                for client in this.clients.values():
                    client.sendVoteBox(this.mapName, this.mapYesVotes, this.mapNoVotes)
            else:
                this.votingMode = False
                this.closeVoting()

        elif this.isTribeHouse and this.isTribeHouseMap:
            pass
        else:
            if this.isVotingMode:
                TotalYes = this.mapYesVotes + this.receivedYes
                TotalNo = this.mapNoVotes + this.receivedNo
                isDel = False

                if TotalYes + TotalNo >= 100:
                    TotalVotes = TotalYes + TotalNo
                    Rating = (1.0 * TotalYes / TotalNo) * 100
                    rate = str(Rating).split(".")
                    if int(rate[0]) < 50:
                        isDel = True

                if isDel:
                    this.Cursor.execute("UPDATE MapEditor SET YesVotes = ?, NoVotes = ?, Del = ? WHERE Code = ?", [TotalYes, TotalNo, 1, this.mapCode])
                else:
                    this.Cursor.execute("UPDATE MapEditor SET YesVotes = ?, NoVotes = ? WHERE Code = ?", [TotalYes, TotalNo, this.mapCode])

                this.isVotingMode = False
                this.receivedNo = 0
                this.receivedYes = 0
                for client in this.clients.values():
                    client.qualifiedVoted = False
                    client.isVoted = False

            this.initVotingMode = True

            this.lastCodePartie += 1
            this.lastCodePartie %= 127

            if this.isSurvivor:
                for client in this.clients.values():
                    if not client.isDead and (not client.isVampire if this.isSurvivorVamp else not client.isShaman):
                        if not this.noAutoScore: client.playerScore += 10

            if this.catchTheCheeseMap:
                this.catchTheCheeseMap = False
            else:
                numCom2 = 0

                if this.isDoubleMap:
                    numCom = this.FSnumCompleted - 1
                    numCom2 = this.SSnumCompleted - 1
                else:
                    numCom = this.numCompleted - 1

                if numCom < 0:
                    numCom = 0

                if numCom2 < 0:
                    numCom2 = 0

                player = this.clients.get(this.currentShamanName)
                if player != None:
                    this.sendAll(Identifiers.old.send.Shaman_Perfomance, [this.currentShamanName, numCom])
                    if not this.noAutoScore: player.playerScore = numCom
                    if numCom > 0:
                        player.skillModule.getPlayerExp(True, numCom)

                player2 = this.clients.get(this.currentSecondShamanName)
                if player2 != None:
                    this.sendAll(Identifiers.old.send.Shaman_Perfomance, [this.currentSecondShamanName, numCom2])
                    if not this.noAutoScore: player2.playerScore = numCom2
                    if numCom2 > 0:
                        player2.skillModule.getPlayerExp(True, numCom2)

            if this.isSurvivor and this.getPlayerCount() >= this.server.needToFirst:
                this.giveSurvivorStats()
            elif this.isRacing and this.getPlayerCount() >= this.server.needToFirst:
                this.giveRacingStats()

            this.currentSyncCode = -1
            this.currentSyncName = ""
            this.currentShamanCode = -1
            this.currentSecondShamanCode = -1
            this.currentShamanName = ""
            this.currentSecondShamanName = ""
            this.currentShamanType = -1
            this.currentSecondShamanType = -1
            this.currentShamanSkills = {}
            this.currentSecondShamanSkills = {}
            this.changed20secTimer = False
            this.isDoubleMap = False
            this.isNoShamanMap = False
            this.FSnumCompleted = 0
            this.SSnumCompleted = 0
            this.numCompleted = 0
            this.iceEnabled = False
            this.iceCount = 2
            this.objectID = 0
            this.tempTotemCount = -1
            this.addTime = 0
            this.cloudID = -1
            this.companionBox = -1
            this.lastHandymouse = [-1, -1]
            this.isTribeHouseMap = False
            this.canChangeMap = True
            this.changeMapAttemps = 0

            this.getSyncCode()

            this.anchors = []

            this.mapStatus += 1
            this.mapStatus %= 13
            this.musicMapStatus += 1
            this.musicMapStatus %= 6
            this.survivorMapStatus += 1
            this.survivorMapStatus %= 11

            this.isRacingP17 = not this.isRacingP17
            this.isBootcampP13 = not this.isBootcampP13

            this.currentMap = this.selectMap()
            this.checkVanillaXML()

            if this.currentMap in [44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 138, 139, 140, 141, 142, 143] or this.mapPerma == 8 and this.getPlayerCount() >= 2:
                this.isDoubleMap = True

            if this.mapPerma == 7 or this.isSurvivorVamp:
                this.isNoShamanMap = True

            if this.currentMap in [108, 109, 110, 111, 112, 113]:
                this.catchTheCheeseMap = True

            this.gameStartTime = TFMUtils.getTime()
            this.gameStartTimeMillis = time.time()
            this.isCurrentlyPlay = False

            if not this.isFixedMap:
                this.changeMapTimer = reactor.callLater(this.roundTime, this.mapChange)

            for client in this.clients.values():
                client.resetPlay()

            for client in this.clients.values():
                client.startPlay()
                if client.isHidden:
                    client.sendPlayerDisconnect()

            this.startTimerLeft = reactor.callLater(3, this.startTimer)

            for player in this.clients.values():
                if player.pet != 0:
                    if TFMUtils.getSecondsDiff(player.petEnd) >= 0:
                        player.pet = 0
                        player.petEnd = 0
                    else:
                        this.sendAllBin(Identifiers.send.Consumable_Angel, ByteArray().writeInt(player.playerCode).writeUnsignedByte(player.pet).toByteArray())
            if this.isSurvivorVamp:
                reactor.callLater(5, this.sendVampireMode)

            if this.isMulodrome:
                this.mulodromeRoundCount += 1
                this.sendMulodromeRound()

                if this.mulodromeRoundCount <= 10:
                    for client in this.clients.values():
                        if client.Username in this.blueTeam:
                            this.setNameColor(client.Username, int("979EFF", 16))
                        else:
                            this.setNameColor(client.Username, int("FF9396", 16))
            else:
                this.sendAllBin(Identifiers.send.Mulodrome_End, "")

            if this.isRacing or this.isDefilante:
                this.roundsCount += 1
                this.roundsCount %= 10

                this.sendAllBin(Identifiers.send.Rounds_Count, ByteArray().writeByte(this.roundsCount).writeInt(this.getHighestScore()).toByteArray())

            this.closeRoomRoundJoinTimer = reactor.callLater(3, setattr, this, "isCurrentlyPlay", True)
            this.killAfkTimer = reactor.callLater(30, this.killAfk)

            if this.autoRespawn or this.isTribeHouseMap:
                this.autoRespawnTimer = reactor.callLater(5, this.respawnMice)

    def getPlayerCount(this):
        return len(this.clients.values())

    def getPlayerCountUnique(this):
        ipList = []
        for client in this.clients.values():
            if not client.ipAddress in ipList:
                ipList.append(client.ipAddress)
        return len(ipList)

    def getPlayerList(this):
        result = []
        for client in this.clients.values():
            result.append(client.getPlayerData())
        return result

    def addClient(this, client):
        this.clients[client.Username] = client

        client.room = this
        client.isDead = this.isCurrentlyPlay
        this.sendAllOthers(client, Identifiers.old.send.Player_Respawn, [client.getPlayerData()])
        client.startPlay()

    def removeClient(this, client):
        if client.Username in this.clients:
            del this.clients[client.Username]

            client.resetPlay()
            client.playerScore = 0

            client.sendPlayerDisconnect()

            if this.isMulodrome:
                if client.Username in this.redTeam: this.redTeam.remove(client.Username)
                if client.Username in this.blueTeam: this.blueTeam.remove(client.Username)

                if len(this.redTeam) == 0 and len(this.blueTeam) == 0:
                    this.mulodromeRoundCount = 10
                    this.sendMulodromeRound()

            if len(this.clients) == 0:
                #for timer in [this.autoRespawnTimer, this.changeMapTimer, this.closeRoomRoundJoinTimer, this.endSnowTimer, this.killAfkTimer, this.voteCloseTimer]:
                #    if timer != None:
                #        timer.cancel()
                        
                this.isClosed = True
                del this.server.rooms[this.name]
            else:
                if client.playerCode == this.currentSyncCode:
                    this.currentSyncCode = -1
                    this.currentSyncName = ""
                    this.getSyncCode()
                    for clientOnline in this.clients.values():
                        clientOnline.sendSync(this.currentSyncCode)
                        if clientOnline.playerCode == this.currentSyncCode:
                            clientOnline.isSync = True

                this.checkShouldChangeMap()

    def checkShouldChangeMap(this):
        if this.isBootcamp or this.autoRespawn or this.isTribeHouse and this.isTribeHouseMap or this.isFixedMap:
            pass
        else:
            allDead = True
            for client in this.clients.values():
                if not client.isDead:
                    allDead = False

            if allDead:
                this.mapChange()

    def sendAll(this, Tokens, packet):
        for client in this.clients.values():
            client.sendPacket(Tokens, packet)

    def sendAllOthers(this, senderClient, Tokens, packet):
        for client in this.clients.values():
            if not client == senderClient:
                client.sendPacket(Tokens, packet)

    def sendAllBin(this, Tokens, packet):
        for client in this.clients.values():
            client.sendPacket(Tokens, packet, True)

    def sendAllOthersBin(this, senderClient, Tokens, packet):
        for client in this.clients.values():
            if not client == senderClient:
                client.sendPacket(Tokens, packet, True)

    def sendAllChat(this, playerCode, playerName, message, LangueByte, isOnly):
        p = ByteArray().writeInt(playerCode).writeUTF(playerName).writeByte(LangueByte).writeUTF(message)
        if not isOnly:
            for client in this.clients.values():
                client.sendPacket(Identifiers.send.All_Chat, p.toByteArray(), True)
        else:
            client = this.clients.get(playerName)
            if client != None:
                client.sendPacket(Identifiers.send.All_Chat, p.toByteArray(), True)

    def getSyncCode(this):
        if this.getPlayerCount() > 0:
            if this.currentSyncCode == -1:
                players = this.clients
                values = players.values()
                client = random.choice(values)
                this.currentSyncCode = client.playerCode
                this.currentSyncName = client.Username
        else:
            if this.currentSyncCode == -1:
                this.currentSyncCode = 0
                this.currentSyncName = ""

        return this.currentSyncCode

    def selectMap(this):
        if not this.forceNextMap == "-1":
            force = this.forceNextMap
            this.forceNextMap = "-1"
            this.mapCode = -1

            if force.isdigit():
                return this.selectMapSpecificic(force, "Vanilla")
            elif force.startswith("@"):
                return this.selectMapSpecificic(force[1:], "Custom")
            elif force.startswith("#"):
                return this.selectMapSpecificic(force[1:], "Perm")
            elif force.startswith("<"):
                return this.selectMapSpecificic(force, "Xml")
            else:
                return 0

        elif this.specificMap:
            this.mapCode = -1
            return this.currentMap
        else:
            if this.isEditeur:
                return this.EMapCode

            elif this.isTribeHouse:
                tribeName = this.roomName[2:]
                runMap = this.server.getTribeHouse(tribeName)

                if runMap == 0:
                    this.mapCode = 0
                    this.mapName = "Unex"
                    this.mapXML = "<C><P /><Z><S><S Y=\"360\" T=\"0\" P=\"0,0,0.3,0.2,0,0,0,0\" L=\"800\" H=\"80\" X=\"400\" /></S><D><P Y=\"0\" T=\"34\" P=\"0,0\" X=\"0\" C=\"719b9f\" /><T Y=\"320\" X=\"49\" /><P Y=\"320\" T=\"16\" X=\"224\" P=\"0,0\" /><P Y=\"319\" T=\"17\" X=\"311\" P=\"0,0\" /><P Y=\"284\" T=\"18\" P=\"1,0\" X=\"337\" C=\"57703e,e7c3d6\" /><P Y=\"284\" T=\"21\" X=\"294\" P=\"0,0\" /><P Y=\"134\" T=\"23\" X=\"135\" P=\"0,0\" /><P Y=\"320\" T=\"24\" P=\"0,1\" X=\"677\" C=\"46788e\" /><P Y=\"320\" T=\"26\" X=\"588\" P=\"1,0\" /><P Y=\"193\" T=\"14\" P=\"0,0\" X=\"562\" C=\"95311e,bde8f3,faf1b3\" /></D><O /></Z></C>"
                    this.mapYesVotes = 0
                    this.mapNoVotes = 0
                    this.mapPerma = 22
                    this.mapDel = 0
                else:
                    run = this.selectMapSpecificic(runMap, "Custom")
                    if run != -1:
                        this.mapCode = 0
                        this.mapName = "Unex"
                        this.mapXML = "<C><P /><Z><S><S Y=\"360\" T=\"0\" P=\"0,0,0.3,0.2,0,0,0,0\" L=\"800\" H=\"80\" X=\"400\" /></S><D><P Y=\"0\" T=\"34\" P=\"0,0\" X=\"0\" C=\"719b9f\" /><T Y=\"320\" X=\"49\" /><P Y=\"320\" T=\"16\" X=\"224\" P=\"0,0\" /><P Y=\"319\" T=\"17\" X=\"311\" P=\"0,0\" /><P Y=\"284\" T=\"18\" P=\"1,0\" X=\"337\" C=\"57703e,e7c3d6\" /><P Y=\"284\" T=\"21\" X=\"294\" P=\"0,0\" /><P Y=\"134\" T=\"23\" X=\"135\" P=\"0,0\" /><P Y=\"320\" T=\"24\" P=\"0,1\" X=\"677\" C=\"46788e\" /><P Y=\"320\" T=\"26\" X=\"588\" P=\"1,0\" /><P Y=\"193\" T=\"14\" P=\"0,0\" X=\"562\" C=\"95311e,bde8f3,faf1b3\" /></D><O /></Z></C>"
                        this.mapYesVotes = 0
                        this.mapNoVotes = 0
                        this.mapPerma = 22
                        this.mapDel = 0

            elif this.is801Room:
                return this.getMap801("801", "801", 801, "_Atelier 801")

            elif this.isVillage:
                return this.getMap801("801", "801", 801, "_Village")

            elif this.isVanilla:
                this.mapCode = -1
                this.mapName = "Invalid";
                this.mapXML = "<C><P /><Z><S /><D /><O /></Z></C>"
                this.mapYesVotes = 0
                this.mapNoVotes = 0
                this.mapPerma = -1
                this.mapDel = 0
                map = random.choice(this.MapList)
                while map == this.currentMap:
                    map = random.choice(this.MapList)
                return map
                
            else:
                this.mapCode = -1
                this.mapName = "Invalid";
                this.mapXML = "<C><P /><Z><S /><D /><O /></Z></C>"
                this.mapYesVotes = 0
                this.mapNoVotes = 0
                this.mapPerma = -1
                this.mapDel = 0
                return this.selectMapStatus(this.mapStatus)
        return -1

    def selectMapStatus(this, mapStatus):
        customMaps = [1, 2, 3, 5, 6, 7, 9, 10, 11]                
        mapList = []

        if this.isVanilla:
            map = random.choice(this.MapList)
            while map == this.currentMap:
                map = random.choice(this.MapList)
            return map

        elif this.isMusic:
            if this.musicMapStatus == 5:
                this.Cursor.execute("select Code from MapEditor where Perma = 19")
                r = this.Cursor.fetchall()
                for rs in r:
                    mapList.append(rs[0])

        elif this.isRacing:
            P7List = []
            P17List = []

            this.Cursor.execute("select Code, Perma from MapEditor where Perma = 7 or Perma = 17")
            r = this.Cursor.fetchall()
            for rs in r:
                perma = rs[1]
                if perma == 7:
                    P7List.append(rs[0])
                else:
                    P17List.append(rs[0])

            if this.isRacingP17 or this.isMulodrome:
                mapList = P7List if len(P17List) == 0 else P17List
            else:
                mapList = P17List if len(P7List) == 0 else P7List

        elif this.isBootcamp:
            P3List = []
            P13List = []

            this.Cursor.execute("select Code, Perma from MapEditor where Perma = 3 or Perma = 13")
            r = this.Cursor.fetchall()
            for rs in r:
                perma = rs[1]
                if perma == 3:
                    P3List.append(rs[0])
                else:
                    P13List.append(rs[0])

            if this.isBootcampP13:
                mapList = P3List if len(P13List) == 0 else P13List
            else:
                mapList = P13List if len(P3List) == 0 else P3List

        elif this.isSurvivor:
            this.isSurvivorVamp = this.survivorMapStatus >= 10

            this.Cursor.execute("select Code from MapEditor where Perma = ?", [11 if this.isSurvivorVamp else 10])
            r = this.Cursor.fetchall()
            for rs in r:
                mapList.append(rs[0])

        elif this.isDefilante:
            this.Cursor.execute("select Code from MapEditor where Perma = 18")
            r = this.Cursor.fetchall()
            for rs in r:
                mapList.append(rs[0])

        elif this.is801Room:
            return 801
            
        elif this.isVillage:
            return Village
        elif mapStatus in customMaps:
            multiple = False
            selectCode = 0

            if mapStatus == 1 or mapStatus == 9:
                multiple = True
            elif mapStatus == 2:
                selectCode = 5
            elif mapStatus == 3:
                selectCode = 9
            elif mapStatus == 5 or mapStatus >= 10:
                selectCode = 6
            elif mapStatus == 6:
                selectCode = 7
            elif mapStatus == 7:
                selectCode = 8
            elif mapStatus >= 10:
                selectCode = 4

            if multiple:
                this.Cursor.execute("select Code from MapEditor where Perma = 0")
                r = this.Cursor.fetchall()
                for rs in r:
                    mapList.append(rs[0])

                this.Cursor.execute("select Code from MapEditor where Perma = 1")
                r = this.Cursor.fetchall()
                for rs in r:
                    mapList.append(rs[0])
            else:
                this.Cursor.execute("select Code from MapEditor where Perma = ?", [selectCode])
                r = this.Cursor.fetchall()
                for rs in r:
                    mapList.append(rs[0])
        else:
            map = random.choice(this.MapList)
            while map == this.currentMap:
                map = random.choice(this.MapList)
            return map

        if len(mapList) >= 1:
            runMap = random.choice(mapList)
        else:
            runMap = 0

        if len(mapList) >= 2:
            while runMap == this.currentMap:
                runMap = random.choice(mapList)

        if runMap == 0:
            map = random.choice(this.MapList)
            while map == this.currentMap:
                map = random.choice(this.MapList)
            return map
        else:
            mapInfo = this.getMapInfo(runMap)
            this.mapCode = runMap
            this.mapName = str(mapInfo[0])
            this.mapXML = str(mapInfo[1])
            this.mapYesVotes = int(mapInfo[2])
            this.mapNoVotes = int(mapInfo[3])
            this.mapPerma = int(mapInfo[4])
            this.mapDel = int(mapInfo[5])
            return -1

    def selectMapSpecificic(this, code, type):
        if type == "Vanilla":
            return int(code)

        elif type == "Custom":
            mapInfo = this.getMapInfo(int(code))
            if mapInfo[0] == None:
                return 0
            else:
                this.mapCode = int(code)
                this.mapName = str(mapInfo[0])
                this.mapXML = str(mapInfo[1])
                this.mapYesVotes = int(mapInfo[2])
                this.mapNoVotes = int(mapInfo[3])
                this.mapPerma = int(mapInfo[4])
                this.mapDel = int(mapInfo[5])
                return -1

        elif type == "Perm":
            mapList = []
            this.Cursor.execute("SELECT Code FROM MapEditor WHERE Perma = ?", [int(str(code))])
            r = this.Cursor.fetchall()
            for rs in r:
                mapList.append(rs["Code"])

            if len(mapList) >= 1:
                runMap = random.choice(mapList)
            else:
                runMap = 0

            if len(mapList) >= 2:
                while runMap == this.currentMap:
                    runMap = random.choice(mapList)

            if runMap == 0:
                map = random.choice(this.MapList)
                while map == this.currentMap:
                    map = random.choice(this.MapList)
                return map
            else:
                mapInfo = this.getMapInfo(runMap)
                this.mapCode = runMap
                this.mapName = str(mapInfo[0])
                this.mapXML = str(mapInfo[1])
                this.mapYesVotes = int(mapInfo[2])
                this.mapNoVotes = int(mapInfo[3])
                this.mapPerma = int(mapInfo[4])
                this.mapDel = int(mapInfo[5])
                return -1

        elif type == "Xml":
            this.mapCode = 0
            this.mapName = "#Module"
            this.mapXML = str(code)
            this.mapYesVotes = 0
            this.mapNoVotes = 0
            this.mapPerma = 22
            this.mapDel = 0
            return -1

    def getMapInfo(this, mapCode):
        mapInfo = ["", "", 0, 0, 0, 0]
        this.Cursor.execute("SELECT Name, XML, YesVotes, NoVotes, Perma, Del FROM MapEditor WHERE Code = ?", [mapCode])
        rs = this.Cursor.fetchone()
        if rs:
            mapInfo = rs["Name"], rs["XML"], rs["YesVotes"], rs["NoVotes"], rs["Perma"], rs["Del"]

        return mapInfo

    def checkDeathCount(this):
        counts = [0, 0]
        for client in this.clients.values():
            counts[0 if client.isDead else 1] += 1
        return counts

    def checkDeathCountNoShaman(this):
        count = 0
        for client in this.clients.values():
            if not client.isShaman and client.isDead and not client.isNewPlayer:
                count += 1
        return count

    def getHighestScore(this):
        scores = []

        for client in this.clients.values():
            scores.append(client.playerScore)

        try:
            for client in this.clients.values():
                if client.playerScore == max(scores):
                    return client.playerCode
        except:
            pass
        return 0

    def getSecondHighestScore(this):
        scores = []

        for client in this.clients.values():
            scores.append(client.playerScore)

        scores.remove(max(scores))

        try:
            for client in this.clients.values():
                if client.playerScore == max(scores):
                    return client.playerCode
        except:
            pass
        return 0

    def getShamanCode(this):
        if this.currentShamanCode == -1:
            if this.currentMap in this.noShamanMaps or this.isNoShamanMap:
                pass
            elif this.noShaman or this.survivorMapStatus == 7 and this.isSurvivor:
                pass
            else:
                if this.forceNextShaman > 0:
                    this.currentShamanCode = this.forceNextShaman
                    this.forceNextShaman = 0
                else:
                    this.currentShamanCode = this.getHighestScore()

            if this.currentShamanCode == -1:
                this.currentShamanName = ""
            else:
                for client in this.clients.values():
                    if client.playerCode == this.currentShamanCode:
                        this.currentShamanName = client.Username
                        this.currentShamanType = client.shamanType
                        this.currentShamanSkills = client.playerSkills
                        break
        return this.currentShamanCode

    def getDoubleShamanCode(this):
        if this.currentShamanCode == -1 and this.currentSecondShamanCode == -1:

            if this.forceNextShaman > 0:
                this.currentShamanCode = this.forceNextShaman
                this.forceNextShaman = 0
            else:
                this.currentShamanCode = this.getHighestScore()

            if this.currentSecondShamanCode == -1:
                this.currentSecondShamanCode = this.getSecondHighestScore()

            if this.currentSecondShamanCode == this.currentShamanCode:
                values = this.clients.values()
                tempClient = random.choice(values)
                this.currentSecondShamanCode = tempClient.playerCode

            for client in this.clients.values():
                if client.playerCode == this.currentShamanCode:
                    this.currentShamanName = client.Username
                    this.currentShamanType = client.shamanType
                    this.currentShamanSkills = client.playerSkills
                    break

            for client in this.clients.values():
                if client.playerCode == this.currentSecondShamanCode:
                    this.currentSecondShamanName = client.Username
                    this.currentSecondShamanType = client.shamanType
                    this.currentSecondShamanSkills = client.playerSkills
                    break

        return [this.currentShamanCode, this.currentSecondShamanCode]

    def closeVoting(this):
        this.initVotingMode = False
        this.isVotingBox = False
        this.mapChange()

    def killAllNoDie(this):
        for client in this.clients.values():
            if not client.isDead:
                client.isDead = True
        this.checkShouldChangeMap()

    def killAll(this):
        for client in this.clients.values():
            if not client.isDead:
                client.sendPlayerDied()
                client.isDead = True
        this.checkShouldChangeMap()

    def killAfk(this):
        if this.isEditeur or this.isTotemEditeur or this.isBootcamp or this.isTribeHouseMap or this.disableAfkKill:
            pass
        else:
            if ((TFMUtils.getTime() - this.gameStartTime) < 32 and (TFMUtils.getTime() - this.gameStartTime) > 28):
                for client in this.clients.values():
                    if not client.isDead and client.isAfk:
                        client.isDead = True
                        if not this.noAutoScore: client.playerScore += 1
                        client.sendPlayerDied()
                this.checkShouldChangeMap()

    def checkIfDoubleShamansAreDead(this):
        client1 = this.clients.get(this.currentShamanName)
        client2 = this.clients.get(this.currentSecondShamanName)
        return (False if client1 == None else client1.isDead) and (False if client2 == None else client2.isDead)

    def checkIfShamanIsDead(this):
        client = this.clients.get(this.currentShamanName)
        return False if client == None else client.isDead

    def checkIfTooFewRemaining(this):
        count = 0
        for client in this.clients.values():
            if not client.isDead:
                count += 1

        if this.getPlayerCount() >= 3:
            if count <= 2:
                return True
        return False

    def checkIfShamanCanGoIn(this):
        for client in this.clients.values():
            if client.playerCode != this.currentShamanCode:
                if not client.isDead:
                    return False
        return True

    def checkIfDoubleShamanCanGoIn(this):
        for client in this.clients.values():
            if client.playerCode != this.currentShamanCode and client.playerCode != this.currentSecondShamanCode:
                if not client.isDead:
                    return False
        return True

    def giveShamanSave(this, shamanName, type):
        if not this.countStats:
            return

        client = this.clients.get(shamanName)
        if client != None:
            if type == 0:
                client.shamanSaves += 1
            elif type == 1:
                client.hardModeSaves += 1
            elif type == 2:
                client.divineModeSaves += 1

            if client.privLevel != 0:
                counts = [client.shamanSaves, client.hardModeSaves, client.divineModeSaves]
                checks = [this.server.ShamanTitleListCheck, this.server.HardModeTitleListCheck, this.server.DivineModeTitleListCheck]
                titles = [this.server.ShamanTitleList, this.server.HardModeTitleList, this.server.DivineModeTitleList]
                rebuilds = ["shaman", "hardmode", "divinemode"]

                if counts[type] in checks[type]:
                    unlockedTitle = titles[type][counts[type]]
                    stitle = str(unlockedTitle).split(".")

                    client.checkAndRebuildTitleList(rebuilds[type])
                    client.sendUnlockedTitle(stitle[0], stitle[1])

                    client.sendCompleteTitleList()
                    client.sendTitleList()

    def respawnMice(this):
        for client in this.clients.values():
            if client.isDead:
                client.isDead = False
                client.playerStartTime = TFMUtils.getTime()
                client.playerStartTimeMillis = time.time()
                this.sendAll(Identifiers.old.send.Player_Respawn, [client.getPlayerData(), 0 if this.isBootcamp else 1])

        if this.autoRespawn or this.isTribeHouseMap:
            this.autoRespawnTimer = reactor.callLater(5, this.respawnMice)

    def respawnSpecific(this, playerName):
        client = this.clients.get(playerName)
        if client != None and client.isDead:
            client.resetPlay()
            client.isAfk = False
            client.playerStartTime = TFMUtils.getTime()
            client.playerStartTimeMillis = time.time()
            this.sendAll(Identifiers.old.send.Player_Respawn, [client.getPlayerData(), 0 if this.isBootcamp else 1])

    def sendMulodromeRound(this):
        this.sendAllBin(Identifiers.send.Mulodrome_Result, ByteArray().writeByte(this.mulodromeRoundCount).writeShort(this.blueCount).writeShort(this.redCount).toByteArray())
        if this.mulodromeRoundCount > 10:
            this.sendAllBin(Identifiers.send.Mulodrome_End, "")
            this.sendAllBin(Identifiers.send.Mulodrome_Winner, ByteArray().writeByte(2 if this.blueCount == this.redCount else (1 if this.blueCount < this.redCount else 0)).writeShort(this.blueCount).writeShort(this.redCount).toByteArray())
            this.isMulodrome = False
            this.mulodromeRoundCount = 0
            this.redCount = 0
            this.blueCount = 0
            this.redTeam = []
            this.blueTeam = []
            this.isRacing = False
            this.mapStatus = 1
            this.never20secTimer = False
            this.noShaman = False

    def checkVanillaXML(this):
        if os.path.exists("./maps/"+str(this.currentMap)+".xml"):
            FileXML = open("./maps/"+str(this.currentMap)+".xml")
            XML = FileXML.read()
            FileXML.close()

            this.mapCode = int(this.currentMap)
            this.mapName = "Transformice"
            this.mapXML = str(XML)
            this.mapYesVotes = 0
            this.mapNoVotes = 0
            this.mapPerma = 2
            this.mapDel = 0
            this.currentMap = -1
 
    def getMap801(this, prefix, map, code, name):
        try:
            with open("./maps/801.xml", "r") as f:
                XML = f.read()
                f.close()

                this.mapCode = code
                this.mapName = name
                this.mapXML = str(XML)
                this.mapYesVotes = 0
                this.mapNoVotes = 0
                this.mapPerma = 41
                this.currentMap = -1
                this.mapInverted = False
        except: pass
            
    def sendVampireMode(this):
        client = this.clients.get(this.currentSyncName)
        if client != None:
            client.sendVampireMode(False)

    def bindKeyBoard(this, playerName, key, down, yes):
        client = this.clients.get(playerName)
        if client != None:
            client.sendPacket(Identifiers.send.Bind_Key_Board, ByteArray().writeShort(key).writeBool(down).writeBool(yes).toByteArray(), True)

    def chatMessage(this, message, playerName):
        p = ByteArray().writeUTF(message)
        if playerName == "":
            this.sendAllBin(Identifiers.send.Message, p.toByteArray())
        else:
            client = this.clients.get(playerName)
            if client != None:
                client.sendPacket(Identifiers.send.Message, p.toByteArray(), True)
                
    def movePlayer(this, playerName, xPosition, yPosition, pOffSet, xSpeed, ySpeed, sOffSet):
        client = this.clients.get(playerName)
        if client != None:
            client.sendPacket(Identifiers.send.Move_Player, ByteArray().writeShort(xPosition).writeShort(yPosition).writeBool(pOffSet).writeShort(xSpeed).writeShort(ySpeed).writeBool(sOffSet).toByteArray(), True)

    def removeObject(this, objectId):
        this.sendAllBin(Identifiers.send.Remove_Object, ByteArray().writeInt(objectId).writeBool(True).toByteArray())

    def setNameColor(this, playerName, color):
        if this.clients.has_key(playerName):
            this.sendAllBin(Identifiers.send.Set_Name_Color, ByteArray().writeInt(this.clients.get(playerName).playerCode).writeInt(color).toByteArray())

    def setPlayerScore(this, playerCode, score):
        this.sendAllBin(Identifiers.send.Set_Player_Score, ByteArray().writeInt(playerCode).writeShort(score).toByteArray())

    def setUIMapName(this, text):
        this.sendAllBin(Identifiers.send.Set_UI_Map_Name, ByteArray().writeUTF(text).toByteArray())

    def setUIShamanName(this, text):
        this.sendAllBin(Identifiers.send.Set_UI_Shaman_Name, ByteArray().writeUTF(text).toByteArray())

    def bindMouse(this, playerName, yes):
        client = this.clients.get(playerName)
        if client != None:
            client.sendPacket(Identifiers.send.Bind_Mouse, ByteArray().writeBool(yes).toByteArray(), True)

    def addPopup(this, id, type, text, targetPlayer, x, y, width, fixedPos):
        p = ByteArray().writeInt(id).witeByte(type).witeUTF(text).writeShort(x).writeShort(y).writeShort(width).writeBool(fixedPos)
        if targetPlayer == "":
            this.sendAllBin(Identifiers.send.Add_Popup, p.toByteArray())
        else:
            client = this.clients.get(targetPlayer)
            if client != None:
                client.sendPacket(Identifiers.send.Add_Popup, p.toByteArray(), True)

    def addTextArea(this, id, text, targetPlayer, x, y, width, height, backgroundColor, borderColor, backgroundAlpha, fixedPos):
        p = ByteArray().writeInt(id).writeUTF(text).writeShort(x).writeShort(y).writeShort(width).writeShort(height).writeInt(backgroundColor).writeInt(borderColor).writeByte(100 if backgroundAlpha > 100 else backgroundAlpha).writeBool(fixedPos)
        if targetPlayer == "":
            this.sendAllBin(Identifiers.send.Add_Text_Area, p.toByteArray())
        else:
            client = this.clients.get(targetPlayer)
            if client != None:
                client.sendPacket(Identifiers.send.Add_Text_Area, p.toByteArray(), True)

    def removeTextArea(this, id, targetPlayer):
        p = ByteArray().writeInt(id)
        if targetPlayer == "":
            this.sendAllBin(Identifiers.send.Remove_Text_Area, p.toByteArray())
        else:
            client = this.clients.get(targetPlayer)
            if client != None:
                client.sendPacket(Identifiers.send.Remove_Text_Area, p.toByteArray(), True)

    def updateTextArea(this, id, text, targetPlayer):
        p = ByteArray().writeInt(id).writeUTF(text)
        if targetPlayer == "":
            this.sendAllBin(Identifiers.send.Update_Text_Area, p.toByteArray())
        else:
            client = this.clients.get(targetPlayer)
            if client != None:
                client.sendPacket(Identifiers.send.Update_Text_Area, p.toByteArray(), True)

    def startSnow(this, millis, power, enabled):
        this.isSnowing = enabled
        this.sendAllBin(Identifiers.send.Snow, ByteArray().writeBool(enabled).writeShort(power).toByteArray())
        if enabled:
            this.endSnowTimer = reactor.callLater(millis, lambda: this.startSnowSchedule(power))

    def giveSurvivorStats(this):
        for client in this.clients.values():
            if not client.isNewPlayer:
                client.survivorStats[0] += 1
                if client.isShaman:
                    client.survivorStats[1] += 1
                    client.survivorStats[2] += this.getDeathCountNoShaman()
                elif not client.isDead:
                    client.survivorStats[3] += 1

                if client.survivorStats[0] >= 100 and not str(120) in client.shopBadges:
                    client.shopModule.sendUnlockedBadge(str(120))
                    client.shopBadges.append(str(120))

                if client.survivorStats[1] >= 100 and not str(121) in client.shopBadges:
                    client.shopModule.sendUnlockedBadge(str(121))
                    client.shopBadges.append(str(121))

                if client.survivorStats[2] >= 100 and not str(122) in client.shopBadges:
                    client.shopModule.sendUnlockedBadge(str(122))
                    client.shopBadges.append(str(122))

                if client.survivorStats[3] >= 100 and not str(123) in client.shopBadges:
                    client.shopModule.sendUnlockedBadge(str(123))
                    client.shopBadges.append(str(123))
                    
    def giveRacingStats(this):
        for client in this.clients.values():
            if not client.isNewPlayer:
                client.racingStats[0] += 1
                if client.hasCheese or client.hasEnter:
                    client.racingStats[1] += 1

                if client.hasEnter:
                    if client.currentPlace <= 3:
                        client.racingStats[2] += 1

                    if client.currentPlace == 1:
                        client.racingStats[3] += 1

                if client.racingStats[0] >= 100 and not str(124) in client.shopBadges:
                    client.shopModule.sendUnlockedBadge(str(124))
                    client.shopBadges.append(str(124))

                if client.racingStats[1] >= 100 and not str(125) in client.shopBadges:
                    client.shopModule.sendUnlockedBadge(str(125))
                    client.shopBadges.append(str(125))

                if client.racingStats[2] >= 100 and not str(127) in client.shopBadges:
                    client.shopModule.sendUnlockedBadge(str(127))
                    client.shopBadges.append(str(127))

                if client.racingStats[3] >= 100 and not str(126) in client.shopBadges:
                    client.shopModule.sendUnlockedBadge(str(126))
                    client.shopBadges.append(str(126))

    def send20SecRemainingTimer(this):
        if not this.changed20secTimer:
            this.changed20secTimer = True
            calc = this.roundTime + (this.gameStartTime - TFMUtils.getTime())

            if this.never20secTimer or calc < 21 or this.roundTime == 0 or this.isEditeur:
                pass
            else:
                this.sendAll(Identifiers.send.Time_20Sec, [])
                if this.changeMapTimer != None: this.changeMapTimer.cancel()
                this.changeMapTimer = reactor.callLater(20, this.mapChange)
                for client in this.clients.values():
                    client.sendRoundTime(20)

    def changeMapTimers(this, seconds):
        if this.changeMapTimer != None: this.changeMapTimer.cancel()
        this.changeMapTimer = reactor.callLater(seconds, this.mapChange)

    def newConsumableTimer(this, objectID):
        this.roomTimers.append(reactor.callLater(10, lambda: this.removeObject(objectID)))

if __name__ == "__main__":
    # Connection Settings
    Config = ConfigParser.ConfigParser()
    Config.read("./config.ini")

    # Connection Database
    Database, Cursor = None, None
    Database = sqlite3.connect("./data/database.db", check_same_thread = False)
    Database.text_factory = str
    Database.isolation_level = None
    Database.row_factory = sqlite3.Row
    Cursor = Database.cursor()

    # Connection Server
    os.system("title Transformice v1.373")
    os.system('color fc')
    validPorts = []
    TFM = Server()
    for port in [443, 44440, 44444, 5555, 3724, 6112]:
        try:
            reactor.listenTCP(port, TFM)
            validPorts.append(port)
        except:
            print "Ports Remaining: " + str(port)

    if not validPorts == []:
        print "Server RUNNING... PORTS " + str(validPorts)
    threading.Thread(target=reactor.run(), args=(False,)).start()
