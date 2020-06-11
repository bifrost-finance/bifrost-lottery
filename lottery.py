#!/usr/bin/env python3

"""
How to start a lottery.
1. Get an array by decoding every address, and sum it.
2. Iterate the list, repeat step 1, generate an list that has the sum of every valid address.
3. Find the min and max from the list that generated from step 2, taking both as lowebound and upperbound.
4. Generate a random number between the min and the max, find out who is nearest to this random number(and bigger than random number), this address is the winner.
5. Repeat 5 times to get 5 winners.
"""

import base58
import json
import random
import re
import sys

expr = r'5[0-9a-zA-Z]{46,48}'

def deserialize_data_from_file(path):
    f = open(path, "r")
    data = f.read()
    f.close()
    return json.loads(data)

def decode_address(address):
    decode = base58.b58decode(address)
    if len(decode) == 35: 
        # the length is 35 if the address is valid
        return decode
    else:
        return None

def find_min_and_max(address_sum):
    _min, _max = address_sum[0]['sum'], address_sum[0]['sum']
    for v in address_sum:
        if _min > v['sum']:
            _min = v['sum']
        if _max < v['sum']:
            _max = v['sum']
    return _min, _max

def who_is_winner(address_sum, random_num):
    nearest = sys.maxsize
    winner = None
    for addr in address_sum:
        stride = addr['sum'] - random_num
        if stride >= 0 and nearest > stride:
            nearest = stride
            winner = addr
    return winner

def lottery(path):
    all_names_list = deserialize_data_from_file(path)

    address_sum = []
    for name in all_names_list:
        t = re.search(expr, name['account'])
        if not t: # invalid address
            continue
        s = decode_address(name['account'])
        if s:
            a = { 'account': name['account'], 'sum': sum(s)}
            address_sum.append(a)

    _min, _max = find_min_and_max(address_sum)
    print(f"The script will generate random number between {_min} and {_max}")

    winner_count = 5
    winners = []
    while True:
        if len(winners) >= winner_count:
            break

        r = random.randint(_min, _max)
        winner = who_is_winner(address_sum, r)
        if winner:
            print(f"Random number: {r}, address sum: {winner['sum']}, {winner['account']} is so lucky!")
            winners.append(winner["account"])
            address_sum.remove(winner) # winner is not allowed to paticipate next round


if __name__ == "__main__":
    path = "data/matched_and_issued_bnc.json"
    lottery(path)