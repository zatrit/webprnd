import { initNetwork } from "./network";
import { initProject } from "./project";

document.addEventListener("DOMContentLoaded", () => {
    const fileInput = document.getElementById('file-input') as HTMLInputElement;
    initProject(fileInput);

    const container = document.getElementById("editor-container")! as HTMLCanvasElement;
    initNetwork(container);
});