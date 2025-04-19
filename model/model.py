import copy

import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):

        self._myGraph = nx.Graph()
        self._idMap = {}
        pass


    def getPath(self, max_dur_min, selected_album):
        max_dur = self._toMillisec(max_dur_min)
        self.path_best = []

        conn_comp = nx.node_connected_component(self._myGraph, selected_album)
        partial = []
        for n in conn_comp:
            if float(selected_album.totDurata) + float(n.totDurata) < float(max_dur):
                partial.append(n)
                self._recursion(partial, max_dur, conn_comp, selected_album)
                partial.pop()

        return self.path_best, self._toMinutes(self._getDuration(self.path_best))


    def _recursion(self, partial, max_dur, conn_comp, selected_album):
        current_node = partial[-1]
        if selected_album in partial and not self._verify_neighbors(self._myGraph.neighbors(current_node), partial, conn_comp, max_dur):
            if len(partial) > len(self.path_best):
                self.path_best = copy.deepcopy(partial)
            return

        for n in self._myGraph.neighbors(current_node):
            if n in conn_comp and self._getDuration(partial) + float(n.totDurata) < float(max_dur):
                partial.append(n)
                self._recursion(partial, max_dur, conn_comp, selected_album)
                partial.pop()



    def _verify_neighbors(self, neighbors, partial, conn_comp, max_dur):
        res = False
        for n in neighbors:
            if n in conn_comp and float(n.totDurata) + self._getDuration(partial) < float(max_dur):
                res = True
        return res

    def _getDuration(self, partial):
        res = 0.0
        for n in partial:
            res += float(n.totDurata)
        return res





    def getConnected(self, selected_album):
        connected_comp = nx.node_connected_component(self._myGraph, selected_album)
        dim = len(connected_comp)
        totDur = 0.0
        for n in connected_comp:
            totDur += float(n.totDurata)
        return dim, self._toMinutes(totDur)

    def buildGraph(self, min_dur):
        self._myGraph.clear()
        self._idMap.clear()
        durMs = self._toMillisec(min_dur)
        nodes = self._getNodes(durMs)
        for n in nodes:
            self._idMap[n.AlbumId] = n
        print(self._idMap)
        self._myGraph.add_nodes_from(nodes)
        self._addEdges()

        pass

    def _getNodes(self, min_dur):
        return DAO.getAlbumsDur(min_dur)

    def _addEdges(self):
        edges = DAO.getAlbumsPlaylist(self._idMap)
        for u, v in edges:
            self._myGraph.add_edge(u, v)
        pass

    def _toMillisec(self, dur):
        return dur*60*1000

    def _toMinutes(self, dur):
        return dur/1000/60
