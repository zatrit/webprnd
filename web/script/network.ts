import { DataSet } from "vis-data";
import vis from "vis-network";
import { Node, NodeType } from "./project";

class VisProjectNode<T extends keyof NodeType> {
    node: Node<T>;
    id: number;
    label: string;
    x?: number;
    y?: number;

    constructor(node: Node<T>, x?: number, y?: number) {
        this.node = node;
        this.label = node.name;
        this.id = node.id;

        if (x) { this.x = x; }
        if (y) { this.y = y; }
    }
}

let nodeCounter: number = 0;
let edgeCounter: number = 0;
let network: vis.Network;
let container: HTMLCanvasElement;

const nodes = new DataSet<VisProjectNode<any>>([new VisProjectNode({ id: 0, name: "Вывод", type: "output" })]);
const edges = new DataSet<vis.Edge>([]);

export function initNetwork(_container: HTMLCanvasElement) {
    container = _container;

    /* Так как файл компилируется в формает IIFE, то
    HTML не имеет доступа к функциям, так что их
    можно указать из скрипта */
    [
        { id: "btn-add", callback: addNode },
        { id: "btn-delete", callback: deleteSelected },
        { id: "btn-connect", callback: connectSelected },
        { id: "btn-select_all", callback: selectAll },
    ].forEach(pair => {
        const element = document.getElementById(pair.id);
        element?.addEventListener("click", pair.callback);
    });

    const style = getComputedStyle(document.body);

    const data = { nodes, edges, };
    const options: vis.Options = {
        height: "100%",
        width: "100%",
        physics: false,
        nodes: {
            color: style.getPropertyValue("--bs-info"),
            shape: "box",
            borderWidth: 0,
            font: {
                color: style.getPropertyValue("--bs-body-color"),
                face: style.getPropertyValue("--bs-body-font-family"),
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

/** https://stackoverflow.com/a/31973533/12245612 */
function pairwise<T>(arr: T[], func: (cur: T, next: T) => void) {
    for (let i = 0; i < arr.length - 1; i++) {
        func(arr[i], arr[i + 1]);
    }
}

export function addNode() {
    container.style.cursor = "cell";

    let listener: (e: MouseEvent) => void;
    container.addEventListener("mousedown", listener = e => {
        const { x, y } = network.DOMtoCanvas(e);
        nodeCounter++;
        nodes.add(new VisProjectNode({ name: "Node " + nodeCounter, id: nodeCounter, type: "random" }, x, y));
        if (!e.shiftKey) {
            container.removeEventListener("mousedown", listener);
            container.style.cursor = "default";
        }
    });
}

export function deleteSelected() {
    const selection = network.getSelection();
    selection.nodes.map(n => {
        // По какой-то причине vis.js не удаляет сам соединения
        // поэтому это прописано здесь
        // Нода с ID 0 не должна быть удалена, так как является выводом
        if (n == 0) {
            return;
        }
        network.getConnectedEdges(n).forEach(e => edges.remove(e));
        nodes.remove(n);
    });
    selection.edges.forEach(e => edges.remove(e));
}

export function selectAll() {
    network.selectNodes(nodes.getIds());
}

export function connectSelected() {
    pairwise(network.getSelectedNodes(), (cur, next) => {
        if (!(network.getConnectedNodes(cur) as vis.IdType[]).some(i => i == next)) {
            edgeCounter++;
            edges.add({ id: edgeCounter, from: cur, to: next });
        }
    });

    network.unselectAll();
}