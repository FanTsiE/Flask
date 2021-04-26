 
#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import hashlib
import requests
import time

from flask import Flask
from flask import request
from flask import redirect
from flask import jsonify


app = Flask(__name__)
 

def calc_score(val):
    ret = 100.0
    
    if val < 0 :
        return 0
    
    stx = 0
    edx = 0

    list_shpv =  [0,   1.5, 3.0, 4.5, 8]
    list_score = [100, 80,  60,  40,  0]
    for i in range(len(list_shpv)):
        if val < list_shpv[i]:
            edx = i
            stx = i - 1
            break
    if edx == 0:
        return 0
    #print("val = {}".format(val))
    #print("val = {},stx= {},edx={}, score:({},{}),ret = {}".format(val,list_shpv[stx], list_shpv[edx],list_score[stx],list_score[edx]),ret)
    ret = list_score[stx]-(list_score[stx]-list_score[edx])*(val-list_shpv[stx])/(list_shpv[edx]-list_shpv[stx])
    print("val = {},stx= {},edx={}, score:({},{}),ret={}".format(val,list_shpv[stx], list_shpv[edx],list_score[stx],list_score[edx],ret))

    return ret

def shape_score(fl,fc):
    ret = 100
    ret = round(calc_score(fl)*0.5+calc_score(fc)*0.5)

    return ret
    

#score for actual set value
@app.route('/shpscore' , methods=['GET', 'POST'])
def model_shape_score():
    print("run /shpscore")
    ret_data = {}
    if request.method == 'POST':
        a = request.get_data()
        dict1 = json.loads(a)
        ret_data["PlateNo"] = dict1["PlateNo"]
        ret_data["BundleNo"] = dict1["BundleNo"]
        ret_data["ctime"] = dict1["ctime"]
        ret_data["steel_grade"]=dict1["steel_grade"]
        ret_data["plate_length"]=dict1["plate_length"]
        ret_data["plate_width"]=dict1["plate_width"]
        ret_data["plate_thick"]=dict1["plate_thick"]
        ret_data["plate_temp"]=dict1["plate_temp"]
        ret_data["yield_point"]=dict1["yield_point"]
        ret_data["tension"]=dict1["tension"]
        if "ht_type" in dict1:
            ret_data["ht_type"]=dict1["ht_type"]
        else:
            ret_data["ht_type"]="N"
        ret_data["inlet_manu"] = dict1["inlet_manu"]
        ret_data["outlet_manu"] = dict1["outlet_manu"]
        ret_data["flexion_manu"] = dict1["flexion_manu"]

        ret_data["full_length_gap"] = dict1["full_length_gap"]
        ret_data["full_cross_gap"] = dict1["full_cross_gap"]

        ret_data["score"] = shape_score(ret_data["full_length_gap"], ret_data["full_cross_gap"])

        return json.dumps(ret_data)

#score for actual set value
@app.route('/setscore' , methods=['GET', 'POST'])
def model_actset_score():
    print("run /setscore")
    map_ht = {"Q":0,"T":1,"X":2,"Q+T":2}
    ret_data = {}
    if request.method == 'POST':
        a = request.get_data()
        dict1 = json.loads(a)
        ret_data["PlateNo"] = dict1["PlateNo"]
        ret_data["BundleNo"] = dict1["BundleNo"]
        ret_data["ctime"] = dict1["ctime"]
        ret_data["steel_grade"]=dict1["steel_grade"]
        ret_data["plate_length"]=dict1["plate_length"]
        ret_data["plate_width"]=dict1["plate_width"]
        ret_data["plate_thick"]=dict1["plate_thick"]
        ret_data["plate_temp"]=dict1["plate_temp"]
        ret_data["yield_point"]=dict1["yield_point"]
        ret_data["tension"]=dict1["tension"]
        ret_data["ht_type"]=dict1["ht_type"]
        ret_data["inlet_manu"] = dict1["inlet_manu"]
        ret_data["outlet_manu"] = dict1["outlet_manu"]
        ret_data["flexion_manu"] = dict1["flexion_manu"]

        plate_length = dict1["plate_length"]
        plate_width = dict1["plate_width"]
        plate_thick = dict1["plate_thick"]
        yield_point = dict1["yield_point"]
        tension = dict1["tension"]
        heattype= map_ht[dict1["ht_type"]]
        plate_temp = dict1["plate_temp"]
        inlet = dict1["inlet_manu"]
        outlet = dict1["outlet_manu"]
        flexion = dict1["flexion_manu"]

        #ret = predict(plate_length,plate_width,plate_thick,yield_point,tension,plate_temp,heattype)

        #ret_data.update(ret)
        ret_shp = set_eval(plate_length,plate_width,plate_thick,yield_point,tension,plate_temp,heattype,inlet,outlet,flexion)
        ret_data.update(ret_shp)
        ret_data["score"] = shape_score(ret_shp["full_length_gap"], ret_shp["full_cross_gap"])

        print("ret ", ret_shp)
        return json.dumps(ret_data)

@app.route('/user/<name>')
def user(name):
    return'<h1>hello, %s</h1>' % name
 

@app.route('/17study',methods=['GET','POST'])
def study_login():
    ret = {"status":"ok"}
    if request.method == 'POST':
        print("recv POST ...")
        a = request.get_data()
        input_json = json.dumps(json.loads(a))
        print(input_json)
        ret = {"type":"POST"}
    elif request.method == 'GET':
        ret = {"type": "GET "}


    return ret

if __name__ =='__main__':
    app.run(host = "0.0.0.0",port=15001, debug=True)
