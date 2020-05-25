// Socket.IO events
var socket = io();

socket.on("connect", function() {
    $("h1#connecting_msg").remove();
    $("div#playerinput").show();
    $("div#lobby").show();
    socket.emit("joined");
});

socket.on("refresh_game_lobby", function(msg) {
    console.log(msg);
    update_lobby(JSON.parse(msg));
});

socket.on("game_status", function(msg) {
    if (msg == "lobby") {
        $("div#lobby").show();
        $("input[name =nameinput]").val("");
    } else if (msg == "waiting_to_start_game") {
        $("div#playerinput").remove();
        $("button#startgame").show();
        console.log("waiting to start game");
    } else if (msg == "game_started") {
        $("div#lobby").remove();
        init_game();
        console.log("game started");
    } else if (msg == "game_over") {
        console.log("game over");
    } else {
        console.log("Received '" + msg + "'. Do not know what to do.");
    }
});

socket.on("cards", function(msg) {
    initialize_cards(JSON.parse(msg));
});

socket.on("update_status", function(msg) {
    update_status(JSON.parse(msg));
});


// Update lobby screen.
function update_lobby(lobby_info) {
    // update table
    $("table#joined_players").empty();
    $("<tr><th>Player name</th><th>Character name</th></tr>").appendTo($("table#joined_players"));
    for (var i = 0; i < lobby_info.joind_players.length; i++) {
        var playername = lobby_info.joind_players[i][0];
        var charactername = lobby_info.joind_players[i][1];
        $('<tr><td>' + playername + '</td><td>' + charactername + '</td></tr>').appendTo($("table#joined_players"));
    }

    // update combobox
    $("select[name =characterinput]").empty();
    for (var i = 0; i < lobby_info.available_characters.length; i++) {
        var charactername = lobby_info.available_characters[i];
        $('<option value="' + charactername + '">' + charactername + '</option>').appendTo($("select[name =characterinput]"));
    }
}


// Lobby join game
$("button#join").click(function() {
    var player_info = {
        playername: $("input[name =nameinput").val(),
        charactername: $("select[name =characterinput").val(),
    };
    socket.emit("join_game", JSON.stringify(player_info));
});

// Start game button
$("button#startgame").click(function() {
    socket.emit("start_game");
});

// Initalize cards.
function initialize_cards(cards) {
    var div = $("<div>", {id: "my_cards"});
    div.append($("<h2>", {html: "My cards"}));
    for (var i = 0; i < cards.length; i++) {
        var cardname = cards[i][0];
        var cardpath = cards[i][1];
        var card_div = $("<div>", {id: cardname, style: "float: left;"});
        var image = $("<img>", {src: cardpath, alt: cardname, onclick: 'card_selected("' + cardname + '")'});
        card_div.append(image);
        div.append(card_div);
    }
    $("body").append(div);
    console.log(div.html());
}

function card_selected(cardname) {
    console.log(cardname);
}