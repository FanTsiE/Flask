import serial

baudrate = 9600
to_r = 1
to_w = 1
ser2 = serial.Serial("COM2", baudrate, timeout=0, write_timeout=to_w)
buffer_size = 14


while True:
    bytes_received = ser2.readline()
    #bytes_received="start"
    if len(bytes_received) >= 1:
        hex_received = bytes_received.hex()
        #hex_received="024f4e0d03024f460d030255313233340d03024937350d030255530d030249530d03"
        print(hex_received)
        split_sym = "0d03"
        msg_received_list = []
        msg_forward_list = []
        hex_forward = []
        msg_split = hex_received
        while msg_split != "":
            temp = msg_split[0:msg_split.index(split_sym)] + "0d03"
            msg_received_list.append(temp)
            msg_split = msg_split[len(temp):]

        for i in range(len(msg_received_list)):
            if bytes.fromhex(msg_received_list[i]) == bytes.fromhex("024F4E0D03"):
                msg_forward_list.append(
                    "4F4E2020202020205052455741524E494E472054494D450A0D53 65 74 20 76 61 6C 75 65 73 3A 20 20 20 31 37 38 2C 30 20 6B 56 20 20 30 35 2C 30 30 20 6D 41 20 20 58 58 3A 58 58 20 6D 69 6E 3A 73 65 63 0A 0A 0D 20 20 20 20 20 20 48 49 47 48 20 54 45 4E 53 49 4F 4E 20 4F 4E 0A 0D 41 63 74 75 61 6C 20 76 61 6C 75 65 73 3A 20 20 20 31 37 38 2C 30 20 6B 56 20 20 30 35 2C 30 30 20 6D 41 20 20 0A 0A 0D".replace(" ",""))
            elif bytes.fromhex(msg_received_list[i]) == bytes.fromhex("024F460D03"):
                msg_forward_list.append(
                    "4F462020202020 20 48 49 47 48 20 54 45 4E 53 49 4F 4E 20 4F 02 4F 46 0D 03 4E 0A 0D 20 20 20 20 20 20 50 4F 53 54 48 45 41 54 49 4E 47 0A 0D 52 65 61 73 6F 6E 3A 20 53 65 72 69 61 6C 20 69 6E 74 65 72 66 61 63 65 0A 0A 0D 20 20 20 20 20 20 53 54 41 4E 44 20 42 59 0A 0D 4D 6F 64 65 34 30 30 20 20 54 75 62 65 20 4D 58 52 33 32 30 48 50 31 31 4E 43 20 20 53 79 73 74 65 6D 20 58 50 33 32 30 0A 0A 0D".replace(" ",""))
            elif msg_received_list[i][0:4] == "0255":
                if bytes.fromhex(msg_received_list[i]) == bytes.fromhex("0255530D03"):  # US1280
                    msg_forward_list.append("5553203132382C300D0A")
                else:  # if bytes_received == bytes.fromhex("0255313233340D03"): #U1234
                    msg_forward_list.append(msg_received_list[i][2:msg_received_list[i].index(split_sym)] + "0d0a")
            elif msg_received_list[i][0:4] == "0249":
                if bytes.fromhex(msg_received_list[i]) == bytes.fromhex("0249530D03"):  # IS0075
                    msg_forward_list.append("49532030302C37350D0A")
                else:  # if bytes_received == bytes.fromhex("02 49 37 35 0D 03"): #I75
                    msg_forward_list.append(msg_received_list[i][2:msg_received_list[i].index(split_sym)] + "0d0a")

        for i in range(len(msg_forward_list)):
            cnt = 1
            while cnt*buffer_size < len(msg_forward_list[i]):
                hex_forward.append(msg_forward_list[i][(cnt-1)*buffer_size:cnt*buffer_size])
                cnt += 1
            if (cnt-1)*buffer_size < len(msg_forward_list[i]):
                hex_forward.append(msg_forward_list[i][(cnt-1) * buffer_size:])

        for j in range(len(hex_forward)):
            print(bytes.fromhex(hex_forward[j]))
            ser2.write(bytes.fromhex(hex_forward[j]))





