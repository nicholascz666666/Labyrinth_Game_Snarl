#!/usr/bin/python3

import sys
import json
from json import JSONDecoder, JSONDecodeError

# method that takes a string as input
# and return a list of JSON string that is correctly formatted
# for example '12 [2, "foo", 4]' would return [12, [2, "foo", 4]]
def decode_json(jsonstring):
    decoder = JSONDecoder()
    pos = 0
    json_list = []
    while True:
        try:
            while pos < len(jsonstring) and jsonstring[pos].isspace():
                pos += 1

            obj, pos = decoder.raw_decode(jsonstring, pos)
            json_list.append(obj)
        except JSONDecodeError:
            break
    return json_list

# method that calculate the sum of all numeric values contained in the NumJSON
# for Object, only consider the "payload" value
def calculate_sum(numjson):
    total = 0
    if type(numjson) == int:
        total += numjson
    elif type(numjson) == list:
        for i in numjson:
            total += calculate_sum(i)
    elif type(numjson) == dict:
        for key in numjson:
            if key == "payload":
                total += calculate_sum(numjson[key])
    return total

# method that calculate the product of all numeric values contained in the NumJSON
# for Object, only consider the "payload" value
def calculate_product(numjson):
    total = 1
    if type(numjson) == int:
        total *= numjson
    elif type(numjson) == list:
        for i in numjson:
            total *= calculate_product(i)
    elif type(numjson) == dict:
        for key in numjson:
            if key == "payload":
                total *= calculate_product(numjson[key])
    return total

def main(op, jsonstring):
    json_list = decode_json(jsonstring)
    
    if op == "--sum":
        output =  [{"object": obj, "total": calculate_sum(obj)} for obj in json_list]
    elif op == "--product":
        output =  [{"object": obj, "total": calculate_product(obj)} for obj in json_list]
    return json.dumps(output)

#The program should also take a single command line argument, which is either --sum or --product.
#Once STDIN is closed, the program should, for each of the given NumJSON values, compute a sum or
#a product (depending on the given argument) of all numeric values contained in the NumJSON.
#The result for a String value should be the unit for the respective operation (0 for --sum, 1 for
#--product). 
#For Objects, only consider the "payload" value.
#The output should be a JSON array of objects with the fields "object",
#containing the original NumJSON value, and "total", containing the total computed for that object.
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("need more arg")
        sys.exit(1)
    if sys.argv[1] != "--sum" and sys.argv[1] != "--product":
        print("--sum or --product")
        sys.exit(1)

    print(main(sys.argv[1], sys.stdin.read()))
        




