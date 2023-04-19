import { Locale, NodeTypes } from "./api";

export function initTypesList(locale: Locale, types: NodeTypes, list: HTMLUListElement) {
    const styles = {
        "seed": "list-group-item-info",
        "random": "list-group-item-success",
        "output": "list-group-item-danger",
    };

    ["seed", "random", "output"].forEach(group => {
        const groupData = types[group];
        if (groupData instanceof Array<string>) {
            groupData.forEach((node: string, _: number) => {
                const name = locale[group][node];
                const listItem = document.createElement("li");

                listItem.classList.add("list-group-item",
                    "p-2", "m-1", "rounded", styles[group])
                listItem.innerHTML = name;

                list.appendChild(listItem);
            });
        }
    });
}