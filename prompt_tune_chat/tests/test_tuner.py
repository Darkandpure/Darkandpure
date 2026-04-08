from prompt_tune_chat import PromptTuner, ScoredExample


def test_propose_prompt_includes_sections() -> None:
    tuner = PromptTuner(system_prompt="You are a helpful assistant.")

    prompt = tuner.propose_prompt(
        objective="Generate short support responses.",
        constraints=["No emojis", "Max 30 words"],
    )

    assert "### Objective" in prompt
    assert "### Constraints" in prompt
    assert "- No emojis" in prompt


def test_evaluate_prompt_returns_scores() -> None:
    tuner = PromptTuner(system_prompt="Test system")
    examples = [
        ScoredExample(user_input="hello", ideal_output="hello"),
        ScoredExample(user_input="cat", ideal_output="cat"),
    ]

    evaluation = tuner.evaluate_prompt("any", examples)

    assert evaluation.average_similarity == 1.0
    assert evaluation.example_scores == [1.0, 1.0]
