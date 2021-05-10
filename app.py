from flask import Flask, request
from time import sleep
import xlrd
import serial
import ast

app = Flask(__name__)


def read_table(table):
    """
    :param table: an xls file
    :return: a list of dictionaries recording diameter and thickness
    """
    book = xlrd.open_workbook(table)
    sheet = book.sheet_by_index(0)
    keys = [sheet.cell(0, col_index).value for col_index in range(sheet.ncols)]
    dict_list = []
    for row_index in range(1, sheet.nrows):
        d = {keys[col_index]: sheet.cell(row_index, col_index).value
             for col_index in range(sheet.ncols)}
        dict_list.append(d)
    return dict_list


def read_dat(dat):
    """
    :param dat: a dat file, config.dat in this situation
    :return: a list of dictionaries recording diameter and thickness
    """
    with open(dat) as data:
        lines = data.readlines()
        text = "".join(lines)
    index1 = text.find('vcList')  # beginning of the list in the file
    index2 = text.find('cameraPixelWidth')  # end of the list in the file
    text_cut = text[index1:index2]
    index3 = text_cut.find('[{')
    index4 = text_cut.find('}]')
    dict_list_str = text_cut[index3:index4 + 2]
    dict_list = ast.literal_eval(dict_list_str)
    return dict_list


def define_serial(config='configure.txt'):
    """
    :param config: a text file (first line) recording parameters of the serial, e.g. COM1 9600 1
    :return: a well defined serial
    """
    f = open(config, 'r')
    parameter = f.readline().split(' ')
    ser = serial.Serial(parameter[0], int(parameter[1]), write_timeout=int(parameter[2]))
    if not ser.isOpen():
        ser.open()
        print("Serial is now open.")
    return ser


def serial_send_ui(ser,d, config='configure.txt'):
    """
    :param ser: a serial
    :param d: a dictionary {'U': XX, 'I': YY}
    :param config: file for configuration, normally configure.txt
    :return: void, ends after the serial sends the values
    """
    f = open(config, 'r')
    lines = f.readlines()
    u = d['U']
    i = d['I']
    msg_u = "0255" + str(u).encode().hex() + "0d03"
    msg_i = "0249" + str(i).encode().hex() + "0d03"
    ser.write(bytes.fromhex(msg_u))
    sleep(float(lines[2]))
    ser.write(bytes.fromhex(msg_i))
    return


@app.route('/getvalues', methods=['GET'])
def get_values():
    """
    This route would get values from the address https://127.0.1.1:5000/?diameter=XX&thickness=YY
    :return: the final values of voltage/current
    """
    ui = {'U': 0, 'I': 0}
    f = open('configure.txt', 'r')
    lines = f.readlines()
    dict_list = read_dat(lines[1].strip('\n'))
    result = {}
    try:
        result = {'diameter': float(request.args.get('diameter')), 'thickness': float(request.args.get('thickness'))}
    except TypeError:  # if the format is not correct
        print("Error.")
    else:
        print(result)
    for i in range(len(dict_list)):
        # condition_d = result['diameter'] == dict_list[i]['diameter']  # diameter
        condition_t = result['thickness'] == dict_list[i]['thickness']  # thickness
        # thickness at top priority
        if condition_t:
            ui['U'] = dict_list[i]['voltage']
            ui['I'] = dict_list[i]['current']
            # diameter:
            """
            elif condition_d:
                ...
            """
    print(ui)
    ser1 = define_serial()
    while ui['U'] * ui['I'] > 1400:  # I-=0.05 until UI<1400
        ui['I'] -= 0.05
    if ui['U'] * ui['I'] == 0:   # if proper values not found
        return "Error."
    serial_send_ui(ser1, ui)
    ui['U'] = round(ui['U'], 1)
    ui['I'] = round(ui['I'], 2)  # in case of inexact float results, like 5.3500000006
    serial_send_ui(ser1, ui)
    return ui


@app.route('/', methods=['POST', 'GET'])
def values():
    """
    This route would get values from the JSON pack，i.e. {'diameter': XX, 'thickness': YY}
    :return: the final values of voltage/current, i.e. {'U': XX, 'I': YY}
    """
    ui = {'U': 0, 'I': 0}
    f = open('configure.txt', 'r')
    lines = f.readlines()
    dict_list = read_dat(lines[1].strip('\n')) # correct path of the dat file
    result = request.get_json(force=True)
    for i in range(len(dict_list)):
        # condition_d = result['diameter'] == dict_list[i]['diameter']  # diameter
        condition_t = result['thickness'] == dict_list[i]['thickness']  # thickness
        if condition_t:
            ui['U'] = dict_list[i]['voltage']
            ui['I'] = dict_list[i]['current']
            # diameter:
            """
            elif condition_d:
               ...
            """
    print(ui)
    ser1 = define_serial()
    while ui['U'] * ui['I'] > 1400:  # I-=0.05 until UI<1400
        ui['I'] -= 0.05
    if ui['U'] * ui['I'] == 0:  # if proper values not found
        return "Error."
    ui['U'] = round(ui['U'], 1)
    ui['I'] = round(ui['I'], 2)  # in case of inexact float results, like 5.3500000006
    serial_send_ui(ser1, ui)
    return ui


@app.route('/on', methods=['POST', 'GET'])
def switch_on():
    """
    This route turns on the high voltage.
    :return: 1 for success, 0 for failure
    """
    ser1 = define_serial()
    ser1.write(bytes.fromhex("024F4E0D03"))
    cnt = 0
    while True:
        msg = ser1.readline()
        print(msg)
        if cnt == 4:  # read the final line of the message back to serial
            break
        cnt += 1
    msg_str = msg.decode().replace(',', '.')  # msg_str should be: 'Actual values: XX.0 kV, YY.0 mA'
    l = []
    for ch in msg_str.split():
        try:
            l.append(float(ch))
        except ValueError:
            pass
    if l is not None:
        ui = {'U': l[0], 'I': l[1]}
        return ui
    else:
        return "Error."


@app.route('/off', methods=['GET'])
def switch_off():
    """
        This route turns off the high voltage.
        :return: 1 for success, 0 for failure
        """
    ser1 = define_serial()
    ser1.write(bytes.fromhex("024F460D03"))
    cnt = 0
    while True:
        msg = ser1.readline()
        if cnt == 2:
            break
        cnt += 1
    if msg is not None:
        return "1"  # success
    else:
        return "0"  # failure


@app.route('/setvalues', methods=['POST', 'GET'])
def set_values():
    """
    This route directly sets the values.
    :return: 1 for success, 0 for failure
    """
    ui = request.get_json(force=True)
    ser1 = define_serial()
    serial_send_ui(ser1, ui)
    if len(ser1.readline()) >= 1:
        return "1"  # success
    else:
        return "0"  # failure


@app.route('/test', methods=['GET'])
def test():
    """
    This route sets the values for test.
    :return: the testing values of voltage/current
    """
    ser1 = define_serial()
    ser1.write(bytes.fromhex("0255530D03"))
    sleep(0.25)
    ser1.write(bytes.fromhex("0249530D03"))
    u_byte = ser1.readline()
    i_byte = ser1.readline()
    u = 0
    i = 0
    if u_byte is not None and i_byte is not None:
        for ch in u_byte.decode().replace(',', '.').split():  # "U1234,0" str -> U=1234.0 float
            try:
                u = float(ch)
            except ValueError:
                pass
        for ch in i_byte.decode().replace(',', '.').split():  # "I00,75" str -> I=0.75 float
            try:
                i = float(ch)
            except ValueError:
                pass
        ui = {'U': u, 'I': i}
        if u > 0 and i > 0:
            return ui
        else:
            return "Error."
    else:
        return "Error."


if __name__ == '__main__':
    app.debug = True
    app.run()
