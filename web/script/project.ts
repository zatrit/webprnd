export class NodeType {
    "random": string;
    "output": string;
    "seed": string;
}

export class Node<T extends keyof NodeType> {
    id: number;
    type: T;
    name: string;
    uses?: number[];
}

export function initProject(fileInput: HTMLInputElement) {

}

export function validateNodes(nodes: Node<keyof NodeType>[]) {
}