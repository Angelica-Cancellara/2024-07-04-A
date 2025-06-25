import copy

from database.DAO import DAO
import networkx as nx

from model.sighting import Sighting


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


    #SE GLI ARCHI FOSSERO PESATI
    # def get_top_edges(self):
    #     '''stampare i 5 archi di peso maggiore, ordinati in oridne decrescente di peso, per ognuno di questi 5 archi stampare
    #     l'id del nodo di origine, l'id del nodo di destinazione ed il peso'''
    #     sorted_edges = sorted(self._graph.edges(data=True), key=lambda edge: edge[2].get('weight'), reverse=True)
    #     return sorted_edges[0:5]

    #su grafi NON orientati --> COMPONENTE CONNESSA: nx.connected_components(self._graph)
    #su grafi orientati --> COMPONENTE DEBOLMENTE CONNESSA: nx.weakly_connected_components(self._graph)
    #su grafi orientati --> COMPONENTE FORTEMENTE CONNESSA: nx.strongly_connected_components(self._graph)



    #SECONDA PARTE
    def cammino_ottimo(self):
        self._cammino_ottimo = []
        self._score_ottimo = 0
        self._occorrenze_mese = dict.fromkeys(range(1, 13), 0)

        for nodo in self._nodes:
            self._occorrenze_mese[nodo.datetime.month] += 1
            successivi_durata_crescente = self._calcola_successivi(nodo)
            self._calcola_cammino_ricorsivo([nodo], successivi_durata_crescente)
            self._occorrenze_mese[nodo.datetime.month] -= 1
        return self._cammino_ottimo, self._score_ottimo

    def _calcola_cammino_ricorsivo(self, parziale: list[Sighting], successivi: list[Sighting]):
        if len(successivi) == 0:
            score = Model._calcola_score(parziale)
            if score > self._score_ottimo:
                self._score_ottimo = score
                self._cammino_ottimo = copy.deepcopy(parziale)
        else:
            for nodo in successivi:
                # aggiungo il nodo in parziale ed aggiorno le occorrenze del mese corrispondente
                parziale.append(nodo)
                self._occorrenze_mese[nodo.datetime.month] += 1
                # nuovi successivi
                nuovi_successivi = self._calcola_successivi(nodo)
                # ricorsione
                self._calcola_cammino_ricorsivo(parziale, nuovi_successivi)
                # backtracking: visto che sto usando un dizionario nella classe per le occorrenze, quando faccio il
                # backtracking vado anche a togliere una visita dalle occorrenze del mese corrispondente al nodo che
                # vado a sottrarre
                self._occorrenze_mese[parziale[-1].datetime.month] -= 1
                parziale.pop()

    def _calcola_successivi(self, nodo: Sighting) -> list[Sighting]:
        """
        Calcola il sottoinsieme dei successivi ad un nodo che hanno durata superiore a quella del nodo, senza eccedere
        il numero ammissibile di occorrenze per un dato mese
        """
        successivi = self._graph.successors(nodo)
        successivi_ammissibili = []
        for s in successivi:
            if s.duration > nodo.duration and self._occorrenze_mese[s.datetime.month] < 3:
                successivi_ammissibili.append(s)
        return successivi_ammissibili

    @staticmethod
    def _calcola_score(cammino: list[Sighting]) -> int:
        """
        Funzione che calcola il punteggio di un cammino.
        :param cammino: il cammino che si vuole valutare.
        :return: il punteggio
        """
        # parte del punteggio legata al numero di tappe
        score = 100 * len(cammino)
        # parte del punteggio legata al mese
        for i in range(1, len(cammino)):
            if cammino[i].datetime.month == cammino[i - 1].datetime.month:
                score += 200
        return score