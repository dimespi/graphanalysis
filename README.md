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



