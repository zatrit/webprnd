import { Node, NodeKey, NodeType, Project } from "./project";
import { DataSet } from "vis-data";
import vis from "vis-network";
import { Colors } from "./editor";
import { Locale } from "./api";
import * as params from "./params";

export type VisProjectNode = vis.Node & NodeKey & params.HasParams;

let locale: Locale;

export let network: vis.Network;
export let container: HTMLCanvasElement;

export const nodes = new DataSet<VisProjectNode>([]);
export const edges = new DataSet<vis.Edge>([]);

export let counter = { nodes: 0, edges: 0 };

export function updateParams(selectNodes: vis.IdType[]) {
    const firstNode = nodes.get(selectNodes[0] as vis.IdType);

    if (!firstNode)
        return;

    const onlyOneNode = selectNodes.length === 1 && params.hasParams(firstNode);

    params.setVisibility(onlyOneNode);

    if (onlyOneNode) {
        params.selectNode(firstNode);
    }
}

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
            selectConnectedEdges: false,
        },
        groups: {
            "seed": { color: style.seed },
            "random": { color: style.random },
            "output": { color: style.output },
        },
    };

    network = new vis.Network(container, data, options);

    const nodesEventHandler = (e: { nodes: vis.IdType[] }) => updateParams(e.nodes);

    network.on("selectNode", nodesEventHandler);
    network.on("deselectNode", nodesEventHandler);

    window.onbeforeunload = () => {
        // По какой-то причине просто return nodes.length > 0 не работает
        if (nodes.length > 0) {
            return true;
        }
    };
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
};

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
    const localizedName = locale[node.type][node.name] ?? node.name;

    nodes.add({
        x, y,
        label: localizedName,
        group: node.type,
        id: node.id,
        name: node.name,
        type: node.type,
        params: {}
    });
}

export function buildProject(): Project {
    const projectNodes = nodes.map(node => <Node>{
        type: node.type,
        name: node.name,
        id: node.id,
        to: [],
        params: node.params,
    });

    projectNodes.forEach(node => {
        network.getConnectedEdges(node.id)
            .map(id => edges.get(id))
            .filter(e => e != undefined)
            .forEach(edge => {
                if (edge?.from == node.id) {
                    node.to?.push(edge?.to as number);
                }
            });
    });

    return { nodes: projectNodes };
}