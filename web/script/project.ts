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
    fileInput.addEventListener("change", () => {
        const file = fileInput.files?.item(0)!;

        const reader = new FileReader();

        reader.onload = e => {
            try {
                let text = e.target?.result!;
                
                // Конвертируем text в string, по необходимости
                if (text instanceof ArrayBuffer) {
                    const decoder = new TextDecoder();
                    text = decoder.decode(text)
                }

                const data = JSON.parse(text);

                console.log(data);
            } catch (err) {
                alert(err);
            }
        };

        reader.readAsText(file)
    });

}

export function validateNodes(nodes: Node<keyof NodeType>[]) {
}