from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._nodes = []
        self._edges = []
        self._idMap = {}


    def getAnni(self):
        return DAO.getAnni()

    def getShape(self, anno):
        return DAO.getShapes(anno)

    def buildGraph(self, anno, shape):
        self._graph.clear()
        self._nodes = DAO.getNodi(anno, shape)
        self._graph.add_nodes_from(self._nodes)

        self._idMap = {}
        for n in self._nodes:
            self._idMap[n.id] = n

        self._edges = DAO.getArchi(anno, shape, self._idMap)
        for e in self._edges:
            self._graph.add_edge(e[0], e[1])

    def getNumNodes(self):
        return self._graph.number_of_nodes()

    def getNumEdges(self):
        return self._graph.number_of_edges()

    def get_num_connesse(self):
        '''Stampare il numero di componenti debolmente connesse.'''
        return nx.number_weakly_connected_components(self._graph)

    def get_largest_connessa(self):
        ''' identificare la componente connessa di
        dimensione maggiore, e stamparne i nodi –
        includendo il dettaglio della città in cui è avvenuto
        l’avvistamento e la data. '''
        conn = list(nx.weakly_connected_components(self._graph))
        conn.sort(key=lambda x: len(x), reverse=True)
        return conn[0]


#su grafi NON orientati --> COMPONENTE CONNESSA: nx.connected_components(self._graph)
#su grafi orientati --> COMPONENTE DEBOLMENTE CONNESSA: nx.weakly_connected_components(self._graph)
#su grafi orientati --> COMPONENTE FORTEMENTE CONNESSA: nx.strongly_connected_components(self._graph)