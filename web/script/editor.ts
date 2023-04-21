import { initNetwork, setNodes } from "./vis_network";
import { initProject } from "./project";
import { initEditorButtons } from "./editor_buttons";
import { loadLocale, loadTypes } from "./api";
import { initTypesList } from "./types_list";
import { initParamsEditor } from "./params";

export type Colors = { seed: string, random: string, output: string, body: string, edges: string, font: string };

const lang = document.documentElement.lang;
const localeLoading = loadLocale(lang);
const typesLoading = loadTypes();

async function initEditor() {
    const fileInput = document.getElementById("file-input") as HTMLInputElement;
    initProject(fileInput, p => setNodes(p.nodes));

    const container = document.getElementById("editor-container")! as HTMLCanvasElement;
    const style = getComputedStyle(document.body);

    initEditorButtons();

    const styleProp = (prop: string) => style.getPropertyValue(prop);

    const locale = await localeLoading;
    const types = await typesLoading;

    initParamsEditor(document.getElementById("params-editor")!, types, locale);
    initTypesList(locale, types, {
        seed: document.getElementById("seed-nodes-list")!,
        random: document.getElementById("random-nodes-list")!,
        output: document.getElementById("output-nodes-list")!,
    });
    initNetwork(container, {
        seed: styleProp("--bs-info"),
        random: styleProp("--bs-success"),
        output: styleProp("--bs-danger"),
        edges: styleProp("--bs-secondary"),
        body: styleProp("--bs-body-color"),
        font: styleProp("--bs-body-font-family"),
    }, locale);
}

if (document.readyState == "loading") {
    document.addEventListener("DOMContentLoaded", initEditor);
} else {
    initEditor();
}