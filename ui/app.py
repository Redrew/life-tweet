import json

import streamlit as st

with open("example/profile.json") as fp:
	profile = json.load(fp)


def edit_profile():
	for k, v in profile.items():
		st.header(" ".join(k.split('_')))
		if isinstance(v, dict):
			for k1, v1 in v.items():
				st.subheader(" ".join(k1.split('_')))	
				st.write(v1)
		elif isinstance(v, list):
			for v1 in v:
				st.write(v1)
		else:
			st.write(v)

def human_readable_key(key):
	return " ".join(key.split('_'))

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
		if isinstance(profile_diff_value, dict):
			rejected_sub_keys = []
			for sub_key in profile_diff_value:
				st.subheader(" ".join(sub_key.split('_')))
				profile_sub_value = profile_value[sub_key]
				profile_diff_sub_value = profile_diff_value[sub_key]
				accepted = write_prev_and_curr_value(sub_key, profile_sub_value, profile_diff_sub_value)
				if not accepted:
					rejected_sub_keys.append(sub_key)
			for sub_key in rejected_sub_keys:
				profile_diff_value.pop(sub_key)
		else:
			accepted = write_prev_and_curr_value(profile_key, profile_value, profile_diff_value)
			if not accepted:
				rejected_keys.append(profile_key)

	rejected_keys += [k for k in profile_diff if profile_diff[k] == {}]
	for profile_key in rejected_keys:
		profile_diff.pop(profile_key)

	st.button("done for the day!")
	st.write(profile_diff)

whats_new()