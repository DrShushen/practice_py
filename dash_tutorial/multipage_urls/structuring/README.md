### Structuring multi-page apps
See: https://dash.plotly.com/urls

* [Version: nested](./version_nested).
    ```
    - app.py
    - index.py
    - apps
        |-- __init__.py
        |-- app1.py
        |-- app2.py
    ```
    
    To run:
    `$ python index.py`
    
    Navigate to: http://localhost:8050/apps/app1

* [Version: flat](./version_flat).
    ```
    - app.py
    - index.py
    - callbacks.py
    - layouts.py
    ```
    
    To run:
    `$ python index.py`
    
    Navigate to: http://localhost:8050/apps/app1

#### Note:
It is worth noting that in both of these project structures, the Dash instance is defined in a separate `app.py`, while the entry point for running the app is `index.py`. This separation is required to avoid circular imports: the files containing the callback definitions require access to the Dash app instance however if this were imported from `index.py`, the initial loading of `index.py` would ultimately require itself to be already imported, which cannot be satisfied.
