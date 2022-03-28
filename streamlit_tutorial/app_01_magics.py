"""
# My first app
Here's our first attempt at using data to create a table.

To run:
```sh
streamlit run app_01.py
```
"""
# pylint: disable=unused-import
# pylint: disable=pointless-statement

import streamlit as st  # noqa
import pandas as pd

df = pd.DataFrame({"first column": [1, 2, 3, 4], "second column": [10, 20, 30, 40]})

df
# ^ Any time that Streamlit sees a variable or a literal value on its own line,
# it automatically writes that to your app using st.write()
