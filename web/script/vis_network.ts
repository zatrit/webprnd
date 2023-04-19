import { Node } from "./project";
import { DataSet } from "vis-data";
import vis from "vis-network";
import { Colors } from "./editor";
import { Locale } from "./api";

type VisProjectNode = vis.Node & { props: Object };

let locale: Locale;

export let network: vis.Network;
export let container: HTMLCanvasElement;

export const nodes = new DataSet<VisProjectNode>([]);
export const edges = new DataSet<vis.Edge>([]);

export let counter = { nodes: 0, edges: 0 };

export function initNetwork(_container: HTMLCanvasElement, style: Colors, _locale: Locale) {
    container = _container;
    locale = _locale;

    const data = { nodes, edges, };
    const margin = 10;
    const options: vis.Options = {
        height: "100%",
        width: "100%",
        physics: false,
        nodes: {
            color: style.seed,
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
            color: style.edges,
        },
        interaction: {
            multiselect: true,
            navigationButtons: false,
            selectConnectedEdges: false,
            keyboard: true
        },
        groups: {
            "seed": { color: style.seed },
            "random": { color: style.random },
            "output": { color: style.output },
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

export function createNode(node: Node, x?: number, y?: number) {
    const localizedName = locale[node.type][node.name] || node.name;

    nodes.add({
        x, y,
        label: localizedName,
        group: node.type,
        id: node.id,
        props: node.props!
    });
}