# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 09:17:44 2019

@author: Mikef
"""

class lru_node:
    def __init__(self, data, key, next = None, prev = None):
        self.data = data
        self.key = key
        self.prev = prev
        self.next = next

class least_recently_used:
    def __init__(self, max_keys):
        self.max_keys = max_keys
        self.head = None
        self.tail = None
        self.key_access = {}
    
    def get(self, key):
        if not self.is_key_valid(key):
            return -1
        value = self.key_access[key].data
        self._shift(key)
        return value
    
    #Because of how uniform this operation is, combined with how often the code will use it, I made it it's own method
    #it's private because the user shouldn't make things more recent all willy-nilly
    def _shift(self, key):
        if not self.is_key_valid(key):
            return
        most_recent = self.key_access[key]
        if most_recent == self.head:
            return
        
        #removes the node from the context of the list
        most_recent.prev.next = most_recent.next
        if most_recent != self.tail:
            most_recent.next.prev = most_recent.prev
        
        #makes the node the head
        most_recent.next = self.head
        most_recent.prev = None
        self.head.prev = most_recent
        self.head = most_recent
        if self.tail.next != None:
            self.tail = self.tail.next
    
    def is_key_valid(self, key):
        if key in self.key_access.keys():
            return True
        return False
    
    def max_capacity(self):
        return self.max_keys
    
    def is_full(self):
        if self.max_keys == len(self.key_access.keys()):
            return True
        return False
    
    def size(self):
        return len(self.key_access.keys())
    
    def put(self, key, value):
        if self.is_key_valid(key):
            self.key_access[key].data = value
            self._shift(key)
            return
        if self.is_full():
            self._remove()
        new_node = lru_node(value, key, self.head)
        if self.size() != 0:
            self.head.prev = new_node
        self.key_access[key] = new_node
        
        new_node.next = self.head
        self.head = new_node
        if self.size() == 1:
            self.tail = self.head
    
    def _remove(self):
        self.key_access.pop(self.tail.key)
        self.tail = self.tail.prev
        self.tail.next = None
    
    def print(self):
        iter = self.head
        while iter != None:
            print(iter.data)
            iter = iter.next

def main():
    lru = least_recently_used(3)
    lru.put(12,5)
    lru.put(0, 336)
    print(lru.get(12), end = '\n \n')
    lru.put(0, 1)
    lru.put(-20, 20)
    lru.put("butts", 3)
    print(lru.get("butts"), end = '\n \n')
    lru.put(0, "smelly smell")
    print(lru.max_capacity(), end = '\n \n')
    print(lru.get(12), end = '\n \n')
    lru.print()
    

if __name__ == "__main__":
    main()