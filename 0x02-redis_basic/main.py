#!/usr/bin/env python3
""" Main file """

get_page = __import__('web').get_page

while(True):
    print("loop")
    print(get_page("https://swapi.dev/api/people/1/"))
