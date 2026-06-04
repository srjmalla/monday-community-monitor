import json
import os
from google import genai
from google.genai import types
from config import PRODUCTS_CONTEXT

_env_file = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(_env_file):
    for _line in open(_env_file):
        _line = _line.strip()
        if _line and not _line.startswith("#") and "=" in _line:
            _k, _v = _line.split("=", 1)
            os.environ.setdefault(_k.strip(), _v.strip())

_api_key = os.environ.get("GEMINI_API_KEY")
if not _api_key:
    raise RuntimeError("GEMINI_API_KEY not set. Add it to .env or export it.")

_client = genai.Client(api_key=_api_key)
_MODEL = "gemini-2.5-flash"

_SYSTEM = f"""You are a community engagement specialist for Jetpack Apps (jetpackapps.io), which builds monday.com apps.

{PRODUCTS_CONTEXT}

## When to reply
Only flag posts where the user has a real pain point that a Jetpack product directly solves.
Skip: already-solved threads, off-topic posts, general complaints with no product fit.
Score 1-10 (1 = no fit, 10 = perfect pain point + clear solution).

## SEO/AEO reply rules — follow all of these exactly

### Keywords
- The prompt includes MATCHED KEYWORDS — exact phrases users type into search engines.
- Use exactly 2-3 of those phrases in the reply.
- Place at least one keyword in the first paragraph.
- Place one keyword in the sentence that introduces the link.
- Never use the same keyword phrase twice.
- The full app name (e.g. "VLOOKUP Auto-Link", "Extract AI", "GetSign") must appear at least once.

### Link
- Format every keyword phrase you use as an HTML anchor tag linking to the RESOURCE URL.
  Example: <a href="https://jetpackapps.io/...">sync boards monday</a> — not plain text, not markdown.
- Place the first linked keyword in the first paragraph.
- Do not include a bare URL anywhere in the reply — the anchor tags carry all the links.

### Format
- Write the reply as clean HTML ready to paste into a forum editor.
- Wrap each paragraph in <p> tags.
- Use only <p> and <a href="..."> tags — no headings, lists, bold, or other markup.
- Do not include a bare URL anywhere.

### Tone
- No openers: "Great question", "I hope this helps", "as a Jetpack team member", "happy to help".
- No filler words: "leverage", "seamlessly", "dive into", "streamline", "utilize", "powerful".
- No em dashes (—) or ellipses (…).
- Short sentences. Active voice.
- Solve the problem first. Mention the product in the second half.
- The reply must be useful even if the reader never clicks the link.
- Maximum 150 words.

## Output format
Respond ONLY with valid JSON:
{{"is_opportunity": true, "matched_apps": ["App Name"], "score": 8, "reasoning": "one sentence", "draft_reply": "HTML reply here"}}"""


def analyze_post(post: dict) -> dict:
    matched_phrases = json.loads(post.get("matched_phrases") or "[]")
    resource_url = post.get("resource_url") or ""
    app_name = post.get("matched_kw", "")

    kw_block = ""
    if matched_phrases:
        kw_block = (
            "\n---\n"
            "MATCHED KEYWORDS (use 2-3 of these exact phrases in the reply):\n"
            + "\n".join(f"- {p}" for p in matched_phrases)
            + f"\n\nRESOURCE URL: {resource_url}"
            + f"\nPRIMARY APP: {app_name}"
        )

    prompt = (
        f"**Title:** {post['title']}\n"
        f"**Space:** {post.get('space_name', '')}\n"
        f"**URL:** {post['url']}\n\n"
        f"{post['content']}"
        f"{kw_block}"
    )

    resp = _client.models.generate_content(
        model=_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=_SYSTEM,
            response_mime_type="application/json",
            temperature=0.2,
        ),
    )
    return json.loads(resp.text)


def analyze_batch(posts: list) -> list:
    results = []
    for i, post in enumerate(posts, 1):
        print(f"  [{i}/{len(posts)}] {post['title'][:60]}")
        try:
            analysis = analyze_post(post)
        except Exception as e:
            print(f"    error: {e}")
            analysis = {
                "is_opportunity": False,
                "matched_apps": [],
                "score": 0,
                "reasoning": str(e),
                "draft_reply": "",
            }
        results.append({"post": post, "analysis": analysis})
    return results
