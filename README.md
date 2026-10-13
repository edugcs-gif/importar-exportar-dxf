# Importar/Exportar DXF — complemento para QGIS

Complemento (plugin) para o QGIS 3.x que adiciona uma barra de ferramentas
própria, **Importar/Exportar DXF**, com dois botões:

| Botão | O que faz |
|---|---|
| **Importar CAD (DXF)** | Abre uma janela para escolher o tipo de entidade e o arquivo DXF, e cria camadas temporárias no projeto separadas por *Layer* do CAD. |
| **Exportar seleção para DXF** | Grava os polígonos selecionados da camada ativa como polilinhas fechadas em `Área de Trabalho\dxf\Exportado(DXF).dxf`. |

Ele reúne num só lugar os antigos plugins "Importador CAD" e "Exportador DXF".

## Importação

A janela de importação oferece quatro opções:

| Opção | Entidades DXF lidas | Resultado no QGIS |
|---|---|---|
| **Pontos / Vértices / Blocos** | `POINT`, vértices de `LWPOLYLINE`/`POLYLINE`, ponto de inserção de `INSERT` (blocos) e centro de `CIRCLE` | Grupo `<arquivo> - Pontos CAD` com uma camada de pontos por Layer do CAD |
| **Textos** | `TEXT` e `MTEXT` (quebras `\P` viram espaço) | Uma camada de pontos `<arquivo> - Textos` no ponto de inserção, com os campos `Texto` e `Layer_CAD` |
| **Linhas (abertas)** | `LINE`, `LWPOLYLINE`, `POLYLINE` abertas | Grupo `<arquivo> - Linhas` com uma camada de linhas por Layer do CAD |
| **Polígonos (fechados)** | `LWPOLYLINE`/`POLYLINE` fechadas (flag *closed* ou primeiro vértice = último) com 3+ vértices | Grupo `<arquivo> - Polígonos` com uma camada de polígonos por Layer do CAD |

Detalhes:

- O arquivo padrão sugerido é `Área de Trabalho\dxf\DXF.dxf` do usuário logado;
  outro arquivo pode ser escolhido em **Procurar...**.
- Todas as camadas criadas têm o campo `Layer_CAD` com o nome do Layer de origem.
- As camadas são **temporárias (memória)** e usam o SRC do projeto atual —
  defina o SRC do projeto antes de importar.
- Geometrias de linhas e polígonos inválidas (segundo o GEOS) são descartadas.
- Arquivos `.dwg` não são suportados: salve como `.dxf` no CAD.
- A leitura usa a biblioteca [ezdxf](https://ezdxf.mozman.at/). Se ela não estiver
  instalada no Python do QGIS, o plugin a instala automaticamente via `pip` na
  primeira importação (é preciso acesso à internet).

## Exportação

1. Selecione a camada de polígonos na legenda (camada ativa).
2. Selecione um ou mais polígonos.
3. Clique em **Exportar seleção para DXF**.

O arquivo `Área de Trabalho\dxf\Exportado(DXF).dxf` é criado (ou **sobrescrito**)
com os polígonos selecionados. A pasta `dxf` é criada se não existir.

A exportação usa o exportador nativo do QGIS (`QgsDxfExport`) em vez do GDAL/OGR.
Os polígonos são copiados para uma camada temporária com simbologia "apenas
contorno" (sem preenchimento); assim o QGIS os grava como **polilinhas fechadas**
(`Closed = Yes`), sem duplicar o último vértice, prontas para uso no CAD.

## Instalação

### A partir de um ZIP

1. Compacte a pasta `importar_exportar_dxf/` deste repositório num `.zip`
   (a pasta precisa estar na raiz do zip).
2. No QGIS: **Complementos → Gerenciar e instalar complementos → Instalar a partir do ZIP**.
3. Ative **Importar/Exportar DXF** na lista de complementos.

### Manualmente

Copie a pasta `importar_exportar_dxf/` para a pasta de plugins do perfil do QGIS:

- Windows: `%APPDATA%\QGIS\QGIS3\profiles\default\python\plugins\`
- Linux: `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/`
- macOS: `~/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins/`

Reinicie o QGIS e ative o complemento.

## Requisitos

- QGIS 3.0 ou superior
- `ezdxf` (instalado automaticamente quando ausente)

## Estrutura do projeto

```
importar_exportar_dxf/
├── __init__.py       # classFactory: ponto de entrada exigido pelo QGIS
├── metadata.txt      # metadados do plugin (nome, versão, autor, categoria...)
├── plugin.py         # barra de ferramentas, menu e ações Importar/Exportar
├── dialog.py         # janela de importação (tipo de entidade + arquivo DXF)
├── logic.py          # rotinas de importação via ezdxf (pontos, textos, linhas, polígonos)
├── exportador.py     # exportação da seleção via QgsDxfExport
├── icon.png          # ícone do plugin
├── icon_importar.png # ícone do botão Importar
└── icon_exportar.png # ícone do botão Exportar
```

## Autor

Edu Gabriel
