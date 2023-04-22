/* Я не придумал, как можно сделать более масштабируемый способ
отделить ID нод от их видимых имён, поэтому сделал так */
import { NodeType, Project } from "./project";
import { saveAs } from "file-saver";

type LocaleDict = { [id: string]: string; };
export type ParamValue = boolean | number | string;

export type ParamType = {
    type: string,
    default: ParamValue,
};

export type ParamTypes = { [id: string]: ParamType; };

export type Locale = {
    seed: LocaleDict,
    random: LocaleDict,
    output: LocaleDict,
    params: LocaleDict,
}

export type NodeTypes = {
    type: NodeType,
    name: string,
    params: ParamTypes,
}[];

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
    const request = await fetch(typesUrl, credFetchProps);
    return request.json();
}

export async function generate(project: Project) {
    const randomUrl = urlFor("/api/v1/random");

    const props: RequestInit = {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(Object.assign({
            format: "7z"
        }, project)),
    };

    const response = await fetch(randomUrl, Object.assign(props, credFetchProps));
    const contentType = response.headers.get("Content-Type");

    switch (contentType) {
        case "application/json":
        case "text/json": {
            const json = await response.json();

            if ("message" in json) {
                alert(json["message"]);
            }

            break;
        }

        case "application/x-7z-compressed": {
            const bodyReadResult = await response.body?.getReader().read();

            if (!bodyReadResult || !bodyReadResult.value) {
                return;
            }

            const body = bodyReadResult.value;

            saveAs(new Blob([body],
                { type: contentType + ";charset=utf-8" }), "result.7z");
        }
    }
}
