import { connectNodes, container, counter, createNode, edges, network, nodes } from "./vis_network";
import { Node } from "./project";
import { pairwise } from "./util";
import { Offcanvas } from "bootstrap";

let offcanvas: Offcanvas;
let addNodeListener: (e: MouseEvent) => void;

function addNode(node: Node) {
    container.style.cursor = "cell";

    container.addEventListener("mousedown", addNodeListener = e => {
        const { x, y } = network.DOMtoCanvas({ x: e.pageX, y: e.pageY });
        createNode(node, x, y);
        if (!e.shiftKey) {
            container.removeEventListener("mousedown", addNodeListener);
            container.style.cursor = "default";
        }
    });
}

const toggleNodesTab = globalThis.toggleNodesTab = () => {
    offcanvas.toggle();
}

const deleteSelected = globalThis.deleteSelected = () => {
    const selection = network.getSelection();
    selection.nodes.map(node => {
        /* По какой-то причине vis.js не удаляет сам соединения
        поэтому это прописано здесь */
        network.getConnectedEdges(node).forEach(e => edges.remove(e));
        nodes.remove(node);
    });

    selection.edges.forEach(e => edges.remove(e));
    network.unselectAll();
}

const selectAll = globalThis.selectAll = () =>
    network.selectNodes(nodes.getIds());

const connectSelected = globalThis.connectSelected = () => {
    pairwise(network.getSelectedNodes(), (cur, next) => {
        if (!(network.getConnectedNodes(cur)).some(i => i == next)) {
            connectNodes(cur, next);
        }
    });

    network.unselectAll();
}

const generate = globalThis.generate = () => {
}

export function initEditorButtons(_offcanvas: Offcanvas) {
    offcanvas = _offcanvas;

    document.addEventListener("keydown", e => {
        if (e.code == "KeyN") {
            toggleNodesTab();
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
        else if (e.code == "Enter") {
            generate();
        }
    });
}