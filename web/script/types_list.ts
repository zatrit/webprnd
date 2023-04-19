import { Locale, NodeTypes } from "./api";
import { NodeInit, addNode } from "./editor_buttons";
import { NodeType } from "./project";

type NodeLists = {
    [id in NodeType]: HTMLElement;
};

export function initTypesList(locale: Locale, types: NodeTypes, lists: NodeLists) {
    const styles = {
        "seed": "btn-info",
        "random": "btn-success",
        "output": "btn-danger",
    };

    types.forEach(type => {
        const list = lists[type.type];

        const name = locale[type.type][type.name] || type.name;
        const button = document.createElement("li");

        button.classList.add("p-2", "m-2", "rounded", "btn", styles[type.type]);
        button.innerHTML = name;

        button.onclick = () => addNode(type as NodeInit);

        list.appendChild(button);
    });
}