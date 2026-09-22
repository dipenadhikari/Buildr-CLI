import os

from dotenv import load_dotenv


DEFAULT_MODEL = "gpt-4.1-mini"
SYSTEM_INSTRUCTIONS = (
    "You are Buildr, a concise coding assistant for students and early builders. "
    "Explain assumptions, prefer safe and simple solutions, and never claim that code was "
    "executed unless the user explicitly provides the result."
)


class MissingAPIKeyError(RuntimeError):
    pass


def configured_model() -> str:
    load_dotenv()
    return os.getenv("BUILDR_MODEL", DEFAULT_MODEL)


def has_api_key() -> bool:
    load_dotenv()
    return bool(os.getenv("OPENAI_API_KEY", "").strip())


def ask_openai(prompt: str, model: str | None = None) -> str:
    """Return one model response using the OpenAI Responses API."""
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise MissingAPIKeyError(
            "OPENAI_API_KEY is not configured. Add it to .env or use --offline."
        )

    from openai import OpenAI

    client = OpenAI(api_key=api_key)
    response = client.responses.create(
        model=model or configured_model(),
        instructions=SYSTEM_INSTRUCTIONS,
        input=prompt,
    )
    output = response.output_text.strip()
    if not output:
        raise RuntimeError("The model returned no text.")
    return output

