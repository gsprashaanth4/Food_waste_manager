from collections import defaultdict
from datetime import datetime, timedelta
import heapq


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
        if self.head.next is None:
            self.head = None
            return
        temp = self.head
        while temp.next.next:
            temp = temp.next
        temp.next = None

    def delete_by_value(self, key, value):
        temp = self.head
        if temp and temp.key == key and temp.value == value:
            self.head = temp.next
            return
        prev = None
        while temp:
            if temp.key == key and temp.value == value:
                if prev:
                    prev.next = temp.next
                else:
                    self.head = temp.next
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
        
    def get_values(self, key):
        values = []
        temp = self.head
        while temp:
            if temp.key == key:
                values.append(temp.value)
            temp = temp.next
        return values

    def delete_all_by_key(self, key):
        pass

class FoodHeap:
    def __init__(self):
        self.heap = []

    def add_food(self, desc, expiry_time, food_type, amt, amt_type, provider_location_id):
        values = (expiry_time, desc, food_type, amt, amt_type, provider_location_id)
        self.heap.append(values)
        self.sift_up(len(self.heap) - 1)

    def sift_up(self, index):
        while index > 0:
            parent = (index - 1) // 2
            if self.heap[parent][0] > self.heap[index][0]:
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
            if left < size and self.heap[left][0] < self.heap[smallest][0]:
                smallest = left
            if right < size and self.heap[right][0] < self.heap[smallest][0]:
                smallest = right
            if smallest != index:
                self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
                index = smallest
            else:
                break

    def pop_soonest(self):
        if not self.heap:
            return None
        root = self.heap[0]
        last = self.heap.pop()
        if self.heap:
            self.heap[0] = last
            self.sift_down(0)
        return root

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

    def delete_by_value(self, key, value):
        idx = self._hash(key)
        self.buckets[idx].delete_by_value(key, value)


food_heap = FoodHeap()
ngo_needs = HashMap()
city_map = defaultdict(dict)
ngo_locations = {}

def add_route_ui():
    print("\n--- Add a New Route ---")
    print("This will add a route to the city map (e.g., from 'Restaurant A' to 'NGO Shelter').")
    loc1 = input("Enter the first location name (e.g., Restaurant A, Cafe B): ")
    loc2 = input("Enter the second location name (e.g., NGO Shelter, Food Bank): ")
    try:
        time = int(input(f"Enter travel time in minutes between '{loc1}' and '{loc2}' (e.g., 15): "))
        if time <= 0:
            print("Error: Time must be a positive number.")
            return
            
        city_map[loc1][loc2] = time
        city_map[loc2][loc1] = time
        print("Route added successfully!")
    except ValueError:
        print("Error: Invalid time. Please enter a number.")

def add_ngo_ui():
    print("\n--- Register an NGO Need ---")
    print("This will register an NGO and what food it needs.")
    ngo_id = input("Enter the NGO's unique name (e.g., City Shelter, Downtown Food Bank): ")
    location = input(f"Enter the location of '{ngo_id}' (this must match a name from your map, e.g., NGO Shelter): ")
    food_type = input(f"What food type does '{ngo_id}' need? (e.g., Vegetables, Bread, Fruit, Dairy): ")
    
    if not ngo_id or not location or not food_type:
        print("Error: All fields are required.")
        return
        
    ngo_needs.insert(food_type, ngo_id)
    ngo_locations[ngo_id] = location
    print("NGO need registered successfully!")

def add_food_ui():
    print("\n--- Add Surplus Food ---")
    print("This will add a food donation to the system.")
    provider_loc = input("Enter the provider's location (this must match a name from your map, e.g., Restaurant A): ")
    desc = input("Enter a brief description (e.g., Box of Carrots, 10 Loaves of Bread): ")
    food_type = input("Enter the food type (this must match an NGO need, e.g., Vegetables, Bread): ")
    try:
        expires_in = int(input("How many HOURS until it expires? (e.g., 6, 24, 48): "))
        if expires_in <= 0:
            print("Error: Hours must be a positive number.")
            return
            
        expiry_time = datetime.now() + timedelta(hours=expires_in)
        
        food_heap.add_food(desc, expiry_time, food_type, 0, "units", provider_loc)
        print("Surplus food added successfully!")
    except ValueError:
        print("Error: Invalid number of hours. Please enter a number.")

def find_match_and_route():
    print("\n========================================")
    print("--- Finding Best Match for Urgent Food ---")
    
    urgent_item = food_heap.pop_soonest()
    
    if not urgent_item:
        print("No surplus food is available to match.")
        print("========================================")
        return

    expiry_time, desc, food_type, _, _, provider_loc = urgent_item

    if expiry_time < datetime.now():
        print(f"'{desc}' from '{provider_loc}' has already expired. Discarding.")
        return

    print(f"\nProcessing urgent item: '{desc}' from '{provider_loc}'")
    
    potential_ngos = ngo_needs.get(food_type)
    if not potential_ngos:
        print(f"No NGOs have registered a need for '{food_type}'.")
        food_heap.add_food(desc, expiry_time, food_type, 0, "units", provider_loc)
        print("========================================")
        return

    best_ngo = None
    min_time = float('inf')

    print("\n--- Calculating Routes ---")
    for ngo_id in potential_ngos:
        ngo_loc = ngo_locations.get(ngo_id)
        if ngo_loc and provider_loc in city_map and ngo_loc in city_map[provider_loc]:
            time = city_map[provider_loc][ngo_loc]
            print(f"  > Route from '{provider_loc}' to '{ngo_loc}' (for NGO '{ngo_id}') takes {time} minutes.")
            if time < min_time:
                min_time = time
                best_ngo = ngo_id
        else:
            print(f"  > No direct route found from '{provider_loc}' to '{ngo_loc}'.")

    if best_ngo:
        print("\n*** MATCH FOUND! ***")
        print(f"  Deliver:    '{desc}'")
        print(f"  From:       '{provider_loc}'")
        print(f"  To:         NGO '{best_ngo}' at '{ngo_locations[best_ngo]}'")
        print(f"  Deliver in: {min_time} minutes")
        ngo_needs.delete_by_value(food_type, best_ngo)
    else:
        print("\nNo suitable match found. Could not find a route to any interested NGO.")
        food_heap.add_food(desc, expiry_time, food_type, 0, "units", provider_loc)
    print("========================================")

def main():
    while True:
        print("\n--- Food Waste Reduction Manager ---")
        print("1. Add a Route to the Map")
        print("2. Register an NGO Need")
        print("3. Add Surplus Food")
        print("4. Find Match for Next Urgent Item")
        print("5. Exit")
        
        choice = input("Enter your choice (1-5): ")
        
        if choice == '1':
            add_route_ui()
        elif choice == '2':
            add_ngo_ui()
        elif choice == '3':
            add_food_ui()
        elif choice == '4':
            find_match_and_route()
        elif choice == '5':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()






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




