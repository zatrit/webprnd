import React from "jsx-dom";
import { ParamValue } from "./api";

/*Тут прописаны разные виды полей для ввода данных для параметров.
Реализация в функциональной парадигме выглядит запутанной, поэтому
я реализовал в объектной*/

export interface InputField<T extends ParamValue> {
    setValue(value: T): void;
    addCallback(callback: (value: T) => void): void;
    getElement(): HTMLElement;
}

abstract class BaseInput<T extends ParamValue> implements InputField<T> {
    input: HTMLInputElement;
    element: HTMLElement;

    abstract setValue(value: T): void;
    abstract addCallback(callback: (value: T) => void): void;
    abstract createInput(id: string): HTMLInputElement;
    abstract createLabel(inputId: string, title: string): HTMLLabelElement;

    getElement(): HTMLElement {
        return this.element;
    }

    constructor(id: string, title: string) {
        this.element = <fieldset>
            {this.createLabel(id, title)}
            {this.input = this.createInput(id)}
        </fieldset> as HTMLElement;
    }
}

abstract class LineInput<T extends (number | string)> extends BaseInput<T> {
    inputType: string;

    abstract getInputType(): string;

    setValue(value: T): void {
        this.input.value = value.toString();
    }

    createInput(id: string): HTMLInputElement {
        return <input type={this.getInputType()} class="form-control mb-2" id={id}></input> as HTMLInputElement;
    }

    createLabel(id: string, title: string): HTMLLabelElement {
        return <label htmlFor={id} class="form-label">{title}</label> as HTMLLabelElement;
    }
}

type NumberType = "float" | "int";

export class RangeInput extends LineInput<number> {
    numberType: NumberType;
    min: number;
    max: number;

    addCallback(callback: (value: number) => void): void {
        this.input.addEventListener("click", e => {
            try {
                const strValue = (e.target as HTMLInputElement).value;
                let parsed: number;

                switch (this.numberType) {
                    case "float":
                        parsed = Number.parseFloat(strValue);
                        break;
                    case "int":
                        parsed = Number.parseInt(strValue);
                        break;
                }

                parsed = Math.max(Math.min(parsed, this.max), this.min);
                this.input.value = parsed.toString();

                callback(parsed);
            } catch (e) {
                console.log(e);
            }
        });
    }

    getInputType(): string {
        return "number";
    }

    constructor(id: string, title: string, numberType: NumberType, min?: number, max?: number) {
        super(id, title);
        this.numberType = numberType;
        this.input.min = (this.min = (min || Number.MIN_SAFE_INTEGER)).toString();
        this.input.max = (this.max = (max || Number.MAX_SAFE_INTEGER)).toString();
    }
}

export class StringInput extends LineInput<string> {
    addCallback(callback: (value: string) => void): void {
        this.input.addEventListener("click", e => callback((e.target as HTMLInputElement).value));
    }

    getInputType(): string {
        return "text";
    }
}

export class BooleanInput extends BaseInput<boolean> {
    setValue(value: boolean): void {
        this.input.checked = value;
    }

    addCallback(callback: (value: boolean) => void): void {
        this.input.addEventListener("click", e =>
            callback((e.target as HTMLInputElement).checked));
    }

    createInput(id: string): HTMLInputElement {
        return <input class="form-check-input"
            type="checkbox" role="switch" id={id}></input> as HTMLInputElement;
    }

    createLabel(id: string, title: string): HTMLLabelElement {
        return <label class="form-check-label" htmlFor={id}>{title}</label> as HTMLLabelElement;
    }

    constructor(id: string, title: string) {
        super(id, title);
        this.element.classList.add("form-check", "form-switch");
    }
}