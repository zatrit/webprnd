import * as vis from "vis-network";

let nodeCounter: number = 0;
let edgeCounter: number = 0;
let network: vis.Network;

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
        edges: {
            arrows: {
                to: true,
            },
            smooth: false
        },
        interaction: {
            multiselect: true,
        },
    };

    network = new vis.Network(container, data, options);

    document.onkeydown = e => {
        console.log(e.code);
        

        if (e.code == "KeyN") {
            addNode();
        }
        else if (e.code == "Delete") {
            deleteSelected();
        }
        else if (e.code == "KeyA") {
            connectSelected();
        }
    };
});

/** https://stackoverflow.com/a/31973533/12245612 */
function pairwise<T>(arr: T[], func: (cur: T, next: T) => void) {
    for (let i = 0; i < arr.length - 1; i++) {
        func(arr[i], arr[i + 1])
    }
}

function addNode() {
    nodeCounter++;
    edgeCounter++;

    nodes.add({ id: nodeCounter, label: "Node " + nodeCounter });
    edges.add({ id: edgeCounter, from: nodeCounter - 1, to: nodeCounter });
}

function deleteSelected() {
    const selection = network.getSelection();
    selection.nodes.forEach(n => {
        // По какой-то причине vis.js не удаляет сам соединения
        // поэтому это прописано здесь
        network.getConnectedEdges(n).forEach(e => edges.remove(e));
        nodes.remove(n);
    });
    selection.edges.forEach(e => edges.remove(e));
}

function connectSelected() {
    pairwise(network.getSelectedNodes(), (cur, next) => {
        edgeCounter++;
        edges.add({ id: edgeCounter, from: cur, to: next });
    });
}