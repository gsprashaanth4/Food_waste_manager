import heapq
from collections import defaultdict
from datetime import datetime, timedelta


food_heap = []


ngo_needs = defaultdict(list)


ngo_locations = {}

class Graph:
    """A weighted graph to represent city routes."""
    def __init__(self):
        self.adj = defaultdict(dict)

    def add_edge(self, u, v, weight):
        """Adds a two-way weighted edge between u and v."""
        self.adj[u][v] = weight
        self.adj[v][u] = weight

    def dijkstra(self, start_node, end_node):
        """Finds the shortest path from start to end using Dijkstra's algorithm."""
        if start_node not in self.adj or end_node not in self.adj:
            return None, float('inf')
        
        distances = {node: float('inf') for node in self.adj}
        previous_nodes = {node: None for node in self.adj}
        distances[start_node] = 0
        
        pq = [(0, start_node)]  # Priority queue: (distance, node)

        while pq:
            current_distance, current_node = heapq.heappop(pq)

            if current_node == end_node:
                break

            if current_distance > distances[current_node]:
                continue

            for neighbor, weight in self.adj[current_node].items():
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous_nodes[neighbor] = current_node
                    heapq.heappush(pq, (distance, neighbor))

        path = []
        node = end_node
        if distances[node] == float('inf'):
            return None, float('inf')
            
        while node is not None:
            path.append(node)
            node = previous_nodes[node]
        
        return path[::-1], distances[end_node]


city_map = Graph()



def add_route():
    """Lets the user add a new route to the city map."""
    print("\n--- Add a New Route ---")
    try:
        loc1 = input("Enter the first location (e.g., Restaurant A): ")
        loc2 = input("Enter the second location (e.g., NGO Shelter): ")
        
        if not loc1 or not loc2:
            print("Error: Location names cannot be empty.")
            return
            
        time = int(input(f"Enter travel time in minutes between {loc1} and {loc2} (e.g., 15): "))
        
        if time <= 0:
            print("Error: Time must be a positive number.")
            return
            
        city_map.add_edge(loc1, loc2, time)
        print(f"Route added: {loc1} <-> {loc2} = {time} mins")
        
    except ValueError:
        print("Error: Invalid time. Please enter a number.")
    except Exception as e:
        print(f"An error occurred: {e}")

def register_ngo_need():
    """Lets the user register a new NGO and its need."""
    print("\n--- Register an NGO Need ---")
    ngo_name = input("Enter the NGO's name (e.g., City Shelter): ")
    ngo_loc = input(f"Enter the location of '{ngo_name}' (e.g., NGO Shelter): ")
    food_type = input(f"What food type does '{ngo_name}' need? (e.g., Vegetables): ")
    
    if not ngo_name or not ngo_loc or not food_type:
        print("Error: All fields are required.")
        return

    ngo_needs[food_type].append(ngo_name)
    ngo_locations[ngo_name] = ngo_loc
    print(f"Need registered: '{ngo_name}' at '{ngo_loc}' needs '{food_type}'.")

def add_surplus_food():
    """Lets the user add a new surplus food item."""
    print("\n--- Add Surplus Food ---")
    try:
        provider_loc = input("Enter the food provider's location (e.g., Restaurant A): ")
        desc = input("Enter a description (e.g., Box of Carrots): ")
        food_type = input("Enter the food type (e.g., Vegetables): ")
        
        if not provider_loc or not desc or not food_type:
            print("Error: All fields are required.")
            return
            
        hours_to_expiry = int(input("How many HOURS until it expires? (e.g., 6): "))
        
        if hours_to_expiry <= 0:
            print("Error: Hours must be a positive number.")
            return
            
        expiry_time = datetime.now() + timedelta(hours=hours_to_expiry)
        
        item = (expiry_time, desc, food_type, provider_loc)
        
        heapq.heappush(food_heap, item)
        print("Food item added to the priority queue!")
        
    except ValueError:
        print("Error: Invalid number. Please enter hours as a number.")
    except Exception as e:
        print(f"An error occurred: {e}")

def find_match_and_route():
    """Main logic to find the best match using Dijkstra's algorithm."""
    print("\n--- Running Matchmaking Algorithm ---")
    
    if not food_heap:
        print("No surplus food available to match.")
        return

    expiry_time, desc, food_type, provider_loc = heapq.heappop(food_heap)
    
    if expiry_time < datetime.now():
        print(f"Item '{desc}' from '{provider_loc}' has already expired. Discarding.")
        return

    print(f"Processing urgent item: '{desc}' ({food_type}) from '{provider_loc}'")
    
    potential_ngos = ngo_needs.get(food_type)
    if not potential_ngos:
        print(f"No NGOs found for '{food_type}'. Item is removed from queue.")
        return

    best_ngo, best_route, min_time = None, None, float('inf')

    print(f"Checking routes from '{provider_loc}' using Dijkstra's Algorithm...")
    for ngo_name in potential_ngos:
        ngo_loc = ngo_locations.get(ngo_name)
        
        if ngo_loc:
            # --- THIS IS THE KEY CHANGE ---
            # Call Dijkstra's algorithm to find the true shortest path
            route, time = city_map.dijkstra(provider_loc, ngo_loc)
            
            if route:
                print(f"  > Shortest path to '{ngo_name}' at '{ngo_loc}' found: {time} minutes.")
                if time < min_time:
                    min_time = time
                    best_ngo = ngo_name
                    best_route = route
            else:
                print(f"  > No path found to '{ngo_name}' at '{ngo_loc}'.")

    if best_ngo:
        print("\n*** MATCH FOUND! ***")
        print(f"  Deliver:     {desc}")
        print(f"  From:        {provider_loc}")
        print(f"  To:          NGO '{best_ngo}' at '{ngo_locations[best_ngo]}'")
        print(f"  Travel Time: {min_time} minutes")
        print(f"  Route:       {' -> '.join(best_route)}")
        
        ngo_needs[food_type].remove(best_ngo)
    else:
        print("\nNo NGOs with a valid route were found for this item.")
        heapq.heappush(food_heap, (expiry_time, desc, food_type, provider_loc))




def main():
    """Runs the main interactive menu for the user."""
    while True:
        print("\n--- Food Waste Reduction Manager ---")
        print("1. Add a Route to the Map")
        print("2. Register an NGO Need")
        print("3. Add Surplus Food")
        print("4. Find Match for Next Urgent Item")
        print("5. Exit")
        
        choice = input("Enter your choice (1-5): ")
        
        if choice == '1':
            add_route()
        elif choice == '2':
            register_ngo_need()
        elif choice == '3':
            add_surplus_food()
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




