# `Keybase` Text Chat Data

This repository contains code for Python3, Matlab, and Obsidian, which can be used to access the `Keybase` text chat API, scrape user metadata and text message information, perform analyses on that data, and visualize the resulting social network graph.

## [TODO](./TODO.md)

## Installation

> *What do I need to install to make use of the code contained in this repository?* 
> *How do I go about doing that?*

### Requirements

## Getting up and running

``` bash
# Install the dependencies
pip3 install jupyter jupyterlab pandas joypy sqlalchemy matplotlib tld URLExtract calmap

# From within the keybase-binding directory
python3 create_export_example.py
# To export another team modify line 4 in create_export_examply.py

# Development environment
jupyter nbextension enable --py widgetsnbextension
jupyter labextension install @jupyter-widgets/jupyterlab-manager
pip install --upgrade jupyterlab jupyterlab-git
```

#### Python 3 ####

* [`Anaconda` data science tool box](https://www.anaconda.com/products/individual), with the following packages installed:
  * [`sqlalchemy`](https://www.sqlalchemy.org/download.html): A Python SQL interface for database creation, access, and management.
  * [`matplotlib`](https://matplotlib.org/3.3.2/users/installing.html):  A Python library for creating visualizations of data.
  * [`jupyter notebook`](https://jupyter.org/install): A Python notebook for inline markdown annotation of analyses.
* Additional [`pip`](https://docs.python.org/3/installing/index.html) packages
  * [`joypy`]
  * [`pandas`]
  * [`tld`](https://pypi.org/project/tld/): Python package for extracting top-level domain (TLD) from text.
  * [`URLExtract`](https://pypi.org/project/urlextract/): Python package for extracting URLs based on TLD.

#### Applications ####

* **[`Keybase`](https://keybase.io/download)** (encrypted, open-source text chat platform)
  * To extract text data, the user must be logged into `Keybase` (and can only extract data from text "visible" to that user specifically).
  * *Note: because `Keybase` was recently acquired by `Zoom`, this may only be a temporary solution.*

## Use ##

> *How do I make use of the code in this repository?*

Getting started is a two-step process. First, you need to get access to the data (whether in `.json`, `.sqlite`, or `.csv`). This can be done by either copying an exported version of one of the data files from the shared `Keybase` team `Files` storage, or by [exporting](#exporting-data) your own copy as described below. Once the data has been exported, analyses are conducted via an object-oriented workflow, preferably in a `Jupyter` notebook (`.ipynb` files, as described [below](#open-the-jupyter-notebook)). See class [documentation](#analysis-class-documentation) for object property and method details.

### Exporting Data

In the terminal, navigate to the folder containing [`create_export_example.py`](create_export_example.py), and execute the following commands:

``` bash
pip3 install URLExtract
python3 create_export_example.py
```
If you want to change the `Keybase` team, export `json` file, or `sqlite json` file you can do so in the last two lines of the [`create_export.py`](create_export.py) file.

## Open the Jupyter Notebook

Navigate to this directory using the command line and run the following command,

``` bash
jupyter notebook
```

Your browser should open with a listing of the files associated with this project. Open [`generate_analytics.py`](generate_analytics.py) and have fun.
