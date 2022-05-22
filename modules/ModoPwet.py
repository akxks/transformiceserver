from ByteArray import ByteArray
from Identifiers import Identifiers

class ModoPwet:
    def __init__(this, player, server):
        this.client = player
        this.server = player.server

    def checkReport(this, array, playerName):
        return playerName in array

    def makeReport(this, playerName, type, comments):
        playerName = this.client.TFMUtils.parsePlayerName(playerName)
        this.server.sendModMessage(7, "<br>[<V>Report <BL>]<br>New Report: User reported: [<J>"+playerName+"<BL>]<br><J>PRESS <font color='#ffffff'>M</font> <J>TO SEE<BL>")

        if this.checkReport(this.server.reports["names"], playerName):
            this.server.reports[playerName]["types"].append(str(type))
            this.server.reports[playerName]["reporters"].append(this.client.Username)
            this.server.reports[playerName]["comments"].append(comments)
        else:
            this.server.reports["names"] = [playerName]
            this.server.reports[playerName] = {}
            this.server.reports[playerName]["types"] = [str(type)]
            this.server.reports[playerName]["reporters"] = [this.client.Username]
            this.server.reports[playerName]["comments"] = [comments]
            this.server.reports[playerName]["status"] = "online" if this.server.checkConnectedAccount(playerName) else "disconnected"
            this.server.reports[playerName]["langue"] = this.getModopwetLangue(playerName)

        this.updateModoPwet()
        this.client.sendBanConsideration()

    def getModopwetLangue(this, playerName):
        player = this.server.players.get(playerName)
        return player.Langue if player != None else "en"

    def updateModoPwet(this):
        for player in this.server.players.values():
            if player.modoPwet and player.privLevel >= 7:
                player.ModoPwet.openModoPwet()

    def getPlayerRoomName(this, playerName):
        player = this.server.players.get(playerName)
        return player.roomName if player != None else "0"

    def getProfileCheeseCount(this, playerName):
        player = this.server.players.get(playerName)
        return player.cheeseCount if player != None else 0

    def openModoPwet(this):
        if len(this.server.reports["names"]) <= 0:
            this.client.sendPacket(Identifiers.send.Open_Modopwet, chr(0), True)
        else:
            reports = 0
            totalReports = len(this.server.reports["names"])
            count = 0

            bannedList = {}
            deletedList = {}
            disconnectList = []

            p = ByteArray()

            while reports < totalReports:
                playerName = this.server.reports["names"][reports]
                reports += 1
                if this.client.modoPwetLangue == "all" or this.server.reports[playerName]["langue"] == this.client.modoPwetLangue.upper():
                    count += 1
                    if count > 255:
                        break

                    p.writeByte(count).writeUTF(this.server.reports[playerName]["langue"].upper()).writeUTF(playerName).writeUTF(this.getPlayerRoomName(playerName)).writeInt(this.getProfileCheeseCount(playerName))

                    reporters = 0
                    totalReporters = len(this.server.reports[playerName]["types"])
                    p.writeByte(totalReporters)

                    while reporters < totalReporters:
                        p.writeUTF(this.server.reports[playerName]["reporters"][reporters]).writeShort(this.getProfileCheeseCount(this.server.reports[playerName]["reporters"][reporters])).writeUTF(this.server.reports[playerName]["comments"][reporters]).writeByte(this.server.reports[playerName]["types"][reporters]).writeShort(reporters)
                        reporters += 1

                    if this.server.reports[playerName]["status"] == "banned":
                        x = {}
                        x["banhours"] = this.server.reports[playerName]["banhours"]
                        x["banreason"] = this.server.reports[playerName]["banreason"]
                        x["bannedby"] = this.server.reports[playerName]["bannedby"]
                        bannedList[playerName] = x

                    if this.server.reports[playerName]["status"] == "deleted":
                        x = {}
                        x["deletedby"] = this.server.reports[playerName]["deletedby"]
                        deletedList[playerName] = x

                    if this.server.reports[playerName]["status"] == "disconnected":
                        disconnectList.append(playerName)

            this.client.sendPacket(Identifiers.send.Open_Modopwet, ByteArray().writeByte(count).writeBytes(p.toByteArray()).toByteArray(), True)

    def changeReportStatusDisconnect(this, playerName):
        this.client.sendPacket(Identifiers.send.Modopwet_Disconnected, ByteArray().writeUTF(playerName).toByteArray(), True)

    def changeReportStatusDeleted(this, playerName, deletedby):
        this.client.sendPacket(Identifiers.send.Modopwet_Deleted, ByteArray().writeUTF(playerName).writeUTF(deletedby).toByteArray(), True)

    def changeReportStatusBanned(this, playerName, banhours, banreason, bannedby):
        this.client.sendPacket(Identifiers.send.Modopwet_Banned, ByteArray().writeUTF(playerName).writeUTF(bannedby).writeInt(int(banhours)).writeUTF(banreason).toByteArray(), True)

    def openChatLog(this, playerName):
        p = ByteArray().writeUTF(playerName).writeByte(len(this.server.chatMessages[playerName]) * 2 if this.server.chatMessages.has_key(playerName) else 0)

        if this.server.chatMessages.has_key(playerName):
            for message in this.server.chatMessages[playerName]:
                p.writeUTF(message[0]).writeUTF(message[1])
                        
        this.client.sendPacket(Identifiers.send.Modopwet_Chatlog, p.toByteArray(), True)
