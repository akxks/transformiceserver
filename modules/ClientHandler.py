#coding: utf-8
from ByteArray import ByteArray
from twisted.internet import protocol

class ClientHandler(protocol.Protocol):
    recvd = ""

    def dataReceived(this, data):
        packet = "" + data
        if packet.startswith("<policy-file-request/>"):
            this.transport.write("<cross-domain-policy><allow-access-from domain=\"*\" to-ports=\"*\" /></cross-domain-policy>")
            this.transport.loseConnection()
            return

        elif packet.startswith("change_avatar_"):
            key = packet.replace("change_avatar_", "")
            if this.server.clientAvatarKeys.has_key(key):
                player = this.server.avatarKeys[key]
                this.transport.write(player.Username + " - " + player.playerID)
            else:
                this.transport.write("error")

        if packet == None or len(packet) < 2:
            return

        this.recvd += data
        while not this.recvd == "":
            dataLength = len(this.recvd)
            if dataLength > 1:
                p = ByteArray(this.recvd)
                sizeBytes = p.readByte()
                length = p.readUnsignedByte() if sizeBytes == 1 else p.readUnsignedShort() if sizeBytes == 2 else ((p.readUnsignedByte() & 0xFF) << 16) | ((p.readUnsignedByte() & 0xFF) << 8) | (p.readUnsignedByte() & 0xFF) if sizeBytes == 3 else 0

                if length == 0:
                    return

                length += 1
                dataLength -= (sizeBytes+1)
                if dataLength == length:
                    this.parseString(this.recvd[sizeBytes+1:])
                    this.recvd = ""

                elif dataLength < length:
                    break
                else:
                    this.parseString(this.recvd[sizeBytes+1:][:length])
                    this.recvd = this.recvd[length+sizeBytes+1:]
            else:
                    break
