from itertools import count

from matplotlib.font_manager import json_load
from common import *

class Node:
    def __init__(self, ID, networksimulator, costs):
        self.myID = ID
        self.ns = networksimulator
        num = self.ns.NUM_NODES 
        self.distanceTable = [[0 for i in range(num)] for j in range(num)]
        self.routes = [0 for i in range(num)]

        for k in range(num):
            for j in range(num):
                if k == self.myID:
                    self.distanceTable[k] = costs

                elif k == j:
                    self.distanceTable[k][j] = 0

                else:
                    self.distanceTable[k][j] = self.ns.INFINITY

        self.routes = self.distanceTable[self.myID]

        source = self.myID

        for destination in range(num):
            if source != destination:
                if costs[destination] != self.ns.INFINITY:
                    pkt = RTPacket(source, destination, costs)

                    self.ns.tolayer2(pkt)

    def recvUpdate(self, pkt):

        self.distanceTable[pkt.sourceid] = pkt.mincosts

        # For every adjacent Node
        for adj_I in range(self.ns.NUM_NODES):

            # Exclude the current node receiving the update
            if adj_I != self.myID:

                # Exclude non existant links (infinity)
                if self.distanceTable[self.myID][adj_I] != self.ns.INFINITY:

                    # Distance for source to the current adjacent router
                    dist_source_adjacent = self.distanceTable[self.myID][adj_I]

                    # For each possible end point of the current source
                    for dest_I in range(self.ns.NUM_NODES):

                        # Exclude the router recieving update, and the router currently adjacent to source
                        if dest_I != self.myID or dest_I != adj_I:

                            # Exclude nonexistant links (infinity)
                            if self.distanceTable[adj_I][dest_I] != self.ns.INFINITY:

                                # Distance from source to destination
                                dist_source_destination = self.distanceTable[self.myID][dest_I]

                                # Distance from current adjacent to destination
                                dist_adjacent_destination = self.distanceTable[adj_I][dest_I]

                                # If there is a lower path from adjacent it becomes the new distance
                                new_distance = min(dist_source_adjacent + dist_adjacent_destination, dist_source_destination)
                                self.distanceTable[self.myID][dest_I] = new_distance
        
        # For every adjacent Node
        for node in range(self.ns.NUM_NODES):

            # Ignore the current node
            if node != self.myID:

                # Exclude nonexistant links (infinity)
                if self.distanceTable[self.myID][node] != self.ns.INFINITY:

                    # Create a packet
                    pkt = RTPacket(self.myID, node, self.distanceTable[self.myID])

                    # Send packet
                    self.ns.tolayer2(pkt)
        return

    def printdt(self):
        print("   D"+str(self.myID)+" |  ", end="")
        for i in range(self.ns.NUM_NODES):
            print("{:3d}   ".format(i), end="")
        print()
        print("  ----|-", end="")
        for i in range(self.ns.NUM_NODES):            
            print("------", end="")
        print()    
        for i in range(self.ns.NUM_NODES):
            print("     {}|  ".format(i), end="" )
            
            for j in range(self.ns.NUM_NODES):
                print("{:3d}   ".format(self.distanceTable[i][j]), end="" )
            print()            
        print()
        
