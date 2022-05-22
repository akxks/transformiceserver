# -*- coding: cp1252 -*-
from ByteArray import ByteArray
from Identifiers import Identifiers
from twisted.internet import reactor

class SkillModule:
    def __init__(this, player, server):
        this.client = player
        this.server = player.server                
        this.rangeArea = 85

    def getPlayerExp(this, isShaman, exp):
        gainExp = exp * (((3 if this.client.shamanLevel < 30 else (6 if this.client.shamanLevel >= 30 and this.client.shamanLevel < 60 else 10)) if this.client.shamanType == 0 else (5 if this.client.shamanLevel < 30 else (10 if this.client.shamanLevel >= 30 and this.client.shamanLevel < 60 else 20))) if isShaman else 1)
        
        this.client.shamanExp += gainExp

        if this.client.shamanExp < this.client.shamanExpNext:
            this.sendGainExp(this.client.shamanExp)
            this.sendExp(this.client.shamanLevel, this.client.shamanExp, this.client.shamanExpNext)
            if isShaman:
                this.sendEarnedExp(gainExp, exp)
        else:
            if this.client.shamanLevel < 160:
                this.client.shamanLevel += 1
                this.client.shamanExp -= this.client.shamanExpNext
                if this.client.shamanExp < 0:
                    this.client.shamanExp = 0

                this.client.shamanExpNext += 10 * this.client.shamanLevel

                this.sendExp(this.client.shamanLevel, 0, this.client.shamanExpNext)
                this.sendGainExp(this.client.shamanExp)
                if isShaman:
                    this.sendEarnedExp(gainExp, exp)

                if this.client.shamanLevel >= 20:
                    this.sendEarnedLevel(this.client.Username, this.client.shamanLevel)

    def buySkill(this, skill):
        countCheck = 0
        for value in this.client.playerSkills.values():
            countCheck += value

        if this.client.shamanLevel - 1 > countCheck:
            if this.client.playerSkills.has_key(skill):
                this.client.playerSkills[skill] += 1
            else:
                this.client.playerSkills[skill] = 1
            this.sendShamanSkills(True)

    def redistributeSkills(this):
        if this.client.shopCheeses >= this.client.shamanLevel:
            if len(this.client.playerSkills) >=  1:
                if this.client.canResSkill:
                    this.client.shopCheeses -= this.client.shamanLevel
                    this.client.playerSkills = {}
                    this.sendShamanSkills(True)
                    this.client.canResSkill = False
                    this.client.resSkillsTimer = reactor.callLater(600, setattr, this, "canResSkill", True)
                    this.client.Totem[0] = 0
                    this.client.Totem[1] = ""
                    this.client.STotem[0] = 0
                    this.client.STotem[1] = ""
                    this.server.setTotemData(this.client.Username, int(str(this.client.Totem[0])), str(this.client.Totem[1]))
                else:
                    this.client.sendPacket(Identifiers.send.Redistribute_Error_Time, "", True)
        else:
            this.client.sendPacket(Identifiers.send.Redistribute_Error_Cheeses, "", True)

    def sendExp(this, level, exp, nextLevel):
        this.client.sendPacket(Identifiers.send.Shaman_Exp, ByteArray().writeShort(level - 1).writeInt(exp).writeInt(nextLevel).toByteArray(), True)

    def sendGainExp(this, amount):
        this.client.sendPacket(Identifiers.send.Shaman_Gain_Exp, ByteArray().writeInt(amount).toByteArray(), True)

    def sendEarnedExp(this, xp, numCompleted):
        this.client.sendPacket(Identifiers.send.Shaman_Earned_Exp, ByteArray().writeShort(xp).writeShort(numCompleted).toByteArray(), True)

    def sendEarnedLevel(this, playerName, level):
        this.client.room.sendAllBin(Identifiers.send.Shaman_Earned_Level, ByteArray().writeUTF(playerName).writeByte(level - 1).toByteArray(), True)

    def sendShamanSkills(this, newBoolean):
        p = ByteArray().writeByte(len(this.client.playerSkills))
        for skill in this.client.playerSkills.items():
            p.writeByte(skill[0]).writeByte(skill[1])

        this.client.sendPacket(Identifiers.send.Shaman_Skills, p.writeBool(newBoolean).toByteArray(), True)

    def sendEnableSkill(this, id, count):
        this.client.sendPacket(Identifiers.send.Enable_Skill, ByteArray().writeByte(id).writeUnsignedByte(count).toByteArray(), True)

    def getShamanBadge(this, skills, shamanCode):
        badgeCode = 0
        badgesCount = [0, 0, 0, 0, 0]

        for skill, count in skills.items():
            if skill > -1 and skill < 14:
                badgesCount[0] += count
            elif skill > 19 and skill < 35:
                badgesCount[1] += count
            elif skill > 39 and skill < 55:
                badgesCount[2] += count
            elif skill > 59 and skill < 75:
                badgesCount[4] += count
            elif skill > 79 and skill < 95:
                badgesCount[3] += count

        maxList = badgesCount
        maxs = max(maxList)
        badgeCode = maxList.index(maxs)
        if badgeCode == 1:
            badgeCode = -1
        elif badgeCode == 2:
            badgeCode = -2
        elif badgeCode == 3:
            badgeCode = -3
        elif badgeCode == 4:
            badgeCode = -4
            
        for client in this.client.server.players.values():
            if client.playerCode == shamanCode:
                if client.shamanSymbol == 1:
                    badgeCode = 1
                elif client.shamanSymbol == 2:
                    badgeCode = 2
                elif client.shamanSymbol == 3:
                    badgeCode = 3
                elif client.shamanSymbol == 4:
                    badgeCode = 4
                elif client.shamanSymbol == 5:
                    badgeCode = 5
                elif client.shamanSymbol == 6:
                    badgeCode = 6
                elif client.shamanSymbol == 7:
                    badgeCode = 7
                elif client.shamanSymbol == 8:
                    badgeCode = 8
                elif client.shamanSymbol == 9:
                    badgeCode = 9
                elif client.shamanSymbol == 10:
                    badgeCode = 10
                elif client.shamanSymbol == 11:
                    badgeCode = 11
                elif client.shamanSymbol == 12:
                    badgeCode = 12
                elif client.shamanSymbol == 13:
                    badgeCode = 13
                elif client.shamanSymbol == 14:
                    badgeCode = 14
                elif client.shamanSymbol == 15:
                    badgeCode = 15
                elif client.shamanSymbol == 16:
                    badgeCode = 16
                elif client.shamanSymbol == 17:
                    badgeCode = 17
                elif client.shamanSymbol == 18:
                    badgeCode = 18
                elif client.shamanSymbol == 19:
                    badgeCode = 19
                elif client.shamanSymbol == 20:
                    badgeCode = 20 
                elif client.shamanSymbol == 21:
                    badgeCode = 21
                elif client.shamanSymbol == 22:
                    badgeCode = 22
                elif client.shamanSymbol == 23:
                    badgeCode = 23
                elif client.shamanSymbol == 24:
                    badgeCode = 24
                elif client.shamanSymbol == 25:
                    badgeCode = 25
                elif client.shamanSymbol == 26:
                    badgeCode = 26
                elif client.shamanSymbol == 27:
                    badgeCode = 27
					
        return badgeCode

    def getShamanSkills(this):
        if this.client.isShaman:
            skills = this.client.playerSkills

            for skill in [5, 8, 9, 11, 12, 26, 28, 29, 31, 41, 46, 48, 51, 52, 53, 60, 62, 65, 66, 67, 69, 71, 74, 80, 81, 83, 88, 90, 93, 85]:
                if skills.has_key(skill) and not (this.client.room.isSurvivor and skill == 81):
                    count = skills[skill]
                    if skill == 28 or skill == 65 or skill == 74 : count *= 2
                    this.sendEnableSkill(skill, count)

            for skill in [7, 14, 27, 86, 87, 94]:
                if skills.has_key(skill):
                    this.sendEnableSkill(skill, 100)

            for skill in [6, 30, 33, 34, 44, 47, 50, 63, 64, 70, 73, 82, 84, 92]:
                if skills.has_key(skill):
                    if skill == 6: this.client.ambulanceCount = skill
                    this.sendEnableSkill(skill, 1)

            if skills.has_key(0) and this.client.room.addTime == 0:
                time = 5 * skills[0]
                this.client.room.addtime = time
                if this.client.room.changeMapTimer != None: this.client.room.changeMapTimer.cancel()
                this.client.room.changeMapTimer = reactor.callLater(this.client.room.roundTime + this.client.room.addTime, this.client.room.mapChange)
                for player in this.client.room.clients.values():
                    player.sendRoundTime(this.client.room.roundTime + (this.client.room.gameStartTime - this.client.TFMUtils.getTime()) + this.client.room.addTime)

            if skills.has_key(4):
                this.client.canShamanRespawn = True

            if skills.has_key(10):
                this.sendEnableSkill(10, 3)

            if skills.has_key(13):
                this.sendEnableSkill(13, 3)

            if skills.has_key(20):
                count = skills[20]
                count = 5 if count > 5 else count
                values = [114, 126, 118, 120, 122]
                
                this.sendEnableSkill(20, values[count - 1])

            if skills.has_key(21):
                this.client.bubblesCount = skills[21]

            if skills.has_key(22):
                count = skills[22]
                count = 5 if count > 5 else count
                values = [25, 30, 35, 40, 45]
                
                this.sendEnableSkill(22, values[count - 1])

            if skills.has_key(23):
                count = skills[23]
                count = 5 if count > 5 else count
                values = [40, 50, 60, 70, 80]
                
                this.sendEnableSkill(23, values[count - 1])

            if skills.has_key(24):
                this.client.isOpportunist = True

            if skills.has_key(32):
                this.client.room.iceCount += skills[32]

            if skills.has_key(40):
                count = skills[40]
                count = 5 if count > 5 else count
                values = [30, 40, 50, 60, 70]
                
                this.sendEnableSkill(40, values[count - 1])

            if skills.has_key(42):
                count = skills[42]
                count = 5 if count > 5 else count
                values = [240, 230, 220, 210, 200]
                
                this.sendEnableSkill(42, values[count - 1])

            if skills.has_key(43):
                count = skills[43]
                count = 5 if count > 5 else count
                values = [240, 230, 220, 210, 200]
                
                this.sendEnableSkill(43, values[count - 1])

            if skills.has_key(45):
                count = skills[45]
                count = 5 if count > 5 else count
                values = [110, 120, 130, 140, 150]
                
                this.sendEnableSkill(45, values[count - 1])

            if skills.has_key(49):
                count = skills[49]
                count = 5 if count > 5 else count
                values = [110, 120, 130, 140, 150]
                
                this.sendEnableSkill(49, values[count - 1])

            if skills.has_key(54):
                this.sendEnableSkill(54, 130)

            if skills.has_key(72):
                count = skills[72]
                count = 5 if count > 5 else count
                values = [25, 30, 35, 40, 45]
                
                this.sendEnableSkill(72, values[count - 1])

            if skills.has_key(89):
                count = skills[89]
                count = 5 if count > 5 else count
                values = [96, 92, 88, 84, 80]
                
                this.sendEnableSkill(49, values[count - 1])
                this.sendEnableSkill(54, values[count - 1])

            if skills.has_key(91):
                this.client.desintegration = True

    def getShamansSkills(this, skills):
        if skills.has_key(1):
            count = skills[1]
            count = 5 if count > 5 else count
            values = [110, 120, 130, 140, 150]

            this.sendEnableSkill(1, values[count - 1])

        if skills.has_key(2):
            count = skills[2]
            count = 5 if count > 5 else count
            values = [114, 126, 118, 120, 122]

            this.sendEnableSkill(2, values[count - 1])

        if skills.has_key(68):
            count = skills[68]
            count = 5 if count > 5 else count
            values = [96, 92, 88, 84, 80]

            this.sendEnableSkill(68, values[count - 1])

    def placeSkill(this, objectID, code, px, py, angle):
        if code == 36:
            for player in this.client.room.clients.values():
                if this.checkQualifiedPlayer(px, py, player):
                    player.sendPacket(Identifiers.send.Can_Transformation, chr(1), True)
                    break

        elif code == 37:
            for player in this.client.room.clients.values():
                if this.checkQualifiedPlayer(px, py, player):
                    this.sendTeleport(36, player.posX, player.posY)
                    player.room.movePlayer(player.Username, this.client.posX, this.client.posY, False, 0, 0, True)
                    this.sendTeleport(37, this.client.posX, this.client.posY)
                    break

        elif code == 38:
            for player in this.client.room.clients.values():
                if player.isDead and not player.hasEnter and not player.isAfk and not player.isShaman:
                    if this.client.ambulanceCount > 0:
                        this.client.ambulanceCount -= 1
                        this.client.room.respawnSpecific(player.Username)
                        player.isDead = False
                        player.hasCheese = False
                        player.room.movePlayer(player.Username, this.client.posX, this.client.posY, False, 0, 0, True)
                        this.sendTeleport(37, this.client.posX, this.client.posY)
                    else:
                        break

            this.client.room.sendAllBin(Identifiers.send.Skill, chr(38) + chr(1))

        elif code == 42:
            this.sendSkillObject(3, px, py, 0)

        elif code == 43:
            this.sendSkillObject(1, px, py, 0)

        elif code == 47:
            if this.client.room.iceEnabled:
                for player in this.client.room.clients.values():
                    if player.hasCheese:
                        if this.checkQualifiedPlayer(px, py, player):
                            player.playerWin(0)
                            break

        elif code == 55:
            for player in this.client.room.clients.values():
                if not player.hasCheese and this.client.hasCheese:
                    if this.checkQualifiedPlayer(px, py, player):
                        player.sendGiveCheese()
                        this.removeShamanCheese()
                        this.client.hasCheese = False
                        break

        elif code == 56:
            this.sendTeleport(36, this.client.posX, this.client.posY)
            this.client.room.movePlayer(this.client.Username, px, py, False, 0, 0, True)
            this.sendTeleport(37, px, py)

        elif code == 57:
            if this.client.room.cloudID == -1:
                this.client.room.cloudID = objectID
            else:
                this.client.room.removeObject(this.client.room.cloudID)
                this.client.room.cloudID = objectID

        elif code == 61:
            if this.client.room.companionBox == -1:
                this.client.room.companionBox = objectID
            else:
                this.client.room.removeObject(this.client.room.companionBox)
                this.client.room.companionBox = objectID

        elif code == 70:
            this.sendSpiderMouseSkill(px, py)

        elif code == 71:
            for player in this.client.room.clients.values():
                if this.checkQualifiedPlayer(px, py, player):
                    this.sendRolloutMouseSkill(player.playerCode)
                    this.client.room.sendAllBin(Identifiers.send.Skill, chr(71) + chr(1))
                    break

        elif code == 73:
            for player in this.client.room.clients.values():
                if this.checkQualifiedPlayer(px, py, player):
                    this.sendDecreaseMouseSkill(player.playerCode)
                    break

        elif code == 74:
            for player in this.client.room.clients.values():
                if this.checkQualifiedPlayer(px, py, player):
                    this.sendLeafMouseSkill(player.playerCode)
                    break

        elif code == 75:
            this.client.room.sendAllBin(Identifiers.send.Remove_All_Objects_Skill, "")

        elif code == 76:
            this.sendSkillObject(5, px, py, angle)

        elif code == 79:
            for player in this.client.room.clients.values():
                if this.checkQualifiedPlayer(px, py, player):
                    this.sendIceMouseSkill(player.playerCode, True)
                    reactor.callLater(this.client.playerSkills[82] * 2, lambda: this.client.skillModule.sendIceMouseSkill(this.client.playerCode, False))

        elif code == 81:
            this.sendGravitationalSkill(this.client.playerSkills[63] * 2, 0)

        elif code == 83:
            for player in this.client.room.clients.values():
                if this.checkQualifiedPlayer(px, py, player):
                    player.canMeep = True
                    player.sendPacket(Identifiers.send.Can_Meep, chr(1), True)
                    break

        elif code == 84:
            this.sendGrapnelSkill(this.client.playerCode, px, py)

        elif code == 86:
            this.sendBonfireSkill(px, py, this.client.playerSkills[86] * 4)

        elif code == 92:
            this.getShamanSkills()
            this.client.room.sendAllBin(Identifiers.send.Reset_Shaman_Skills, "")

        elif code == 93:
            for player in this.client.room.clients.values():
                if this.checkQualifiedPlayer(px, py, player):
                    this.sendEvolutionSkill(player.playerCode)
                    break

        elif code == 94:
            this.sendGatmanSkill(this.client.playerCode)

    def checkQualifiedPlayer(this, px, py, player):
        if not player.Username == this.client.Username and not player.isShaman:
            if player.posX >= px - this.rangeArea and player.posX <= px + this.rangeArea:
                if player.posY >= py - this.rangeArea and player.posY <= py + this.rangeArea:
                    return True
        return False

    def parseSkillPacket(this, skill, packet):
        p = ByteArray(packet)
        if this.client.isShaman:
            if skill == "fly":
                fly = p.readBool()
                this.sendShamanFly(fly)

            elif skill == "projection":
                posX = p.readShort()
                posY = p.readShort()
                dir = p.readShort()
                this.sendProjectionSkill(posX, posY, dir)

            elif skill == "demoliton":
                objectID = p.readInt()
                this.sendDemolitionSkill(objectID)

            elif skill == "convert":
                objectID = p.readInt()
                this.sendConvertSkill(objectID)
                        
            elif skill == "recycling":
                id = p.readShort()
                this.sendRecyclingSkill(id)
                        
            elif skill == "antigravity":
                objectID = p.readInt()
                this.sendAntigravitySkill(objectID)
                
            elif skill == "restorative":
                objectID = p.readInt()
                id = p.readInt()
                this.sendRestorativeSkill(objectID, id)
                
            elif skill == "handymouse":
                handyMouseByte = p.readByte()
                objectID = p.readInt()

                if this.client.room.lastHandymouse[0] == -1:
                    this.client.room.lastHandymouse = [objectID, handyMouseByte]
                else:
                    this.sendHandymouseSkill(handyMouseByte, objectID)
                    this.client.room.sendAllBin(Identifiers.send.Skill, chr(77) + chr(1))
                    this.client.room.lastHandymouse = [-1, -1]
                        
            elif skill == "gravitational":
                id = p.readInt()
                this.sendGravitationalSkill(0, id)

    def parseEmoteSkill(this, emote):
        count = 0
        if emote == 0:
            if this.client.playerSkills.has_key(3):
                can = this.client.playerSkills[3]
                for player in this.client.room.clients.values():
                    if count <= can:
                        if player.posX >= this.client.posX - 400 and player.posX <= this.client.posX + 400:
                            if player.posY >= this.client.posY - 300 and player.posY <= this.client.posY + 300:
                                player.sendPlayerEmote(0, "", False, False)
                                count += 1
                    else:
                        break

        elif emote == 4:
            if this.client.playerSkills.has_key(61):
                can = this.client.playerSkills[61]
                for player in this.client.room.clients.values():
                    if count <= can:
                        if player.posX >= this.client.posX - 400 and player.posX <= this.client.posX + 400:
                            if player.posY >= this.client.posY - 300 and player.posY <= this.client.posY + 300:
                                player.sendPlayerEmote(2, "", False, False)
                                count += 1
                    else:
                        break

        elif emote == 8:
            if this.client.playerSkills.has_key(25):
                can = this.client.playerSkills[25]
                for player in this.client.room.clients.values():
                    if count <= can:
                        if player.posX >= this.client.posX - 400 and player.posX <= this.client.posX + 400:
                            if player.posY >= this.client.posY - 300 and player.posY <= this.client.posY + 300:
                                player.sendPlayerEmote(3, "", False, False)
                                count += 1
                    else:
                        break

    def sendSkillObject(this, objectID, posX, posY, angle):
        this.client.room.sendAllBin(Identifiers.send.Skill_Object, ByteArray().writeShort(posX).writeShort(posY).writeByte(objectID).writeShort(angle).toByteArray())

    def sendTeleport(this, type, posX, posY):
        this.client.room.sendAllBin(Identifiers.send.Teleport, ByteArray().writeByte(type).writeShort(posX).writeShort(posY).toByteArray())

    def removeShamanCheese(this):
        this.client.room.sendAllBin(Identifiers.send.Remove_Cheese, ByteArray().writeInt(this.client.playerCode).toByteArray())

    def sendSpiderMouseSkill(this, px, py):
        this.client.room.sendAllBin(Identifiers.send.Spider_Mouse_Skill, ByteArray().writeShort(px).writeShort(py).toByteArray())

    def sendRolloutMouseSkill(this, playerCode):
        this.client.room.sendAllBin(Identifiers.send.Rollout_Mouse_Skill, ByteArray().writeInt(playerCode).toByteArray())

    def sendDecreaseMouseSkill(this, playerCode):
        this.client.room.sendAllBin(Identifiers.send.Mouse_Size, ByteArray().writeInt(playerCode).writeShort(70).writeBool(True).toByteArray())

    def sendLeafMouseSkill(this, playerCode):
        this.client.room.sendAllBin(Identifiers.send.Leaf_Mouse_Skill, ByteArray().writeByte(1).writeInt(playerCode).toByteArray())

    def sendIceMouseSkill(this, playerCode, iced):
        this.client.room.sendAllBin(Identifiers.send.Iced_Mouse_Skill, ByteArray().writeInt(playerCode).writeBool(iced).toByteArray())

    def sendGravitationalSkill(this, seconds, id):
        this.client.room.sendAllBin(Identifiers.send.Gravitation_Skill, ByteArray().writeShort(seconds).writeInt(id).toByteArray())
        
    def sendGrapnelSkill(this, playerCode, px, py):
        this.client.room.sendAllBin(Identifiers.send.Grapnel_Mouse_Skill, ByteArray().writeInt(playerCode).writeShort(px).writeShort(py).toByteArray())
        
    def sendBonfireSkill(this, px, py, seconds):
        this.client.room.sendAllBin(Identifiers.send.Bonfire_Skill, ByteArray().writeShort(px).writeShort(py).writeByte(seconds).toByteArray())

    def sendEvolutionSkill(this, playerCode):
        this.client.room.sendAllBin(Identifiers.send.Shaman_Position, ByteArray().writeInt(playerCode).writeByte(0).toByteArray())

    def sendGatmanSkill(this, playerCode):
        this.client.room.sendAllBin(Identifiers.send.Gatman_Skill, ByteArray().writeInt(playerCode).writeByte(1).toByteArray())

    def sendShamanFly(this, fly):
        this.client.room.sendAllOthersBin(this.client, Identifiers.send.Shaman_Fly, ByteArray().writeInt(this.client.playerCode).writeBool(fly).toByteArray())
        
    def sendProjectionSkill(this, posX, posY, dir):
        this.client.room.sendAllOthersBin(this.client, Identifiers.send.Projection_Skill, ByteArray().writeShort(posX).writeShort(posY).writeShort(dir).toByteArray())

    def sendDemolitionSkill(this, objectID):
        this.client.room.sendAllBin(Identifiers.send.Demolition_Skill, ByteArray().writeInt(objectID).toByteArray())

    def sendConvertSkill(this, objectID):
        this.client.room.sendAllBin(Identifiers.send.Convert_Skill, ByteArray().writeInt(objectID).writeByte(0).toByteArray())

    def sendRecyclingSkill(this, id):
        this.client.room.sendAllBin(Identifiers.send.Recycling_Skill, ByteArray().writeShort(id).toByteArray())

    def sendAntigravitySkill(this, objectID):
        this.client.room.sendAllBin(Identifiers.send.Antigravity_Skill, ByteArray().writeInt(objectID).writeShort(0).toByteArray())

    def sendRestorativeSkill(this, objectID, id):
        this.client.room.sendAllBin(Identifiers.send.Restorative_Skill, ByteArray().writeInt(objectID).writeInt(id).toByteArray())

    def sendHandymouseSkill(this, handyMouseByte, objectID):
        this.client.room.sendAllBin(Identifiers.send.Handymouse_Skill, ByteArray().writeByte(handyMouseByte).writeInt(objectID).writeByte(this.client.room.lastHandymouse[1]).writeInt(this.client.room.lastHandymouse[0]).toByteArray())
