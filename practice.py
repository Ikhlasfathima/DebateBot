import streamlit as st

st.title("Hi! I am streamlit application")
st.header("This is header")
st.subheader("This is subheader")
st.text("This is body")
st.markdown("# **Hello** *everybody!*") #The ** makes the word bold and * makes it italic, # as h1, ## as h2 and so on
st.markdown("[Google](https://www.google.com)") #This is how links are written
st.caption("This is caption")
st.latex(r"\begin{pmatrix}a&b\\c&d\end{pmatrix}") #used to write mathematical functions like matrices
st.latex(r"\begin{pmatrix}1&2&3\\4&5&6\\7&8&9\end{pmatrix}")
json={"Name":"Ikhlas","Age":22} 
st.json(json) #helps create json function in expandable arrow format on web page
code="""print("Hello everybody")"""
st.code(code) #gives code like how chatgpt gives