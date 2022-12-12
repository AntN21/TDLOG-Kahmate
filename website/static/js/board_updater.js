var socket = io.connect()

var players = ["clever_red", "strong_red", "tough_red", "fast_red", "ordinary_red", "ko_red",
                "clever_blue", "strong_blue", "tough_blue", "fast_blue", "ordinary_blue","ko_blue"];

function get_src(player) {
    console.log("../static/images/" + player + ".png");

    return "../static/images/" + player + ".png";
}

function add_image(chip_data, player, element) {
    if(chip_data.includes(player)) {
        var image = document.createElement("img");
        image.src = get_src(player);
        image.draggable = false;
        image.style.width = "40px";
        image.style.width = "40px";
        element.appendChild(image);
    }
}

function updateChips(chips) {
    for (let row = 0; row < chips.length; row++) {
        for (let col = 0; col < chips[0].length; col++) {
            var selected_chip = document.getElementById('('+String(row)+', '+String(col) + ')')
            var child = selected_chip.lastElementChild; 
            while (child) {
                selected_chip.removeChild(child);
                child = selected_chip.lastElementChild;
            }
            if(chips[row][col].includes('b')){
                var image = document.createElement("img");
                image.src = get_src("ball");
                image.draggable = false;
                image.style.top = "20px";
                image.style.left = "20px";
                image.style.position = "absolute";
                image.style.width = "40px";
                image.style.width = "40px";
                selected_chip.appendChild(image);
            }
            players.forEach(player => {
                add_image(chips[row][col], player, selected_chip);
            })
        }
    }
}

socket.on("updateChips", function (data) {
    console.log("UPDATES CHIPS");
    updateChips(data.chips);
});    