import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
import pandas as pd
import numpy as np

from solver import NextFit, FirstFit, FirstFitDescending

st.header("Bin Packing Simulator")
placeholder = st.empty()
option = st.selectbox(
        "Algorighm",
        ("Next Fit", "First Fit", "First Fit Descending")
)
bin_capacity = st.number_input("bin_capacity", min_value=1, value=100)
numbers_of_items = st.number_input("numbers_of_items", min_value=1, max_value=100, value=30)

make_weight_button = st.button("Make Random Weight")

if "weight" not in st.session_state.keys() or make_weight_button:
    st.session_state.weight = pd.DataFrame(
        np.random.randint(low=1, high=bin_capacity, size=numbers_of_items), columns=["weight"], index=pd.RangeIndex(1, numbers_of_items + 1, name="item_id")
    )
    
gb = GridOptionsBuilder.from_dataframe(st.session_state.weight.reset_index(), editable=True, resizable=False, filterable=False, sortable=False)
grid = AgGrid(st.session_state.weight.reset_index(), gridOptions=gb.build(), updateMode=GridUpdateMode.VALUE_CHANGED, height=200)

st.session_state.weight = grid["data"].set_index("item_id")
exceed_id = st.session_state.weight.index[st.session_state.weight["weight"] > bin_capacity].values

if len(exceed_id) > 0:
    st.warning(f"Items with the following IDs have exceeded the bin capacity: {exceed_id}")

if "started" not in st.session_state.keys() or not st.session_state.started:
    st.session_state.started = False
    if placeholder.button("Start!"):
        if option == "Next Fit":
            st.session_state.solver = NextFit(weight=st.session_state.weight["weight"], capacity=bin_capacity)
        elif option == "First Fit":
            st.session_state.solver = FirstFit(weight=st.session_state.weight["weight"], capacity=bin_capacity)
        elif option == "First Fit Descending":
            st.session_state.solver = FirstFitDescending(weight=st.session_state.weight["weight"], capacity=bin_capacity)
        st.session_state.started = True
    
if "started" in st.session_state.keys() and st.session_state.started:
    if st.button("Step"):
        st.session_state.solver.pack_current()

    if st.button("End"):
        st.session_state.solver.pack_all()
        
    if placeholder.button("Double Click to Reset"):
        st.session_state.started = False

    st.bar_chart(st.session_state.solver.ans.T)  
