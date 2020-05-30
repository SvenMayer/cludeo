$("h1").html("Connecting to server.")

let allow_answer = false;

let status_messages = [
    "#playername#'s turn to move.",
    "Your turn to move.",
    "#playername# is making a guess.",
    "Your turn to guess.",
    "#playername#'s guess: <b>#killer#</b> with the <b>#weapon#</b> in the <b>#room#</b>.",
    " #answerplayername#'s turn to answer.",
    " Your turn to answer."
]
// Socket.IO events
var socket = io();

socket.on("connect", function() {
    /*$("h1#connecting_msg").remove();
    $("div#playerinput").removeClass("hidden");
    $("div#playerinput").addClass("visible");
    $("div#lobby").removeClass("hidden");
    $("div#lobby").addClass("visible");*/
    socket.emit("joined");
});

socket.on("update_game_lobby", function(msg) {
    console.log(msg);
    update_lobby(JSON.parse(msg));
});

socket.on("game_status", function(msg) {
    if (msg == "lobby") {
        $("body").empty();
        $("body").load("lobby/", function(responseTxt, statusTxt, xhr) {
            $("input[name =nameinput]").val("");
            socket.emit("refresh_game_lobby");
        });
    } else if (msg == "waiting_to_start_game") {
        $("body").empty();
        $("body").load("lobby/", function(responseTxt, statusTxt, xhr) {
            $("input[name =nameinput]").val("");
            $("div#playerinput").remove();
            $("button#startgame").show();
            socket.emit("refresh_game_lobby");
        });
        console.log("waiting to start game");
    } else if (msg == "game_started") {
        load_gamepage();
    } else if (msg == "game_over") {
        console.log("game over");
    } else {
        console.log("Received '" + msg + "'. Do not know what to do.");
    }
});

socket.on("update_status", function(msg) {
    var data = JSON.parse(msg);
    place_mobs(data.mobpos);
    act_player = data.active_player;
    
    imup = is_me(act_player);

    if (imup && data.active_move == "move") {
        enable_move();
    } else {
        disable_move();
    }
    
    if (imup && data.active_move == "guess") {
        enable_guess();
    } else {
        disable_guess();
    }

    if (data.active_move == "answer") {
        update_answer_table(data.guess);
        $("div.guessorder table").show();
        if (is_me(data.guess.guess_order[0])) {
            enable_answer();
        } else {
            disable_answer();
        }
    } else {
        $("div.guessorder table").hide();
        disable_answer();
    }

    update_status_message(data);
});

socket.on("cards", function(msg) {
    initialize_cards(JSON.parse(msg));
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
function player_join_game() {
    var player_info = {
        playername: $("input[name =nameinput").val(),
        charactername: $("select[name =characterinput").val(),
    };
    socket.emit("join_game", JSON.stringify(player_info));
}

// Start game button
function start_game() {
    socket.emit("start_game");
}

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
    if (allow_answer) {
        send_answer(cardname);
    }
}


function send_card(cardname) {
    socket.emit("answer", cardname);
}


function load_lobbypage () {
    $("body").empty();
    $("body").load("lobby/", function() {
        socket.emit("refresh_game_lobby");
    });
}


function load_gamepage () {
    $("body").empty();
    $("body").load("gamepanel/", function(responseTxt, statusTxt, xhr){
        if(statusTxt == "success") {
            load_pass_card();
            initialize_gameboard();
            socket.emit("refresh_gamestatus");
        }
      });
}

function load_pass_card () {
    $("<img>", {id: "passcard", src: "{{ passcard_path }}",
              alt: "pass", onclick: 'card_selected("pass")'}
        ).appendTo($("div.mycards"));
    $("img#passcard").hide();
}

function is_me(playername) {
    if ($("p#playername").html() == playername) {
        return true;
    }
    return false;
}

function enable_guess(guess) {
    $("div.myguess").hide();
    $("div.myguess").empty();
    $("div.myguess").load("guess/", function(responseTxt, statusTxt, xhr) {
        $("div.myguess").show();
    });
}

function disable_guess() {
    $("div.myguess").hide();
}

function send_movement(direction) {
    socket.emit("move", direction);
}


function send_guess() {
    var guess = [$("div.myguess select#killerinput").val(),
                 $("div.myguess select#weaponinput").val(),
                 $("div.myguess select#roominput").val()];
    socket.emit("guess", JSON.stringify(guess));
}

function update_status_message(data) {
    var seloffset = 0;
    if (is_me(data.active_player)) {
        seloffset = 1;
    }
    if (data.active_move == "move") {
        msg = status_messages[0 + seloffset];
    } else if (data.active_move == "guess") {
        msg = status_messages[2 + seloffset];
    } else if (data.active_move == "answer") {
        msg = status_messages[4].replace("#killer#", data.guess.killer)
                                .replace("#weapon#", data.guess.weapon)
                                .replace("#room#", data.guess.room);
        if (data.guess.guess_order.length > 0) {
            if (is_me(data.guess.guess_order[0])) {
                msg = msg + status_messages[6];
            } else {
                msg = msg + status_messages[5].replace("#answerplayername#", data.guess.guess_order[0]);
            }   
        }
    } else {
        msg = "";
    }
    msg = msg.replace("#playername#", data.active_player);
    $("div.statuspanel div.status").empty();
    $("div.statuspanel div.status").append("<h2>Status</h2>" + msg);
}

function enable_answer() {
    allow_answer = true;
    $("img#passcard").show();
}

function disable_answer() {
    allow_answer = true;
    $("img#passcard").hide();
}

function update_answer_table(guess) {
    $("div.guessorder table tr").not(":first").remove();
    var table = $("div.guessorder table");
    for (var i = 0; i < guess.passed_players.length; i++) {
        var tr = $("<tr>");
        tr.append($("<td>").append(guess.passed_players[i]));
        tr.append($("<td>", {class: "pass"}).append("pass"));
        table.append(tr);
    }
    if (guess.guess_order.length >= 1) {
        var tr = $("<tr>");
        tr.append($("<td>").append(guess.guess_order[0]));
        tr.append($("<td>", {class: "show"}).append("show"));
        table.append(tr);
    }
    for (var i = 1; i < guess.guess_order.length; i++) {
        var tr = $("<tr>");
        tr.append($("<td>").append(guess.guess_order[i]));
        tr.append($("<td>", {class: ""}));
        table.append(tr);
    }
}

function test_answer_table() {
    var guess = {passed_players: ["Test1", "Test2"], guess_order: ["Test3", "Test4", "Test5"]};
    update_answer_table(guess);
}

function send_answer(cardname) {
    socket.emit("answer", cardname);
}