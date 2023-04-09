import { Node, NodeType } from "./project";
import { pairwise } from "./util";
import { DataSet } from "vis-data";
import vis from "vis-network";

type ColorsDictionary = { [id in NodeType]: string };
type Style = { info: string, success: string, danger: string, body: string, secondary: string, font: string }

class VisProjectNode implements vis.Node {
    node: Node;
    id: number;
    label: string;
    color: string;
    x?: number;
    y?: number;

    constructor(node: Node, colors: ColorsDictionary, x?: number, y?: number) {
        this.node = node;
        this.label = node.name;
        this.id = node.id;
        this.color = colors[node.type];
        this.x = x;
        this.y = y;
    }
}

let counter = { nodes: 0, edges: 0 };
let network: vis.Network;
let container: HTMLCanvasElement;
let nodeColors: ColorsDictionary;

const nodes = new DataSet<VisProjectNode>([]);
const edges = new DataSet<vis.Edge>([]);


export function initNetwork(_container: HTMLCanvasElement, style: Style) {
    container = _container;

    /* Так как файл компилируется в формает IIFE, то
    HTML не имеет доступа к функциям, так что их
    можно указать из скрипта */
    [
        { id: "btn-add", callback: addNode },
        { id: "btn-delete", callback: deleteSelected },
        { id: "btn-connect", callback: connectSelected },
        { id: "btn-select-all", callback: selectAll },
    ].forEach(pair => {
        const element = document.getElementById(pair.id);
        element?.addEventListener("click", pair.callback);
    });

    nodeColors = {
        "seed": style.info,
        "random": style.success,
        "output": style.danger,
    };

    const data = { nodes, edges, };
    const margin = 10;
    const options: vis.Options = {
        height: "100%",
        width: "100%",
        physics: false,
        nodes: {
            color: style.info,
            shape: "box",
            borderWidth: 0,
            font: {
                color: style.body,
                face: style.font,
            },
            margin: {
                top: margin,
                left: margin,
                right: margin,
                bottom: margin
            },
        },
        edges: {
            arrows: {
                to: true,
            },
            smooth: false,
            color: style.secondary,
        },
        interaction: {
            multiselect: true,
            navigationButtons: false,
            selectConnectedEdges: false,
            keyboard: true
        },
    };

    network = new vis.Network(container, data, options);

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

    window.onbeforeunload = () => nodes.length != 0;
}

export function addNode() {
    container.style.cursor = "cell";

    let listener: (e: MouseEvent) => void;
    container.addEventListener("mousedown", listener = e => {
        const { x, y } = network.DOMtoCanvas(e);
        const id = ++counter.nodes;
        nodes.add(new VisProjectNode({ name: "Node " + id, id, type: "random" }, nodeColors, x, y));
        if (!e.shiftKey) {
            container.removeEventListener("mousedown", listener);
            container.style.cursor = "default";
        }
    });
}

export function deleteSelected() {
    const selection = network.getSelection();
    selection.nodes.map(n => {
        /* По какой-то причине vis.js не удаляет сам соединения
        поэтому это прописано здесь */
        network.getConnectedEdges(n).forEach(e => edges.remove(e));
        nodes.remove(n);
    });
    selection.edges.forEach(e => edges.remove(e));
}

export const selectAll = () => network.selectNodes(nodes.getIds());
const connectNodes = (from: vis.IdType, to: vis.IdType) => edges.add({ from, to, id: counter.edges++ });

export function connectSelected() {
    pairwise(network.getSelectedNodes(), (cur, next) => {
        if (!(network.getConnectedNodes(cur) as vis.IdType[]).some(i => i == next)) {
            connectNodes(cur, next);
        }
    });

    network.unselectAll();
}

export function setNodes(addedNodes: Node[]) {
    [nodes, edges].forEach(d => d.clear());
    counter = { nodes: addedNodes.length, edges: 0 };

    addedNodes.forEach(node => {
        nodes.add(new VisProjectNode(node, nodeColors));
        node.uses?.forEach(from => connectNodes(from, node.id));
    });

    network.stabilize(addedNodes.length);
}