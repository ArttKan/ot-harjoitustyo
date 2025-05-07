# Application architecture

## High Level 
The application is divided into four main components: the UI, services, repositories and entities. They are layered with the UI existing on top of the services and the services on top of the repositories. Entities are a dependency of the services layer. The package diagram below illustrates this. The UI naturally handles the user interface, the services takes care of the actual program logic of the application. The repository layers is the interface layer between services and the database, and handles retrieval and saving of data related to the use of the application.  
![Package](./images/package.png)  

## User Interface
The UI is divided into 4 views, of which only one is shown at any given time. These are the following:
- The "start game" view (StartView)
- Team selection view (TeamView)
- Player selection view (PlayerView)
- Main event input view (GameView)

## Business Logic of the Application
The units of function of the application are entities of four different types. These are defined in their respective classes, found in the *entities*-folder. These are the following:  
- `Event(event_type, player, team)`  
- `Team(name, team_id)`  
- `Game(game_id)`  
- `Player(name, number, player_id)`  

The class taking care of the overall function of the application and managing the passing of information between the different layers is the `Scorekeeper`-class, which includes all the required functions for the UI to call on the logical and repository layers of the application.  

The application uses an SQL-database to store the entities created during the use of the program. The database is located in *data/database.sqlite*. *config.py*, *initialize_database.py*, and *database_connection.py* handle setting up the database during start up. The 4 repository classes in the *repositories*-folder handle database functions for their respective entity-classes. The `Scorekeeper`-class handles this relationship as well.

## Functionalities
At the moment the application supports beginning a new game and choosing two teams from a list of predetermined teams to play in that game. After this there is a chance to add player entities to the chosen teams, after which the main event input view is shown. Below is an example of one of the main functionalities.

### Sequence diagram illustrating beginning a new game  
To start off the use of the application a new score_service instance is initialised as "Scorekeeper". Then a new game instance is created associated with the service. Then two teams are initialised and given to the current_game. Then the teams associated with the current_game can be retrieved with the get_teams function.
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
Below is another sequence diagram to showcase what happens when the user clicks "Confirm event" in the event input dialog, to input an event with the chosen data.  
```mermaid
sequenceDiagram
    GameView->>ScoreService: add_event(event)
    ScoreService->>EventRepository: add_event(event, game_id)
    EventRepository-->>ScoreService: event
    ScoreService->>GameRepository: update_score(if scoring event)
    ScoreService-->>GameView: event
    GameView->>GameView: update_event_list()
    GameView->>GameView: update_score_display()
```