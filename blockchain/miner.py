import hashlib
import requests

import sys

from uuid import uuid4

from timeit import default_timer as timer

import random

import time


def proof_of_work(last_proof):
    """
    Multi-Ouroboros of Work Algorithm
    - Find a number p' such that the last six digits of hash(p) are equal
    to the first six digits of hash(p')
    - IE:  last_hash: ...AE9123456, new hash 123456888...
    - p is the previous proof, and p' is the new proof
    - Use the same method to generate SHA-256 hashes as the examples in class
    - Note:  We are adding the hash of the last proof to a number/nonce for the new proof
    """

    start = timer()

    print("Searching for next proof")
    proof = 0
    #  TODO: Your code here
    l_proof = last_proof
    last_hash = hashlib.sha256(f"{last_proof}".encode()).hexdigest()

    while valid_proof(last_hash, proof) is False:
        if int(timer())%20 == 0:
            time.sleep(1)
            r = requests.get(url=node + "/last_proof")
            data = r.json()
            if l_proof != data.get('proof'):
                l_proof = data.get('proof')
                print("changing last hash")
                print(data.get('proof'))
                last_hash = hashlib.sha256(f"{data.get('proof')}".encode()).hexdigest()
        proof = int(timer()*1000000)

    new_hash = hashlib.sha256(f'{proof}'.encode()).hexdigest()
    print(f"old: {last_hash}")
    print(f"new: {new_hash}")
    print("Proof found: " + str(proof) + " in " + str(timer() - start))
    return proof


def valid_proof(last_hash, proof):
    """
    Validates the Proof:  Multi-ouroborus:  Do the last six characters of
    the hash of the last proof match the first six characters of the proof?

    IE:  last_hash: ...AE9123456, new hash 123456888...
    """

    # TODO: Your code here!
    new_hash = hashlib.sha256(f'{proof}'.encode()).hexdigest()

    return new_hash[:6] == last_hash[-6:]


if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "https://lambda-coin.herokuapp.com/api"

    coins_mined = 0

    # Load or create ID
    f = open("my_id.txt", "r")
    id = f.read()
    print("ID is", id)
    f.close()

    if id == 'NONAME\n':
        print("ERROR: You must change your name in `my_id.txt`!")
        exit()
    # Run forever until interrupted
    while True:
        # Get the last proof from the server
        r = requests.get(url=node + "/last_proof")
        data = r.json()
        print(data)
        new_proof = proof_of_work(data.get('proof'))

        post_data = {"proof": new_proof,
                     "id": id}

        r = requests.post(url=node + "/mine", json=post_data)
        data = r.json()
        if data.get('message') == 'New Block Forged':
            coins_mined += 1
            print("Total coins mined: " + str(coins_mined))
        else:
            print(data.get('message'))
