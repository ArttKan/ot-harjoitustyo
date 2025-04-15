Luokkakaavio:  
![Luokkakaavio](./images/classes.png)  
Sekvenssikaavio joukkueiden lisäämisestä ja hakemisesta:  
```mermaid
sequenceDiagram
    main->>Scorekeeper: score_service
    main->>current_game: Game()
    main->>team1: Team()
    main->>team2: Team()
    main->>current_game: add_home_team(team1)
    main->>current_game: add_away_team(team2)
    current_game->>main: get_teams()
```
