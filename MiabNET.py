import matplotlib.pyplot as plt
import networkx as nx
import random


class bottle:
    def __init__(self, bottle_id, src, dest):
        self.src = src
        self.dest = dest
        self.btl_id = bottle_id
        self.rf = False
        self.history = [src, ]

class node:
    def __init__(self, node_id, neighbors):
        self.nid = node_id
        self.bid = 0
        self.nbors = neighbors
        self.rtab = {}
        self.state = 'idle'
        self.pkt_queue = []
        self.btl_queue = []
    
    def fetchBottle(self):
        if len(bottleList[self.nid]) == 0:
            pass
        else:
            for each_btl in bottleList[self.nid]:
                self.btl_queue.append(each_btl)
            bottleList[self.nid] = []
        return 0

    def sendBottle(self, receipient, new_bottle):
        if receipient in self.nbors:
            bottleList[receipient].append(new_bottle)
        else:
            raise ValueError('Receipient is not a neighbor!')
        return 0

    def routeRequest(self, dest):
        self.bid = self.bid + 1
        new_btl = bottle(str(self.nid) + str(self.bid), self.nid, dest)
        self.sendBottle(self.nbors[random.randint(0, len(self.nbors) - 1)], new_btl) #should not use shuffle here
        return 0

    def bottleManage(self, btl):
        if btl.dest == self.nid:
            btl.history.append(self.nid)
            print('Bottle #' + str(btl.btl_id) + ' successfully finds a route:')
            print(btl.history)
        else:
            his_node_idx = 0
            for history_node in btl.history:
                if history_node in self.rtab.keys():
                    if (len(btl.history) - his_node_idx) < self.rtab[history_node][0]:
                        self.rtab[history_node][0] = len(btl.history) - his_node_idx
                        self.rtab[history_node][1] = btl.history[-1]
                else:
                    self.rtab.update({history_node : [(len(btl.history) - his_node_idx), btl.history[-1]]})
                his_node_idx = his_node_idx + 1

            if btl.rf:
                my_position = btl.history.index(self.node_id)
                self.sendBottle(my_position - 1, btl)
            else:
                btl.history.append(self.nid)
                next_hop_cand = []
                for each_neighbor in self.nbors:
                    if each_neighbor in btl.history:
                        pass
                    else:
                        next_hop_cand.append(each_neighbor)
                
                if len(next_hop_cand) == 0:
                    self.sendBottle(self.nbors[random.randint(0, len(self.nbors) - 1)], btl)
                else:
                    random.shuffle(next_hop_cand)
                    self.sendBottle(next_hop_cand[0], btl)
        return 0

    def fsm(self):
        if self.state == 'idle':
            self.fetchBottle()
            if len(self.pkt_queue) != 0:
                if self.pkt_queue[-1] in self.rtab.keys():
                    pass
                else:
                    self.state = 'route_req'
            else:
                if len(self.btl_queue) != 0:
                    self.state = 'btl_manage'
                else:
                    self.state = 'idle'
        elif self.state == 'route_req':
            self.routeRequest(self.pkt_queue.pop(0))
            if len(self.btl_queue) != 0:
                self.state = 'btl_manage'
            else:
                self.state = 'idle'
        elif self.state == 'btl_manage':
            self.bottleManage(self.btl_queue.pop(0))
            self.state = 'idle'
        return 0
         
if __name__ == '__main__':
    #Parameters
    cntNode = 20
    connectRate = 0.2
    tick_limit = 500

    #Global variables
    G = nx.erdos_renyi_graph(cntNode, connectRate, seed=36, directed=False)
    plt.subplot(111)
    nx.draw(G, with_labels=True)
    plt.savefig('./nwk.pdf')

    nodeList = []
    bottleList = []
    for each_node in range(G.number_of_nodes()):
        nodeList.append(node(each_node, [nbor for nbor in G[each_node]]))
        bottleList.append([])



    for tick in range(tick_limit):
        if tick == 0:
            nodeList[1].pkt_queue.append(8)
        for each_node in nodeList:
            each_node.fsm()
  
