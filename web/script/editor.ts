import { initNetwork, setNodes } from "./vis_network";
import { initProject } from "./project";
import { initEditorButtons } from "./editor_buttons";
import { loadLocale, loadTypes } from "./api";
import { Offcanvas } from "bootstrap";
import { initTypesList } from "./types_list";

export type Colors = { seed: string, random: string, output: string, body: string, edges: string, font: string };

const lang = document.documentElement.lang;
const localeLoading = loadLocale(lang);
const typesLoading = loadTypes();

async function initEditor() {
    const fileInput = document.getElementById("file-input") as HTMLInputElement;
    initProject(fileInput, p => setNodes(p.nodes));

    const container = document.getElementById("editor-container")! as HTMLCanvasElement;
    const style = getComputedStyle(document.body);

    const offcanvasElement = document.getElementById("nodes-offcanvas")!;
    const offcanvas = new Offcanvas(offcanvasElement);
    initEditorButtons(offcanvas);

    const nodesList = document.getElementById("nodes-list")! as HTMLUListElement;
    const styleProp = (prop: string) => style.getPropertyValue(prop);

    const locale = await localeLoading;
    const types = await typesLoading;

    console.log(locale, types);

    initTypesList(locale, types, nodesList);
    initNetwork(container, {
        seed: styleProp("--bs-info"),
        random: styleProp("--bs-success"),
        output: styleProp("--bs-danger"),
        edges: styleProp("--bs-secondary"),
        body: styleProp("--bs-body-color"),
        font: styleProp("--bs-body-font-family"),
    }, locale);
};

if (document.readyState == "loading") {
    document.addEventListener("DOMContentLoaded", initEditor);
} else {
    initEditor();
}