# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 17:21:40 2019

@author: Mikef

code for heap collected from BlackBoard, edited by Michael
"""

import matplotlib.pyplot as plt
import math

class node:
    def __init__(self, word, count):
        self.word = word
        self.count = count


class MaxHeap(object):
    # Constructor
    def __init__(self):
        self.tree = []

    def is_empty(self):
        return len(self.tree) == 0

    def parent(self, i):
        if i == 0:
            return -math.inf
        return self.tree[(i - 1) // 2]

    def left_child(self, i):
        c = 2 * i + 1
        if c >= len(self.tree):
            return node("~~~~~~~~~~~~~~~",-math.inf)
        return self.tree[c]

    def right_child(self, i):
        c = 2 * i + 2
        if c >= len(self.tree):
            return node("~~~~~~~~~~~~~~~",-math.inf)
        return self.tree[c]

    def insert(self, item):
        self.tree.append(item)
        self._percolate_up(len(self.tree) - 1)

    def _percolate_up(self, i):
        if i == 0:
            return

        parent_index = (i - 1) // 2

        if self.tree[parent_index].count < self.tree[i].count:
            self.tree[i], self.tree[parent_index] = self.tree[parent_index], self.tree[i]
            self._percolate_up(parent_index)
            
        #I'm assuming it's by count, then in alphabetical order
        elif self.tree[parent_index].word > self.tree[i].word and self.tree[parent_index].count == self.tree[i].count:
            self.tree[i], self.tree[parent_index] = self.tree[parent_index], self.tree[i]
            self._percolate_up(parent_index)

    def extract_max(self):
        if len(self.tree) < 1:
            return None
        if len(self.tree) == 1:
            return self.tree.pop()

        root = self.tree[0]
        self.tree[0] = self.tree.pop()

        self._percolate_down(0)

        return root

    def _percolate_down(self, i):
        if self.tree[i].count > max(self.left_child(i).count, self.right_child(i).count):
            return
        
        
        if self.tree[i].count == max(self.left_child(i).count, self.right_child(i).count):
            print("Something's broke.")
            offending_child_index =  2 * i + 1 if self.left_child(i).count == self.tree[i].count else 2 * i + 2
            if self.left_child(i).count == self.right_child(i).count and self.right_child(i).word < self.left_child(i).word:
                offending_child_index = 2 * i + 2
            else:
                offending_child_index = 2 * i + 1
            print(offending_child_index)
            if self.tree[i].word < self.tree[offending_child_index].word:
                return

            self.tree[i], self.tree[offending_child_index] = self.tree[offending_child_index], self.tree[i]
            self._percolate_down(offending_child_index)
            return
                
        
        max_child_index = 2 * i + 1 if self.left_child(i).count > self.right_child(i).count else 2 * i + 2

        self.tree[i], self.tree[max_child_index] = self.tree[max_child_index], self.tree[i]
        self._percolate_down(max_child_index)


    def draw(self):
        if not self.is_empty():
            fig, ax = plt.subplots()
            self.draw_(0, 0, 0, 100, 50, ax)
            ax.axis('off')
            ax.set_aspect(1.0)

            plt.show()

    def draw_(self, i, x, y, dx, dy, ax):
        if self.left_child(i) > -math.inf:
            ax.plot([x, x - dx], [y, y - dy], linewidth=1, color='k')
            self.draw_(2 * i + 1, x - dx, y - dy, dx / 2, dy, ax)
        if self.right_child(i) > -math.inf:
            ax.plot([x, x + dx], [y, y - dy], linewidth=1, color='k')
            self.draw_(2 * i + 2, x + dx, y - dy, dx / 2, dy, ax)
        ax.text(x, y, str(self.tree[i]), size=20,
                ha="center", va="center",
                bbox=dict(facecolor='w', boxstyle="circle"))
    
    def print(self):
        for item in self.tree:
            print(item.word, ": ", item.count, end = ', ')
        print()

def count_occurance(list):
    dict = {}
    for item in list:
        if item.lower() in dict.keys():
            dict[item.lower()] += 1
        else:
            dict[item.lower()] = 1
    return dict

def throw_it_on_the_pile(dict):
    heap = MaxHeap()
    for key in dict.keys():
        heap.insert(node(key, dict[key]))
    return heap

def read_to_list():
    file = open("words.txt", 'r')
    list = []
    uncollected = file.readlines()
    for line in uncollected:
        list.append(line.lower().strip())
    file.close()
    return list

if __name__ == "__main__":
    list = read_to_list()
    dict = count_occurance(list)
    heap = throw_it_on_the_pile(dict)
    k = int(input("How many items do you wish to see?\n"))
    while not heap.is_empty() and k != 0:
        curr_max = heap.extract_max()
        print(curr_max.word, ": ", curr_max.count, end = '')
        if k != 1:
            print(end = ', ')
        k = k - 1
    if k != 0:
        print("\nSorry, that's all the items here.")
    