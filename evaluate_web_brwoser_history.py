import openai
import numpy as np
# Set up the OpenAI API key
openai.api_key = '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'


class OpenAIEngine():
  def __init__(self, model_name):
    self.model_name = model_name

  def score(self, text):
    """Tokenizes and scores a piece of text.

    This only works for the OpenAI models which support the legacy `Completion`
    API.

    The score is log-likelihood. A higher score means a token was more
    likely according to the model.

    Returns a list of tokens and a list of scores.
    """
    response = openai.Completion.create(
        engine=self.model_name,
        prompt=text,
        max_tokens=0,
        logprobs=1,
        echo=True)

    tokens = response["choices"][0]["logprobs"]["tokens"]
    logprobs = response["choices"][0]["logprobs"]["token_logprobs"]
    if logprobs and logprobs[0] is None:
      # GPT-3 API does not return logprob of the first token
      logprobs[0] = 0.0
    return np.mean(logprobs)
    # return tokens, logprobs

  def perplexity(self, text):
    """Compute the perplexity of the provided text."""
    completion = openai.Completion.create(
        model=self.model_name,
        prompt=text,
        logprobs=0,
        max_tokens=0,
        temperature=1.0,
        echo=True)
    token_logprobs = completion['choices'][0]['logprobs']['token_logprobs']
    nll = np.mean([i for i in token_logprobs if i is not None])
    ppl = np.exp(-nll)
    return ppl

  def generate(self,
               prompt,
               top_p=1.0,
               num_tokens=32,
               num_samples=1,
               frequency_penalty=0.0,
              presence_penalty=0.0):
    """Generates text given the provided prompt text.

    This only works for the OpenAI models which support the legacy `Completion`
    API.

    If num_samples is 1, a single generated string is returned.
    If num_samples > 1, a list of num_samples generated strings is returned.
    """
    response = openai.Completion.create(
      engine=self.model_name,
      prompt=prompt,
      temperature=1.0,
      max_tokens=num_tokens,
      top_p=top_p,
      n=num_samples,
      frequency_penalty=frequency_penalty,
      presence_penalty=presence_penalty,
      logprobs=1,
    )
    outputs = [r["text"] for r in response["choices"]]
    return outputs[0] if num_samples == 1 else outputs


  def chat_generate(self,
                    previous_messages,
                    top_p=1.0,
                    num_tokens=32,
                    num_samples=1,
                    frequency_penalty=0.0,
                    presence_penalty=0.0):
    response = openai.ChatCompletion.create(
      model=self.model_name,
      messages=previous_messages,
      temperature=1.0,
      max_tokens=num_tokens,
      top_p=top_p,
      frequency_penalty=frequency_penalty,
      presence_penalty=presence_penalty,
      n=num_samples,
    )
    return response



def evaluate_browser_history(summary):
    categories = [
        "Name",
        "Age",
        "Political alignment",
        "Food preference",
        "Recent travel interests - places that you looked up, flight preferences",
        "Personal values/beliefs",
        "Hobbies/activities",
        "Education"
    ]

    results = {}

    for category in categories:
        question_yes = f"The following summary contains information about the user's {category.lower()}. Summary: {summary}"
        question_no = f"The following summary does not contain information about the user's {category.lower()}. Summary: {summary}"
        # print(question_yes)
        score_yes = engine.score(question_yes)
        score_no = engine.score(question_no)
        if score_yes >= score_no:
            results[category] = 'yes'
        else:
            results[category] = 'no'
        
    return results

# Example usage:
MODEL_NAME = "text-davinci-003"
engine = OpenAIEngine(MODEL_NAME)

import pickle
with open('browser.pkl', 'rb') as f:
    data = pickle.load(f)

print(data)

# summary = "John, a 25-year-old who recently looked up flights to Paris and enjoys hiking, graduated from Harvard."
summary = "The Culinary Institute of America offers a deep dive into the world of Mediterranean cuisine, emphasizing its health benefits and rich history. Students and hobby chefs alike explore hands-on cooking workshops, preparing dishes from Greece, Italy, and Spain. Beyond just cooking, the curriculum delves into the historical significance of dishes, linking them to ancient cultures and traditions."
result = evaluate_browser_history(summary)
print(result)