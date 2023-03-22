function createBlock() {
    var block = document.createElement("div");
    block.classList.add("block")

    var blockHeader = document.createElement("div");
    blockHeader.classList.add("blockheader");
    blockHeader.innerHTML = "Very long string aaaa";
    block.appendChild(blockHeader);

    var button = document.createElement("p");
    button.innerHTML = "Hello, World!";
    block.appendChild(button)

    document.body.appendChild(block);

    dragElement(block, blockHeader);
}

// https://www.w3schools.com/howto/howto_js_draggable.asp
function dragElement(element: HTMLDivElement, header: HTMLDivElement | null = null) {
    var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
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