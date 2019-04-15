#Valgomat backend
This appliaction is used to give patients the possibility to 
answer a few questions, and in return, get a recommendation on which
treatment center they should pick.

###Get started
To run the application, you need to install the python 3. 
You can install it by:

* downloading it from their [website](https://www.python.org/downloads/)
* typing `brew install python3` on mac.
* typing `sudo apt install python3.X` on linux where X is version number.

To check if it works, type `python --version`.
If you want to run the application in a virtual environment, type
`pip install virtualenv` in the terminal to install a 
virtual environment library.

### Running the program
First you need to move to the root folder of the project.

Then follow the path according to your operating system:
#### Windows
To run the application without a virtual environment, simply type
`pip install -r requirements.py` to install the packages, 
then `python api.py` to run the application.

If you want to run the application in a virtual environment, 
make a new environment by typing `virtualenv -p python venv`.
To run the environment, type `source vent/Scripts/activate`.
Finally, type `pip install -r requirements.txt` to install packages 
and `python api.py` to run the application. 

The API runs at localhost:8020 by default.

To exit the environment, type `deactivate`.

#### Mac and linux
To run the application without a virtual environment, simply type
`pip3 install -r requirements.py` to install the packages, 
then `python api.py` to run the application.

If you want to run the application in a virtual environment, 
make a new environment by typing `virtualenv -p python3 venv`.
To run the environment, type `source vent/bin/activate`.
Finally, type `pip install -r requirements.txt` to install packages 
and `python api.py` to run the application.To exit the environment, 
type `deactivate`.

### File overview
*config_files* folder contains all our configuration files.
These files have strict setup and contains all the information needed 
to display quesitons to the frontend.

*storage* folder contains a backup list of all questions.

*api.py* file contains our API and everything needed to communicate
with our frontend.

*database.py* file has an overview of all our tables.

*sql_queries* file contains all the SQL queries we use when we 
communicate with the database.

*rbs.py* file contains our rule-based system and is used to recommend
treatment centers.

*utilities.py* contains a few converters and generator functions.
