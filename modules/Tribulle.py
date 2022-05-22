# -*- coding: cp1252 -*-
import time, re

from ByteArray import ByteArray
from Identifiers import Identifiers

class Tribulle:
    def __init__(this, player, server):
        this.client = player
        this.server = player.server
        this.Cursor = player.Cursor

        this.TRIBE_RANKS = "2000060|${trad#tribu.memb}|6|0,0,0,0,0,0,0,0,0,0,0|0;2000070|${trad#tribu.nouv}|7|0,0,0,0,0,0,0,0,0,0,0|1;2000030|${trad#TG_7}|3|0,0,1,0,0,1,0,1,1,1,0|0;2000040|${trad#TG_6}|4|0,0,0,0,0,1,0,1,0,1,0|0;2000050|${trad#TG_4}|5|0,0,0,0,0,1,0,0,0,0,0|0;2000010|${trad#tribu.chef}|1|0,1,1,1,1,1,1,1,1,1,1|1;2000020|${trad#TG_8}|2|0,0,1,1,1,1,1,1,1,1,1|0";
        this.GAME_MODE = 4
        this.MAX_FRIENDS = 200
        this.PLAYER_NAME_LEN = 20
        this.TRIBE_CHEESES = 500
        this.MAX_TRIBE_MEMBERS = 1000
        this.SUCESS = 0
        this.ALREADY_IN_TRIBE = 1
        this.USER_NOT_CONNECTED = 2
        this.INVALID_NAME = 3
        this.NAME_UNAVAILABLE = 4
        this.ALREADY_FRIEND = 5
        this.NOT_FRIEND = 6
        this.ALREADY_IN_BLACK_LIST = 8
        this.NOT_IN_BLACK_LIST = 9
        this.INTERNAL_ERROR = 11
        this.RECIPIENT_INVALID = 12
        this.ALREADY_THIS_CHANNEL = 15
        this.MAX_REACHED = 18
        this.PROHIBITED = 20
        this.INVALID_TRIBE = 21
        this.ENOUGH_MONEY = 22
        this.USER_ALREADY_MARRIED = 29
        this.USER_DIVORCE = 32
        this.RECIPIENT_ALREADY_MARRIED = 31
        this.RECIPIENT_DIVORCE = 32

    def getString(this, text, length):
        return str(text).ljust(int(length), chr(0)).encode("UTF-8")

    def getTime(this):
        return int(time.time()/60)

    def sendPacket(this, code, result):
        p = ByteArray()
        p.writeShort(code)
        p.write(result)
        this.client.sendPacket(Identifiers.send.Tribulle, p.toByteArray(), True)
        if this.server.VERBOSE:
            this.server.sendOutput("Tribulle SEND: "+str(code)+" : "+repr(result))
                    
    def sendPacketToPlayer(this, playerName, code, result):
        player = this.server.players.get(playerName)
        if player != None:
            player.tribulle.sendPacket(code, result)

    def sendPacketWholeTribe(this, code, result, all=False):
        for player in this.server.players.values():
            if player.playerCode != this.client.playerCode or all:
                if player.tribeCode == this.client.tribeCode:
                    player.tribulle.sendPacket(code, result)

    def sendPacketWholeChat(this, chatID, code, result, all=False):
        for player in this.server.players.values():
            if player.playerCode != this.client.playerCode or all:
                if chatID in player.chats:
                    player.tribulle.sendPacket(code, result)

    def updateTribeData(this):
        tribeData = this.server.getTribeInfo(this.client.tribeCode)
        for player in this.server.players.values():
            if player.tribeCode == this.client.tribeCode:
                player.tribeData = tribeData

    def parseTribulleCode(this, code, packet): 
        if code == Identifiers.tribulle.recv.ST_ListeAmis:
            this.sendFriendList(packet[2:])
        elif code == Identifiers.tribulle.recv.ST_AjoutAmi:
            this.addFriend(packet[2:])
        elif code == Identifiers.tribulle.recv.ST_RetireAmi:
            this.removeFriend(packet[2:])
        elif code == Identifiers.tribulle.recv.ST_AjoutListeNoire:
            this.ignorePlayer(packet[2:])
        elif code == Identifiers.tribulle.recv.ST_RetireListeNoire:
            this.removeIgnore(packet[2:])
        elif code == Identifiers.tribulle.recv.ST_EnvoitMessagePrive:
            this.whisperMessage(packet[2:])
        elif code == Identifiers.tribulle.recv.ST_DefinitModeSilence:
            this.disableWhispers(packet[2:])
        elif code == Identifiers.tribulle.recv.ST_ChangerDeGenre:
            this.changeGender(packet[2:])
        elif code == Identifiers.tribulle.recv.ST_DemandeEnMariage:
            this.marriageInvite(packet[2:])
        elif code == Identifiers.tribulle.recv.ST_RepondDemandeEnMariage:
            this.marriageAnswer(packet[2:])
        elif code == Identifiers.tribulle.recv.ST_DemandeDivorce:
            this.marriageDivorce(packet[2:])
        elif code == Identifiers.tribulle.recv.ST_DemandeInformationsTribu:
            this.sendTribeInfo(packet[2:], True)
        elif code == Identifiers.tribulle.recv.ST_DemandeMembresTribu:
            this.sendTribeList(packet[2:])
        elif code == Identifiers.tribulle.recv.ST_CreerTribu:
            this.createTribe(packet[2:])
        elif code == Identifiers.tribulle.recv.ST_InviterMembre:
            this.tribeInvite(packet[2:])
        elif code == Identifiers.tribulle.recv.ST_RepondInvitationTribu:
            this.tribeInviteAnswer(packet[2:])
        elif code == Identifiers.tribulle.recv.ST_ChangerMessageJour:
            this.changeTribeMessage(packet[2:])
        elif code == Identifiers.tribulle.recv.ST_ChangerCodeMaisonTFM:
            this.changeTribeCode(packet[2:])
        elif code == Identifiers.tribulle.recv.ST_AjouterRang:
            this.createNewTribeRank(packet[2:])
        elif code == Identifiers.tribulle.recv.ST_SupprimerRang:
            this.deleteTribeRank(packet[2:])
        elif code == Identifiers.tribulle.recv.ST_RenommerRang:
            this.renameTribeRank(packet[2:])
        elif code == Identifiers.tribulle.recv.ST_InverserOrdreRangs:
            this.changeRankPosition(packet[2:])
        elif code == Identifiers.tribulle.recv.ST_AjouterDroitRang:
            this.setRankPermition(packet[2:], True)
        elif code == Identifiers.tribulle.recv.ST_SupprimerDroitRang:
            this.setRankPermition(packet[2:], False)
        elif code == Identifiers.tribulle.recv.ST_AffecterRang:
            this.changeTribePlayerRank(packet[2:])
        elif code == Identifiers.tribulle.recv.ST_ListeHistoriqueTribu:
            this.showTribeHistorique(packet[2:])
        elif code == Identifiers.tribulle.recv.ST_QuitterTribu:
            this.leaveTribe(packet[2:])
        elif code == Identifiers.tribulle.recv.ST_ExclureMembre:
            this.kickPlayerTribe(packet[2:])
        elif code == Identifiers.tribulle.recv.ST_DesignerChefSpirituel:
            this.setTribeMaster(packet[2:])
        elif code == Identifiers.tribulle.recv.ST_DissoudreTribu:
            this.finishTribe(packet[2:])
        elif code == Identifiers.tribulle.recv.ST_RejoindreCanal:
            this.customChat(packet[2:])
        elif code == Identifiers.tribulle.recv.ST_EnvoitMessageCanal:
            this.chatMessage(packet[2:])
        elif code == Identifiers.tribulle.recv.ST_DemandeMembresCanal:
            this.chatMembersList(packet[2:])
        else:
            if this.server.DEBUG:
                this.server.sendOutput("Warning: ["+this.client.Username+"] Invalid tribulle code: Code: "+str(code)+" packet: "+repr(packet))
        
    def sendFriendList(this, packet):
        readpacket = ByteArray(packet)
        tribulleID = 0 if packet == None else readpacket.readInt()

        p = ByteArray()
        p.writeInt(tribulleID)

        infos = {}
        this.Cursor.execute("select Username, PlayerID, FriendsList, Marriage, Gender, LastOn from Users where Username in (%s)" %(this.client.TFMUtils.joinWithQuotes(this.client.friendsList)))
        r = this.Cursor.fetchall()
        for rs in r:
            infos[rs["Username"]] = [rs["PlayerID"], rs["FriendsList"], rs["Marriage"], rs["Gender"], rs["LastOn"]]

        list = ByteArray()
        count = 0
        for playerName in this.client.friendsList:
            if not infos.has_key(playerName):
                continue

            info = infos[playerName]
            player = this.server.players.get(playerName)
            list.writeInt(info[0])
            list.writeInt(info[0])
            list.writeUTF(playerName)
            isFriend = this.client.Username in player.friendsList if player != None else this.client.Username in info[1].split(",")
            list.writeInt((this.getInGendersMarriage(player.marriage if player != None else info[2], player.gender if player != None else info[3])) if (player.marriage if player != None else info[2] == this.client.Username) else (this.getInGendersMarriage("", player.gender if player != None else info[3])))
            list.writeInt(info[4] if isFriend else 0)
            list.writeInt(this.GAME_MODE)
            list.writeUTF(player.roomName if isFriend and player != None else "")
            list.writeBool(player != None)
            count += 1

        p.writeShort(count)
        p.writeBytes(list.toByteArray())

        this.sendPacket(Identifiers.tribulle.send.ET_ResultatListeAmis, p.toByteArray())

    def sendIgnoredsList(this):
        p = ByteArray()
        p.writeInt(0)
        p.writeShort(len(this.client.ignoredsList))
        for playerName in this.client.ignoredsList:
            p.write(this.getString(playerName, this.PLAYER_NAME_LEN))

        this.sendPacket(Identifiers.tribulle.send.ET_ResultatListeNoire, p.toByteArray())

    def sendFriendConnected(this, playerName):
        if playerName in this.client.friendsList:
            p = ByteArray()
            id = this.server.getPlayerID(playerName)
            p.writeInt(id)
            p.writeInt(id)
            p.writeUTF(playerName)
            p.writeInt(this.getInGenderMarriage(playerName))
            p.writeInt(this.getPlayerLastOn(playerName))
            p.writeInt(this.GAME_MODE)
            p.writeUTF(this.server.getPlayerRoomName(playerName))
            p.writeBool(this.checkFriend(playerName, this.client.Username))
            this.sendPacket(Identifiers.tribulle.send.ET_SignaleConnexionAmi, p.toByteArray())

    def sendFriendChangedRoom(this, playerName, langueByte):
        if playerName in this.client.friendsList:
            p = ByteArray()
            p.writeInt(this.server.getPlayerID(playerName))
            p.writeInt(this.GAME_MODE)
            p.writeUTF(this.server.getPlayerRoomName(playerName))
            p.writeByte(langueByte)
            this.sendPacket(Identifiers.tribulle.send.ET_SignaleModificationLocalisationAmi, p.toByteArray())

    def sendFriendDisconnected(this, playerName):
        if playerName in this.client.friendsList:
            p = ByteArray()
            p.writeInt(this.GAME_MODE)
            p.writeInt(this.server.getPlayerID(playerName))
            this.sendPacket(Identifiers.tribulle.send.ET_SignaleDeconnexionAmi, p.toByteArray())

    def addFriend(this, packet):
        readPacket = ByteArray(packet)
        tribulleID, playerName = readPacket.readInt(), this.client.TFMUtils.parsePlayerName(readPacket.readUTF())

        p = ByteArray()
        p.writeInt(tribulleID)

        if playerName.startswith("*"):
            p.writeByte(this.INVALID_NAME)
        elif playerName == this.client.Username:
            p.writeByte(this.PROHIBITED)
        elif not this.server.checkExistingUser(playerName):
            p.writeByte(this.RECIPIENT_INVALID)
        elif playerName in this.client.friendsList:
            p.writeByte(this.ALREADY_FRIEND)
        elif len(this.client.friendsList) >= this.MAX_FRIENDS:
            p.writeByte(this.MAX_REACHED)
        else:
            p.writeByte(this.SUCESS)
            this.client.friendsList.append(playerName)
            id = this.server.getPlayerID(playerName)

            p2 = ByteArray()
            p2.writeInt(id)
            p2.writeInt(id)
            p2.writeUTF(playerName)
            isFriend = this.checkFriend(playerName, this.client.Username)
            p2.writeInt(this.getInGenderMarriage(playerName))
            p2.writeInt(this.getPlayerLastOn(playerName) if isFriend else 0)
            p2.writeInt(this.GAME_MODE)
            p2.writeUTF(this.server.getPlayerRoomName(playerName) if isFriend else "")
            p2.writeBool(this.server.checkConnectedAccount(playerName) if isFriend else False)
            this.sendPacket(Identifiers.tribulle.send.ET_SignaleAjoutAmi, p2.toByteArray())

            if isFriend:
                p3 = ByteArray()
                p3.writeInt(this.client.playerID)
                p3.writeInt(this.client.playerID)
                p3.writeUTF(playerName)
                p3.writeInt(this.getInGenderMarriage(this.client.Username))
                p3.writeInt(this.getPlayerLastOn(playerName) if isFriend else 0)
                p3.writeInt(this.GAME_MODE)
                p3.writeUTF(this.client.Username if isFriend else "")
                p3.writeBool(True)
                this.sendPacketToPlayer(playerName, Identifiers.tribulle.send.ET_SignaleAjoutAmiBidirectionnel, p3.toByteArray())

            if playerName in this.client.ignoredsList:
                this.client.ignoredsList.remove(playerName)
                p4 = ByteArray()
                p4.writeUTF(playerName)
                this.sendPacket(Identifiers.tribulle.send.ET_SignaleRetraitListeNoire, p4.toByteArray())

            if isFriend:
                player = this.server.players.get(playerName)
                if player != None:
                    player.tribulle.sendFriendConnected(this.client.Username)
                    player.tribulle.sendFriendChangedRoom(this.client.Username, this.client.langueByte)

        this.sendPacket(Identifiers.tribulle.send.ET_ResultatAjoutAmi, p.toByteArray())

    def removeFriend(this, packet):
        readPacket = ByteArray(packet)
        tribulleID, playerName = readPacket.readInt(), this.client.TFMUtils.parsePlayerName(readPacket.readUTF())

        p = ByteArray()
        p.writeInt(tribulleID)

        if playerName in this.client.friendsList:
            p.writeByte(this.SUCESS)
            this.client.friendsList.remove(playerName)

            p2 = ByteArray()
            p2.writeUTF(playerName)
            this.sendPacket(Identifiers.tribulle.send.ET_SignaleRetraitAmi, p2.toByteArray())

            if this.checkFriend(playerName, this.client.Username):
                p3 = ByteArray()
                p3.writeInt(this.client.playerID)
                this.sendPacketToPlayer(playerName, Identifiers.tribulle.send.ET_SignaleRetraitAmiBidirectionnel, p3.toByteArray())
        else:
            p.writeByte(this.NOT_FRIEND)

        this.sendPacket(Identifiers.tribulle.send.ET_ResultatRetireAmi, p.toByteArray())

    def ignorePlayer(this, packet):
        readPacket = ByteArray(packet)
        tribulleID, playerName = readPacket.readInt(), this.client.TFMUtils.parsePlayerName(readPacket.readUTF())

        p = ByteArray()
        p.writeInt(tribulleID)

        if playerName.startswith("*") or not this.server.checkExistingUser(playerName):
            p.writeByte(this.INVALID_NAME)
        elif playerName == this.client.Username:
            p.writeByte(this.PROHIBITED)
        elif playerName in this.client.ignoredsList:
            p.writeByte(this.ALREADY_IN_BLACK_LIST)
        else:
            p.writeByte(this.SUCESS)
            this.client.ignoredsList.append(playerName)

            p2 = ByteArray()
            p2.writeUTF(playerName)
            this.sendPacket(Identifiers.tribulle.send.ET_SignaleAjoutListeNoire, p2.toByteArray())

            if playerName in this.client.friendsList:
                this.client.friendsList.remove(playerName)

                p3 = ByteArray()
                p3.writeUTF(playerName)
                this.sendPacket(Identifiers.tribulle.send.ET_SignaleRetraitAmi, p3.toByteArray())

                player = this.server.players.get(playerName)
                if player != None:
                    if this.client.Username in player.friendsList:
                        p4 = ByteArray()
                        p4.writeInt(this.client.playerID)
                        player.tribulle.sendPacket(Identifiers.tribulle.send.ET_SignaleRetraitAmiBidirectionnel, p4.toByteArray())

        this.sendPacket(Identifiers.tribulle.send.ET_ResultatAjoutListeNoire, p.toByteArray())

    def removeIgnore(this, packet):
        readPacket = ByteArray(packet)
        tribulleID, playerName = readPacket.readInt(), this.client.TFMUtils.parsePlayerName(readPacket.readUTF())

        p = ByteArray()
        p.writeInt(tribulleID)

        if playerName.startswith("*"):
            p.writeByte(this.INVALID_NAME)
        elif not playerName in this.client.ignoredsList:
            p.writeByte(this.NOT_IN_BLACK_LIST)
        else:
            p.writeByte(this.SUCESS)
            this.client.ignoredsList.remove(playerName)

            p2 = ByteArray()
            p2.writeUTF(playerName.lower())
            this.sendPacket(Identifiers.tribulle.send.ET_SignaleRetraitListeNoire, p2.toByteArray())

        this.sendPacket(Identifiers.tribulle.send.ET_ResultatRetireListeNoire, p.toByteArray())

    def whisperMessage(this, packet):
        readPacket = ByteArray(packet)
        tribulleID, playerName, message = readPacket.readInt(), this.client.TFMUtils.parsePlayerName(readPacket.readUTF()), readPacket.readUTF()
        isSuspect = this.client.privLevel < 6 and this.server.checkMessage(this.client, message)

        if not message == "":
            can = True

            p = ByteArray()
            p.writeInt(tribulleID)

            if playerName.startswith("*") or not this.server.players.has_key(playerName):
                can = False
                p.writeByte(this.RECIPIENT_INVALID)
            else:
                p.writeByte(this.SUCESS)
                if this.client.modMute:
                    if not this.client.isGuest:
                        muteInfo = this.server.getModMuteInfo(this.client.Username)
                        timeCalc = this.client.TFMUtils.getHoursDiff(int(muteInfo[0]))

                        if timeCalc <= 0:
                            this.server.removeModMute(this.client.Username)
                        else:
                            can = False
                            this.client.sendModMute(this.client.Username, timeCalc, (muteInfo[1]), True)

            this.sendPacket(Identifiers.tribulle.send.ET_ResultatMessagePrive, p.toByteArray())

            if can:
                player = this.server.players.get(playerName)
                if player != None:
                    if not this.client.Username in player.ignoredsList:
                        if player.silenceType != 0:
                            if this.client.privLevel == 10 or (player.silenceType == 1 and this.checkFriend(playerName, this.client.Username)):
                                pass
                            else:
                                this.sendSilenceMessage(playerName)
                                return

                    if not isSuspect:
                        p2 = ByteArray()
                        p2.writeUTF(this.client.Username.lower())
                        p2.writeUTF(message)
                        p2.writeByte(this.client.langueByte)
                        p2.writeBool(False)

                        player.tribulle.sendPacket(Identifiers.tribulle.send.ET_RecoitMessagePrive, p2.toByteArray())

                    p3 = ByteArray()
                    p3.writeUTF(player.Username.lower())
                    p3.writeUTF(message)
                    p3.writeByte(player.langueByte)
                    p3.writeBool(True)

                    this.sendPacket(Identifiers.tribulle.send.ET_RecoitMessagePrive, p3.toByteArray())

    def disableWhispers(this, packet):
        readPacket = ByteArray(packet)
        tribulleID, type, message = readPacket.readInt(), readPacket.readByte(), readPacket.readUTF()

        p = ByteArray()
        p.writeInt(tribulleID)
        p.writeByte(this.SUCESS)
        this.sendPacket(Identifiers.tribulle.send.ET_ResultatDefinitModeSilence, p.toByteArray())

        this.client.silenceType = type
        this.client.silenceMessage = "" if (this.client.privLevel < 6 and this.server.checkMessage(this.client, message)) else message

    def sendSilenceMessage(this, playerName):
        player = this.server.players.get(playerName)
        if player != None:
            p = ByteArray()
            p.writeUTF(player.Username)
            p.writeUTF("${trad#Silence}" if player.silenceMessage == "" else "${trad#Silence} : " + player.silenceMessage)
            this.sendPacket(Identifiers.tribulle.send.ET_RecoitMessagePriveSysteme, p.toByteArray())

    def changeGender(this, packet):
        readPacket = ByteArray(packet)
        tribulleID, gender = readPacket.readInt(), readPacket.readInt()
        this.client.gender = gender

        p = ByteArray()
        p.writeInt(tribulleID)
        p.writeByte(this.SUCESS)
        this.sendPacket(Identifiers.tribulle.send.ET_ResultatChangerDeGenre, p.toByteArray())

        p2 = ByteArray()
        p2.writeUTF(this.client.Username)
        p2.writeInt(gender)
        this.sendPacket(Identifiers.tribulle.send.ET_SignaleChangementDeGenre, p2.toByteArray())

        for player in this.server.players.values():
            if this.client.Username in player.friendsList and player.Username in this.client.friendsList:
                player.tribulle.sendPacket(Identifiers.tribulle.send.ET_SignaleChangementDeGenre, p2.toByteArray())

    def marriageInvite(this, packet):
        readPacket = ByteArray(packet)
        tribulleID, playerName = readPacket.readInt(), this.client.TFMUtils.parsePlayerName(readPacket.readUTF())

        p = ByteArray()
        p.writeInt(tribulleID)

        time = this.client.TFMUtils.getTime()

        player = this.server.players.get(playerName)
        if player != None:
            if playerName.startswith("*"):
                p.writeByte(this.RECIPIENT_INVALID)
            elif playerName == this.client.Username:
                p.writeByte(this.PROHIBITED)
            elif not this.client.marriage == "":
                p.writeByte(this.USER_ALREADY_MARRIED)
            elif not player.marriage == "":
                p.writeByte(this.RECIPIENT_ALREADY_MARRIED)
            elif time < this.client.lastDivorceTimer:
                p.writeByte(this.USER_DIVORCE)
            elif time < player.lastDivorceTimer:
                p.writeByte(this.RECIPIENT_DIVORCE)
            else:
                if not this.client.Username in player.ignoredMarriageInvites:
                    player.marriageInvite = [this.client.Username, tribulleID]
                    p2 = ByteArray()
                    p2.writeInt(this.getTime()/2)
                    p2.writeInt(this.client.playerID)
                    p2.write(this.getString(this.client.Username, this.PLAYER_NAME_LEN))
                    player.tribulle.sendPacket(Identifiers.tribulle.send.ET_SignaleDemandeEnMariage, p2.toByteArray())
                    return
        else:
            p.writeByte(this.RECIPIENT_INVALID)

        this.sendPacket(Identifiers.tribulle.send.ET_ErreurDemandeEnMariage, p.toByteArray())

    def marriageAnswer(this, packet):
        readPacket = ByteArray(packet)
        tribulleID, answer = readPacket.readInt(), readPacket.readByte()

        playerName = str(this.client.marriageInvite[0])
        resultTribulleID = int(this.client.marriageInvite[1])
        this.client.marriageInvite = []
        player = this.server.players.get(playerName)

        p = ByteArray()
        p.writeInt(tribulleID)
        p.writeByte(answer)

        p2 = ByteArray()
        p2.writeInt(resultTribulleID)
        p2.writeByte(answer)

        if player != None:
            if answer == 0:
                player.marriage = this.client.Username
                this.client.marriage = player.Username

                if not this.client.Username in player.friendsList:
                    player.friendsList.append(this.client.Username)

                if not player.Username in this.client.friendsList:
                    this.client.friendsList.append(player.Username)

                p3 = ByteArray()
                p3.writeInt(player.playerID)
                p3.writeInt(player.playerID)
                p3.writeUTF(playerName)
                p3.writeInt(this.getInGenderMarriage(playerName))
                p3.writeInt(this.getPlayerLastOn(playerName))
                p3.writeInt(this.GAME_MODE)
                p3.writeUTF(player.roomName)
                p3.writeBool(True)
                p3.writeInt(this.client.playerID)
                p3.writeInt(this.client.playerID)
                p3.writeUTF(this.client.Username)
                p3.writeInt(this.getInGenderMarriage(this.client.Username))
                p3.writeInt(this.client.lastOn)
                p3.writeInt(this.GAME_MODE)
                p3.writeUTF(player.roomName)
                p3.writeBool(True)

                this.sendPacket(Identifiers.tribulle.send.ET_SignaleMariage, p3.toByteArray())
                player.tribulle.sendPacket(Identifiers.tribulle.send.ET_SignaleMariage, p3.toByteArray())

            elif answer == 2:
                this.client.ignoredMarriageInvites.append(this.client.Username)

            player.tribulle.sendPacket(Identifiers.tribulle.send.ET_ResultatDemandeEnMariage, p2.toByteArray())
                
        this.sendPacket(Identifiers.tribulle.send.ET_ResultatRepondDemandeEnMariage, p.toByteArray())

    def marriageDivorce(this, packet):
        readPacket = ByteArray(packet)
        tribulleID = readPacket.readInt()
        time = this.client.TFMUtils.getTime() + 3600

        p = ByteArray()
        p.writeInt(tribulleID)
        p.writeByte(this.SUCESS)
        this.sendPacket(Identifiers.tribulle.send.ET_ResultatDemandeDivorce, p.toByteArray())

        p2 = ByteArray()
        p2.write(this.getString(this.client.Username.lower(), this.PLAYER_NAME_LEN))
        p2.write(this.getString(this.client.marriage.lower(), this.PLAYER_NAME_LEN))

        this.sendPacket(Identifiers.tribulle.send.ET_SignaleDivorce, p2.toByteArray())

        player = this.server.players.get(this.client.marriage)
        if player != None:
            player.tribulle.sendPacket(Identifiers.tribulle.send.ET_SignaleDivorce, p2.toByteArray())
            player.marriage = ""
            player.lastDivorceTimer = time
        else:
            this.removeMarriage(this.client.marriage, time)

        this.client.marriage = ""
        this.client.lastDivorceTimer = time

    def sendTribe(this, isNew):
        if this.client.tribeName == "":
            p = ByteArray()
            p.writeInt(0)
            p.writeByte(this.SUCESS)
            this.sendPacket(Identifiers.tribulle.send.ET_ErreurInformationsTribu, p.toByteArray())
            return

        if not int(this.client.tribeData[4]) in this.client.chats:
            this.client.chats.append(int(this.client.tribeData[4]))

        p2 = ByteArray()
        p2.writeInt(int(this.client.tribeData[4]))
        p2.writeUTF("~" + this.client.tribeName.lower())
        p2.write(chr(0) * 5)
        this.sendPacket(Identifiers.tribulle.send.ET_SignaleRejointCanal, p2.toByteArray())

        p3 = ByteArray()
        p3.writeInt(int(this.client.tribeData[4]))
        p3.writeInt(this.client.playerID)
        p3.writeUTF(this.client.Username.lower())
        this.sendPacketWholeTribe(Identifiers.tribulle.send.ET_SignaleMembreRejointCanal, p3.toByteArray())

        this.sendTribeInfo(None, isNew)

    def sendTribeInfo(this, packet, isNew):
        if this.client.tribeName == "":
            p = ByteArray()
            p.writeInt(0)
            p.writeByte(this.SUCESS)
            this.sendPacket(Identifiers.tribulle.send.ET_ErreurInformationsTribu, p.toByteArray())
            return
        
        readPacket = ByteArray(packet)
        tribulleID = 0 if packet == None else readPacket.readInt()

        p = ByteArray()
        if not isNew: p.writeInt(tribulleID)
        p.writeInt(this.client.tribeCode)
        
        p.writeUTF(this.client.tribeName)

        tribeRankings = this.client.tribeData[3]
        tribeRankings[2000010] = "${trad#tribu.chef}|1|1,1,1,1,1,1,1,1,1,1,1|1"
        
        p.writeUTF(str(this.client.tribeData[1]))
        p.writeInt(int(this.client.tribeData[2]))
        p.writeInt(this.client.tribeRank)
        p.writeShort(len(tribeRankings))

        for rank, count in tribeRankings.items():
            values = count.split("|")
            perms = values[2].split(",")

            p.writeInt(rank)
            p.writeUTF(values[0])
            p.writeByte(int(values[3]))
            p.writeInt(0)
            p.writeByte(int(values[1]))
            p.writeShort(len(perms))

            for perm in perms:
                p.writeByte(int(perm))

        this.sendPacket(Identifiers.tribulle.send.ET_SignaleTribuCreee if isNew else Identifiers.tribulle.send.ET_ResultatInformationsTribu, p.toByteArray())

    def sendTribeList(this, packet):
        readPacket = ByteArray(packet)
        tribulleID = readPacket.readInt()
        members = this.getTribeMembers(this.client.tribeCode)

        p = ByteArray()
        p.writeInt(tribulleID)
        p.writeShort(len(members))

        for playerName in members:
            id = this.server.getPlayerID(playerName)
            p.writeInt(id)
            p.writeInt(id)
            p.writeUTF(playerName)
            info = this.getPlayerTribeInfo(this.client.TFMUtils.parsePlayerName(playerName)).split("#")
            p.writeInt(int(info[1]))
            p.writeInt(int(info[2]))
            p.writeInt(this.getPlayerLastOn(playerName))
            p.writeInt(this.GAME_MODE)
            player = this.server.players.get(playerName)
            p.writeUTF("" if player == None else player.roomName)
            p.writeBool(player != None)

        this.sendPacket(Identifiers.tribulle.send.ET_ResultatMembresTribu, p.toByteArray())

    def sendTribeMemberConnected(this):
        p = ByteArray()
        p.writeInt(this.client.playerID)
        p.writeInt(this.client.playerID)
        p.writeUTF(this.client.Username)
        p.writeInt(this.client.tribeRank)
        p.writeInt(this.client.tribeJoined)
        p.writeInt(this.client.lastOn)
        p.writeInt(this.GAME_MODE)
        p.writeUTF("")
        p.writeBool(True)
        this.sendPacketWholeTribe(Identifiers.tribulle.send.ET_SignaleConnexionMembre, p.toByteArray())

    def sendTribeMemberChangeRoom(this):
        p = ByteArray()
        p.writeInt(this.client.playerID)
        p.writeInt(this.GAME_MODE)
        p.writeUTF(this.client.roomName)
        this.sendPacketWholeTribe(Identifiers.tribulle.send.ET_SignaleModificationLocalisationMembreTribu, p.toByteArray())

    def sendTribeMemberDisconnected(this):
        p = ByteArray()
        p.writeInt(int(this.client.tribeData[4]))
        p.writeInt(this.client.playerID)
        this.sendPacketWholeTribe(Identifiers.tribulle.send.ET_SignaleMembreQuitteCanal, p.toByteArray())

        p2 = ByteArray()
        p2.writeInt(this.GAME_MODE)
        p2.writeInt(this.client.playerID)
        p2.writeUTF(this.client.Username.lower())
        this.sendPacketWholeTribe(Identifiers.tribulle.send.ET_SignaleDeconnexionMembre, p2.toByteArray())

        p3 = ByteArray()
        p3.writeInt(int(this.client.tribeData[4]))
        this.sendPacket(Identifiers.tribulle.send.ET_SignaleQuitteCanal, p3.toByteArray())

    def sendPlayerInfo(this):
        p = ByteArray()
        p.writeInt(0)
        p.writeInt(this.client.playerID)
        p.writeInt(this.client.playerID)
        p.writeInt(this.getInGenderMarriage(this.client.Username))
        p.writeInt(this.server.getPlayerID(this.client.marriage) if not this.client.marriage == "" else 0)
        p.writeUTF(this.client.marriage)

        this.sendPacket(Identifiers.tribulle.send.ET_ReponseDemandeInfosJeuUtilisateur, p.toByteArray())

    def createTribe(this, packet):
        readPacket = ByteArray(packet)
        tribulleID, tribeName = readPacket.readInt(), readPacket.readUTF()

        p = ByteArray()
        p.writeInt(tribulleID)

        if this.checkExistingTribe(tribeName) or tribeName == "":
            p.writeByte(this.INVALID_TRIBE)
        elif this.client.shopCheeses < this.TRIBE_CHEESES:
            p.writeByte(this.ENOUGH_MONEY)
        else:
            p.writeByte(this.SUCESS)
            this.server.lastTribeID += 1
            this.server.setServerSetting("Last Tribe ID", str(this.server.lastTribeID))
            this.server.lastChatID += 1
            this.server.setServerSetting("Last Chat ID", str(this.server.lastChatID))
            createTime = this.getTime()

            this.Cursor.execute("insert into Tribe (Code, Name, Message, House, Rankings, Historique, Members, Chat, Points) values (?, ?, ?, ?, ?, ?, ?, ?, ?)", [this.server.lastTribeID, tribeName, "", 0, this.TRIBE_RANKS, "", this.client.Username, this.server.lastChatID, 0])

            this.client.shopCheeses -= this.TRIBE_CHEESES
            this.client.tribeCode = this.server.lastTribeID
            this.client.tribeRank = 2000010
            this.client.tribeName = tribeName
            this.client.tribeJoined = createTime
            this.client.tribeData = this.server.getTribeInfo(this.client.tribeCode)
            this.sendTribe(True)
            this.setTribeCache(this.client.tribeCode, 1, createTime, this.client.playerID, 0, 0, this.client.Username, tribeName)

        this.sendPacket(Identifiers.tribulle.send.ET_ResultatCreerTribu, p.toByteArray())

    def tribeInvite(this, packet):
        readPacket = ByteArray(packet)
        tribulleID, playerName, isError = readPacket.readInt(), this.client.TFMUtils.parsePlayerName(readPacket.readUTF()), True

        p = ByteArray()
        p.writeInt(tribulleID)

        if len(this.getTribeMembers(this.client.tribeCode)) >= this.MAX_TRIBE_MEMBERS:
            p.writeByte(this.MAX_REACHED)
        elif playerName.startswith("*"):
            p.writeByte(this.INVALID_NAME)
        elif playerName == this.client.Username:
            p.writeByte(this.PROHIBITED)
        elif not this.server.checkExistingUser(playerName):
            p.writeByte(this.RECIPIENT_INVALID)
        else:
            player = this.server.players.get(playerName)
            if player == None:
                p.writeByte(this.USER_NOT_CONNECTED)
            else:
                if not player.tribeName == "" or len(player.tribeInvite) != 0:
                    p.writeByte(this.ALREADY_IN_TRIBE)
                else:
                    isError = False
                    if not this.client.tribeCode in player.ignoredTribeInvites:
                            player.tribeInvite = [tribulleID, this.client]
                            p2 = ByteArray()
                            p2.writeInt(tribulleID)
                            p2.writeInt(this.client.playerID)
                            p2.writeUTF(this.client.Username)
                            p2.writeUTF(this.client.tribeName)
                            player.tribulle.sendPacket(Identifiers.tribulle.send.ET_SignaleInvitationTribu, p2.toByteArray())
        if isError:
            this.sendPacket(Identifiers.tribulle.send.ET_ErreurInviterMembre, p.toByteArray())

    def tribeInviteAnswer(this, packet):
        readPacket = ByteArray(packet)
        tribulleID, answer = readPacket.readInt(), readPacket.readByte()

        resultTribulleID = int(this.client.tribeInvite[0])
        player = this.client.tribeInvite[1]
        this.client.tribeInvite = []

        p = ByteArray()
        p.writeInt(tribulleID)
        p.writeByte(this.SUCESS)

        p2 = ByteArray()
        p2.writeInt(resultTribulleID)
        p2.writeByte(answer)

        if answer == 0:
            members = this.getTribeMembers(player.tribeCode)
            members.append(this.client.Username)
            this.setTribeMembers(player.tribeCode, members)

            this.client.tribeCode = player.tribeCode
            this.client.tribeRank = 2000070
            this.client.tribeName = player.tribeName
            this.client.tribeJoined = this.getTime()
            this.client.tribeData = this.server.getTribeInfo(this.client.tribeCode)

            this.setTribeCache(this.client.tribeCode, 2, this.getTime(), this.client.playerID, 0, 0, player.Username, this.client.Username)

            p3 = ByteArray()
            p3.writeInt(this.client.playerID)
            p3.writeInt(this.client.playerID)
            p3.writeUTF(this.client.Username)
            p3.writeInt(this.client.tribeRank)
            p3.writeInt(this.getTime())
            p3.writeInt(this.client.lastOn)
            p3.writeShort(1)
            p3.writeInt(this.GAME_MODE)
            p3.writeUTF(this.client.roomName)
            this.sendPacketWholeTribe(Identifiers.tribulle.send.ET_SignaleNouveauMembre, p3.toByteArray())
            this.sendTribe(False)
            this.sendTribeMemberConnected()
            this.sendTribeMemberChangeRoom()

        elif answer == 2:
            this.client.ignoredTribeInvites.append(player.tribeCode)

        this.sendPacket(Identifiers.tribulle.send.ET_ErreurRepondInvitationTribu, p.toByteArray())
        player.tribulle.sendPacket(Identifiers.tribulle.send.ET_ResultatInviterMembre, p2.toByteArray())

    def changeTribeMessage(this, packet):
        readPacket = ByteArray(packet)
        tribulleID, message = readPacket.readInt(), readPacket.readUTF()

        this.Cursor.execute("update Tribe set Message = ? where Code = ?", [message, this.client.tribeCode])
        
        this.setTribeCache(this.client.tribeCode, 6, this.getTime(), this.client.playerID, 0, 0, this.client.Username)

        p = ByteArray()
        p.writeUTF(this.client.Username)
        p.writeUTF(message)
        this.sendPacketWholeTribe(Identifiers.tribulle.send.ET_SignaleChangementMessageJour, p.toByteArray(), True)

        p2 = ByteArray()
        p2.writeInt(tribulleID)
        p2.writeByte(this.SUCESS)
        this.sendPacket(Identifiers.tribulle.send.ET_ResultatChangerMessageJour, p2.toByteArray())

        this.updateTribeData()

    def changeTribeCode(this, packet):
        readPacket = ByteArray(packet)
        tribulleID, mapCode = readPacket.readInt(), readPacket.readInt()

        this.Cursor.execute("update Tribe set House = ? where Code = ?", [mapCode, this.client.tribeCode])
        
        this.setTribeCache(this.client.tribeCode, 8, this.getTime(), this.client.playerID, 0, 0, this.client.Username, mapCode)

        p = ByteArray()
        p.writeUTF(this.client.Username)
        p.writeInt(mapCode)
        this.sendPacketWholeTribe(Identifiers.tribulle.send.ET_SignaleChangementCodeMaisonTFM, p.toByteArray(), True)

        p2 = ByteArray()
        p2.writeInt(tribulleID)
        p2.writeByte(this.SUCESS)
        this.sendPacket(Identifiers.tribulle.send.ET_ResultatChangerCodeMaisonTFM, p2.toByteArray())

        mapInfo = this.client.room.getMapInfo(mapCode)
        if mapInfo[0] == None:
            this.client.sendPacket(Identifiers.old.send.Change_Tribe_Code_Result, [16])
        elif mapInfo[4] != 22:
            this.client.sendPacket(Identifiers.old.send.Change_Tribe_Code_Result, [17])
                
        for room in this.server.rooms.values():
            if room.roomName == "*" + chr(3) + this.client.tribeName:
                room.mapChange()
                break

        this.updateTribeData()

    def createNewTribeRank(this, packet):
        readPacket = ByteArray(packet)
        tribulleID, rankName = readPacket.readInt(), readPacket.readUTF()

        if this.checkTribeExistingRank(rankName) or rankName == "" or not re.match("^[ a-zA-Z0-9]*$", rankName):
            pass
        else:
            tribeRankings = this.client.tribeData[3]
            rankID = 0
            rankPosition = len(tribeRankings)

            for rank, count in tribeRankings.items():
                rankID = rank + 1 if rank >= rankID else rankID
                args = count.split("|")
                if int(args[1]) == rankPosition:
                    args[1] = str(int(args[1]) + 1)
                    tribeRankings[rank] = "|".join(map(str, args))

            tribeRankings[rankID] = str(rankName) + "|" + str(rankPosition) + "|0,0,0,0,0,0,0,0,0,0,0|0"
            ranks = ""
            for rank, count in tribeRankings.items():
                ranks += ";" + str(rank) + "|" + str(count)

            this.Cursor.execute("update Tribe set Rankings = ? where Code = ?", [ranks[1:], this.client.tribeCode])

            p = ByteArray()
            p.writeInt(tribulleID)
            p.writeInt(rankID)
            p.writeUTF(rankName)
            p.writeBool(False)
            p.writeInt(0)
            p.writeByte(rankPosition)
            p.write(chr(0) * 11)
            this.sendPacketWholeTribe(Identifiers.tribulle.send.ET_ResultatAjouterRang, p.toByteArray(), True)

            this.updateTribeData()

    def deleteTribeRank(this, packet):
        readPacket = ByteArray(packet)
        tribulleID, rankID = readPacket.readInt(), readPacket.readInt()
        tribeRankings = this.client.tribeData[3]

        rankInfo = tribeRankings[rankID].split("|")
        rankPosition = int(rankInfo[1])

        for rank, count in tribeRankings.items():
            args = count.split("|")
            if int(args[1]) > rankPosition:
                args[1] = str(int(args[1]) - 1)
                tribeRankings[rank] = "|".join(map(str, args))

        del tribeRankings[rankID]
        ranks = ""
        for rank, count in tribeRankings.items():
            ranks += ";" + str(rank) + "|" + str(count)

        this.Cursor.execute("update Tribe set Rankings = ? where Code = ?", [ranks[1:], this.client.tribeCode])

        p = ByteArray()
        p.writeInt(tribulleID)
        p.writeByte(this.SUCESS)
        this.sendPacket(Identifiers.tribulle.send.ET_ResultatSupprimerRang, p.toByteArray())

        this.updateTribeData()

        members = this.getTribeMembers(this.client.tribeCode)
        for playerName in members:
            player = this.server.players.get(playerName)
            if player != None:
                if player.tribeRank == rankID:
                    playerID = player.playerID
                    player.tribeRank = 2000070
                else:
                    continue
            else:
                tribeInfo = this.getPlayerTribeInfo(playerName).split("#")
                if int(tribeInfo[1]) == rankID:
                    playerID = this.server.getPlayerID(playerName)
                    tribeInfo[1] = "2000070"
                    this.Cursor.execute("update Users set TribeInfo = ? where Username = ?", ["#".join(map(str, tribeInfo)), playerName])
                else:
                    continue

            this.setTribeCache(this.client.tribeCode, 5, this.getTime(), this.client.Username, playerID, 1109464, "${trad#tribu.nouv}", this.client.Username, playerName)

            p2 = ByteArray()
            p2.writeInt(playerID)
            p2.writeUTF(playerName)
            p2.writeInt(2000070)
            p2.writeUTF("${trad#tribu.nouv}")
            this.sendPacketWholeTribe(Identifiers.tribulle.send.ET_SignaleChangementRang, p2.toByteArray(), True)

    def renameTribeRank(this, packet):
        readPacket = ByteArray(packet)
        tribulleID, rankID, rankName = readPacket.readInt(), readPacket.readInt(), readPacket.readUTF()
        tribeRankings = this.client.tribeData[3]

        p = ByteArray()
        p.writeInt(tribulleID)

        if this.checkTribeExistingRank(rankName):
            p.writeByte(this.NAME_UNAVAILABLE)
        elif rankName == "" or not re.match("^[ a-zA-Z0-9]*$", rankName):
            p.writeByte(this.INVALID_NAME)
        else:
            p.writeByte(this.SUCESS)
            tribeRankings = this.client.tribeData[3]
            rankInfo = tribeRankings[rankID].split("|")
            rankInfo[0] = rankName
            tribeRankings[rankID] = "|".join(map(str, rankInfo))

            ranks = ""
            for rank, count in tribeRankings.items():
                ranks += ";" + str(rank) + "|" + str(count)

            this.Cursor.execute("update Tribe set Rankings = ? where Code = ?", [ranks[1:], this.client.tribeCode])

            this.updateTribeData()
                
        this.sendPacket(Identifiers.tribulle.send.ET_ResultatRenommerRang, p.toByteArray())

    def changeRankPosition(this, packet):
        readPacket = ByteArray(packet)
        tribulleID, rankID, rankID2 = readPacket.readInt(), readPacket.readInt(), readPacket.readInt()
        tribeRankings = this.client.tribeData[3]

        rankInfo = tribeRankings[rankID].split("|")
        rankInfo[1] = str(int(rankInfo[1]) - 1)
        tribeRankings[rankID] = "|".join(map(str, rankInfo))

        rankInfo2 = tribeRankings[rankID2].split("|")
        rankInfo2[1] = str(int(rankInfo2[1]) + 1)
        tribeRankings[rankID2] = "|".join(map(str, rankInfo2))

        ranks = ""
        for rank, count in tribeRankings.items():
            ranks += ";" + str(rank) + "|" + str(count)

        this.Cursor.execute("update Tribe set Rankings = ? where Code = ?", [ranks[1:], this.client.tribeCode])

        p = ByteArray()
        p.writeInt(tribulleID)
        p.writeByte(this.SUCESS)
        this.sendPacket(Identifiers.tribulle.send.ET_ResultatInverserOrdreRangs, p.toByteArray())

        this.updateTribeData()

    def setRankPermition(this, packet, perm):
        readPacket = ByteArray(packet)
        tribulleID, rankID, permID = readPacket.readInt(), readPacket.readInt(), readPacket.readInt()
        tribeRankings = this.client.tribeData[3]

        rankInfo = tribeRankings[rankID].split("|")
        rankPerms = rankInfo[2].split(",")
        rankPerms[permID] = "1" if perm else "0"
        rankInfo[2] = ",".join(map(str, rankPerms))
        tribeRankings[rankID] = "|".join(map(str, rankInfo))

        ranks = ""
        for rank, count in tribeRankings.items():
            ranks += ";" + str(rank) + "|" + str(count)

        this.Cursor.execute("update Tribe set Rankings = ? where Code = ?", [ranks[1:], this.client.tribeCode])

        p = ByteArray()
        p.writeInt(tribulleID)
        p.writeByte(this.SUCESS)
        this.sendPacket(Identifiers.tribulle.send.ET_ResultatAjouterDroitRang if perm else Identifiers.tribulle.send.ET_ResultatSupprimerDroitRang, p.toByteArray())

        this.updateTribeData()

    def changeTribePlayerRank(this, packet):
        readPacket = ByteArray(packet)
        tribulleID, playerID, rankID = readPacket.readInt(), readPacket.readInt(), readPacket.readInt()
        playerName = this.server.getPlayerName(playerID)
        tribeRankings = this.client.tribeData[3]
        rankName = tribeRankings[rankID].split("|")[0]

        p = ByteArray()
        p.writeInt(tribulleID)
        p.writeByte(this.SUCESS)
        this.sendPacket(Identifiers.tribulle.send.ET_ResultatAffecterRang, p.toByteArray())

        p2 = ByteArray()
        p2.writeInt(playerID)
        p2.writeUTF(playerName)
        p2.writeInt(rankID)
        p2.writeUTF(rankName)
        this.sendPacketWholeTribe(Identifiers.tribulle.send.ET_SignaleChangementRang, p2.toByteArray(), True)

        player = this.server.players.get(playerName)
        if player != None:
            player.tribeRank = rankID
        else:
            playerTribe = this.getPlayerTribeInfo(playerName).split("#")
            this.Cursor.execute("update Users set TribeInfo = ? where Username = ?", [playerTribe[0] + "#" + str(rankID) + "#" + playerTribe[2], playerName])

        this.setTribeCache(this.client.tribeCode, 5, this.getTime(), this.client.playerID, playerID, 1109465, rankName, this.client.Username, playerName)

    def showTribeHistorique(this, packet):
        readPacket = ByteArray(packet)
        tribulleID = readPacket.readInt()

        p = ByteArray()
        historique = this.getTribeHistorique(this.client.tribeCode).split("|")
        length = len(historique)

        for event in historique:
            informations = event.split("/")
            if len(informations) < 6:
                length -= 1
                break

            type = int(informations[0])
            info = ""

            if type == 1:
                info = "{\"auteur\":\"%s\", \"tribu\":\"%s\"}" %(informations[5].lower(), informations[6])
            elif type == 2:
                info = "{\"auteur\":\"%s\", \"membreAjoute\":\"%s\"}" %(informations[5].lower(), informations[6].lower())
            elif type == 3:
                info = "{\"auteur\":\"%s\", \"membreExclu\":\"%s\"}" %(informations[5].lower(), informations[6].lower())
            elif type == 4:
                info = "{\"membreParti\":\"%s\"}" %(informations[5].lower())
            elif type == 5:
                info = "{\"rang\":\"%s\", \"auteur\":\"%s\", \"cible\":\"%s\"}" %(informations[5], informations[6].lower(), informations[7].lower())
            elif type == 6:
                info = "{\"auteur\":\"%s\"}" %(informations[5].lower())
            elif type == 7:
                info = "{\"auteur\":\"%s\"}" %(informations[5].lower())
            elif type == 8:
                info = "{\"auteur\":\"%s\", \"code\":\"%s\"}" %(informations[5].lower(), informations[6])

            p.writeInt(type)
            p.writeInt(int(informations[2]))
            p.writeInt(int(informations[3]))
            p.writeInt(int(informations[4]))
            p.writeUTF(info)
            p.writeInt(int(informations[1]))

        p2 = ByteArray()
        p2.writeInt(tribulleID)
        p2.writeShort(length)
        p2.writeBytes(p.toByteArray())
        p2.writeShort(0)
        p2.writeShort(length)
        this.sendPacket(Identifiers.tribulle.send.ET_ResultatListeHistoriqueTribu, p2.toByteArray())

    def leaveTribe(this, packet):
        readPacket = ByteArray(packet)
        tribulleID = readPacket.readInt()

        p = ByteArray()
        p.writeInt(tribulleID)

        if this.client.tribeRank == 2000010:
            p.writeByte(this.PROHIBITED)
        else:
            p.writeByte(this.SUCESS)

            p2 = ByteArray()
            p2.writeInt(this.client.playerID)
            p2.writeUTF(this.client.Username.lower())
            this.sendPacketWholeTribe(Identifiers.tribulle.send.ET_SignaleDepartMembre, p2.toByteArray(), True)

            members = this.getTribeMembers(this.client.tribeCode)
            members.remove(this.client.Username)
            this.setTribeMembers(this.client.tribeCode, members)

            this.setTribeCache(this.client.tribeCode, 4, this.getTime(), this.client.playerID, 0, 0, this.client.Username)

            p3 = ByteArray()
            p3.writeInt(int(this.client.tribeData[4]))
            p3.writeInt(this.client.playerID)
            this.sendPacketWholeTribe(Identifiers.tribulle.send.ET_SignaleMembreQuitteCanal, p3.toByteArray())

            p4 = ByteArray()
            p.writeInt(int(this.client.tribeData[4]))
            this.sendPacket(Identifiers.tribulle.send.ET_SignaleQuitteCanal, p4.toByteArray())

            this.client.updateTribePoints()
            this.client.tribeCode = 0
            this.client.tribeName = ""
            this.client.tribeRank = 0
            this.client.tribeJoined = 0
            this.client.tribeData = []

        this.sendPacket(Identifiers.tribulle.send.ET_ResultatQuitterTribu, p.toByteArray())

    def kickPlayerTribe(this, packet):
        readPacket = ByteArray(packet)
        tribulleID, playerID = readPacket.readInt(), readPacket.readInt()
        playerName = this.server.getPlayerName(playerID)
        tribeInfo = this.getPlayerTribeInfo(playerName)

        p = ByteArray()
        p.writeInt(tribulleID)

        if not tribeInfo == "":
            p.writeByte(this.SUCESS)
            members = this.getTribeMembers(this.client.tribeCode)
            members.remove(playerName)
            this.setTribeMembers(this.client.tribeCode, members)
            
            this.setTribeCache(this.client.tribeCode, 3, this.getTime(), this.client.playerID, 0, 0, this.client.Username, playerName)

            p2 = ByteArray()
            p2.writeUTF(this.client.Username)
            p2.writeInt(playerID)
            p2.writeUTF(playerName)
            this.sendPacketWholeTribe(Identifiers.tribulle.send.ET_SignaleExclusion, p2.toByteArray())

            player = this.server.players.get(playerName)
            if player != None:
                p3 = ByteArray()
                p3.writeInt(int(player.tribeData[4]))
                p3.writeInt(player.playerID)
                player.tribulle.sendPacketWholeTribe(Identifiers.tribulle.send.ET_SignaleMembreQuitteCanal, p3.toByteArray())

                p4 = ByteArray()
                p4.writeInt(int(player.tribeData[4]))
                player.tribulle.sendPacket(Identifiers.tribulle.send.ET_SignaleQuitteCanal, p4.toByteArray())

                player.updateTribePoints()
                player.tribeCode = 0
                player.tribeName = ""
                player.tribeRank = 0
                player.tribeJoined = 0
                player.tribeData = []
            else:
                this.Cursor.execute("update Users set TribeInfo = ? where Username = ?", ["", playerName])
        else:
            p.writeByte(this.INTERNAL_ERROR)

        this.sendPacket(Identifiers.tribulle.send.ET_ResultatExclureMembre, p.toByteArray())

    def setTribeMaster(this, packet):
        readPacket = ByteArray(packet)
        tribulleID, playerID = readPacket.readInt(), readPacket.readInt()
        playerName = this.server.getPlayerName(playerID)
        tribeRankings = this.client.tribeData[3]
        rankName = tribeRankings[2000010].split("|")[0]
        rankName2 = tribeRankings[2000020 if tribeRankings.has_key(2000020) else 2000070].split("|")[0]

        p2 = ByteArray()
        p2.writeInt(playerID)
        p2.writeUTF(playerName)
        p2.writeInt(2000010)
        p2.writeUTF(rankName)
        this.sendPacketWholeTribe(Identifiers.tribulle.send.ET_SignaleChangementRang, p2.toByteArray(), True)

        p3 = ByteArray()
        p3.writeInt(this.client.playerID)
        p3.writeUTF(this.client.Username)
        p3.writeInt(2000020 if tribeRankings.has_key(2000020) else 2000070)
        p3.writeUTF(rankName2)
        this.sendPacketWholeTribe(Identifiers.tribulle.send.ET_SignaleChangementRang, p3.toByteArray(), True)

        this.setTribeCache(this.client.tribeCode, 5, this.getTime(), this.client.playerID, playerID, 1109464, rankName, this.client.Username, playerName)
        this.setTribeCache(this.client.tribeCode, 5, this.getTime(), this.client.playerID, 0, 1109465, rankName2, this.client.Username, this.client.Username)
        this.client.tribeRank = 2000020 if tribeRankings.has_key(2000020) else 2000070
        player = this.server.players.get(playerName)
        if player != None:
            player.tribeRank = 2000010
        else:
            tribeInfo = this.getPlayerTribeInfo(playerName).split("#")
            tribeInfo[1] = "2000010"

            this.Cursor.execute("update Users set TribeInfo = ? where Username = ?", ["#".join(map(str, tribeInfo)), playerName])

        p = ByteArray()
        p.writeInt(tribulleID)
        p.writeByte(this.SUCESS)
        this.sendPacket(Identifiers.tribulle.send.ET_ResultatDesignerChefSpirituel, p.toByteArray())

    def finishTribe(this, packet):
        readPacket = ByteArray(packet)
        tribulleID = readPacket.readInt()

        this.sendPacketWholeTribe(Identifiers.tribulle.send.ET_SignaleDissolutionTribu, "", True)

        this.Cursor.execute("delete from Tribe where Code = ?", [this.client.tribeCode])

        this.client.tribeCode = 0
        this.client.tribeName = ""
        this.client.tribeRank = 0
        this.client.tribeJoined = 0
        this.client.tribeData = []
        this.client.tribePoints = 0
        
        p = ByteArray()
        p.writeInt(tribulleID)
        p.writeByte(this.SUCESS)
        this.sendPacket(Identifiers.tribulle.send.ET_ResultatDissoudreTribu, p.toByteArray())

    def customChat(this, packet):
        readPacket = ByteArray(packet)
        tribulleID, chatName = readPacket.readInt(), readPacket.readUTF()

        p = ByteArray()
        p.writeInt(tribulleID)

        chatID = this.getChatID(chatName)
        if chatID == -1:
            chatID = this.server.lastChatID + 1
            this.server.setServerSetting("Last Chat ID", str(chatID))
            this.Cursor.execute("insert into Chats (ID, Name) values (?, ?)", [chatID, chatName])

        if chatID in this.client.chats:
            p.writeByte(this.ALREADY_THIS_CHANNEL)
        else:
            p.writeByte(this.SUCESS)
            this.client.chats.append(chatID)

            p2 = ByteArray()
            p.writeInt(chatID)
            p.writeInt(this.client.playerID)
            p.writeUTF(this.client.Username.lower())
            this.sendPacketWholeChat(chatID, Identifiers.tribulle.send.ET_SignaleMembreRejointCanal, p2.toByteArray())

            p3 = ByteArray()
            p3.writeInt(chatID)
            p3.writeUTF(chatName)
            p3.writeBool(True)
            p3.writeInt(0)
            this.sendPacket(Identifiers.tribulle.send.ET_SignaleRejointCanal, p3.toByteArray())

        this.sendPacket(Identifiers.tribulle.send.ET_ResultatRejoindreCanal, p.toByteArray())

    def chatMessage(this, packet):
        readPacket = ByteArray(packet)
        tribulleID, chatID, message = readPacket.readInt(), readPacket.readInt(), readPacket.readUTF()

        p = ByteArray()
        p.writeInt(chatID)
        p.writeUTF(this.client.Username)
        p.writeUTF(message)
        p.writeByte(this.client.langueByte)
        this.sendPacketWholeChat(chatID, Identifiers.tribulle.send.ET_SignaleMessageCanal, p.toByteArray(), True)

        p2 = ByteArray()
        p2.writeInt(tribulleID)
        p2.writeByte(this.SUCESS)
        this.sendPacket(Identifiers.tribulle.send.ET_ResultatMessageCanal, p2.toByteArray())

    def chatMembersList(this, packet):
        readPacket = ByteArray(packet)
        tribulleID, chatID = readPacket.readInt(), readPacket.readInt()

        p = ByteArray()
        p.writeInt(tribulleID)

        length = 0
        ids = ByteArray()
        names = ByteArray()

        for player in this.server.players.values():
            if chatID in player.chats:
                length += 1
                ids.writeInt(player.playerID)
                names.writeUTF(player.Username)

        p.writeShort(length)
        p.write(ids.toByteArray())
        p.writeShort(length)
        p.write(names.toByteArray())
        this.sendPacket(Identifiers.tribulle.send.ET_ResultatDemandeMembresCanal, p.toByteArray())

    def getPlayerLastOn(this, playerName):
        player = this.server.players.get(playerName)
        if player != None:
            return this.server.players[playerName].lastOn
        else:
            this.Cursor.execute("select LastOn from Users where Username = ?", [playerName])
            rs = this.Cursor.fetchone()
            if rs:
                return rs["LastOn"]
        return 0

    def checkFriend(this, playerName, usernameToCheck):
        checkList = this.server.players[playerName].friendsList if this.server.players.has_key(playerName) else this.getUserFriends(playerName)
        return usernameToCheck in checkList

    def getUserFriends(this, username):
        this.Cursor.execute("select FriendsList from Users where Username = ?", [username])
        rs = this.Cursor.fetchone()
        if rs:
            return rs["FriendsList"].split(",")
        return []

    def getPlayerGender(this, playerName):
        this.Cursor.execute("select Gender from Users where Username = ?", [playerName])
        rs = this.Cursor.fetchone()
        if rs:
            return rs["Gender"]
        return 0

    def getPlayerMarriage(this, playerName):
        this.Cursor.execute("select Marriage from Users where Username = ?", [playerName])
        rs = this.Cursor.fetchone()
        if rs:
            return rs["Marriage"]
        return ""

    def removeMarriage(this, playerName, time):
        this.Cursor.execute("update Users set Marriage = ?, LastDivorceTimer = ? where Username = ?", ["", time, playerName])

    def getInGenderMarriage(this, playerName):
        if this.server.players.has_key(playerName):
            player = this.server.players.get(playerName)
            gender = player.gender
            marriage = player.marriage
        else:
            gender = this.getPlayerGender(playerName)
            marriage = this.getPlayerMarriage(playerName)

        return (5 if gender == 1 else 9 if gender == 2 else 1) if marriage == "" else (7 if gender == 1 else 11 if gender == 2 else 3)

    def getInGendersMarriage(this, marriage, gender):
        return (5 if gender == 1 else 9 if gender == 2 else 1) if marriage == "" else (7 if gender == 1 else 11 if gender == 2 else 3)

    def getTribeMembers(this, tribeCode):
        this.Cursor.execute("select Members from Tribe where Code = ?", [tribeCode])
        rs = this.Cursor.fetchone()
        if rs:
            return rs["Members"].split(",")
        return []

    def setTribeMembers(this, tribeCode, members):
        this.Cursor.execute("update Tribe set Members = ? where Code = ?", [",".join(map(str, members)), tribeCode])

    def getPlayerTribeInfo(this, playerName):
        player = this.server.players.get(playerName)
        if player != None:
            return "#".join(map(str, [player.tribeCode, player.tribeRank, player.tribeJoined]))
        else:
            this.Cursor.execute("select TribeInfo from Users where Username = ?", [playerName])
            rs = this.Cursor.fetchone()
            if rs:
                return rs["TribeInfo"]
        return ""

    def checkExistingTribe(this, tribeName):
        this.Cursor.execute("select Name from Tribe where Code = ?", [tribeName])
        if this.Cursor.fetchone():
            return True
        return False

    def checkTribeExistingRank(this, rankName):
        tribeRankings = this.client.tribeData[3]
        rankNameLangue = "${trad#tribu.memb}" if rankName == "Membro" else "${trad#tribu.nouv}" if rankName == "Novo membro" else "${trad#TG_7}" if rankName == "Aprendiz de Shaman" else "${trad#TG_6}" if rankName == "Estagiário" else "${trad#TG_4}" if rankName == "Recrutador" else "${trad#tribu.chef}" if rankName == "Chefe espiritual" else "${trad#TG_8}" if rankName == "Shaman da Tribo" else rankName
        for rank in tribeRankings.values():
            checkRankName = rank.split("|")[0]
            if checkRankName == rankName or checkRankName == rankNameLangue:
                return True
        return False

    def getTribeHistorique(this, tribeCode):
        this.Cursor.execute("select Historique from Tribe where Code = ?", [tribeCode])
        rs = this.Cursor.fetchone()
        if rs:
            return rs["Historique"]
        return ""

    def setTribeHistorique(this, tribeCode, historique):
        this.Cursor.execute("update Tribe set Historique = ? where Code = ?", [historique, tribeCode])

    def setTribeCache(this, tribeCode, *data):
        historique = this.getTribeHistorique(tribeCode)
        if historique == "":
            historique = "/".join(map(str, data))
        else:
            historique = "/".join(map(str, data)) + "|" + historique

        this.setTribeHistorique(tribeCode, historique)

    def getChatID(this, chatName):
        this.Cursor.execute("select ID from Chats where Name = ?", [chatName])
        rs = this.Cursor.fetchone()
        if rs:
            return rs["ID"]
        return -1
