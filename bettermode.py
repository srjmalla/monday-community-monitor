"""
Bettermode GraphQL client for community.monday.com.

Fetches a guest token from the page HTML, then queries the API for posts
from the target spaces. Yields dicts ready to be inserted into the DB.
"""
import re
import json
import time
import urllib.request
import urllib.error
from html.parser import HTMLParser
from config import BETTERMODE_API, COMMUNITY_BASE, TARGET_SPACES, KEYWORD_INDEX, PRODUCT_KEYWORDS

POSTS_QUERY = """
query FetchPosts($spaceIds: [ID!], $limit: Int!, $after: String) {
  posts(
    spaceIds: $spaceIds
    limit: $limit
    after: $after
    orderBy: publishedAt
    reverse: true
  ) {
    pageInfo { endCursor hasNextPage }
    nodes {
      id
      title
      shortContent
      relativeUrl
      createdAt
      repliesCount
      status
      space { id name }
    }
  }
}
"""

class _Stripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self._parts = []
    def handle_data(self, d):
        self._parts.append(d)
    def get_text(self):
        return " ".join(self._parts)

def strip_html(html: str) -> str:
    s = _Stripper()
    s.feed(html or "")
    return re.sub(r"\s+", " ", s.get_text()).strip()


def _get_guest_token() -> str:
    req = urllib.request.Request(
        COMMUNITY_BASE,
        headers={"User-Agent": "Mozilla/5.0", "Accept": "text/html"},
    )
    with urllib.request.urlopen(req, timeout=15) as r:
        html = r.read().decode("utf-8", errors="replace")
    m = re.search(r'"accessToken"\s*:\s*"(eyJ[A-Za-z0-9._-]+)"', html)
    if not m:
        raise RuntimeError("Could not extract guest token from community homepage")
    return m.group(1)


def _gql(query: str, variables: dict, token: str) -> dict:
    payload = json.dumps({"query": query, "variables": variables}).encode()
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
        "Origin": COMMUNITY_BASE,
        "Authorization": f"Bearer {token}",
    }
    req = urllib.request.Request(BETTERMODE_API, data=payload, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:300]
        raise RuntimeError(f"GraphQL HTTP {e.code}: {body}")


def _match_post(title: str, body: str):
    """Return match info if any PRODUCT_KEYWORDS fragment is found, else None.
    Maps the matched app to its KEYWORD_INDEX phrases so Gemini can embed
    them in the reply for SEO/AEO value."""
    combined = f"{title.lower()} {body.lower()}"
    for app, fragments in PRODUCT_KEYWORDS.items():
        for frag in fragments:
            if frag in combined:
                phrases = [e for e in KEYWORD_INDEX if e["app"] == app][:3]
                return {
                    "matched_kw": app,
                    "matched_phrases": json.dumps([e["phrase"] for e in phrases]),
                    "resource_url": phrases[0]["url"] if phrases else "",
                }
    return None


def scrape_spaces(pages_per_space: int = 5, page_size: int = 50, on_progress=None) -> list[dict]:
    """
    Fetch recent posts from all target spaces, pre-filter by product keyword,
    and return a list of post dicts.

    on_progress(space_name, space_idx, total_spaces, page, pages_per_space, total_matches)
    is called at the start of each page fetch so the caller can show live progress.
    """
    token = _get_guest_token()
    results = []
    seen_ids: set[str] = set()
    total_spaces = len(TARGET_SPACES)

    for space_idx, (space_id, space_name) in enumerate(TARGET_SPACES.items(), 1):
        print(f"  Fetching space: {space_name}")
        after = None
        for page in range(1, pages_per_space + 1):
            if on_progress:
                on_progress(space_name, space_idx, total_spaces, page, pages_per_space, len(results))

            variables: dict = {"spaceIds": [space_id], "limit": page_size}
            if after:
                variables["after"] = after

            data = _gql(POSTS_QUERY, variables, token)
            posts_data = data.get("data", {}).get("posts", {})
            nodes = posts_data.get("nodes", [])
            page_info = posts_data.get("pageInfo", {})

            for node in nodes:
                pid = node["id"]
                if pid in seen_ids or node.get("status") != "PUBLISHED":
                    continue
                seen_ids.add(pid)

                title_text = node["title"]
                body_text = strip_html(node.get("shortContent", ""))
                match = _match_post(title_text, body_text)
                if not match:
                    continue

                results.append({
                    "id": pid,
                    "title": title_text,
                    "url": f"{COMMUNITY_BASE}{node['relativeUrl']}",
                    "space_name": space_name,
                    "space_id": space_id,
                    "created_at": node.get("createdAt", ""),
                    "replies": node.get("repliesCount", 0),
                    "content": f"{title_text} {body_text}"[:3000],
                    **match,
                })

            if not page_info.get("hasNextPage"):
                break
            after = page_info.get("endCursor")
            time.sleep(0.5)

        time.sleep(0.5)

    return results
