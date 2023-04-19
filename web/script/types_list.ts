import { Locale, NodeTypes } from "./api";
import { addNode } from "./editor_buttons";
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

    ["seed", "random", "output"].forEach(type => {
        const groupData = types[type];
        const list = lists[type];
        if (groupData instanceof Array<string>) {
            groupData.forEach((node: string, _: number) => {
                const name = locale[type][node] || node;
                const button = document.createElement("li");

                button.classList.add("p-2", "m-2", "rounded", "btn", styles[type]);
                button.innerHTML = name;

                const nodeInit = {
                    type,
                    name: node
                };
                button.onclick = () => addNode(nodeInit);

                list.appendChild(button);
            });
        }
    });
}