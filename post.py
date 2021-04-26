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
    url = "http://127.0.0.1:5000/"
    radius=input("radius:")
    radius=float(radius)
    thickness=input("thickness:")
    thickness=float(thickness)
    requests.post(url, json={"radius": radius, "thickness": thickness})
    return 0


if __name__ == "__main__":
    main()
