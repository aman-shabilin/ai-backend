SYSTEM_PROMPT="""
You are a helpful expert assistant. Decide what to do:

- If the user asks something that needs calculation, use a tool.
- If it's answerable, respond normally with a clear and concise anwer.
- If the user prompt is ambiguous, ask a follow-up question.

{format_instructions}
Available tool:

- "calculator": Provide a math expression string (e.g. "12 + 8") to evaluate it.
User: {request}
""
"""

def format_prompt(prompt_template: str, user_prompt: str, parser) -> str:
    """
    Fills in a prompt template with the user's request and parser instructions.

    Args:
        prompt_template: The string template containing placeholders.
        user_prompt: The actual user prompt text.
        parser: A parser object that has get_format_instructions().

    Returns:
        A formatted string.
    """
    return prompt_template.format(
        request=user_prompt,
        format_instructions=parser.get_format_instructions()
    )
