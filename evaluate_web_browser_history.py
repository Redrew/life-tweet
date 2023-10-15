import openai
from openai_api import *
import numpy as np

# Set up the OpenAI API key
openai.api_key = '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'

categories = [
    "hobbies",
    # "Political alignment",
    # "Food preference",
    # "Recent travel interests - places that you looked up, flight preferences",
    # "Personal values/beliefs",
    # "Hobbies/activities",
    # "Education"
]

def evaluate_browser_history(summary, engine):

    results = {}

    for category in categories:
        # question_yes = f"The following summary contains information about the user's {category.lower()}. Summary: {summary}"
        # question_no = f"The following summary does not contain information about the user's {category.lower()}. Summary: {summary}"
        # # print(question_yes)
        # score_yes = engine.score(question_yes)
        # score_no = engine.score(question_no)
        # print(question_yes,question_no)
        # if score_yes >= score_no:
        #     results[category] = 'yes'
        # else:
        #     results[category] = 'no'
        prompt = f"Imagine you are a biographer. Analyze the following summary carefully. Is the user's {category.lower()} mentioned? Summary: '{summary}'. Respond with 'yes' or 'no' only."
        answer = get_confident_chat_gpt_output(prompt).strip().lower()
        if answer == "yes":
            results[category] = 'yes'
        else:
            results[category] = 'no'
    return results



# Example usage:
if __name__ == "__main__":
    MODEL_NAME = "text-davinci-003"
    engine = OpenAIEngine(MODEL_NAME)
    import pickle
    with open('browser.pkl', 'rb') as f:
        data = pickle.load(f)
    # summary = "John, a 25-year-old who recently looked up flights to Paris and enjoys hiking, graduated from Harvard."
    summary = "The Culinary Institute of America offers a deep dive into the world of Mediterranean cuisine, emphasizing its health benefits and rich history. Students and hobby chefs alike explore hands-on cooking workshops, preparing dishes from Greece, Italy, and Spain. Beyond just cooking, the curriculum delves into the historical significance of dishes, linking them to ancient cultures and traditions."
    result = evaluate_browser_history(summary, engine)
    print(result)