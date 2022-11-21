
function mark_box(x, y) {
    if(x >= 0 && x < 11 && y >= 0 && y < 8) {
        var element = document.getElementById(String(x)+String(y))
        element.style.borderColor="white"
    }
}

function click_box(e) {
    var cursorX = Math.floor((e.pageX - document.getElementById("board").offsetLeft - 5)/52)
    var cursorY = Math.floor((e.pageY - document.getElementById("board").offsetTop - 5)/52)
    var element = document.getElementById(String(cursorX)+String(cursorY))
    if(element.style.borderColor=="white") {
        console.log("CREATES")
        console.log(selected_chip)
        console.log(selected_chip.firstChild)
        selected_chip.removeChild(selected_chip.firstChild)
        var image = document.createElement("img");
        image.src = "../static/circle-256.png"
        image.draggable = false
        element.appendChild(image)
        clear()
    } else {
        if(element.firstChild != null) {
            clear()
            selected_chip = element
            console.log("SELECTS")
            for(dx = -2; dx < 3; dx++) 
                for(dy = 0; dy < 3 - Math.abs(dx); dy++) {
                    mark_box(cursorX+dx,cursorY+dy)
                    mark_box(cursorX+dx,cursorY-dy)
                }
        } else {
            clear()
        }
    }
}

function clear() {
    selected_chip = null
    var boxes = document.getElementById('board').children
    for (i = 0; i <= boxes.length - 1; i++) {
        var box = document.getElementById(boxes[i].id)
        box.style.borderColor="black";
    }
}