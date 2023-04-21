import { Locale, NodeTypes, ParamType, ParamTypes, ParamValue } from "./api";
import { BooleanInput } from "./input_field";
import { NodeType } from "./project";
import { VisProjectNode } from "./vis_network";

export type Params = { [id: string]: ParamValue; };
export type RangeParam = ParamType & { min: number, max: number };
export type HasParams = { params: Params };

type NodeTypeParams = { [id in NodeType]: { [id: string]: ParamTypes } };

let parent: HTMLElement;
let paramsElements: HTMLElement[] = [];
let locale: Locale;

const paramTypes: NodeTypeParams = { seed: {}, random: {}, output: {} };

export function initParamsEditor(_parent: HTMLElement, types: NodeTypes, _locale: Locale) {
    types.forEach(type => paramTypes[type.type][type.name] = type.params);
    parent = _parent;
    locale = _locale;
}

export function hasParams(node: VisProjectNode): boolean {
    return Object.keys(paramTypes[node.type][node.name]).length > 0;
}

export function selectNode(node: VisProjectNode) {
    setVisibility(true);
    paramsElements.forEach(el => el.remove());
    paramsElements = [];

    const params = paramTypes[node.type][node.name];

    Object.entries(params).forEach(
        ([key, param]) => {
            const value = node.params[key] || param.default;
            const title = locale.params[key] || key;
            const id = key + "-param";

            const field = new BooleanInput(id, title);
            field.setValue(value as boolean);
            field.addCallback(console.log);

            paramsElements.push(field.element);
            parent.append(field.element);
        }
    );
}

export const setVisibility = (visible: boolean) =>
    parent.style.visibility = visible ? "visible" : "hidden";