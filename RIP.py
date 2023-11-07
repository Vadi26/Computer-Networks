import networkx as nx

# Create a network topology
G = nx.Graph()

# Add nodes representing routers
G.add_node("Router1")
G.add_node("Router2")
G.add_node("Router3")

# Add links between routers with link costs (for RIP)
G.add_edge("Router1", "Router2", cost=1)
G.add_edge("Router2", "Router3", cost=2)
G.add_edge("Router3", "Router1", cost=3)

# Simulate RIP protocol
def rip_routing(graph):
    # Initialize routing table with directly connected networks
    routing_table = {node: {node: 0} for node in graph.nodes}

    # Perform RIP routing (simplified)
    for node in graph.nodes:
        for neighbor in graph.neighbors(node):
            for destination in graph.nodes:
                if destination not in routing_table[node]:
                    routing_table[node][destination] = float('inf')
                new_cost = routing_table[node][neighbor] + graph[neighbor][destination]['cost']
                if new_cost < routing_table[node][destination]:
                    routing_table[node][destination] = new_cost

    return routing_table

rip_result = rip_routing(G)
print("Routing table using RIP:")
print(rip_result)

# Simulate OSPF protocol
def ospf_routing(graph):
    # Initialize routing table with directly connected networks
    routing_table = {node: {node: 0} for node in graph.nodes}

    # Perform OSPF routing (simplified)
    for node in graph.nodes:
        for neighbor in graph.neighbors(node):
            for destination in graph.nodes:
                if destination not in routing_table[node]:
                    routing_table[node][destination] = float('inf')
                new_cost = routing_table[node][neighbor] + graph[neighbor][destination]['cost']
                if new_cost < routing_table[node][destination]:
                    routing_table[node][destination] = new_cost

    return routing_table

ospf_result = ospf_routing(G)
print("Routing table using OSPF:")
print(ospf_result)
