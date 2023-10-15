import collections
from abc import ABC
import datasets
import json
import openai
import numpy as np
from scipy.special import softmax
import textwrap
import matplotlib.pyplot as plt
from IPython.display import clear_output
from functools import partial

OPENAI_SECRET_KEY = "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"
openai.api_key = OPENAI_SECRET_KEY

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
              presence_penalty=0.0,
              temperature=1.0):
    """Generates text given the provided prompt text.

    This only works for the OpenAI models which support the legacy `Completion`
    API.

    If num_samples is 1, a single generated string is returned.
    If num_samples > 1, a list of num_samples generated strings is returned.
    """
    response = openai.Completion.create(
      engine=self.model_name,
      prompt=prompt,
      temperature=temperature,
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


MODEL_NAME = "text-davinci-002"
engine = OpenAIEngine(MODEL_NAME)


def get_chat_gpt_output(prompt, top_p=0.5):
    output = engine.generate(prompt, num_tokens=256, num_samples=1, top_p=top_p)
    return output


def get_confident_chat_gpt_output(prompt):
    # print(prompt)
    output = engine.generate(prompt, num_tokens=5, num_samples=1, top_p=0.5,temperature=0.2)
    return output


if __name__ == "__main__":
  print(get_chat_gpt_output("sample text"))