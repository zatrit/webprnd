import { connectNodes, container, counter, createNode, edges, network, nodes } from "./vis_network";
import { Node } from "./project";
import { pairwise } from "./util";

let addNodeListener: (e: MouseEvent) => void;

type NodeInit = {
    name: string,
    type: string,
};

export function addNode(nodeInit: NodeInit) {
    container.style.cursor = "cell";

    container.addEventListener("mousedown", addNodeListener = e => {
        const { x, y } = network.DOMtoCanvas({ x: e.pageX, y: e.pageY });

        const _node: Node = Object.assign({
            id: ++counter.nodes,
        }, nodeInit) as Node;
        createNode(_node, x, y);

        if (!e.shiftKey) {
            container.removeEventListener("mousedown", addNodeListener);
            container.style.cursor = "default";
        }
    });
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

export function initEditorButtons() {
    document.addEventListener("keydown", e => {
        if (e.code == "KeyN") {
            document.getElementById("btn-toggle-offcanvas")?.click()
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