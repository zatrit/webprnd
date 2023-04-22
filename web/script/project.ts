export type NodeType = "random" | "output" | "seed";

export type NodeKey = {
    type: NodeType,
    name: string,
}

export type Node = NodeKey & {
    id: number,
    to?: number[],
}

type Project = {
    nodes: Node[],
}

type SetProject = (p: Project) => void;

export function initProject(fileInput: HTMLInputElement, setProject: SetProject) {
    fileInput.onchange = () => {
        const file = fileInput.files?.item(0);

        const reader = new FileReader();
        const decoder = new TextDecoder();

        reader.onload = e => {
            try {
                let text = e.target?.result;

                if (!text) {
                    throw "Не удалось прочитать файл";
                }

                // Конвертируем text в string, по необходимости
                if (text instanceof ArrayBuffer) {
                    text = decoder.decode(text);
                }

                const project: Project = JSON.parse(text);

                if (!project.nodes) {
                    throw "Неверный формат проекта";
                }

                setProject(project);
            } catch (err) {
                alert(err);
            }
        };

        if (!file) {
            return;
        }

        reader.readAsText(file);
    };
}