import * as vis from "vis-network"

document.addEventListener("DOMContentLoaded", () => {
    const nodeArray = [
        { id: 1, label: 'Node 1' },
        { id: 2, label: 'Node 2' },
        { id: 3, label: 'Node 3' },
        { id: 4, label: 'Node 4' },
        { id: 5, label: 'Node 5' },
    ];
    const nodes = new vis.DataSet(nodeArray);
    const style = getComputedStyle(document.body);

    const edges = new vis.DataSet([
        { id: 1, from: 1, to: 3 },
        { id: 2, from: 1, to: 2 },
        { id: 3, from: 2, to: 4 },
        { id: 4, from: 2, to: 5 },
    ]);

    const container = document.getElementById("editor-container")!;

    const data = {
        nodes: nodes,
        edges: edges,
    };
    const options: vis.Options = {
        height: '100%',
        width: '100%',
        physics: false,
        nodes: {
            color: style.getPropertyValue("--aren-cyan"),
            shape: "box",
            borderWidth: 0,
            font: {
                face: "Arial, sans-serif"
            },
        },
    };

    const network = new vis.Network(container, data, options);
});