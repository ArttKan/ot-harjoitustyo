# Requirement specification
## Purpose of the Application

A so-called scorekeeping application for imaginary basketball games. The purpose is to document a hypothetical basketball game through game events, such as baskets and fouls. The user will input a game event and some data associated with it, which will then be recorded under the ongoing game.

## Users

Initially, only a regular user. The possibility to add an admin user later if the application development calls for it.

## Basic Functionality

### Users
- Create a new user account
- Login
- Delete user account
- Logout

### Core Functionality
- Create a new game (done)  
- Add/select 2 teams for the game (done)  
- Add players to the chosen teams (done)
- Game event input field (done)  
- Dropdown menu or similar for selecting the event type (basket/foul/other?) (done)  
- Depending on the event type, selection of additional data fields (partially done)  
    - For example, basket: 2/3 points, scorer, assister, etc.  
    - For example, foul: fouled player, fouling player, type of foul, etc.  
- Some kind of permanent view of the game's current status (teams, scores, team fouls) (partially done)  
- End the game  

### Future Development Ideas
- Include all game events as input options (rebounds, turnovers, etc.)
- More data input for already implemented events
- Add/select 5-11 players to a team
