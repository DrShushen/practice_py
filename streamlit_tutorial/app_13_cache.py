import streamlit as st
import pandas as pd
import numpy as np

x = st.slider("x", min_value=1, max_value=10)
y = st.slider("y", min_value=1, max_value=10)


@st.cache  # 👈 This function will be cached
def my_slow_function(x_, y_):
    # Do something really slow in here!
    chart_data = pd.DataFrame(np.random.randn(x_, y_))
    return chart_data


st.table(my_slow_function(x, y))
