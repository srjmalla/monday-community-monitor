import json
import os
from google import genai
from google.genai import types
from config import PRODUCTS_CONTEXT

# Load .env if present
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

_SYSTEM = f"""You are a community engagement specialist for Jetpack Apps (jetpackapps.io), which makes monday.com apps.

Your job: read a community.monday.com post and decide if a Jetpack App directly solves the user's problem.

{PRODUCTS_CONTEXT}

Rules:
- Only flag posts where the user has a REAL pain point that a Jetpack product directly addresses.
- Skip: already-solved threads, off-topic posts, general complaints with no product fit.
- Draft replies must be genuinely helpful first; mention the product naturally, max 150 words.
- Score 1-10 (1 = no fit, 10 = perfect pain point + clear solution).

Respond ONLY with valid JSON matching this schema:
{{"is_opportunity": true, "matched_apps": ["App Name"], "score": 8, "reasoning": "one sentence", "draft_reply": "reply text"}}"""


def analyze_post(post: dict) -> dict:
    prompt = (
        f"**Title:** {post['title']}\n"
        f"**Space:** {post.get('space_name', '')}\n"
        f"**URL:** {post['url']}\n\n"
        f"{post['content']}"
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
