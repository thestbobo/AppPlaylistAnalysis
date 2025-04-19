import warnings

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self.min_dur = None
        self.selected_album = None
        self.dTotMaxFloat = None
        pass

    def handle_build_graph(self,e):
        durstr = self._view._txtInDurata.value
        try:
            self.min_dur = float(durstr)
        except ValueError:
            self._view.txt_result.controls.append(f"Please, insert a valid value...")
            self._view.update_page()



        self._model.buildGraph(self.min_dur)

        self._view.txt_result.controls.append(ft.Text(
            f"Graph created with n. of nodes = {len(self._model._myGraph.nodes)} and n. of edges = {len(self._model._myGraph.edges)}"))

        # fill DD
        for n in self._model._myGraph.nodes:
            self._view._ddAlbum.options.append(ft.dropdown.Option(data=n, text=n.Title, on_click=self._handleDdAlbum))

        self._view.update_page()

        pass

    def _handleDdAlbum(self, e):
        if e.control.data is None:
            self.selected_album = None
        else:
            self.selected_album = e.control.data



    def handle_analisi_comp(self, e):
        dim, totDur = self._model.getConnected(self.selected_album)
        self._view.txt_result.controls.append(ft.Text(f"Connected component found:\n"
                                                      f"Dimension: {dim}\n"
                                                      f"Total Duration: {totDur}\n"))
        self._view.update_page()
        pass

    def handle_get_set_album(self, e):
        dTotMax = self._view._txtInSoglia.value
        try:
            self.dTotMaxFloat = float(dTotMax)
        except ValueError:
            self._view.txt_result.contols.append(ft.Text(
                f"Please insert a valid value for the maximum complessive duration..."
            ))
            self._view.update_page()
        path, dur = self._model.getPath(self.dTotMaxFloat, self.selected_album)
        self._view.txt_result.controls.append(ft.Text(
            f"Path found with length = {len(path)} and total duration = {dur}"
        ))
        self._view.update_page()

        pass






