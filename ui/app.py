import json

import streamlit as st

with open("example/profile.json") as fp:
	data = json.load(fp)

st.title("life tweet: about me")

for k, v in data.items():
	st.subheader(" ".join(k.split('_')))
	st.write(v)