#  Hint:  You may not need all of these.  Remove the unused functions.
from hashtables import (HashTable,
                        hash_table_insert,
                        hash_table_remove,
                        hash_table_retrieve,
                        hash_table_resize)

def find_second_index(weights, search_val):
    for i in range(0, len(weights)):
        if weights[i] == search_val:
            return i
    return


def get_indices_of_item_weights(weights, length, limit):
    ht = HashTable(16)

    """
    YOUR CODE HERE
    """

    if length <= 1:
        return None

    first = None
    second = None

    for i in range(0, length):
        hash_table_insert(ht, weights[i], limit-weights[i])
        if hash_table_retrieve(ht, limit-weights[i]):
            first = i
            second = find_second_index(weights, limit-weights[i])
    
    for i in range(0, length):
        if hash_table_retrieve(ht, limit-weights[i]):
            first = i
            second = find_second_index(weights, limit-weights[i])

    if first == None or second == None:
        return None
    elif first > second:
        return (first, second)
    else:
        return (second, first)


def print_answer(answer):
    if answer is not None:
        print(str(answer[0] + " " + answer[1]))
    else:
        print("None")
