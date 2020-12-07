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
