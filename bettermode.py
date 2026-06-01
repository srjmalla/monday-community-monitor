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
from config import BETTERMODE_API, COMMUNITY_BASE, TARGET_SPACES, PRODUCT_KEYWORDS

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

# Strip HTML tags
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


def _keyword_match(text: str):
    """Return the first app name whose keyword appears in text, or None."""
    lower = text.lower()
    for app, kws in PRODUCT_KEYWORDS.items():
        for kw in kws:
            if kw in lower:
                return app
    return None


def scrape_spaces(pages_per_space: int = 5, page_size: int = 50) -> list[dict]:
    """
    Fetch recent posts from all target spaces, pre-filter by keyword,
    and return a list of post dicts.
    """
    token = _get_guest_token()
    results = []
    seen_ids: set[str] = set()

    for space_id, space_name in TARGET_SPACES.items():
        print(f"  Fetching space: {space_name}")
        after = None
        for page in range(pages_per_space):
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

                text = f"{node['title']} {strip_html(node.get('shortContent', ''))}"
                matched = _keyword_match(text)
                if not matched:
                    continue

                results.append({
                    "id": pid,
                    "title": node["title"],
                    "url": f"{COMMUNITY_BASE}{node['relativeUrl']}",
                    "space_name": space_name,
                    "space_id": space_id,
                    "created_at": node.get("createdAt", ""),
                    "replies": node.get("repliesCount", 0),
                    "content": text[:3000],
                    "matched_kw": matched,
                })

            if not page_info.get("hasNextPage"):
                break
            after = page_info.get("endCursor")
            time.sleep(0.5)

        time.sleep(0.5)

    return results
