from common import *

class Node:
    def __init__(self, ID, networksimulator, costs):
        self.myID = ID
        self.ns = networksimulator
        num = self.ns.NUM_NODES 
        self.distanceTable = [[0 for i in range(num)] for j in range(num)]
        self.routes = [0 for i in range(num)]

        self.has_link = [[] for i in range(num)]

        # -----------------------INITALIZING DISTANCE TABLE---------------------
        # For ever source in distanceTable
        for k in range(num):

            # For each destination of the current source
            for j in range(num):

                # If at row of the current node
                if k == self.myID:
                    # DistanceTable row is equals to the costs parameters
                    self.distanceTable[k] = costs


                # If at the destination is equlas to source
                elif k == j:
                    # No connection (0)
                    self.distanceTable[k][j] = 0

                # If not a self connection (0) or at the proper row for current source distanceTable at current [source][destination] connection is nonexistant (999)
                else:
                    self.distanceTable[k][j] = self.ns.INFINITY

        # -------------------------INITALIZING ROUTES LIST and SAVING LINKS TO ALL NEIGHBORING NODES---------------------------

        for dest in range(self.ns.NUM_NODES):

            # If route exists
            if self.distanceTable[self.myID][dest] != self.ns.INFINITY:
                self.routes[dest] = dest
                self.has_link[dest] = [dest, True]

            else:

                self.has_link[dest] = [dest, False]


        # -------------------------TRANSMITTING DISTANCE TABLE TO ALL NEIGHBOURS-----

        for link in self.has_link:

            router_id = link[0]
            link_state = link[1]

            if link_state is True and router_id != self.myID:
                pkt = RTPacket(self.myID, router_id, costs)
                self.ns.tolayer2(pkt)




    def recvUpdate(self, pkt):

        self.distanceTable[pkt.sourceid] = pkt.mincosts

        # -------------------------BELLMAN FORD DISTANCE VECTOR ROUTING ALGORITHM--------------------------

        retransmit = False


        # Assume some router destinaion can be reached via router_id (updated costs from pkt.sourceid)
        router_id = pkt.sourceid

        # distance of link between this node and router_id (router with new min costs)
        d1 = self.distanceTable[self.myID][router_id]

        # for every destination router accessable via router
        for router_destination_id in range(self.ns.NUM_NODES): # Excluding non-existant links
            if self.distanceTable[router_id][router_destination_id] == self.ns.INFINITY:
                pass

            direct_cost = self.distanceTable[self.myID][router_destination_id]

            # cost of link from router_id to router_destination_id
            d3 = self.distanceTable[router_id][router_destination_id]

            # Cost of path to router_destination_id via router
            cost_via_router = d1 + d3

            # If cost via router is less than direct cost
            if cost_via_router < direct_cost and self.has_link[router_id][1]:

                # set new distance as the cost via router
                self.distanceTable[self.myID][router_destination_id] = cost_via_router
                # Set the next hop for reaching router_destination_id to be via router

                next_hop_to_router = self.routes[router_id]
                self.routes[router_destination_id] = next_hop_to_router

                # Since an alteration to this nodes distance table and next hop list was made, inform neighbours
                retransmit = True

        # -------------------------TRANSMIT NEW DISTANCETABLE TO ALL ADJACENT NODES--------------------------

        # Do not retransmit if there were no new paths found
        if retransmit:
        
            for link in self.has_link:

                router_id = link[0]
                link_state = link[1]

                if link_state is True and router_id != self.myID:
                    pkt = RTPacket(self.myID, router_id, self.distanceTable[self.myID])
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
