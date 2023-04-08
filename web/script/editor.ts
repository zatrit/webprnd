import { initNetwork, setNodes } from "./network";
import { initProject } from "./project";

function initEditor() {
    const fileInput = document.getElementById('file-input') as HTMLInputElement;
    initProject(fileInput, p => setNodes(p.nodes));

    const container = document.getElementById("editor-container")! as HTMLCanvasElement;
    initNetwork(container);
}

// Потенциально исправляет спонтанный вылет при загрузке страницы
if (document.readyState == "complete") {
    initEditor()
}
else {
    document.addEventListener("DOMContentLoaded", initEditor);
}