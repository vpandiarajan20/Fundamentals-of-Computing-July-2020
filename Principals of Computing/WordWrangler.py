"""
Student code for Word Wrangler game
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    return_value = list([])
    for value in list1:
        if(value not in return_value):
            return_value.append(value)
    return return_value

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    return_value = list([])
    for value1 in list1:
        if(value1 in list2):
            return_value.append(value1)
    return remove_duplicates(return_value)

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing those elements that are in
    either list1 or list2.

    This function can be iterative.
    """   
    return_value = list([])
    first_list = list(list1)
    second_list = list(list2)
    while(len(first_list) != 0 and len(second_list) != 0):
        if(first_list[0] < second_list[0]):
            return_value.append(first_list.pop(0))
        elif(first_list[0] > second_list[0]):
            return_value.append(second_list.pop(0))
        else:
            return_value.append(first_list.pop(0))
            return_value.append(second_list.pop(0))
    return_value.extend(first_list)
    return_value.extend(second_list)
    return return_value
                
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    if(len(list1) == 2):
        first_list = list()
        first_list.append(list1[0])
        second_list = list()
        second_list.append(list1[1])
        return merge(first_list, second_list)
    if(len(list1) == 1):
        return list1
    if(len(list1) > 2):
        return merge(merge_sort(list1[:len(list1)/2]), merge_sort(list1[len(list1)/2:]))
    return []

# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    return_value = list()
    if(len(word) == 0):
        return [word]
    else:
        first = word[0]
        rest = word[1:]
        rest_strings = gen_all_strings(rest)
        return_value.extend(rest_strings)
        for string in rest_strings:
            for index in range(len(string)+1):
                return_value.append(string[:index] + first + string[index:])
        return return_value

# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    url = codeskulptor.file2url(filename)
    word_list = urllib2.urlopen(url)
    return word_list.read()

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
#run()

