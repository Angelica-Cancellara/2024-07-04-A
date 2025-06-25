import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handle_graph(self, e):
        # Controllo degli inputs
        if self._view.ddyear.value is None:
            self._view.create_alert("Selezionare un anno!")
            return
        anno = int(self._view.ddyear.value)
        if self._view.ddshape.value is None or self._view.ddshape.value == "":
            self._view.create_alert("Selezionare una shape!")
            return
        shape = self._view.ddshape.value

        # stampa dei risultati
        self._view.txt_result1.controls.clear()
        self._model.buildGraph(anno, shape)
        self._view.txt_result1.controls.append(ft.Text(f"Numero di vertici: {self._model.getNumNodes()}"))
        self._view.txt_result1.controls.append(ft.Text(f"Numero di archi: {self._model.getNumEdges()}"))

        self._view.txt_result1.controls.append(
            ft.Text(f"Il grafo ha: {self._model.get_num_connesse()} componenti connesse"))
        connessa = self._model.get_largest_connessa()
        self._view.txt_result1.controls.append(ft.Text(f"La componente connessa più grande "
                                                       f"è costituita da {len(connessa)} nodi:"))
        for c in connessa:
            self._view.txt_result1.controls.append(ft.Text(c))

        # SE GLI ARCHI FOSSERO PESATI
        #STAMPA NODI MAGGIORI
        # self._view.txt_result1.controls.append(ft.Text(f"I 5 archi di peso maggiore sono:"))
        # top_edges = self._model.get_top_edges()
        # for edge in top_edges:
        #     self._view.txt_result1.controls.append(
        #         ft.Text(f"{edge[0].id} -> {edge[1].id} | weight = {edge[2]['weight']}"))

        self._view.btn_path.disabled = False

        self._view.update_page()

    def handle_path(self, e): #SECONDA PARTE
        self._view.txt_result2.controls.clear()

        path, punteggio = self._model.cammino_ottimo()
        self._view.txt_result2.controls.append(ft.Text(f"Il punteggio del percorso ottimo è {punteggio}"))
        self._view.txt_result2.controls.append(ft.Text(f"Il percorso ottimo è costituito da {len(path)} nodi:"))
        for p in path:
            self._view.txt_result2.controls.append(ft.Text(f"{p} | {p.shape} | {p.state} | {p.duration}"))

        self._view.update_page()

    def fillDDAnno(self):
        for a in self._model.getAnni():
            self._view.ddyear.options.append(ft.dropdown.Option(a))
        self._view.update_page()

    def fillDDShape(self, anno):
        anno = int(self._view.ddyear.value)
        self._view.ddshape.options.clear()
        for s in self._model.getShape(anno):
            self._view.ddshape.options.append(ft.dropdown.Option(s))
        self._view.update_page()