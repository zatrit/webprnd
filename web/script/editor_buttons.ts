import { buildProject, connectNodes, container, counter, createNode, edges, network, nodes, updateParams } from "./vis_network";
import { Node, NodeType } from "./project";
import { pairwise } from "./util";
import { unselectButton } from "./types_list";
import * as api from "./api";
import * as params from "./params";

export type NodeInit = {
    name: string,
    type: string,
};

export function addNode(nodeInit: NodeInit) {
    container.style.cursor = "cell";

    container.onmousedown = e => {
        const { x, y } = network.DOMtoCanvas({ x: e.pageX, y: e.pageY });

        const _node: Node = Object.assign({
            id: counter.nodes++,
        }, nodeInit) as Node;
        createNode(_node, x, y);
        unselectButton();

        if (!e.shiftKey) {
            container.onmousedown = null;
            container.style.cursor = "default";
        }
    };
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
    params.setVisibility(false);
};

const selectAll = globalThis.selectAll = () => {
    network.selectNodes(nodes.getIds());

    updateParams(network.getSelectedNodes());
};

const connectSelected = globalThis.connectSelected = () => {
    pairwise(network.getSelectedNodes(), (cur, next) => {
        if (!(network.getConnectedNodes(cur)).some(i => i == next)) {
            connectNodes(cur, next, id => nodes.get(id)?.group as NodeType);
        }
    });

    network.unselectAll();
};

const generate = globalThis.generate = async () => {
    const project = buildProject();
    await api.generate(project);
};

export function initEditorButtons() {
    document.addEventListener("keydown", e => {
        if (e.code == "KeyN") {
            document.getElementById("btn-toggle-offcanvas")?.click();
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
        else if (e.code == "KeyG" && e.ctrlKey) {
            e.preventDefault();
            generate();
        }
    });
}