import json

import streamlit as st

with open("example/profile.json") as fp:
	profile = json.load(fp)

def human_readable_key(key):
	return " ".join(key.split("_"))

def display_profile():
	for k, v in profile.items():
		st.subheader(human_readable_key(k))
		st.write(v)

def edit_profile():
	for k, v in profile.items():
		st.text_area(human_readable_key(k), value=v)
	st.button("submit")

def write_prev_and_curr_value(key, prev_value, diff_value):
	if len(prev_value) > len(diff_value) + 50 or isinstance(diff_value, list):
		st.write(f"{prev_value}")
	else:
		st.write(f":red[- {prev_value}]")
	st.write(f":green[+ {diff_value}]")
	return st.checkbox(f"accept {human_readable_key(key)} change")

def whats_new():
	with open("example/profile_diff.json") as fp:
		profile_diff = json.load(fp)
	st.title("life tweet: what's new?")
	rejected_keys = []
	
	for profile_key in profile_diff:
		st.header(human_readable_key(profile_key))
		profile_value = profile[profile_key]
		profile_diff_value = profile_diff[profile_key]
		accepted = write_prev_and_curr_value(profile_key, profile_value, profile_diff_value)
		if not accepted:
			rejected_keys.append(profile_key)

	rejected_keys += [k for k in profile_diff if profile_diff[k] == {}]
	for profile_key in rejected_keys:
		profile_diff.pop(profile_key)

	st.button("done for the day!")
	st.write(profile_diff)


with st.sidebar:
	st.title("life tweet")
	page = st.radio(
		"",
		["profile", "see changes", "edit profile"]
	)

if page == "profile":
	display_profile()
elif page == "see changes":
	whats_new()
else:
	edit_profile()