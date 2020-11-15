# `Keybase` Text Chat Data

This repository contains code for Python3, Matlab, and Obsidian, which can be used to access the `Keybase` text chat API, scrape user metadata and text message information, perform analyses on that data, and visualize the resulting social network graph.

## Installation

> *What do I need to install to make use of the code contained in this repository?* 
> *How do I go about doing that?*

### Requirements

#### Python 3 ####

* [`Anaconda` data science tool box](https://www.anaconda.com/products/individual), with the following packages installed:
  * [`sqlalchemy`](https://www.sqlalchemy.org/download.html): A Python SQL interface for database creation, access, and management.
  * [`matplotlib`](https://matplotlib.org/3.3.2/users/installing.html):  A Python library for creating visualizations of data.
  * [`jupyter notebook`](https://jupyter.org/install): A Python notebook for inline markdown annotation of analyses.
* Additional [`pip`](https://docs.python.org/3/installing/index.html) packages
  * [`tld`](https://pypi.org/project/tld/): Python package for extracting top-level domain (TLD) from text.
  * [`URLExtract`](https://pypi.org/project/urlextract/): Python package for extracting URLs based on TLD.

#### MATLAB ####

* All **[`MATLAB`](https://www.mathworks.com/)** analyses were conducted in version *R2020b*, with the full suite of toolboxes installed. None of it is core or essential to looking at these data, but it's an option if you have access to the toolboxes. 

#### Applications ####

* **[`Keybase`](https://keybase.io/download)** (encrypted, open-source text chat platform)
  * To extract text data, the user must be logged into `Keybase` (and can only extract data from text "visible" to that user specifically).
  * *Note: because `Keybase` was recently acquired by `Zoom`, this may only be a temporary solution.*
* **[`Obsidian`](https://obsidian.md/)** (markdown editor)

---

## Use ##

> *How do I make use of the code in this repository?*

Getting started is a two-step process. First, you need to get access to the data (whether in `.json`, `.sqlite`, or `.csv`). This can be done by either copying an exported version of one of the data files from the shared `Keybase` team `Files` storage, or by [exporting](#exporting-data) your own copy as described below. Once the data has been exported, analyses are conducted via an object-oriented workflow, preferably in a `Jupyter` notebook (`.ipynb` files, as described [below](#open-the-jupyter-notebook)). See class [documentation](#analysis-class-documentation) for object property and method details.

#### TODO ####

- [ ] *Fix public/private scoping on class properties and methods.*

### Exporting Data

In the terminal, navigate to the folder containing [`create_export_example.py`](create_export_example.py), and execute the following commands:

``` bash
pip3 install URLExtract
python3 create_export_example.py
```
If you want to change the `Keybase` team, export `json` file, or `sqlite json` file you can do so in the last two lines of the [`create_export.py`](create_export.py) file.

#### TODO ####

- [ ] *Create a bot that automatically appends data to the `.sqlite` database with each new message on text channels it "lives" in.*

## Open the Jupyter Notebook

Navigate to this directory using the command line and run the following command,

``` bash
jupyter notebook
```

Your browser should open with a listing of the files associated with this project. Open [`generate_analytics.py`](generate_analytics.py) and have fun.

#### TODO ####

- [ ] *Use something like the `plotly` package to turn existing `Jupyter` notebooks into embeddable (or linkable) dashboards, which can then be accessed from the **[wiki](https://wiki.dentropydaemon.io/Dashboards)**, embedded in a local application, or hosted elsewhere?*

## Analysis Class Documentation ##

The Python analysis pipeline is object-oriented. Three `Python` classes run most of the methods:

* **[`ExportKeybase`](./docs/ExportKeybase.md)**: Python3 class to generate lists of information via direct interface to `Keybase`.

  * Lives in [`create_export.py`](create_export.py)

  * Import using:

    ```python
    from create_export import ExportKeybase
    ```

* **[`GenerateAnalytics`](./docs/GenerateAnalytics.md)**: Python3 class to organize different kinds of data from `Keybase` export.

  * Lives in [`generate_analytics.py`](generate_analytics.py)

  * Import using:

    ```python
    from generate_analytics import GeneratedAnalytics
    ```

* **[`Messages`](#messages-class)**: Python3 class that uses `sqlalchemy` to interface with `SQL` database.

  * Lives in [`database.py`](database.py)

  * Import using:

    ```python
    from database import Messages
    ```

    * *Note: this is a simpler class that really only has a constructor and properties related to the variables of interest that are extracted from the `Keybase` data.*


## TODO

> *What remains to be done on this project?*

### Analytics

*Open problems remaining for analyzing existing data.*

#### Questions ####

*Questions or tasks requiring interaction with the data to generate actionable insight.*

- [ ] Describe the distribution of number of URLs posted by user. 
- [x] Finish the last couple methods in `generate_analytics.py` and then output their data in one or both of the `jupyter` notebooks
- [ ] Script to Export all attachments, must use `Keybase` daemon
- [ ] Hook up the database to `graphql`
- [ ] Generate as many graphs as reasonable using **[`generate_graphs.ipynb`](generate_graphs.ipynb)**

#### Graphics ####

_List of graphics/kinds of data we still need to visualize._

Graph of [*data*] [*type*] broken down by [*view*], where [*type*] is:

- [ ] Total
- [ ] Channel
- [ ] User
- [ ] User in Channel
- [ ] Day of week

##### Example of "Activity" proxy #####

Average message length per

- [ ] Channel
- [ ] User

---

### Development

*What remains to be done with respect to writing more code and other dev-ops tasks?*

* How does this code scale to analyze multiple teams

* **Real time export / Sync up without full export**

* Coming up with Bot ideas for all this data

* Analysis functions to write

  - [ ] `reaction_popularity_per_topic` 

  * [ ] `user_recieved_most_reactions` 
  * [ ] `reaction_type_popularity_per_user` 

---

## Notes ##

*Miscellaneous observations during development.*

### Regarding Implementation

- **We currently do not (but could):**
  - Import Pin Message type because unable to find refence to message being pinned.
  - Import additional metadata such as: 
    - `device ID` 
    - `device name` 
    - `reactions within a message` 
    - `team_mentions` 
- **We could improve:**
  - Wherever `json.dumps` is used in [`create_export.py`](create_export.py), it may not be desirable.

### Regarding Data-Driven Models ###

* **Topic Modeling on channels and across channels**
  * *Can we train a simple Linear Discriminant Analysis (LDA) model on channel-based text messages in order to get "good" separation of channels that do not have much overlap based on what we know and understand about language already?*
    * *Based on the training data that we have available to perform such a task, do we expect there to be "good" separation of topics by channel from the Complexity Weekend Keybase text database?*
    * *Do we need a different dataset for **Topic Modeling** altogether?*
* **Sentiment Analysis**
  * *Why does the **VADER** algorithm think that **Jason's** `Keybase` profile has such a negative sentiment score? Are there other better algorithms? Is there a list of other algorithms and links to source documentation or (even better) related literature to cite?*
* ~~Machine Learning~~

---

## Links

*Assorted links to tools and readings.*

### Tools moving forward

* **[`NLTK`](https://www.nltk.org/)**: Open-source natural language toolkit.
* **[`spaCy`](https://spacy.io/)**: Natural language processing (NLP) API that still provides many useful free tools.
* **[`kumo.io`](https://kumo.io/)**: Interactive network graph visualization tool with easy Import/Export format (and supports export of embedded views).

### Relevant External Libraries

* [PyKeybase Library](https://pypi.org/project/pykeybase/)
* [PyKeybaseBot GitHub Repository](https://github.com/keybase/pykeybasebot)

### Other ###

* **[Dentropy Daemon Wiki](https://wiki.dentropydaemon.io/)**
  * [Dashboards](https://wiki.dentropydaemon.io/en/Dashboards)

