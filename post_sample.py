#!/usr/bin/python
# -*- coding:utf-8 -*-
# 
# 
import sys
import os
import time
import json
import requests

def main():
	url = "http://127.0.0.1:5000/SetValue"
	dict_val = {}
	dict_val["name"] = "Tom"
	dict_val["age"] = 18
	dict_val["addr"] = "Street 18"

	ret = requests.post(url, json=json.dumps(dict_val))
	#print("recv: ", ret.json()," type: ", type(ret.json()))

if __name__=="__main__":
	main()