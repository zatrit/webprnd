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
    props?: Map<string, any>;
}

export class Project {
    nodes: Node<any>[];
}

export function initProject(fileInput: HTMLInputElement) {
    fileInput.onchange = () => {
        const file = fileInput.files?.item(0)!;

        const reader = new FileReader();
        const decoder = new TextDecoder();

        reader.onload = e => {
            try {
                let text = e.target?.result!;

                // Конвертируем text в string, по необходимости
                if (text instanceof ArrayBuffer)
                    text = decoder.decode(text);

                const project: Project = JSON.parse(text);

                validateNodes(project.nodes);
            } catch (err) {
                alert(err);
            }
        };

        reader.readAsText(file);
    };
}

export function validateNodes(nodes: Node<keyof NodeType>[]) {
    nodes.forEach(console.log);
}
