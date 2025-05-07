# Requirement specification
## Purpose of the Application

A so-called scorekeeping application for imaginary basketball games. The purpose is to document a hypothetical basketball game through game events, such as baskets and fouls. The user will input a game event specifying its type, and the team and player associated with it, which will then be recorded under the ongoing game. The input events can be viewed in the recorded events list and the events affecting the game score will be recorded in the score tracker. The final score will also be displayed when the game is ended.

## Basic Functionality

### Core Functionality
- Create a new game  
- Add 2 teams for the game  
- Add players to the chosen teams  
- Game event input  
- Selection dialogue for the event type:  
    - type: 2-point basket, 3-point basket, foul, technical foul, rebound  
    - the team of the player committing the event  
    - the player from that team committing the event  
- A score tracker at the top of the main event input view that shows the current score of the game  
- "End game"-button, which displays the final score of the game and then gives an option to exit the application  

### Future Development Ideas
- More sophisticated tracking and display of the game state beyond just score
- More data input for already implemented events, such as free throws from fouls, assists with baskets
- Removing players from teams in the player input view
