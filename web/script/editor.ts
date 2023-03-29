import * as vis from "vis-network";

let counter: number = 0;
const nodesArray = [{ id: 0, label: "Node 0" }];
const nodes = new vis.DataSet<vis.Node>(nodesArray);
const edges = new vis.DataSet<vis.Edge>([]);

document.addEventListener("DOMContentLoaded", () => {
    const style = getComputedStyle(document.body);
    const container = document.getElementById("editor-container")!;

    const data = { nodes, edges, };
    const options: vis.Options = {
        height: '100%',
        width: '100%',
        physics: false,
        nodes: {
            color: style.getPropertyValue("--bs-info"),
            shape: "box",
            borderWidth: 0,
            font: {
                color: style.getPropertyValue("--bs-body-color"),
            },
        },
        interaction: {
            multiselect: true,
        },
    };

    const network = new vis.Network(container, data, options);
});

function addNode() {
    counter++;

    nodes.add({ id: counter, label: "Node " + counter });
    edges.add({ id: counter, from: counter - 1, to: counter })
}