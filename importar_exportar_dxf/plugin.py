import os

from qgis.PyQt.QtWidgets import QAction
from qgis.PyQt.QtGui import QIcon

from .dialog import DialogoImportarCAD
from .exportador import exportar_selecao, OUTPUT_FILE

MENU = "Importar/Exportar DXF"


def _icone(nome):
    caminho = os.path.join(os.path.dirname(__file__), nome)
    return QIcon(caminho) if os.path.exists(caminho) else QIcon()


class ImportarExportarDXF:
    def __init__(self, iface):
        self.iface = iface
        self.toolbar = None
        self.actions = []

    def initGui(self):
        janela = self.iface.mainWindow()

        acao_importar = QAction(_icone("icon_importar.png"), "Importar CAD (DXF)", janela)
        acao_importar.setToolTip(
            "Importar Pontos/Vértices/Blocos/Círculos, Textos, Linhas ou Polígonos de um DXF"
        )
        acao_importar.triggered.connect(self.importar)

        acao_exportar = QAction(_icone("icon_exportar.png"), "Exportar seleção para DXF", janela)
        acao_exportar.setToolTip("Exporta os polígonos selecionados para:\n" + OUTPUT_FILE)
        acao_exportar.triggered.connect(self.exportar)

        self.actions = [acao_importar, acao_exportar]

        self.toolbar = self.iface.addToolBar(MENU)
        self.toolbar.setObjectName("ImportarExportarDXFToolbar")
        for acao in self.actions:
            self.toolbar.addAction(acao)
            self.iface.addPluginToMenu(MENU, acao)

    def unload(self):
        for acao in self.actions:
            self.iface.removePluginMenu(MENU, acao)
        if self.toolbar is not None:
            self.toolbar.deleteLater()
            self.toolbar = None
        self.actions = []

    def importar(self):
        DialogoImportarCAD(self.iface.mainWindow()).exec_()

    def exportar(self):
        exportar_selecao(self.iface)
