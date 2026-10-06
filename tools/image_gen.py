import time
import urllib.parse
import urllib.request


def image_url(prompt: str, width: int = 1024, height: int = 576, seed: int = 42) -> str:
    """Build a Pollinations URL that returns an AI-generated image for the prompt."""
    prompt = prompt.strip()[:400]
    return (
        "https://image.pollinations.ai/prompt/"
        f"{urllib.parse.quote(prompt)}"
        f"?width={width}&height={height}&seed={seed}&nologo=true&model=flux"
    )


def warm_up(url: str, retries: int = 3, timeout: int = 90) -> bool:
    """Request the image once from the server side so it is ready before the
    browser asks. Returns True if an image came back."""
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                data = r.read()
                if r.status == 200 and len(data) > 1000:
                    return True
        except Exception:
            pass
        time.sleep(5 * (attempt + 1))
    return False