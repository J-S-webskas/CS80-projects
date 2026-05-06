class Node():
    def __init__(self, state, parent, action):
        self.state = state    # Current actor's person_id
        self.parent = parent  # Previous node (None for the start)
        self.action = action  # Movie connecting previous actor to current actor (movie_id)


class StackFrontier():
    def __init__(self):
        self.frontier = []  # Stores the node to-be processed

    def add(self, node):
        self.frontier.append(node)

    # 
    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)  # Loops through each node in self-frontier + compares person_ids

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node


class QueueFrontier(StackFrontier):

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]  # Removes first element from the list by slicing it
            return node
