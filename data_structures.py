from collections import defaultdict
from datetime import datetime, timedelta


class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def add_top(self, key, value):
        new_node = Node(key, value)
        new_node.next = self.head
        self.head = new_node

    def add_bottom(self, key, value):
        new_node = Node(key, value)
        if self.head is None:
            self.head = new_node
            return
        temp = self.head
        while temp.next:
            temp = temp.next
        temp.next = new_node

    def insert_at_position(self, key, value, position):
        new_node = Node(key, value)
        if position == 1:
            new_node.next = self.head
            self.head = new_node
            return

        temp = self.head
        for _ in range(position - 2):
            if temp is None:
                print("Position out of range")
                return
            temp = temp.next

        if temp is None:
            print("Position out of range")
            return

        new_node.next = temp.next
        temp.next = new_node

    def delete_head(self):
        if self.head is None:
            print("List is empty (underflow_)")
            return
        self.head = self.head.next

    def delete_tail(self):
        if self.head is None:
            print("List is empty (underflow_)")
            return
        if self.head.next is None:  # only one element
            self.head = None
            return
        temp = self.headm
        while temp.next.next:
            temp = temp.next
        temp.next = None

    def delete_by_value(self, key, value):
        """Delete node where key == food type AND value == NGO"""
        temp = self.head

        # if head matches
        if temp and temp.key == key and temp.value == value:
            self.head = temp.next
            return

        prev = None
        while temp:
            if temp.key == key and temp.value == value:
                prev.next = temp.next
                return
            prev = temp
            temp = temp.next

        print(f"Value ({key}, {value}) not found")

    def display(self):
        if self.head is None:
            print("underflow_")
            return
        temp = self.head
        while temp:
            print(f"[{temp.key} : {temp.value}]", end=" -> ")
            temp = temp.next
        print("null")



class FoodHeap:
    def __init__(self):
        self.heap = []

    def add_food(self, desc, goes_out_in, goi_type, food_type, amt, amt_type):
        if goi_type == "days":
            goi = datetime.now() + timedelta(days=goes_out_in)
        elif goi_type == "hrs":
            goi = datetime.now() + timedelta(hours=goes_out_in)
        else:
            raise ValueError("goi_type must be 'days' or 'hrs'")

        values = [desc, goi, food_type, amt, amt_type]
        self.heap.append(values)
        self.sift_up(len(self.heap) - 1)

    def sift_up(self, index):
        while index > 0:
            parent = (index - 1) // 2
            if self.heap[parent][1] > self.heap[index][1]:
                self.heap[parent], self.heap[index] = self.heap[index], self.heap[parent]
                index = parent
            else:
                break

    def sift_down(self, index):
        size = len(self.heap)
        while True:
            left = 2 * index + 1
            right = 2 * index + 2
            smallest = index

            if left < size and self.heap[left][1] < self.heap[smallest][1]:
                smallest = left
            if right < size and self.heap[right][1] < self.heap[smallest][1]:
                smallest = right

            if smallest != index:
                self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
                index = smallest
            else:
                break

    def redo_heap(self):
        n = len(self.heap)
        for i in range(n // 2 - 1, -1, -1):
            self.sift_down(i)

    def pop_expiring(self):
        if not self.heap:
            return None

        if datetime.now() >= self.heap[0][1]:
            root = self.heap[0]
            last = self.heap.pop()
            if self.heap:
                self.heap[0] = last
                self._sift_down(0)
            return root
        return None

    

class HashMap:
    def __init__(self, size=10):
        self.size = size
        self.buckets = [LinkedList() for _ in range(size)]

    def _hash(self, key):
        return sum(ord(c) for c in key) % self.size

    def insert(self, key, value):
        idx = self._hash(key)
        self.buckets[idx].add_bottom(key, value)

    def get(self, key):
        idx = self._hash(key)
        return self.buckets[idx].get_values(key)

    def delete_by_key(self, key):
        idx = self._hash(key)
        return self.buckets[idx].delete_all_by_key(key)

    def delete_by_value(self, key, value):
        idx = self._hash(key)
        return self.buckets[idx].delete_by_value(key, value)

    def display(self):
        for i, bucket in enumerate(self.buckets):
            print(f"Bucket {i}: ", end="")
            bucket.display()






## THE BELOW IS AI GENERATED...FOR REFERENCE
# # ---------- HashMap for NGO needs ----------
# class NGOMap:
#     def __init__(self):
#         self.map = defaultdict(list)  # food_type -> [(ngo_id, qty)]

#     def add_need(self, ngo_id, food_type, qty):
#         self.map[food_type].append((ngo_id, qty))

#     def get_ngos_for_food(self, food_type):
#         return self.map.get(food_type, [])


# # ---------- Union-Find for Clustering ----------
# class UnionFind:
#     def __init__(self):
#         self.parent = {}

#     def find(self, x):
#         if self.parent[x] != x:
#             self.parent[x] = self.find(self.parent[x])
#         return self.parent[x]

#     def union(self, x, y):
#         for node in [x, y]:
#             if node not in self.parent:
#                 self.parent[node] = node
#         root_x, root_y = self.find(x), self.find(y)
#         if root_x != root_y:
#             self.parent[root_y] = root_x




