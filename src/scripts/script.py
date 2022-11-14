#!/usr/bin/env python
# To be run as:
# seq <START_BLOCK> <END_BLOCK> | parallel -j32 --bar ./script.py > ../results/out.csv

import sys
from web3.auto import w3


def get_transaction_data(block_number):
    """
    A function that given a block number
    returns a list of lists of the same size.
    Each sub-list contains a information of a single row.
    """
    rows = []
    num_trans = len(w3.eth.get_block(block_number).transactions)
    for j in range(num_trans):
        tx = w3.eth.get_transaction_by_block(block_number, j)
        row = [tx['from'], tx['to'], tx['value'], tx['blockNumber'], tx['hash'].hex( )]
        rows.append(row)
    return rows


def get_transaction_data_fake(block_number):
    """
    A function that given a block number
    returns a list of lists of the same size.
    Each sub-list contains a information of a single row.
    """
    row1 = [block_number * 3 for i in range(4)]
    row2 = [block_number + 3 for i in range(4)]
    row3 = [block_number / 3 for i in range(4)]
    return [row1, row2, row3]


def print_rows(data):
    for line in data:
        line_str = ",".join(map(str,line))
        print(line_str)


if __name__ == "__main__":
    line = sys.argv[1]
    if line.isnumeric():
        line = int(line)
        data = get_transaction_data(line)
        print_rows(data)

