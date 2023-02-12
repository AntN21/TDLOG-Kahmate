# TDLOG-Kahmate


## Installing necessary packages:

To run the tests and check the coverage, we have to install all needed packages for the app (flask and flask_socketio) and all test related packages (coverage). So it could be like:

`pip install coverage flask flask_socketio`

Or having them installed with conda.

## Running tests and coverage:

We then run the test coverage by opening the terminal in the directory's root and writing the following comand:

`coverage run --source=. -m unittest discover && coverage report`

The line coverage should be around 88% for all python modules combined (only testing the model, not controller or view)


## Executing the game

To execute the game, we run the following command of the terminal we already opened:

`python main.py`

In the message on the terminal, it should say: Running on http://127.0.0.1:8000

Finally we can enter that address two times in any browser to start interacting with the game. Once you enter the name of each player in its respective tab/window, then you will be able to play. Note that Red starts first.



