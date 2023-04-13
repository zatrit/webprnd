import { initNetwork, setNodes } from "./vis_network";
import { initProject } from "./project";
import { initEditorButtons } from "./editor_buttons";

function initEditor() {
    const fileInput = document.getElementById("file-input") as HTMLInputElement;
    initProject(fileInput, p => setNodes(p.nodes));

    const container = document.getElementById("editor-container")! as HTMLCanvasElement;
    const style = getComputedStyle(document.body);
    const styleProp = (prop: string) => style.getPropertyValue(prop);
    initNetwork(container, {
        info: styleProp("--bs-info"),
        success: styleProp("--bs-success"),
        danger: styleProp("--bs-danger"),
        secondary: styleProp("--bs-secondary"),
        body: styleProp("--bs-body-color"),
        font: styleProp("--bs-body-font-family"),
    });
    initEditorButtons();
}

// Потенциально исправляет спонтанный вылет при загрузке страницы
if (document.readyState == "complete") {
    initEditor();
}
else {
    document.addEventListener("DOMContentLoaded", initEditor);
}