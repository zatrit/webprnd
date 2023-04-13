import { Node } from "./project";
import { DataSet } from "vis-data";
import vis from "vis-network";

type Style = { info: string, success: string, danger: string, body: string, secondary: string, font: string }

export class VisProjectNode implements vis.Node {
    id: number;
    label: string;
    group: string;

    constructor(node: Node, x?: number, y?: number) {
        this.label = node.name;
        this.id = node.id;
        this.group = node.type;
        // Короткое присвоение полей
        Object.assign(this, { x, y })
    }
}

export let network: vis.Network;
export let container: HTMLCanvasElement;

export const nodes = new DataSet<VisProjectNode>([]);
export const edges = new DataSet<vis.Edge>([]);

export let counter = { nodes: 0, edges: 0 };

export function initNetwork(_container: HTMLCanvasElement, style: Style) {
    container = _container;

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
        groups: {
            "seed": { color: style.info },
            "random": { color: style.success },
            "output": { color: style.danger },
        },
    };

    network = new vis.Network(container, data, options);

    window.onbeforeunload = () => nodes.length != 0;
}

export function setNodes(addedNodes: Node[]) {
    [nodes, edges].forEach(d => d.clear());
    counter = { nodes: addedNodes.length, edges: 0 };

    addedNodes.forEach(node => {
        createNode(node);
        node.from?.forEach(from => connectNodes(from, node.id));
    });

    network.stabilize();
}

export const connectNodes = (from: vis.IdType, to: vis.IdType) =>
    edges.add({ from, to, id: counter.edges++ });

export const createNode = (node: Node, x?: number, y?: number) =>
    nodes.add(new VisProjectNode(node, x, y));