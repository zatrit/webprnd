import Ajv from 'ajv';

class Node {
    id: number;
    type: string;
    name: string;
    uses: number[];
}

class Project {
    nodes: Node[]
}

export function initProject(fileInput: HTMLInputElement) {
    const ajv = new Ajv();
    const host = window.location.host;
}