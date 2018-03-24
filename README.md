### NodeGraphQt - PySide Widget

This is a *work in progress* widget I'm working on in my spare time, as
a learning exercise on how to write a custom node graph in PySide.

`NodeGraphQt` is node graph widget that can be implemented and repurposed into vfx applications that supports PySide.

![screencap01](https://raw.githubusercontent.com/jchanvfx/NodeGraphQt/master/example/screenshot.png)

#### Navigation:
zoom in/out : `Right Mouse Click + Drag` or `Mouse Scroll Up`/`Mouse Scroll Down`<br/>
pan scene : `Middle Mouse Click + Drag` or `Alt + Left Mouse Click + Drag`<br/>
fit to screen : `F`

![screencap02](https://raw.githubusercontent.com/jchanvfx/NodeGraphQt/master/example/screenshot_menu.png)

#### Shortcuts:
select all nodes : `Ctrl + A`<br/>
delete selected node(s) : `Backspace` or `Delete`<br/>
copy node(s): `Ctrl + C` _(copy to clipboard)_<br/>
paste node(s): `Ctrl + V` _(paste from clipboard)_<br/>
duplicate node(s) : `Alt + C`<br/>
save node layout : `Ctrl + S`<br/>
open node layout : `Ctrl + O` <br/>
undo action: `Ctrl+z` or `Command+z` _(OSX)_ <br/>
redo action: `Ctrl+Shift+z` or `Command+Shift+z` _(OSX)_ <br/>
toggle node (enable/disable): `d`

#### Tab Search for Nodes
![screencap03](https://raw.githubusercontent.com/jchanvfx/NodeGraphQt/master/example/screenshot_tab_search.png)

#### Example snippet
```python
from NodeGraphQt import NodeGraphWidget, Node

# create a node object
class MyNode(Node):
    """This is a example test node."""

    NODE_TYPE = 'MyNode'

    def __init__(self):
        super(MyNode, self).__init__()
        self.set_name('foo node')
        self.set_color(81, 54, 88)
        self.add_input('in')
        self.add_output('out')

# create a node
my_node = MyNode()

# create node graph.
graph = NodeGraphWidget()

# register node into the node graph.
graph.register_node(MyNode)

# add node to the node graph.
graph.add_node(my_node)

graph.show()
```

[view example.py script](https://github.com/jchanvfx/bpNodeGraph/blob/master/example.py)
