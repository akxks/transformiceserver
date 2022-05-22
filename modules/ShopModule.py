from ByteArray import ByteArray
from Identifiers import Identifiers

class ShopModule:
    def __init__(this, player, server):
        this.client = player
        this.server = player.server
        this.Cursor = player.Cursor

    def getShopLength(this):
        return 0 if this.client.shopItems == "" else len(this.client.shopItems.split(","))

    def checkUnlockShopTitle(this):
        if this.getShopLength() in this.server.ShopTitleListCheck:
            unlockedTitle = this.server.ShopTitleList[this.getShopLength()]
            stitle = str(unlockedTitle).split(".")

            this.client.checkAndRebuildTitleList("shop")
            this.client.sendUnlockedTitle(stitle[0], stitle[1])

            this.client.sendCompleteTitleList()
            this.client.sendTitleList()

    def checkAndRebuildBadges(this):
        rebuild = False
        for badgeNumber in this.server.ShopBadgesCheck:
            badge = this.server.ShopBadges[badgeNumber]
            if not str(badge) in this.client.shopBadges and this.checkInShop(badgeNumber):
                this.client.shopBadges.append(badge)
                rebuild = True

        if rebuild:
            tempBadges = []
            tempBadges.extend(this.client.shopBadges)
            this.client.shopBadges = []
            for badge in tempBadges:
                if not badge in this.client.shopBadges:
                    this.client.shopBadges.append(badge)

    def checkUnlockShopBadge(this, itemID):
        if not this.client.isGuest:
            if itemID in this.server.ShopBadgesCheck:
                unlockBadge = this.server.ShopBadges[itemID]
                this.sendUnlockedBadge(unlockBadge)
                this.checkAndRebuildBadges()

    def checkInShop(this, checkItem):
        if this.client.shopItems == "":
            return False
        else:
            splitedItems = this.client.shopItems.split(",")
            for shopItem in splitedItems:
                item = shopItem.split("_")[0] if "_" in shopItem else shopItem
                if checkItem == int(item):
                    return True
        return False

    def checkInShamanShop(this, checkItem):
        if this.client.shamanItems == "":
            return False
        else:
            splitedItems = this.client.shamanItems.split(",")
            for shopItem in splitedItems:
                item = shopItem.split("_")[0] if "_" in shopItem else shopItem
                if checkItem == int(item):
                    return True
        return False

    def checkInPlayerShop(this, type, username, checkItem):
        this.Cursor.execute("select " + type + " from Users where Username = ?", [username])
        rs = this.Cursor.fetchone()
        if rs:
            items = rs[0]
            if items == "":
                return False
            else:
                splitedItems = items.split(",")
                for shopItems in splitedItems:
                    item = shopItem.split("_")[0] if "_" in shopItem else shopItem
                    if checkItem == int(item):
                        return True
        return False

    def getItemCustomization(this, checkItem, isShamanShop):
        items = this.client.shamanItems if isShamanShop else this.client.shopItems
        if items == "":
            return ""
        else:
            splitedItems = items.split(",")
            for shopItem in splitedItems:
                if "_" in shopItem:
                    itemSplited = shopItem.split("_")
                    item = itemSplited[0]
                    custom = itemSplited[1] if len(itemSplited) >= 2 else ""
                else:
                    item = shopItem
                    custom = ""

                if int(item) == checkItem:
                    return "" if custom == "" else "_" + custom
        return ""

    def getShamanItemCustomization(this, code):
        items = this.client.shamanItems.split(",")
        for item in items:
            if "_" in item:
                itemSplited = item.split("_")
                realItem = itemSplited[0]
                custom = itemSplited[1] if len(itemSplited) >= 2 else ""
                realCustom = [] if custom == "" else custom.split("+")

                if code == int(realItem):
                    packet = ByteArray().writeByte(len(realCustom))

                    x = 0
                    while x < len(realCustom):
                        packet.writeInt(int(realCustom[x], 16))
                        x += 1
                    return packet.toByteArray()
        return chr(0)

    def getShopItemPrice(this, fullItem):
        itemStr = str(fullItem)
        itemCat = (0 if fullItem / 10000 == 1 else fullItem / 10000) if len(itemStr) > 4 else fullItem / 100
        item = int(itemStr[2 if len(itemStr) > 3 else 1:]) if len(itemStr) >= 3 else fullItem
        itemCheck = str(itemCat) + "|" + str(item)
        return this.getItemPromotion(fullItem, this.server.shopListCheck[itemCheck][1])
                
    def getShamanShopItemPrice(this, fullItem):
        return this.server.shamanShopListCheck[str(fullItem)][1]

    def getItemPromotion(this, itemCat, item, price):
        for promotion in this.server.shopPromotions:
            if promotion[0] == itemCat and promotion[1] == item:
                return int(promotion[2] / 100.0 * price)
        return price

    def sendShopInfo(this):            
        this.client.sendPacket(Identifiers.send.Shop_Info, ByteArray().writeInt(this.client.shopCheeses).writeInt(this.client.shopFraises).writeShort(0).toByteArray(), True)

    def sendCanGift(this):
        this.client.sendPacket(Identifiers.send.Can_Gift, ByteArray().writeInt(11).toByteArray(), True)

    def sendShopList(this, sendItems=True):
        shopItems = [] if this.client.shopItems == "" else this.client.shopItems.split(",")

        packet = ByteArray().writeInt(this.client.shopCheeses).writeInt(this.client.shopFraises).writeUTF(this.client.playerLook).writeInt(len(shopItems))
        for item in shopItems:
            if "_" in item:
                itemSplited = item.split("_")
                realItem = itemSplited[0]
                custom = itemSplited[1] if len(itemSplited) >= 2 else ""
                realCustom = [] if custom == "" else custom.split("+")

                packet.writeByte(len(realCustom)+1).writeInt(int(realItem))

                x = 0
                while x < len(realCustom):
                    packet.writeInt(int(realCustom[x], 16))
                    x += 1
            else:
                packet.writeByte(0).writeInt(int(item))

        shop = this.server.shopList if sendItems else []
        packet.writeInt(len(shop))

        for item in shop:
            value = item.split(",")
            packet.writeShort(int(value[0]))
            packet.writeShort(int(value[1])).writeByte(int(value[2])).writeByte(int(value[3])).writeByte(int(value[4])).writeInt(int(value[5])).writeInt(int(value[6])).writeShort(0)
                
         
        looks = [] 

        packet.writeByte(len(looks))
        for look in looks:
            packet.writeUTF(look[0])
            packet.writeByte(look[1])
            
        packet.writeByte(0)
        
        packet.writeByte(len(this.client.clothes))

        for clothe in this.client.clothes:
            clotheSplited = clothe.split("/")
            packet.writeUTF(clotheSplited[1] + ";" + clotheSplited[2] + ";" + clotheSplited[3])    

        shamanItems = [] if this.client.shamanItems == "" else this.client.shamanItems.split(",")
        packet.writeShort(len(shamanItems))



        for item in shamanItems:
            if "_" in item:
                itemSplited = item.split("_")
                realItem = itemSplited[0]
                custom = itemSplited[1] if len(itemSplited) >= 2 else ""
                realCustom = [] if custom == "" else custom.split("+")

                packet.writeShort(int(realItem))

                packet.writeBool(item in this.client.shamanLook.split(",")).writeByte(len(realCustom)+1)

                x = 0
                while x < len(realCustom):
                    packet.writeInt(int(realCustom[x], 16))
                    x += 1
            else:
                packet.writeShort(int(item)).writeBool(item in this.client.shamanLook.split(",")).writeByte(0)

        shamanShop = this.server.shamanShopList if sendItems else []
        packet.writeShort(len(shamanShop))

        for item in shamanShop:
            value = item.split(",")
            packet.writeInt(int(value[0])).writeByte(int(value[1])).writeByte(int(value[2])).writeInt(int(value[3])).writeShort(int(value[4]))

        this.client.sendPacket(Identifiers.send.Shop_List, packet.toByteArray(), True)
                        
    def sendShamanItems(this):
        packet = ByteArray()
        
        shamanItems = [] if this.client.shamanItems == "" else this.client.shamanItems.split(",")
        packet.writeShort(len(shamanItems))

        for item in shamanItems:
            if "_" in item:
                itemSplited = item.split("_")
                realItem = itemSplited[0]
                custom = itemSplited[1] if len(itemSplited) >= 2 else ""
                realCustom = [] if custom == "" else custom.split("+")

                packet.writeShort(int(realItem))
                packet.writeBool(item in this.client.shamanLook.split(","))
                packet.writeByte(len(realCustom)+1)

                x = 0
                while x < len(realCustom):
                    packet.writeInt(int(realCustom[x], 16))
                    x += 1
            else:
                packet.writeShort(int(item)).writeBool(item in this.client.shamanLook.split(",")).writeByte(0)
                        
        this.client.sendPacket(Identifiers.send.Shaman_Items, packet.toByteArray(), True)

    def sendLookChange(this):
        packet = ByteArray()
        skinID, clothes = this.client.playerLook.split(";")
        clothes = clothes.split(",")

        packet.writeByte(int(skinID))

        for item in clothes:
            if "_" in item:
                itemID, custom = item.split("_")
                custom = custom.split("+") if custom else []

                packet.writeInt(int(itemID))
                packet.writeByte(len(custom))

                x = 0
                while x < len(custom):
                    packet.writeInt(int(custom[x], 16))
                    x += 1
            else:
                packet.writeInt(int(item)).writeByte(0)

        packet.writeInt(int(this.client.MouseColor, 16))
        this.client.sendPacket(Identifiers.send.Look_Change, packet.toByteArray(), True)

    def sendShamanLook(this):
        packet = ByteArray()
        items = ByteArray()
        shamanLook = this.client.shamanLook.split(",")
        count = 0

        for item in shamanLook:
            realItem = int(item.split("_")[0]) if "_" in item else int(item)
            if realItem != 0:
                items.writeShort(realItem)
                count += 1

        this.client.sendPacket(Identifiers.send.Shaman_Look, packet.writeShort(count).writeBytes(items.toByteArray()).toByteArray(), True)

    def sendItemBuy(this, fullItem):
        this.client.sendPacket(Identifiers.send.Item_Buy, ByteArray().writeShort(fullItem).writeByte(1).toByteArray(), True)

    def sendUnlockedBadge(this, badge):
        this.client.room.sendAllBin(Identifiers.send.Unlocked_Badge, ByteArray().writeInt(this.client.playerCode).writeShort(badge).toByteArray())

    def sendGiftResult(this, code, username):
        this.client.room.sendAllBin(Identifiers.send.Gift_Result, ByteArray().writeByte(code).writeUTF(username).writeByte(0).writeShort(323).toByteArray())

    def buyItem(this, packet):
        p = ByteArray(packet)
        fullItem = p.readShort()
        withFraises = p.readBool()
        itemStr = str(fullItem)
        itemCat = (0 if fullItem / 10000 == 1 else fullItem /10000) if len(itemStr) > 4 else fullItem / 100
        item = int(itemStr[2 if len(itemStr) > 3 else 1:]) if len(itemStr) >= 3 else fullItem
        itemCheck = str(itemCat) + "|" + str(item)

        this.client.shopItems += str(fullItem) if this.client.shopItems == "" else "," + str(fullItem)
        price = this.getItemPromotion(itemCat, item, this.server.shopListCheck[str(itemCat) + "|" + str(item)][1 if withFraises else 0])
        
        if withFraises:
            this.client.shopFraises -= price
        else:
            this.client.shopCheeses -= price

        this.sendItemBuy(fullItem)
        this.sendShopList(True)
        this.client.sendAnimZelda(0, fullItem)
        this.checkUnlockShopTitle()
        this.checkUnlockShopBadge(fullItem)

    def equipItem(this, packet):
        p = ByteArray(packet)
        fullItem = p.readInt()
        itemStr = str(fullItem)
        itemCat = (0 if fullItem / 10000 == 1 else fullItem /10000) if len(itemStr) > 4 else fullItem / 100
        item = int(itemStr[2 if len(itemStr) > 3 else 1:]) if len(itemStr) >= 3 else fullItem
        itemStr = str(item)

        equip = str(item) + this.getItemCustomization(fullItem, False)

        lookList = this.client.playerLook.split(";")
        lookItems = lookList[1].split(",")
        lookCheckList = lookItems[:]
        idx = 0
        while idx < len(lookCheckList):
            lookCheckList[idx] = lookCheckList[idx].split("_")[0] if "_" in lookCheckList[idx] else lookCheckList[idx]
            idx += 1

        if itemCat <= 10:
            if lookCheckList[itemCat] == itemStr:
                lookItems[itemCat] = "0"
            else:
                lookItems[itemCat] = str(equip)

        elif itemCat == 21:
            lookList[0] = "1"
            color = "bd9067" if item == 0 else "593618" if item == 1 else "8c887f" if item == 2 else "dfd8ce" if item == 3 else "4e443a" if item == 4 else "e3c07e" if item == 5 else "272220" if item == 6 else "78583a"
            this.client.MouseColor = "78583a" if this.client.MouseColor == color else color
        else:
            if lookList[0] == itemStr:
                lookList[0] = "1"
            else:
                lookList[0] = itemStr

        this.client.playerLook = lookList[0] + ";" + ",".join(map(str, lookItems))
        this.sendLookChange()

    def customItemBuy(this, packet):
        p = ByteArray(packet)
        fullItem, withFraises = p.readShort(), p.readBool()

        items = this.client.shopItems.split(",")
        for shopItem in items:
            item = shopItem.split("_")[0] if "_" in shopItem else shopItem
            if fullItem == int(item):
                items[items.index(shopItem)] = shopItem + "_"
                break

        this.client.shopItems = ",".join(items)

        if withFraises:
            this.client.shopFraises -= 20
        else:
            this.client.shopCheeses -= 2000
                
        this.sendShopList(False)

    def customItem(this, packet):
        p = ByteArray(packet)
        fullItem, length = p.readShort(), p.readByte()
        custom = length
        customs = list()

        i = 0
        while i < length:
            customs.append(p.readInt())
            i += 1

        items = this.client.shopItems.split(",")
        for shopItem in items:
            sItem = shopItem.split("_")[0] if "_" in shopItem else shopItem
            if fullItem == int(sItem):
                newCustoms = map(lambda color: "%06X" %(0xffffff & color), customs)

                items[items.index(shopItem)] = sItem + "_" + "+".join(newCustoms)
                this.client.shopItems = ",".join(items)

                itemStr = str(fullItem)
                itemCat = (0 if fullItem / 10000 == 1 else fullItem /10000) if len(itemStr) > 4 else fullItem / 100
                item = int(itemStr[2 if len(itemStr) > 3 else 1:]) if len(itemStr) >= 3 else fullItem
                equip = str(item) + this.getItemCustomization(fullItem, False)

                lookList = this.client.playerLook.split(";")
                lookItems = lookList[1].split(",")

                if "_" in lookItems[itemCat]:
                    if lookItems[itemCat].split("_")[0] == itemStr:
                        lookItems[itemCat] = equip
                                
                elif lookItems[itemCat] == itemStr:
                    lookItems[itemCat] = equip

                this.client.playerLook = lookList[0] + ";" + ",".join(lookItems)
                this.sendShopList(False)
                this.sendLookChange()
                break

    def buyShamanItem(this, packet):
        p = ByteArray(packet)
        fullItem, withFraises = p.readShort(), p.readBool()
        itemStr = str(fullItem)
        itemCat = int(itemStr[len(itemStr)-2:])
        item = int(itemStr[:len(itemStr)-2])
        price = this.server.shamanShopListCheck[itemStr][1 if withFraises else 0]

        this.client.shamanItems += str(fullItem) if this.client.shamanItems == "" else "," + str(fullItem)

        if withFraises:
            this.client.shopFraises -= price
        else:
            this.client.shopCheeses -= price

        this.sendShopList(False)
        this.client.sendAnimZelda(1, fullItem)

    def equipShamanItem(this, packet):
        p = ByteArray(packet)
        fullItem = p.readInt()
        item = str(fullItem) + this.getItemCustomization(fullItem, True)
        itemStr = str(fullItem)
        itemCat = int(itemStr[:len(itemStr)-2])
        index = itemCat if itemCat <= 4 else itemCat - 1 if itemCat <= 7 else 7 if itemCat == 10 else 8 if itemCat == 17 else 9
        index -= 1
        lookItems = this.client.shamanLook.split(",")

        if "_" in lookItems[index]:
            if lookItems[index].split("_")[0] == itemStr:
                lookItems[index] = "0"
            else:
                lookItems[index] = item

        elif lookItems[index] == itemStr:
            lookItems[index] = "0"
        else:
            lookItems[index] = item

        this.client.shamanLook = ",".join(lookItems)
        this.sendShamanLook()

    def customShamanItemBuy(this, packet):
        p = ByteArray(packet)
        fullItem, withFraises = p.readShort(), p.readBool()

        items = this.client.shamanItems.split(",")
        for shopItem in items:
            item = shopItem.split("_")[0] if "_" in shopItem else shopItem
            if fullItem == int(item):
                items[items.index(shopItem)] = shopItem + "_"
                break

        this.client.shamanItems = ",".join(items)

        if withFraises:
            this.client.shopFraises -= 150
        else:
            this.client.shopCheeses -= 4000
                
        this.sendShopList(False)

    def customShamanItem(this, packet):
        p = ByteArray(packet)
        fullItem, length = p.readShort(), p.readByte()
        customs = list()

        i = 0
        while i < length:
            customs.append(p.readInt())
            i += 1

        items = this.client.shamanItems.split(",")
        for shopItem in items:
            sItem = shopItem.split("_")[0] if "_" in shopItem else shopItem
            if fullItem == int(sItem):
                newCustoms = map(lambda color: "%06X" %(0xffffff & color), customs)

                items[items.index(shopItem)] = sItem + "_" + "+".join(newCustoms)
                this.client.shamanItems = ",".join(items)

                item = str(fullItem) + this.getItemCustomization(fullItem, True)
                itemStr = str(fullItem)
                itemCat = int(itemStr[len(itemStr)-2:])
                index = itemCat if itemCat <= 4 else itemCat - 1 if itemCat <= 7 else 7 if itemCat == 10 else 8 if itemCat == 17 else 9
                index -= 1
                lookItems = this.client.shamanLook.split(",")

                if "_" in lookItems[index]:
                    if lookItems[index].split("_")[0] == itemStr:
                        lookItems[index] = item
                                
                elif lookItems[index] == itemStr:
                    lookItems[index] = item

                this.client.shamanLook = ",".join(lookItems)
                this.sendShopList(False)
                this.sendShamanLook()
                break

    def buyClothe(this, packet):
        p = ByteArray(packet)
        clotheID, withFraises = p.readByte(), p.readBool()

        this.client.clothes.append("%02d/%s/%s/%s" %(clotheID, "1;0,0,0,0,0,0,0,0,0", "78583a", "fade55" if this.client.shamanSaves >= 1000 else "95d9d6"))

        if withFraises:
            this.client.shopFraises -= 5 if clotheID == 0 else 50 if clotheID == 1 else 100
        else:
            this.client.shopFraises -= 40 if clotheID == 0 else 1000 if clotheID == 1 else 2000 if clotheID == 2 else 4000

        this.sendShopList(False)

    def equipClothe(this, packet):
        p = ByteArray(packet)
        clotheID = p.readByte()
        for clothe in this.client.clothes:
            values = clothe.split("/")
            if values[0] == "%02d" %(clotheID):
                this.client.playerLook = values[1]
                this.client.MouseColor = values[2]
                this.client.ShamanColor = values[3]
                break
                
        this.sendLookChange()
        this.sendShopList(False)

    def saveClothe(this, packet):
        p = ByteArray(packet)
        clotheID = p.readByte()
        for clothe in this.client.clothes:
            values = clothe.split("/")
            if values[0] == "%02d" %(clotheID):
                values[1] = this.client.playerLook
                values[2] = this.client.MouseColor
                values[3] = this.client.ShamanColor
                this.client.clothes[this.client.clothes.index(clothe)] = "/".join(values)
                break

        this.sendShopList(False)

    def sendGift(this, packet):
        p = ByteArray(packet)
        username, isShamanItem, fullItem, message = p.readUTF(), p.readBool(), p.readShort(), p.readUTF()

        if not this.server.checkExistingUser(username):
            this.sendGiftResult(1, username)
        else:
            player = this.server.players.get(username)
            if player != None:
                found = player.shopModule.checkInShamanShop(fullItem) if isShamanItem else player.shopModule.checkInShop(fullItem)

                if found:
                    this.sendGiftResult(2, username)
                else:
                    this.server.lastGiftID += 1

                    player.sendPacket(Identifiers.send.Shop_Gift, ByteArray().writeInt(this.server.lastGiftID).writeUTF(this.client.Username).writeUTF(this.client.playerLook).writeBool(isShamanItem).writeShort(fullItem).writeUTF(message).toByteArray(), True)

                    this.sendGiftResult(0, username)
                    this.server.shopGifts[this.server.lastGiftID] = [this.client.Username, isShamanItem, fullItem]
                    this.client.shopFraises -= this.getShamanShopItemPrice(fullItem) if isShamanItem else this.getShopItemPrice(fullItem)
                    this.sendShopList(False)
            else:
                found = this.checkInPlayerShop("ShamanItems" if isShamanItem else "ShopItems", username, fullItem)

                if found:
                    this.sendGiftResult(2, username)
                else:
                    this.Cursor.execute("select LastReceivedGifts from Users where Username = ?", [username])
                    rs = this.Cursor.fetchone()
                    lastReceivedGifts = rs["LastReceivedGifts"]

                lastReceivedGifts = ("" if lastReceivedGifts == "" else lastReceivedGifts + "/") + "[" + "|".join(map(str, [this.client.Username, this.client.playerLook, isShamanItem, fullItem, message]))

                this.Cursor.execute("update Users set LastReceivedGifts = ? where Username = ?", [lastReceivedGifts, username])

    def giftResult(this, packet):
        p = ByteArray(packet)
        loc1, giftID, isOpen, message, loc2 = p.readShort(), p.readShort(), p.readBool(), p.readUTF(), p.readByte()

        if isOpen:
            values = this.server.shopGifts[int(giftID)]
            player = this.server.players.get(str(values[0]))
            if player != None:
                player.sendMessageLangue("$DonItemRecu", this.client.Username)

            isShamanItem = bool(values[1])
            fullItem = int(values[2])

            if isShamanItem:
                itemStr = str(fullItem)
                itemCat = int(itemStr[len(itemStr)-2:])
                item = int(itemStr[:len(itemStr)-2])
                this.client.shamanItems += str(fullItem) if this.client.shamanItems == "" else "," + str(fullItem)
                this.sendShopList(False)
                this.client.sendAnimZelda(1, fullItem)
            else:
                itemStr = str(fullItem)
                itemCat = (0 if fullItem / 10000 == 1 else fullItem / 10000) if len(itemStr) > 4 else fullItem / 100
                item = int(itemStr[2 if len(itemStr) > 3 else 1:]) if len(itemStr) >= 3 else fullItem
                this.client.shopItems += str(fullItem) if this.client.shopItems == "" else "," + str(fullItem)
                this.client.sendAnimZelda(itemCat, item)
                this.checkUnlockShopTitle()
                this.checkUnlockShopBadge(fullItem)

        elif not message == "":
            values = this.server.shopGifts[int(giftID)]
            player = this.server.players.get(str(values[0]))
            if player != None:
                player.sendPacket(Identifiers.send.Shop_GIft_Message, ByteArray().writeShort(0).writeShort(giftID).writeUTF(this.client.Username).writeBool(bool(values[1])).writeShort(int(values[2])).writeUTF(message).writeUTF(this.client.playerLook).toByteArray(), True)
            else:
                this.Cursor.execute("select LastReceivedMessages from Users where Username = ?", [str(values[0])])
                rs = this.Cursor.fetchone()
                lastReceivedMessages = rs["LastReceivedMessages"]

                lastReceivedMessages = ("" if lastReceivedMessages == "" else lastReceivedMessages + "/") + "[" + "|".join(map(str, [this.client.Username, values[1], values[2], this.client.playerLook, message])) + "]"

                this.Cursor.execute("update Users set LastReceivedMessages = ? where Username = ?", [lastReceivedMessages, str(values[0])])

    def checkGiftsAndMessages(this, lastReceivedGifts, lastReceivedMessages):
        needUpdate = False
        gifts = lastReceivedGifts.split("/")
        for gift in gifts:
            if not gift == "":
                values = gift[gift.index("[") + 1:gift.index("]")].split("|", 4)
                this.server.lastGiftId += 1
                this.client.sendPacket(Identifiers.send.Shop_Gift, ByteArray().writeInt(this.server.lastGiftID).writeUTF(values[0]).writeUTF(values[1]).writeBool(bool(values[2])).writeShort(int(values[3])).writeUTF(values[4] if len(values) > 4 else "").toByteArray(), True)
                this.server.shopGifts[this.server.lastGiftID] = [values[0], bool(values[2]), int(values[3])]
                needUpdate = True

        messages = lastReceivedMessages.split("/")
        for message in messages:
            if not message == "":
                values = message[message.index("[") + 1:message.index("]")].split("|", 4)
                this.client.sendPacket(Identifiers.send.Shop_GIft_Message, ByteArray().writeShort(0).writeShort(0).writeUTF(values[0]).writeBool(bool(values[1])).writeShort(int(values[2])).writeUTF(values[4]).writeUTF(values[3]).toByteArray(), True)
                needUpdate = True

        if needUpdate:
            this.Cursor.execute("update Users set LastReceivedGifts = ?, LastReceivedMessages = ? where Username = ?", ["", "", this.client.Username])
