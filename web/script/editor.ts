import * as vis from "vis"

const nodes = new vis.DataSet([
    { id: 1, label: 'Node 1', shape: "rect" },
    { id: 2, label: 'Node 2' },
    { id: 3, label: 'Node 3' },
    { id: 4, label: 'Node 4' },
    { id: 5, label: 'Node 5' }
]);

// create an array with edges
const edges = new vis.DataSet([
    { from: 1, to: 3 },
    { from: 1, to: 2 },
    { from: 2, to: 4 },
    { from: 2, to: 5 }
]);

// create a network
const container = document.getElementById("editor-container");

// provide the data in the vis format
const data = {
    nodes: nodes,
    edges: edges
};
const options = {
    height: '100%',
    width: '100%'
};

// initialize your network!
const network = new vis.Network(container!, data, options);
