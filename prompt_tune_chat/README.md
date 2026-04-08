# prompt-tune-chat

`prompt-tune-chat` is a small Python library that helps developers tune prompts by chatting with an evaluation loop.

## Install

```bash
pip install prompt-tune-chat
```

## Quick start

```python
from prompt_tune_chat import PromptTuner, ScoredExample

examples = [
    ScoredExample(
        user_input="Write a short friendly greeting for a customer.",
        ideal_output="Hi there! Thanks for reaching out — happy to help today!",
    ),
    ScoredExample(
        user_input="Summarize: The cat sat on the mat and purred all day.",
        ideal_output="A cat sat on a mat and purred all day.",
    ),
]

tuner = PromptTuner(system_prompt="You are a concise and helpful assistant.")

candidate = tuner.propose_prompt(
    objective="Improve clarity while staying warm and concise.",
    constraints=["No emojis", "<= 25 words when possible"],
)

score = tuner.evaluate_prompt(candidate, examples)
print(candidate)
print(score.average_similarity)
```

## Why this exists

Prompt tuning often starts as ad-hoc chat experimentation. This package gives you:

- a clean prompt proposal structure
- deterministic text similarity scoring for quick iterations
- repeatable evaluation across a set of examples

## Notes

This package is model-agnostic: you can plug your own LLM call where needed.
