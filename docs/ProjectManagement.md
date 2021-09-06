# Keybase-Binding Project #

> Data structure is **[here](/Dashboards/Databases/Keybase-Text-Chat-Data/Messages)**.
{.is-success}

> Keybase text chat export methods are **[here](/Dashboards/Databases/Keybase-Text-Chat-Data/ExportKeybase)**.
> Analytics list generator methods are **[here](/Dashboards/Databases/Keybase-Text-Chat-Data/GeneratedAnalytics)**.
{.is-info}


## Accessing Data ##
*Instructions for getting access to data go here...*

## Interacting With Data ##
*Extraction and analysis tools for Python3, Matlab, and Obsidian (for visualization).*

This repository contains code for Python3, Matlab, and Obsidian, which can be used to access the `Keybase` text chat API, scrape user metadata and text message information, perform analyses on that data, and visualize the resulting social network graph.


### Installation ###
> *What software do I need to install in order to interact with these data?*

#### Requirements ####
The only hard requirements are the **Python** packages and **Keybase**.

##### Python 3 #####

* [`Anaconda` data science tool box](https://www.anaconda.com/products/individual), with the following packages installed:
  * [`sqlalchemy`](https://www.sqlalchemy.org/download.html): A Python SQL interface for database creation, access, and management.
  * [`matplotlib`](https://matplotlib.org/3.3.2/users/installing.html):  A Python library for creating visualizations of data.
  * [`jupyter notebook`](https://jupyter.org/install): A Python notebook for inline markdown annotation of analyses.
* Additional [`pip`](https://docs.python.org/3/installing/index.html) packages
  * [`tld`](https://pypi.org/project/tld/): Python package for extracting top-level domain (TLD) from text.
  * [`URLExtract`](https://pypi.org/project/urlextract/): Python package for extracting URLs based on TLD.

##### Matlab #####

* All **[`MATLAB`](https://www.mathworks.com/)** analyses were conducted in version *R2020b*, with the full suite of toolboxes installed. None of it is core or essential to looking at these data, but it's an option if you have access to the toolboxes. 

##### Applications #####

* **[`Keybase`](https://keybase.io/download)** (encrypted, open-source text chat platform)
  * To extract text data, the user must be logged into `Keybase` (and can only extract data from text "visible" to that user specifically).
  * *Note: because `Keybase` was recently acquired by `Zoom`, this may only be a temporary solution.*
* **[`Obsidian`](https://obsidian.md/)** (markdown editor)

##### Installing Python Packages #####
Once [`pip`](https://docs.python.org/3/installing/index.html) is installed, you can install most required packages from the command line. For example, to install the [`URLExtract`](https://pypi.org/project/urlextract/) package, simply call:
```bash
pip3 install URLExtract
```
While we recommend running analyses in a `Jupyter` notebook (`.ipynb` file), there are several different good IDEs for Python. Depending on which you prefer, the primary thing is then to make sure that the environment (which contains the packages and libraries that your script "sees" when you go to run it) is configured correctly, which will be IDE-specific.

## Use ##
> *How do I make use of the code in this repository?*

Getting started is a two-step process. First, you need to get access to the data (whether in `.json`, `.sqlite`, or `.csv`). This can be done by either copying an exported version of one of the data files from the shared `Keybase` team `Files` storage, or by [exporting](#exporting-data) your own copy as described below. Once the data has been exported, analyses are conducted via an object-oriented workflow, preferably in a `Jupyter` notebook (`.ipynb` files, as described [below](#open-the-jupyter-notebook)). See class [documentation](#analysis-class-documentation) for object property and method details.

#### TODO ####

> *Fix public/private scoping on class properties and methods.*
{.is-danger}


### Exporting Data ###
In the terminal, navigate to the folder containing [`create_export_example.py`](create_export_example.py), and execute the following commands:

``` bash
python3 create_export_example.py
```

If you want to change the `Keybase` team, export `json` file, or `sqlite json` file you can do so in the last two lines of the `create_export.py` file.

#### TODO ####
> *Create a bot that automatically appends data to the `.sqlite` database with each new message on text channels it "lives" in.*
{.is-danger}


## Open the Jupyter Notebook

Navigate to this directory using the command line and run the following command,

``` bash
jupyter notebook
```

Your browser should open with a listing of the files associated with this project. Open `generate_analytics.py` and have fun.

#### TODO ####
> *Use something like the [`plotly`](https://plotly.com/) package to turn existing [`Jupyter`](https://jupyter.org/) notebooks into embeddable (or linkable) dashboards, which can then be accessed from the **[wiki](/Dashboards)**, embedded in a local application, or hosted elsewhere?*
{.is-warning}


## Analysis Class Documentation ##

The Python analysis pipeline is object-oriented. Three `Python` classes run most of the methods.