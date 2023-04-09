import { initNetwork, setNodes } from "./vis_network";
import { initProject } from "./project";

function initEditor() {
    const fileInput = document.getElementById('file-input') as HTMLInputElement;
    initProject(fileInput, p => setNodes(p.nodes));

    const container = document.getElementById("editor-container")! as HTMLCanvasElement;
    const style = getComputedStyle(document.body);
    initNetwork(container, {
        info: style.getPropertyValue("--bs-info"),
        success: style.getPropertyValue("--bs-success"),
        danger: style.getPropertyValue("--bs-danger"),
        secondary: style.getPropertyValue("--bs-secondary"),
        body: style.getPropertyValue("--bs-body-color"),
        font: style.getPropertyValue("--bs-body-font-family")
    });
}

// Потенциально исправляет спонтанный вылет при загрузке страницы
if (document.readyState == "complete") {
    initEditor()
}
else {
    document.addEventListener("DOMContentLoaded", initEditor);
}