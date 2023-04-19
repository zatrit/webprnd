import { Node, NodeType } from "./project";
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
}

export function setNodes(addedNodes: Node[]) {
    [nodes, edges].forEach(d => d.clear());
    counter = { nodes: addedNodes.length, edges: 0 };

    addedNodes.forEach(node => {
        createNode(node);
        node.to?.forEach(to => connectNodes(node.id, to, id =>
            addedNodes.filter(node => node.id == id)[0].type));
    });

    network.stabilize();
}

const connectable: { [id in NodeType]: Array<string> } = {
    "random": ["random", "output"],
    "seed": ["random", "output"],
    "output": []
}

export function connectNodes(from: vis.IdType, to: vis.IdType, getGroup: (id: vis.IdType) => NodeType) {
    const tryConnect = (from: vis.IdType, to: vis.IdType, fromGroup: NodeType, toGroup: NodeType) => {
        if (connectable[fromGroup].includes(toGroup)) {
            return edges.add({ from, to, id: counter.edges++ });
        }
    };

    const fromGroup = getGroup(from);
    const toGroup = getGroup(to);

    if (!tryConnect(from, to, fromGroup, toGroup))
        tryConnect(to, from, toGroup, fromGroup);
}

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