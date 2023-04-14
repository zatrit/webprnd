import { connectNodes, container, counter, createNode, edges, network, nodes } from "./vis_network";
import { pairwise } from "./util";

function addNode() {
    container.style.cursor = "cell";

    let listener: (e: MouseEvent) => void;
    container.addEventListener("mousedown", listener = e => {
        const { x, y } = network.DOMtoCanvas({
            x: e.clientX - container.offsetLeft,
            y: e.clientY - container.offsetTop
        });
        const id = ++counter.nodes;
        createNode({ name: "Node " + id, id, type: "random" }, x, y);
        if (!e.shiftKey) {
            container.removeEventListener("mousedown", listener);
            container.style.cursor = "default";
        }
    });
}

function deleteSelected() {
    const selection = network.getSelection();
    selection.nodes.map(node => {
        /* По какой-то причине vis.js не удаляет сам соединения
        поэтому это прописано здесь */
        network.getConnectedEdges(node).forEach(e => edges.remove(e));
        nodes.remove(node);
    });
    selection.edges.forEach(e => edges.remove(e));
}

const selectAll = () => network.selectNodes(nodes.getIds());

function connectSelected() {
    pairwise(network.getSelectedNodes(), (cur, next) => {
        if (!(network.getConnectedNodes(cur)).some(i => i == next)) {
            connectNodes(cur, next);
        }
    });

    network.unselectAll();
}

export function initEditorButtons() {
    /* Так как файл компилируется в формает IIFE, то
    HTML не имеет доступа к функциям, так что их
    можно указать из скрипта */
    const byId = (e: string) => document.getElementById(e);
    byId("btn-add")!.onclick = addNode;
    byId("btn-delete")!.onclick = deleteSelected;
    byId("btn-connect")!.onclick = connectSelected;
    byId("btn-select-all")!.onclick = selectAll;

    document.addEventListener("keydown", e => {
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
    });
}