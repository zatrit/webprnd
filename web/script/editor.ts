import * as vis from "vis-network";

let nodeCounter: number = 0;
let edgeCounter: number = 0;
let network: vis.Network;
let container: HTMLCanvasElement;

const nodes = new vis.DataSet<vis.Node>([]);
const edges = new vis.DataSet<vis.Edge>([]);

document.addEventListener("DOMContentLoaded", () => {
    container = document.getElementById("editor-container")! as HTMLCanvasElement;
    const style = getComputedStyle(document.body);

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
            navigationButtons: false,
            selectConnectedEdges: false,
            keyboard: true
        },
    };

    network = new vis.Network(container, data, options);

    document.onkeydown = e => {
        if (e.code == "KeyN") {
            addNode();
        }
        else if (e.code == "Delete") {
            deleteSelected();
        }
        else if (e.code == "KeyA") {
            if (e.ctrlKey) {
                e.preventDefault();
                selectAll();
            } else {
                connectSelected();
            }
        }
        else if (e.code == "Escape") {
            network.unselectAll();
        }
    };
});

/** https://stackoverflow.com/a/31973533/12245612 */
function pairwise<T>(arr: T[], func: (cur: T, next: T) => void) {
    for (let i = 0; i < arr.length - 1; i++) {
        func(arr[i], arr[i + 1]);
    }
}

function addNode() {
    container.style.cursor = "cell";

    container.onmousedown = e => {
        const p = network.DOMtoCanvas(e);
        nodeCounter++;
        nodes.add({ id: nodeCounter, label: "Node " + nodeCounter, x: p.x, y: p.y });
        if (!e.shiftKey) {
            container.onmousedown = null;
            container.style.cursor = "default";
        }
    }
}

function deleteSelected() {
    const selection = network.getSelection();
    selection.nodes.map(n => {
        // По какой-то причине vis.js не удаляет сам соединения
        // поэтому это прописано здесь
        network.getConnectedEdges(n).forEach(e => edges.remove(e));
        nodes.remove(n);
    });
    selection.edges.forEach(e => edges.remove(e));
}

function selectAll() {
    network.selectNodes(nodes.getIds());
}

function connectSelected() {
    pairwise(network.getSelectedNodes(), (cur, next) => {
        if (!(network.getConnectedNodes(cur) as vis.IdType[]).some(i => i == next)) {
            edgeCounter++;
            edges.add({ id: edgeCounter, from: cur, to: next });
        }
    });

    network.unselectAll();
}