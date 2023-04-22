import { Locale, NodeTypes } from "./api";
import { NodeInit, addNode } from "./editor_buttons";
import { NodeType } from "./project";
import React from "jsx-dom";

type NodeLists = { [id in NodeType]: HTMLElement; };

const selectedClasses = ["border-5", "border-white"];
let selectedButton: HTMLElement | null;

export function initTypesList(locale: Locale, types: NodeTypes, lists: NodeLists) {
    const styles = {
        "seed": "btn-info",
        "random": "btn-success",
        "output": "btn-danger",
    };

    types.forEach(type => {
        const list = lists[type.type];

        const name = locale[type.type][type.name] ?? type.name;
        const classes = ["p-2", "m-2", "rounded", "btn", styles[type.type]];

        const button = <li class={classes}>{name}</li> as HTMLElement;

        button.onclick = () => {
            unselectButton();
            selectedButton = button;
            button.classList.add(...selectedClasses);

            addNode(type as NodeInit);
        };

        list.append(button);
    });
}

export function unselectButton() {
    if (selectedButton) {
        selectedButton.classList.remove(...selectedClasses);
    }
    selectedButton = null;
}