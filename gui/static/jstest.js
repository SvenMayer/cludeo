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
    initialize_cards(JSON.loads(msg));
});

socket.on("mob_pos", function(msg) {
    set_mob_pos(JSON.loads(msg));
});

socket.on("guess", function(msg) {
    handle_guess(JSON.loads(msg));
});

socket.on("status", function(msg) {
    update_status(JSON.loads(msg));
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