## Install

The plugin is compatible with QGIS 3 only (minimum version 3.4.1).


In QGIS, open the "Plugins" > "Manage and install plugin" dialog. Install the "Graph Analysis" plugin.


## Usage

The plugin installs the following UI elements:


- The “Graph Analysis” toolbar is installed and visible by default. It can be hidden using the corresponding entry in the “View” > “Toolbars” menu. This toolbar contains the following tools:
  * “Add a graph” button
  * “Select Nodes or Edges” selection tool

![graphanalysis](https://user-images.githubusercontent.com/31792531/51313636-55c11800-1a4e-11e9-92dc-19bfd308b618.png)

Above, the toolbar with all the tools enabled, in the order described above.

## “Add a graph” tool
![addgraph](https://user-images.githubusercontent.com/31792531/51313635-55288180-1a4e-11e9-8725-3f34d2949feb.png)

This tool adds a graph to the map. It uses the model and Qt to read and and write the graph and is therefore limited to the formats supported by that library. Note also that the raster layer added by this tool does not have all the capabilities of a normal QGIS vector or raster layer: It is limited to visualization and modification using the provided tools.


Click on “Browse…” to select a file (graph, txt) and OK to load the graph.

As a result, a new layer is created in the Table of Content and is displayed on the map canvas.

Properties of the layer can be visualized by right-clicking on it: A dialog opens where some details about the layer are displayed, including the location of the graph file and the CRS that is applied to it. It is also possible to get the nodes and edges attributes types. The add Edge and add node attribute dialogs do not work although it has been implemented in the backend. The same goes for the graphical properties.

![properties](https://user-images.githubusercontent.com/31792531/51314372-d3d1ee80-1a4f-11e9-81a4-604d5975f5fd.png)


## “Select Nodes or Edges” tool
![selecttool](https://user-images.githubusercontent.com/31792531/51314534-32976800-1a50-11e9-95e1-7b9ab77fd230.png)

This tool lets you select and edit graph nodes or edges on the map. To edit a node/edge value, make a click on the toolbar and make the selection then a dialog window appears. Click on the corresponding value you want to modify. To confirm your changes, proceed this way:
- If you have changed a node value, you have to click on the upper left corner icon to apply your changes

  ![selecticon](https://user-images.githubusercontent.com/31792531/51314904-3c6d9b00-1a51-11e9-8c44-d9e4c45f6a85.png)
- If you have changed an edge value, you have to click on the blank icon on the bottom left corner under "Add from vector layers"

  ![validateedge](https://user-images.githubusercontent.com/31792531/51314905-3d063180-1a51-11e9-975f-7115a7bb46c4.png)

## Symbology
The backend for the symbology has been implemented. To change the graphical style of the nodes/edges, you need a render.xml file. The one provided at the root of the plugin directory contains SVG shapes for the nodes. It is possible to apply your own style by modifying manually the render.xml file. The render.xml file contains some nodes IDs and edges start/end nodes Ids so you need to put the corresponding IDs in the render.xml. Here is an example with SVG shapes:


![svg](https://user-images.githubusercontent.com/31792531/51315787-4ee8d400-1a53-11e9-8d4e-f40326e6496f.png)

The corresponding xml code part for the nodes' shapes:

![renderxml](https://user-images.githubusercontent.com/31792531/51315889-89eb0780-1a53-11e9-8a9b-d22d150da2f6.png)







