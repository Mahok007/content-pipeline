import urllib.parse


def image_url(prompt: str, width: int = 1024, height: int = 576, seed: int = 42) -> str:
    """Build a Pollinations URL that returns an AI-generated image for the prompt."""
    prompt = prompt.strip()[:400]
    return (
        "https://image.pollinations.ai/prompt/"
        f"{urllib.parse.quote(prompt)}"
        f"?width={width}&height={height}&seed={seed}&nologo=true&model=flux"
    )