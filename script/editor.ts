import PIXI from "pixi.js";

const app = new PIXI.Application<HTMLCanvasElement>({ background: '#1099bb' });
app.view.classList.add("background");
document.body.appendChild(app.view);

function createBlock() {
    const container = document.getElementById("container-main");
    const block = document.createElement("div");
    block.classList.add("block")

    const blockHeader = document.createElement("div");
    blockHeader.classList.add("blockheader");
    blockHeader.innerHTML = "Very long string aaaa";
    block.appendChild(blockHeader);

    const blockLabel = document.createElement("p");
    blockLabel.classList.add("blocklabel");
    blockLabel.contentEditable = "true";
    blockLabel.spellcheck = false;
    blockLabel.innerHTML = "Редактируемая область";
    block.appendChild(blockLabel)

    container?.appendChild(block);

    dragElement(block, blockHeader);
}

// https://www.w3schools.com/howto/howto_js_draggable.asp
function dragElement(element: HTMLDivElement, header: HTMLDivElement | null = null) {
    let pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
    // Если передан header, настроить обработчик для него
    // Иначе для element
    (header || element).onmousedown = dragMouseDown;

    function dragMouseDown(e: MouseEvent) {
        e = e || window.event as MouseEvent;
        e.preventDefault();
        // Получаем начальные координаты мыши
        pos3 = e.clientX;
        pos4 = e.clientY;
        document.onmouseup = (_e: MouseEvent) => {
            // Прекращаем двигать, когда мышь больше не нажата
            document.onmouseup = null;
            document.onmousemove = null;
        }
        // Функция, вызываемая при движении мыши
        document.onmousemove = (e: MouseEvent) => {
            e = e || window.event as MouseEvent;
            e.preventDefault();
            // Вычисляем новую позицию
            pos1 = pos3 - e.clientX;
            pos2 = pos4 - e.clientY;
            pos3 = e.clientX;
            pos4 = e.clientY;
            // Задаём позицию элемента
            element.style.top = (element.offsetTop - pos2) + "px";
            element.style.left = (element.offsetLeft - pos1) + "px";
        }
    }
}