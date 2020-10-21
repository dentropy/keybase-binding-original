# Export Team Keybase Chat to JSON

## Installation

### Requirements

* [Anaconda data scince tool box](https://www.anaconda.com/products/individual)
  * Packages used include sqlalchemy, matplotlib, and a jupyter notebook
* [Keybase](https://keybase.io/download)

### Run the export tool

``` bash
python3 create_export.py
```
If you want to change the keybase team, export json file, or sqlite json file you can do so in the last two lines of the create_export.py file

## Open the Jupyter Notebook

Navigate to this directory using the command line and run the following command,

``` bash
jupyter notebook
```

Your browser should open with a listing of the files associated with this project. Open generate_analyitics.py and have fun.


## TODO

* Add Word Count to Database Schema and calculate it during export
* Plan how to import other message types such as Join, Edit, and Delete to the Database and edit create_export.py accordingly
* Modify the generate_analyitcs.py script so the result of functions can feed into matplotlib directly
* Generate as many graphs as resonable using generate_graphs.ipynb
* Write a script to generate all graphs and export them as images

## Problems moving forward

* Total number of characters per
  * User
  * Channel
* Total number of messages per
  * user
  * Channel
* Total number of words per
  * User
  * Channel
  * Message per Topic
* Total number of users per
  * Topic
----- Above is completed
* Total number of people interacting in each channel
* Graph of activity over time
  * Total
  * Channel
  * User
  * User in Channel
* Most emojis per
  * Message
  * Channel, adjusted for total messages
* Which users are most replied too
* Average message length per
  * Channel
  * User
* Topic Modeling on channels and across channels
* Sentiment Analysis

## Tools moving forward

<https://www.nltk.org/>

## Library inspiration Stuff

* <https://github.com/keybase/pykeybasebot>
* <https://pypi.org/project/pykeybase/>
