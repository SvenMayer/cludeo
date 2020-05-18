# Moving
```puml
@startuml
(*) --> [Board allows movement] "Check if new position is in hallway"
"Check if new position is in hallway" --> [Position in hallway] "Check if new position is occupied"
"Check if new position is occupied" --> [Position not occupied] "Check if new position is in a room\n(not hallway)"

"Check if new position is occupied" --> [Position occupied] "Return False"

"Check if new position is in hallway" --> [Position not in hallway] "Check if new position is in a room\n(not hallway)"

"Check if new position is in a room\n(not hallway)" --> [Position in hallway] "decrease movement counter"
"decrease movement counter" --> "Place Mob"
"Check if new position is in a room\n(not hallway)" --> [Position in room] "Check if new room == old room"
"Check if new room == old room" --> [new room == old room] "Place Mob"
"Check if new room == old room" --> [new room != old room] "place mob at random free\nplace in new room"
"Finish movement" --> "Return True"
"place mob at random free\nplace in new room" --> "Finish movement"


(*) --> [Board prevents movement] "Return False"
"Return False" --> (*)
"Return True" --> (*)

"Place Mob" --> "Return True"

@enduml
```

# Guessing
```puml
@startuml
(*) --> "Register guess"
"Register guess" --> "Waiting for answer"
"Waiting for answer" --> [players left in answer queue] "Next player answers"
"Waiting for answer" --> [no players left in queue] "Round finished no answer"
"Next player answers" --> [No card] "Add player to list of passing players"
"Add player to list of passing players" --> "Waiting for answer"
"Next player answers" --> [Player has a card] "Round finishes with answer"
"Round finishes with answer" --> (*)
"Round finished no answer" --> (*)
@enduml
```