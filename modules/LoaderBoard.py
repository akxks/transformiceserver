#coding: utf-8
import time, random, thread

class shop:
    def __init__(this, client, server):
        this.client = client
        this.server = client.server
        currentPage = 1

    def getText(this, object, *params):
        keys = object.split(".")
        json = this.server.menu["texts"][this.client.Langue if this.client.Langue in this.server.menu["texts"] else "EN"]
        i = 0
        while i < len(keys):
            key = keys[i]
            if i == len(keys) - 1:
                text = json[key]
                count = 0
                while count < len(params):
                    text = text.replace("%" + str(count + 1), str(params[count]))
                    count += 1

                return text
            else:
                json = json[key]
            i += 1
        return ""

    def open(this):
        this.close()
        this.client.room.addTextArea(10001, "<img src='http://i.imgur.com/HvXJhLq.png'>", this.client.Username, 115, 25, 540, 320, 0, 0, 0, False)
        this.client.room.addTextArea(10002, this.getText("shop.main", this.client.Username, this.client.iceCoins), this.client.Username, 250, 80, 400, 260, 0, 0, 0, False)
        this.client.room.addTextArea(10003, this.getText("shop.menu"), this.client.Username, 145, 70, 100, 260, 0, 0, 0, False)
        this.client.room.addTextArea(10004, "<R><b><a href='event:shop:close'>X</a></b></font>", this.client.Username, 148, 83, 0, 0, 0, 0, 0, False)

    def changeTab(this, tab):
        this.client.room.updateTextArea(10002, this.getText("shop.main" if tab == 1 else "shop.profileTab" if tab == 2 else "shop.titlesTab" if tab == 3 else "shop.tokensTab" if tab == 4 else "shop.main", this.client.Username, this.client.iceCoins), this.client.Username)

    def buyItem(this, type, id):
        typeName = "profile" if type == 1 else "title" if type == 2 else "token"
        item = this.getText("shop.items." + str(typeName) + "." + str(id))
        price = this.server.menu["shop"][typeName][str(id)]
        this.client.room.updateTextArea(10002, this.getText("shop.confirmBuy", item, price, type, id, type + 1), this.client.Username)

    def confirmBuyItem(this, type, id):
        typeName = "profile" if type == 1 else "title" if type == 2 else "token"
        item = this.getText("shop.items." + str(typeName) + "." + str(id))
        price = this.server.menu["shop"][typeName][str(id)]
        canBuy = True

        if this.client.iceCoins < price:
            canBuy = False
            this.client.room.updateTextArea(10002, this.getText("shop.buyErrorNoCoins", item, type + 1), this.client.Username)
        elif type == 2:
            if id == 1 and 1000.1 in this.client.specialTitleList:
                canBuy = False
                this.client.room.updateTextArea(10002, this.getText("shop.buyErrorHas", item, type + 1), this.client.Username)

        if canBuy:
            this.client.room.updateTextArea(10002, this.getText("shop.buySucess", item, type + 1), this.client.Username)
            this.client.iceCoins -= price
            if type == 1:
                if id == 1:
                    this.client.shopCheeses += 2500
                    this.client.shopFraises += 1500
                elif id == 2:
                    this.client.firstCount += 100
                    this.client.cheeseCount += 100
                    this.client.bootcampCount += 50
                elif id == 3:
                    this.client.firstCount += 200
                    this.client.cheeseCount += 200
                    this.client.shamanSaves += 300
                elif id == 4:
                    this.client.firstCount += 200
                    this.client.cheeseCount += 200
                    this.client.shamanSaves += 400
                    this.client.bootcampCount += 100
                elif id == 5:
                    this.client.shamanSaves += 600
                    this.client.hardModeSaves += 300
                    this.client.divineModeSaves += 200

            elif type == 2:
                if id == 1:
                  titleID = 71.1 if id == 1 else 0.1
                  this.client.specialTitleList.append(titleID);
                  this.client.sendUnlockedTitle(str(int(titleID)), "1")
                  this.client.sendCompleteTitleList()
                  this.client.sendTitleList()
                if id == 2:
                  titleID = 230.1 if id == 1 else 230.1
                  this.client.specialTitleList.append(titleID);
                  this.client.sendUnlockedTitle(str(int(titleID)), "1")
                  this.client.sendCompleteTitleList()
                  this.client.sendTitleList()
                if id == 3:
                  titleID = 229.1 if id == 1 else 229.1
                  this.client.specialTitleList.append(titleID);
                  this.client.sendUnlockedTitle(str(int(titleID)), "1")
                  this.client.sendCompleteTitleList()
                  this.client.sendTitleList()
                if id == 4:
                  titleID = 114.1 if id == 1 else 114.1
                  this.client.specialTitleList.append(titleID);
                  this.client.sendUnlockedTitle(str(int(titleID)), "1")
                  this.client.sendCompleteTitleList()
                  this.client.sendTitleList()
                if id == 5:
                  titleID = 112.1 if id == 1 else 112.1
                  this.client.specialTitleList.append(titleID);
                  this.client.sendUnlockedTitle(str(int(titleID)), "1")
                  this.client.sendCompleteTitleList()
                  this.client.sendTitleList()
                if id == 6:
                  titleID = 451.1 if id == 1 else 451.1
                  this.client.specialTitleList.append(titleID);
                  this.client.sendUnlockedTitle(str(int(titleID)), "1")
                  this.client.sendCompleteTitleList()
                  this.client.sendTitleList()   

            elif type == 3:
                10 if this.client.iceTokens + id == 1 else 20 if id == 2 else 30 if id == 3 else 40 if id == 4 else 50 if id == 5 else 0

    def close(this):
        i = 10001
        while i <= 10004:
            this.client.room.removeTextArea(i, this.client.Username)
            i += 1

class spinTheWheel:
    def __init__(this, client, server):
        this.client = client
        this.server = client.server
        this.lastResult = -1
        this.isRunning = False

    def getText(this, object, *params):
        keys = object.split(".")
        json = this.server.menu["texts"][this.client.Langue if this.client.Langue in this.server.menu["texts"] else "EN"]
        i = 0
        while i < len(keys):
            key = keys[i]
            if i == len(keys) - 1:
                text = json[key]
                count = 0
                while count < len(params):
                    text = text.replace("%" + str(count + 1), str(params[count]))
                    count += 1

                return text
            else:
                json = json[key]
            i += 1
        return ""

class vipInfo:
    def __init__(this, client, server):
        this.client = client
        this.server = client.server

    def getText(this, object, *params):
        keys = object.split(".")
        json = this.server.menu["texts"][this.client.Langue if this.client.Langue in this.server.menu["texts"] else "EN"]
        i = 0
        while i < len(keys):
            key = keys[i]
            if i == len(keys) - 1:
                text = json[key]
                count = 0
                while count < len(params):
                    text = text.replace("%" + str(count + 1), str(params[count]))
                    count += 1

                return text
            else:
                json = json[key]
            i += 1
        return ""

    def open(this):
        this.close()
        this.client.room.addTextArea(10033, "<img src='http://i.imgur.com/ahiK0Eg.png'>", this.client.Username, 155, 45, 500, 450, 0x27373f, 0x31454f, 0, False)
        this.client.room.addTextArea(10034, "<VP>" + this.getText("vipInfo.menu.1"), this.client.Username, 192, 75, 70, 18, 0x27373f, 0x31454f, 0, False)
        this.client.room.addTextArea(10035, "<J>" + this.getText("vipInfo.menu.2"), this.client.Username, 192, 107, 70, 18, 0x27373f, 0x31454f, 0, False)
        this.client.room.addTextArea(10036, "<J>" + this.getText("vipInfo.menu.3"), this.client.Username, 192, 139, 70, 18, 0x27373f, 0x31454f, 0, False)
        this.client.room.addTextArea(10037, this.getText("vipInfo.menu.4"), this.client.Username, 192, 173, 70, 18, 0x27373f, 0x31454f, 0, False)
        this.client.room.addTextArea(10038, this.getText("vipInfo.main", this.client.Username), this.client.Username, 260, 80, 300, 260, 0x27373f, 0x31454f, 0, False)

    def changeTab(this, tab):
        this.client.room.updateTextArea(10034, ("<VP>" if tab == 1 else "<J>") + this.getText("vipInfo.menu.1"), this.client.Username)
        this.client.room.updateTextArea(10035, ("<VP>" if tab == 2 else "<J>") + this.getText("vipInfo.menu.2"), this.client.Username)
        this.client.room.updateTextArea(10036, ("<VP>" if tab == 3 else "<J>") + this.getText("vipInfo.menu.3"), this.client.Username)
        if tab == 1:
            this.client.room.updateTextArea(10038, this.getText("vipInfo.main", this.client.Username), this.client.Username)
        elif tab == 2:
            this.client.room.updateTextArea(10038, this.getText("vipInfo.functions"), this.client.Username)
        elif tab == 3:
            vips = []
            for player in this.server.players.values():
                if player.privLevel == 2:
                    vips.append(player.Username)

            names = "<p align='center'><ROSE><b>Vips Onlines</b>\n\n<N"
            if len(vips) == 0:
                names += this.getText("vipInfo.noVips")
            else:
                for username in vips:
                    names += "<font color='#00CFFF'" +str(username)+ "</font>\n"

            this.client.room.updateTextArea(10038, names + "</p>", this.client.Username)

    def close(this):
        i = 10033
        while i <= 10038:
            this.client.room.removeTextArea(i, this.client.Username)
            i += 1

class consumablesShop:
    def __init__(this, client, server):
        this.client = client
        this.server = client.server
        this.itemsCache = {}
        this.cheesesCount = 0
        this.fraisesCount = 0
        this.currentPage = 0

    def getText(this, object, *params):
        keys = object.split(".")
        json = this.server.menu["texts"][this.client.Langue if this.client.Langue in this.server.menu["texts"] else "EN"]
        i = 0
        while i < len(keys):
            key = keys[i]
            if i == len(keys) - 1:
                text = json[key]
                count = 0
                while count < len(params):
                    text = text.replace("%" + str(count + 1), str(params[count]))
                    count += 1

                return text
            else:
                json = json[key]
            i += 1
        return ""

    def open(this):
        this.currentPage = 1
        this.client.room.addTextArea(10039, "<img src='http://i.imgur.com/k6luqkk.png' hspace='0' vspace='-2'>", this.client.Username, 180, 15, 455, 370, 0, 0, 0, False)
        consumables = this.server.menu["consumables"]

        slot = 0
        while slot < 6:
            if slot >= len(consumables):
                break
            
            consumable = consumables[str(slot)]
            this.client.room.addTextArea(10040 + slot, "<img src='http://www.novaeramice.com.br/consumablesShop/getItem.php?cheeses=%s&fraises=%s&id=%s' hspace='-2' vspace='0'>" %(consumable[1], consumable[2], consumable[0]), this.client.Username, (200 + (140 * slot)) - (420 * (slot / 3)), 95 + (110 * (slot / 3)), 130, 105, 0, 0, 0, False)
            this.client.room.addTextArea(10046 + slot, "<p align='center'><CH2>" + ("<a href='event:consumablesShop:removeItem-1-" + str(slot) + "'>" if this.itemsCache.has_key(consumable[0]) else "") + "-" + ("</a>" if this.itemsCache.has_key(consumable[0]) else "") + "    <CEP>" + (this.itemsCache[consumable[0]] if this.itemsCache.has_key(consumable[0]) else "0") + "   <CH2>" + ((("<a href='event:consumablesShop:addItem-1-" + str(slot) + "'>" if this.itemsCache[consumable[0]] < (80 - (this.client.playerConsumables[consumable[0]] if this.client.playerConsumables.has_key(consumable[0]) else 0)) else "") if this.itemsCache.has_key(consumable[0]) else "<a href='event:consumablesShop:addItem-1-" + str(slot) + "'>") if (this.client.playerConsumables[consumable[0]] < 80 if this.client.playerConsumables.has_key(consumable[0]) else True) else "") + "+" + ((("</a>" if this.itemsCache[consumable[0]] < (80 - (this.client.playerConsumables[consumable[0]] if this.client.playerConsumables.has_key(consumable[0]) else 0)) else "") if this.itemsCache.has_key(consumable[0]) else "</a>") if (this.client.playerConsumables[consumable[0]] < 80 if this.client.playerConsumables.has_key(consumable[0]) else True) else "") + "</p>", this.client.Username, (210 + (140 * slot)) - (420 * (slot / 3)), 170 + (110 * (slot / 3)), 76, 20, 0, 0, 0, False)
            slot += 1

        this.client.room.addTextArea(10052, "", this.client.Username, 210, 340, 16, 16, 0x000001, 0x000001, 100, False)
        this.client.room.addTextArea(10053, "<p align='center'><BL><b>&lt;</b></p>", this.client.Username, 210, 339, 18, 16, 0x324650, 0x324650, 100, False);
        this.client.room.addTextArea(10054, "", this.client.Username, 250, 340, 16, 16, 0x000001, 0x000001, 100, False)
        this.client.room.addTextArea(10055, "<p align='center'>" + ("<N><a href='event:consumablesShop:changePage-2'>" if (len(consumables) / 6 + 1) > 1 else "<BL>") + "<b>&gt;</b>" + ("</a>" if (len(consumables) % 6 + 1) > 1 else "") + "</p>", this.client.Username, 250, 339, 18, 16, 0x324650, 0x324650, 100, False)
        this.client.room.addTextArea(10056, this.getText("consumablesShop.endBuy"), this.client.Username, 335, 339, 150, 16, 0x324650, 0x324650, 100, False)
        this.client.room.addTextArea(10057, "<img src='http://www.novaeramice.com.br/consumablesShop/price.png' hspace='0' vspace='0'>", this.client.Username, 550, 315, 20, 45, 0x000001, 0x000001, 0, False)
        this.client.room.addTextArea(10058, "<b><font size='13'><J>%s</font>\n<font size='7'>\n</font><font size='13'><R>%s</font></b>" %(this.cheesesCount, this.fraisesCount), this.client.Username, 575, 315, 45, 45, 0x000001, 0x000001, 0, False)
        this.client.room.addTextArea(10059, "<R><b><a href='event:consumablesShop:close'>X</a></b></font>", this.client.Username, 192, 60, 20, 20, 0x27373f, 0x27373f, 0, False)

    def changePage(this, page):
        isCancel = page == -1
        page = this.currentPage if isCancel else page
        this.currentPage = page
        i = 10040
        while i <= 10051:
            this.client.room.removeTextArea(i, this.client.Username)
            i += 1

        i = 10060
        while i <= 10065:
            this.client.room.removeTextArea(i, this.client.Username)
            i += 1

        consumables = this.server.menu["consumables"]

        slot = (page - 1) * 6
        while slot < ((page - 1) * 6) + 6:
            if slot >= len(consumables):
                break

            consumable = consumables[str(slot)]
            this.client.room.addTextArea(10040 + (slot % 6), "<img src='http://www.novaeramice.com.br/consumablesShop/getItem.php?cheeses=%s&fraises=%s&id=%s' hspace='-2' vspace='0'>" %(consumable[1], consumable[2], consumable[0]), this.client.Username, (200 + (140 * (slot % 6))) - (420 * ((slot % 6) / 3)), 95 + (110 * ((slot % 6) / 3)), 130, 105, 0, 0, 0, False)
            this.client.room.addTextArea(10046 + (slot % 6), "<p align='center'><CH2>" + ("<a href='event:consumablesShop:removeItem-" + str(page) + "-" + str(slot % 6) + "'>" if this.itemsCache.has_key(consumable[0]) else "") + "-" + ("</a>" if this.itemsCache.has_key(consumable[0]) else "") + "    <CEP>" + (str(this.itemsCache[consumable[0]]) if this.itemsCache.has_key(consumable[0]) else "0") + "   <CH2>" + ((("<a href='event:consumablesShop:addItem-" + str(page) + "-" + str((slot % 6)) + "'>" if this.itemsCache[consumable[0]] < (80 - (this.client.playerConsumables[consumable[0]] if this.client.playerConsumables.has_key(consumable[0]) else 0)) else "") if this.itemsCache.has_key(consumable[0]) else "<a href='event:consumablesShop:addItem-" + str(page) + "-" + str((slot % 6)) + "'>") if (this.client.playerConsumables[consumable[0]] < 80 if this.client.playerConsumables.has_key(consumable[0]) else True) else "") + "+" + ((("</a>" if this.itemsCache[consumable[0]] < (80 - (this.client.playerConsumables[consumable[0]] if this.client.playerConsumables.has_key(consumable[0]) else 0)) else "") if this.itemsCache.has_key(consumable[0]) else "</a>") if (this.client.playerConsumables[consumable[0]] < 80 if this.client.playerConsumables.has_key(consumable[0]) else True) else "") + "</p>", this.client.Username, (210 + (140 * (slot % 6))) - (420 * ((slot % 6) / 3)), 170 + (110 * ((slot % 6) / 3)), 76, 20, 0, 0, 0, False)
            slot += 1

        if not isCancel:
            this.client.room.updateTextArea(10053, "<p align='center'>" + (("<N><a href='event:consumablesShop:changePage-" + str((page - 1)) + "'>") if page > 1 else "<BL>") + "<b>&lt;</b>" + ("</a>" if page == 0 else "") + "</p>", this.client.Username)
            this.client.room.updateTextArea(10055, "<p align='center'>" + ("<N><a href='event:consumablesShop:changePage-" + str((page + 1)) + "'>" if (page < len(consumables) / 6 + 1) else "<BL>") + "<b>&gt;</b>" + ("</a>" if page == 0 else "") + "</p>", this.client.Username)
        else:
            this.client.room.addTextArea(10052, "", this.client.Username, 210, 340, 16, 16, 0x000001, 0x000001, 100, False)
            this.client.room.addTextArea(10053, "<p align='center'>" + (("<N><a href='event:consumablesShop:changePage-" + str((page - 1)) + "'>") if page > 1 else "<BL>") + "<b>&lt;</b>" + ("</a>" if page == 0 else "") + "</p>", this.client.Username, 210, 339, 18, 16, 0x324650, 0x324650, 100, False)
            this.client.room.addTextArea(10054, "", this.client.Username, 250, 340, 16, 16, 0x000001, 0x000001, 100, False)
            this.client.room.addTextArea(10055, "<p align='center'>" + ("<N><a href='event:consumablesShop:changePage-" + str((page + 1)) + "'>" if (page < len(consumables) / 6 + 1) else "<BL>") + "<b>&gt;</b>" + ("</a>" if page == 0 else "") + "</p>", this.client.Username, 250, 339, 18, 16, 0x324650, 0x324650, 100, False)
            this.client.room.addTextArea(10056, this.getText("consumablesShop.endBuy"), this.client.Username, 335, 339, 150, 16, 0x324650, 0x324650, 100, False)
            this.client.room.addTextArea(10057, "<img src='http://www.novaeramice.com.br/consumablesShop/price.png' hspace='0' vspace='0'>", this.client.Username, 550, 315, 20, 45, 0x000001, 0x000001, 0, False)
            this.client.room.addTextArea(10058, "<b><font size='13'><J>%s</font>\n<font size='7'>\n</font><font size='13'><R>%s</font></b>" %(this.cheesesCount, this.fraisesCount), this.client.Username, 575, 315, 45, 45, 0x000001, 0x000001, 0, False)

    def addItem(this, page, itemIndex):
        object = this.server.menu["consumables"][str(((page - 1) * 6) + itemIndex)]
        id = object[0]
        if this.itemsCache.has_key(id):
            this.itemsCache[id] += 1
        else:
            this.itemsCache[id] = 1

        this.cheesesCount += object[1]
        this.fraisesCount += object[2]

        consumables = this.server.menu["consumables"]
        currentItems = []
        index = (page - 1) * 6
        consumable = 0
        while consumable < len(consumables):
            info = consumables[str(consumable)]
            if consumable >= index and consumable < index + 6:
                currentItems.append([info[0], info[1], info[2]])
            consumable += 1

        this.client.room.updateTextArea(10046 + itemIndex, "<p align='center'><CH2>" + ("<a href='event:consumablesShop:removeItem-" + str(page) + "-" + str(itemIndex) + "'>" if this.itemsCache.has_key(currentItems[itemIndex][0]) else "") + "-" + ("</a>" if this.itemsCache.has_key(currentItems[itemIndex][0]) else "") + "    <CEP>" + (str(this.itemsCache[currentItems[itemIndex][0]]) if this.itemsCache.has_key(currentItems[itemIndex][0]) else "0") + "   <CH2>" + ((("<a href='event:consumablesShop:addItem-" + str(page) + "-" + str(itemIndex) + "'>" if this.itemsCache[currentItems[itemIndex][0]] < (80 - (this.client.playerConsumables[currentItems[itemIndex][0]] if this.client.playerConsumables.has_key(currentItems[itemIndex][0]) else 0)) else "") if this.itemsCache.has_key(currentItems[itemIndex][0]) else "<a href='event:consumablesShop:addItem-" + str(page) + "-" + str(itemIndex) + "'>") if (this.client.playerConsumables[currentItems[itemIndex][0]] < 80 if this.client.playerConsumables.has_key(currentItems[itemIndex][0]) else True) else "") + "+" + ((("</a>" if this.itemsCache[currentItems[itemIndex][0]] < (80 - (this.client.playerConsumables[currentItems[itemIndex][0]] if this.client.playerConsumables.has_key(currentItems[itemIndex][0]) else 0)) else "") if this.itemsCache.has_key(currentItems[itemIndex][0]) else "</a>") if (this.client.playerConsumables[currentItems[itemIndex][0]] < 80 if this.client.playerConsumables.has_key(currentItems[itemIndex][0]) else True) else "") + "</p>", this.client.Username)
        this.client.room.updateTextArea(10058, "<b><font size='13'><J>%s</font>\n<font size='7'>\n</font><font size='13'><R>%s</font></b>" %(this.cheesesCount, this.fraisesCount), this.client.Username)

    def removeItem(this, page, itemIndex):
        object = this.server.menu["consumables"][str(((page - 1) * 6) + itemIndex)]
        id = object[0]
        if this.itemsCache.has_key(id):
            count = this.itemsCache[id]
            if count == 1:
                del this.itemsCache[id]
            else:
                this.itemsCache[id] = count - 1

            this.cheesesCount -= object[1]
            this.fraisesCount -= object[2]

        consumables = this.server.menu["consumables"]
        currentItems = []
        index = (page - 1) * 6
        consumable = 0
        while consumable < len(consumables):
            info = consumables[str(consumable)]
            if consumable >= index and consumable < index + 6:
                currentItems.append([info[0], info[1], info[2]])
            consumable += 1

        this.client.room.updateTextArea(10046 + itemIndex, "<p align='center'><CH2>" + ("<a href='event:consumablesShop:removeItem-" + str(page) + "-" + str(itemIndex) + "'>" if this.itemsCache.has_key(currentItems[itemIndex][0]) else "") + "-" + ("</a>" if this.itemsCache.has_key(currentItems[itemIndex][0]) else "") + "    <CEP>" + (str(this.itemsCache[currentItems[itemIndex][0]]) if this.itemsCache.has_key(currentItems[itemIndex][0]) else "0") + "   <CH2>" + ((("<a href='event:consumablesShop:addItem-" + str(page) + "-" + str(itemIndex) + "'>" if this.itemsCache[currentItems[itemIndex][0]] < (80 - (this.client.playerConsumables[currentItems[itemIndex][0]] if this.client.playerConsumables.has_key(currentItems[itemIndex][0]) else 0)) else "") if this.itemsCache.has_key(currentItems[itemIndex][0]) else "<a href='event:consumablesShop:addItem-" + str(page) + "-" + str(itemIndex) + "'>") if (this.client.playerConsumables[currentItems[itemIndex][0]] < 80 if this.client.playerConsumables.has_key(currentItems[itemIndex][0]) else True) else "") + "+" + ((("</a>" if this.itemsCache[currentItems[itemIndex][0]] < (80 - (this.client.playerConsumables[currentItems[itemIndex][0]] if this.client.playerConsumables.has_key(currentItems[itemIndex][0]) else 0)) else "") if this.itemsCache.has_key(currentItems[itemIndex][0]) else "</a>") if (this.client.playerConsumables[currentItems[itemIndex][0]] < 80 if this.client.playerConsumables.has_key(currentItems[itemIndex][0]) else True) else "") + "</p>", this.client.Username)
        this.client.room.updateTextArea(10058, "<b><font size='13'><J>%s</font>\n<font size='7'>\n</font><font size='13'><R>%s</font></b>" %(this.cheesesCount, this.fraisesCount), this.client.Username);

    def endBuy(this):
        consumablesCount = 0 if len(this.itemsCache) == 0 else sum(this.itemsCache.values())
        if consumablesCount > 0:
            i = 10040
            while i <= 10058:
                this.client.room.removeTextArea(i, this.client.Username)
                i += 1

            this.client.room.addTextArea(10060, this.getText("consumablesShop.buyMessage", this.client.Username, this.client.shopCheeses, this.client.shopFraises, consumablesCount), this.client.Username, 192, 100, 430, 250, 0, 0, 0, False);
            this.client.room.addTextArea(10061, ("<a href='event:consumablesShop:confirmBuy-0'>" if this.client.shopCheeses >= this.cheesesCount else "") + "<img src='http://www.novaeramice.com.br/consumablesShop/getPrice.php?type=0&value=%s&can=%s' hspace='0' vspace='-2'>" %(this.cheesesCount, ("1" if this.client.shopCheeses >= this.cheesesCount else "0")) + ("</a>" if this.client.shopCheeses >= this.cheesesCount else ""), this.client.Username, 250, 190, 120, 60, 0, 0, 0, False)
            this.client.room.addTextArea(10062, ("<a href='event:consumablesShop:confirmBuy-1'>" if this.client.shopFraises >= this.fraisesCount else "") + "<img src='http://www.novaeramice.com.br/consumablesShop/getPrice.php?type=1&value=%s&can=%s' hspace='0' vspace='-2'>" %(this.fraisesCount, ("1" if this.client.shopFraises >= this.fraisesCount else "0")) + ("</a>" if this.client.shopFraises >= this.fraisesCount else ""), this.client.Username, 450, 190, 120, 60, 0, 0, 0, False)
            this.client.room.addTextArea(10063, "", this.client.Username, 335, 340, 150, 16, 0x000001, 0x000001, 100, False)
            this.client.room.addTextArea(10064, this.getText("consumablesShop.cancelBuy"), this.client.Username, 335, 339, 150, 16, 0x324650, 0x324650, 100, False)

    def confirmBuy(this, withFraises):
        consumablesCount = 0 if len(this.itemsCache) == 0 else sum(this.itemsCache.values())
        if withFraises:
            this.client.shopFraises -= this.fraisesCount
        else:
            this.client.shopCheeses -= this.cheesesCount

        i = 10061
        while i <= 10063:
            this.client.room.removeTextArea(i, this.client.Username)
            i += 1

        for consumable in this.itemsCache.items():
            this.client.sendAnimZelda(-3, consumable[0])
            this.client.sendNewConsumable(consumable[0], consumable[1])
            if this.client.playerConsumables.has_key(consumable[0]):
                this.client.playerConsumables[consumable[0]] += consumable[1]
            else:
                this.client.playerConsumables[consumable[0]] = consumable[1]

        this.client.room.updateTextArea(10060, this.getText("consumablesShop.buySucess", consumablesCount, "<R>" if withFraises else "<J>", this.fraisesCount if withFraises else this.cheesesCount, this.getText("consumablesShop.fraises") if withFraises else this.getText("consumablesShop.cheeses")), this.client.Username)
        this.client.room.updateTextArea(10064, this.getText("consumablesShop.returnToHome"), this.client.Username)

        this.cheesesCount = 0
        this.fraisesCount = 0
        this.itemsCache = {}

    def close(this):
        i = 10039
        while i <= 10064:
            this.client.room.removeTextArea(i, this.client.Username)
            i += 1

        this.cheesesCount = 0
        this.fraisesCount = 0
        this.currentPage = 0
        this.itemsCache = {}
