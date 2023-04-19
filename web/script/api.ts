/* Я не придумал, как можно сделать более масштабируемый способ
отделить ID нод от их видимых имён, поэтому сделал так */
import { Node } from "./project";

type LocaleDict = { [id: string]: string; };
export class Locale {
    seed: LocaleDict;
    random: LocaleDict;
    output: LocaleDict;
}

type TypeArray = string[];
export class NodeTypes {
    seed: TypeArray;
    random: TypeArray;
    output: TypeArray;
}

const credFetchProps: RequestInit = {
    credentials: "include",
    cache: "default",
};

function urlFor(...sub_url: string[]) {
    return window.origin + sub_url.join("");
}

export async function loadLocale(lang: string): Promise<Locale> {
    const localeUrl = urlFor("/static/json/editor/", lang, ".json");
    const request = await fetch(localeUrl);
    return request.json();
}

export async function loadTypes(): Promise<NodeTypes> {
    const typesUrl = urlFor("/api/v1/types");
    let request = await fetch(typesUrl, credFetchProps);
    return request.json();
}

export async function generate(nodes: Node[]) {
    const randomUrl = urlFor("/api/v1/random");

    const props: RequestInit = {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            nodes
        })
    };

    const request = await fetch(randomUrl, Object.assign(props, credFetchProps));
}