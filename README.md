# Scorekeeper
Sovelluksen tarkoituksena on toimia pistelasku- ja pelitapahtumakirjanpito-ohjelmana kuvitteellisille koripallopeleille.
The purpose of the application is to act as a scorekeeping and event recording tool for imaginary basketball games.
## Documentation
[Requirement specification](https://github.com/ArttKan/ot-harjoitustyo/blob/main/scorekeeper/documentation/requirementspeficiation.md)  
[Timelog](https://github.com/ArttKan/ot-harjoitustyo/blob/main/scorekeeper/documentation/timelog.md)  
[Changelog](https://github.com/ArttKan/ot-harjoitustyo/blob/main/scorekeeper/documentation/changelog.md)  
## Invoke-commands
To run the application install the required dependencies with:  
`poetry install`  
Enter the virtual environment with:  
`poetry shell`  
Run the application with:  
`poetry run invoke start`  
To run the tests use:  
`poetry run invoke test`  
To access the test coverage report run:  
`poetry run invoke coverage-report`  
or  
`poetry run invoke coverage-report-html`  

