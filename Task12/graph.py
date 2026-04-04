import json
import os
from collections import defaultdict, deque

WAL_FILE = "graphdb_wal.log"

class Node:
    def __init__(self, node_id, label, properties):
        self.id = node_id
        self.label = label
        self.properties = properties

class Edge:
    def __init__(self, src, dst, label, properties):
        self.src = src
        self.dst = dst
        self.label = label
        self.properties = properties

class GraphDB:
    def __init__(self):
        self.nodes = {}
        self.edges = []
        self.adj = defaultdict(list)
        self.node_counter = 0
        self.index = defaultdict(dict)

        self.recover_from_wal()

    def write_wal(self, record):
        with open(WAL_FILE, "a") as f:
            f.write(json.dumps(record) + "\n")

    def recover_from_wal(self):
        if not os.path.exists(WAL_FILE):
            return

        with open(WAL_FILE) as f:
            for line in f:
                record = json.loads(line.strip())
                if record["type"] == "node":
                    self._create_node_internal(**record["data"])
                elif record["type"] == "edge":
                    self._create_edge_internal(**record["data"])

    def create_node(self, label, properties):
        node = self._create_node_internal(label, properties)

        self.write_wal({
            "type": "node",
            "data": {
                "label": label,
                "properties": properties
            }
        })

        print(f"Node created: {label}#{node.id}")
        return node

    def _create_node_internal(self, label, properties):
        self.node_counter += 1
        node = Node(self.node_counter, label, properties)
        self.nodes[node.id] = node

        if "name" in properties:
            self.index[(label, "name")][properties["name"]] = node.id

        return node

    def create_edge(self, src_id, dst_id, label, properties):
        edge = self._create_edge_internal(src_id, dst_id, label, properties)

        self.write_wal({
            "type": "edge",
            "data": {
                "src_id": src_id,
                "dst_id": dst_id,
                "label": label,
                "properties": properties
            }
        })

        print(f"Edge created: {src_id} --{label}--> {dst_id}")
        return edge

    def _create_edge_internal(self, src_id, dst_id, label, properties):
        edge = Edge(src_id, dst_id, label, properties)
        self.edges.append(edge)
        self.adj[src_id].append(edge)
        return edge

    def match_friends_work_company(self, company_name):
        result = []

        for node in self.nodes.values():
            if node.label != "Person":
                continue

            for edge1 in self.adj[node.id]:
                if edge1.label != "FRIENDS_WITH":
                    continue

                friend = self.nodes[edge1.dst]

                for edge2 in self.adj[friend.id]:
                    if edge2.label != "WORKS_AT":
                        continue

                    company = self.nodes[edge2.dst]

                    if company.properties.get("name") == company_name:
                        result.append((node.properties["name"], company_name))

        return result

    def shortest_path(self, start_id, end_id):
        queue = deque([(start_id, [start_id])])
        visited = set()

        while queue:
            current, path = queue.popleft()

            if current == end_id:
                return path

            visited.add(current)

            for edge in self.adj[current]:
                if edge.dst not in visited:
                    queue.append((edge.dst, path + [edge.dst]))

        return None

    def stats(self):
        wal_entries = 0

        if os.path.exists(WAL_FILE):
            with open(WAL_FILE) as f:
                wal_entries = sum(1 for _ in f)

        print(f"Nodes: {len(self.nodes)}")
        print(f"Edges: {len(self.edges)}")
        print(f"Indexes: {len(self.index)}")
        print(f"WAL entries: {wal_entries}")


if __name__ == "__main__":
    db = GraphDB()

    person1 = db.create_node("Person", {"name": "Vicky", "age": 30})
    person2 = db.create_node("Person", {"name": "Maha", "age": 28})
    pres = db.create_node("Company", {"name": "Presidio"})

    db.create_edge(person1.id, person2.id, "FRIENDS_WITH", {"since": 2021})
    db.create_edge(person2.id, pres.id, "WORKS_AT", {"role": "Associate Engineer"})

    print("\nMATCH Query Result:")
    print(db.match_friends_work_company("Presidio"))

    print("\nShortest Path:")
    print(db.shortest_path(person1.id, pres.id))

    print("\nStats:")
    db.stats()
