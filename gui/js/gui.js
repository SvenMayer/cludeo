//Aliases
let Application = PIXI.Application,
    Container = PIXI.Container,
    loader = PIXI.loader,
    resources = PIXI.loader.resources,
    TextureCache = PIXI.utils.TextureCache,
    Sprite = PIXI.Sprite,
    Rectangle = PIXI.Rectangle;

let app = new PIXI.Application({ 
    width: 792,         // default: 800
    height: 630,        // default: 600
    antialias: true,    // default: false
    transparent: false, // default: false
    resolution: 1,       // default: 1
    backgroundColor: 0x939a92,
  }
);
app.stage.scale.set(0.7, 0.7);

//document.body.appendChild(app.view);
$("body").append(app.view);

let move_buttons = new PIXI.Container();
move_buttons.x = 100;
move_buttons.y = 820;
app.stage.addChild(move_buttons);
move_buttons.pivot.x = 75
move_buttons.pivot.y = 75
move_buttons.anchor = 0.5;

// load background
loader
  .add("media/gameboard.jpg")
  .add("media/mv_btn.png")
  .add("media/prof_plum.png")
  .add("media/mrs_white.png")
  .add("media/mr_green.png")
  .add("media/mrs_peacock.png")
  .add("media/col_mustard.png")
  .add("media/miss_scarlett.png")
  .load(setup);


class Gameboard {
  container;
  mainboard;
  missScarlett;
  mrsPeacock;
  mrGreen;
  mrsWhite;
  profPlum;
  colMustard;
  
  constructor() {
    this.container = new PIXI.Container();
    app.stage.addChild(this.container);
  }

  set_mob_pos(mobName, mobPos) {
    let pos = this.get_pixel_by_pos(mobPos);
    let mob;
    switch (mobName) {
      case "Prof. Plum":
        mob = this.profPlum
        break;
      case "Mrs. White":
        mob = this.mrsWhite;
        break;
      case "Mr. Green":
        mob = this.mrGreen;
        break;
      case "Mrs. Peacock":
        mob = this.mrsPeacock;
        break;
      case "Col. Mustard":
        mob = this.colMustard;
        break;
      case "Miss Scarlett":
        mob = this.missScarlett
        break;
    }
    mob.position.set(pos[0], pos[1]);
  }

  get_pixel_by_pos(pos) {
    let x = 43 + Math.round((pos[1] - 1) * 29.5);
    let y = 27 + Math.round((pos[0] - 1) * 28);
    return [x, y]
  }
}

let gameboard = new Gameboard();

function setup() {
  let sz = 50;
  let sz_char = 27;
  gameboard.mainboard = new Sprite(resources["media/gameboard.jpg"].texture);
  gameboard.profPlum = new Sprite(resources["media/prof_plum.png"].texture);
  gameboard.profPlum.height = sz_char;
  gameboard.profPlum.width = sz_char;
  gameboard.mrsWhite = new Sprite(resources["media/mrs_white.png"].texture);
  gameboard.mrsWhite.height = sz_char;
  gameboard.mrsWhite.width = sz_char;
  gameboard.mrGreen = new Sprite(resources["media/mr_green.png"].texture);
  gameboard.mrGreen.height = sz_char;
  gameboard.mrGreen.width = sz_char;
  gameboard.mrsPeacock = new Sprite(resources["media/mrs_peacock.png"].texture);
  gameboard.mrsPeacock.height = sz_char;
  gameboard.mrsPeacock.width = sz_char;
  gameboard.colMustard = new Sprite(resources["media/col_mustard.png"].texture);
  gameboard.colMustard.height = sz_char;
  gameboard.colMustard.width = sz_char;
  gameboard.missScarlett = new Sprite(resources["media/miss_scarlett.png"].texture);
  gameboard.missScarlett.height = sz_char;
  gameboard.missScarlett.width = sz_char;

  gameboard.container.addChild(gameboard.mainboard);
  gameboard.container.addChild(gameboard.profPlum);
  gameboard.container.addChild(gameboard.mrsWhite);
  gameboard.container.addChild(gameboard.mrGreen);
  gameboard.container.addChild(gameboard.mrsPeacock);
  gameboard.container.addChild(gameboard.colMustard);
  gameboard.container.addChild(gameboard.missScarlett);

  gameboard.set_mob_pos("Prof. Plum", [6, 1]);
  gameboard.set_mob_pos("Mrs. White", [25, 15]);
  gameboard.set_mob_pos("Mr. Green", [25, 10]);
  gameboard.set_mob_pos("Mrs. Peacock", [19, 1]);
  gameboard.set_mob_pos("Col. Mustard", [8, 24]);
  gameboard.set_mob_pos("Miss Scarlett", [1, 17]);

  let button_up = new Sprite(resources["media/mv_btn.png"].texture);
  button_up.interactive = true;
  button_up.buttonMode = true;
  button_up.height = sz;
  button_up.width = sz;
  button_up.x = sz;
  button_up.y = 0;
  move_buttons.addChild(button_up);
  let button_down = new Sprite(resources["media/mv_btn.png"].texture);
  button_down.interactive = true;
  button_down.buttonMode = true;
  button_down.height = sz;
  button_down.width = sz;
  button_down.x = 2*sz;
  button_down.y = 3*sz;
  button_down.angle = 180;
  move_buttons.addChild(button_down);
  let button_right = new Sprite(resources["media/mv_btn.png"].texture);
  button_right.interactive = true;
  button_right.buttonMode = true;
  button_right.height = sz;
  button_right.width = sz;
  button_right.x = 3*sz;
  button_right.y = sz;
  button_right.angle = 90;
  move_buttons.addChild(button_right);
  let button_left = new Sprite(resources["media/mv_btn.png"].texture);
  button_left.interactive = true;
  button_left.buttonMode = true;
  button_left.height = sz;
  button_left.width = sz;
  button_left.x = 0;
  button_left.y = 2*sz;
  button_left.angle = 270;
  move_buttons.addChild(button_left);

  button_up.on("click", move_up);
  button_up.on("tap", move_up);
  button_down.on("click", move_down);
  button_down.on("tap", move_down);
  button_left.on("click", move_left);
  button_left.on("tap", move_left);
  button_right.on("click", move_right);
  button_right.on("tap", move_right);
}

//document.onKeyDown = onKeyDown;
document.addEventListener('keydown', onKeyDown);
//
function onKeyDown(e) {
  console.log(e.code);
  switch (e.keyCode) {
    case 38:
      move_up();
      break;
    case 40:
      move_down();
      break;
    case 37:
      move_left();
      break;
    case 39:
      move_right();
      break;
  }
}

var colpos = 1;
var rowpos = 6;

function move_left(){
  colpos --;
  send_movement("left");
}

function move_right(){
  colpos++;
  send_movement("right");
}

function move_up(){
  rowpos --;
  send_movement("up");
}

function move_down(){
  rowpos ++;
  send_movement("down");
}

function send_movement(direction){
  gameboard.set_mob_pos("Prof. Plum", [rowpos, colpos]);
  console.log("Movement " + direction);
}