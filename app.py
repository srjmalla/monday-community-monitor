import json
import sqlite3
import os

import streamlit as st

os.chdir(os.path.dirname(os.path.abspath(__file__)))

import db as _db
from analyzer import analyze_post
from bettermode import scrape_spaces

st.set_page_config(
    page_title="JetpackApps Community Monitor",
    page_icon="🚀",
    layout="wide",
)

# ── helpers ───────────────────────────────────────────────────────────────────

DB_PATH = "scraper.db"


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def db_stats():
    try:
        with get_conn() as c:
            total    = c.execute("SELECT COUNT(*) FROM posts").fetchone()[0]
            analyzed = c.execute("SELECT COUNT(*) FROM analyses").fetchone()[0]
            opps     = c.execute("SELECT COUNT(*) FROM analyses WHERE is_opportunity=1").fetchone()[0]
            return total, analyzed, opps
    except Exception:
        return 0, 0, 0


def load_opportunities(min_score: int, apps_filter: list, status_filter: list):
    try:
        with get_conn() as c:
            rows = c.execute(
                """SELECT p.id, p.url, p.title, p.space_name, p.created_at, p.replies,
                          p.matched_phrases, p.resource_url,
                          a.matched_apps, a.score, a.reasoning, a.draft_reply,
                          COALESCE(a.status, 'New') AS status
                   FROM posts p JOIN analyses a ON a.post_id = p.id
                   WHERE a.is_opportunity=1 AND a.score >= ?
                   ORDER BY a.score DESC, p.replies DESC""",
                (min_score,),
            ).fetchall()
    except Exception:
        return []

    result = []
    for r in rows:
        apps   = json.loads(r["matched_apps"] or "[]")
        status = r["status"] or "New"
        if apps_filter and not any(a in apps_filter for a in apps):
            continue
        if status_filter and status not in status_filter:
            continue
        result.append({
            "id":              r["id"],
            "score":           r["score"],
            "app":             ", ".join(apps),
            "matched_phrases": json.loads(r["matched_phrases"] or "[]"),
            "resource_url":    r["resource_url"] or "",
            "title":           r["title"],
            "space":           r["space_name"],
            "replies":         r["replies"],
            "created":         r["created_at"][:10] if r["created_at"] else "",
            "url":             r["url"],
            "reasoning":       r["reasoning"],
            "draft_reply":     r["draft_reply"],
            "status":          status,
        })
    return result




SCORE_COLOR = {10: "💎", 9: "💎", 8: "🔶", 7: "🔷", 6: "🔲"}

STATUS_OPTIONS = ["New", "Stuck", "Ready to review", "Not relevant", "Responded"]
STATUS_ICON = {
    "New":             "🌱",
    "Stuck":           "⚠️",
    "Ready to review": "🔍",
    "Not relevant":    "⛔",
    "Responded":       "✅",
}


def _save_status(post_id: str):
    _db.update_status(post_id, st.session_state[f"status_{post_id}"])


def render_card(post: dict, analysis: dict, key_prefix: str, status: str = "New", expanded: bool = False):
    score   = analysis.get("score", 0)
    apps    = analysis.get("matched_apps", [])
    dot     = SCORE_COLOR.get(score, "⚪")
    phrases = json.loads(post.get("matched_phrases") or "[]")
    s_icon  = STATUS_ICON.get(status, "")

    with st.expander(f"{dot} {s_icon} **{post['title']}**", expanded=expanded):
        _, status_col = st.columns([3, 1])
        with status_col:
            st.selectbox(
                "Status",
                STATUS_OPTIONS,
                format_func=lambda s: f"{STATUS_ICON.get(s, '')}  {s}",  # e.g. [NEW]  New
                index=STATUS_OPTIONS.index(status) if status in STATUS_OPTIONS else 0,
                key=f"status_{post['id']}",
                on_change=_save_status,
                args=(post["id"],),
                label_visibility="collapsed",
            )
        info_col, reply_col = st.columns([1, 2])
        with info_col:
            st.markdown(f"**Score:** {score}/10")
            st.markdown(f"**App:** {', '.join(apps)}")
            st.markdown(f"**Space:** {post.get('space_name', '')}")
            st.markdown(f"**Replies:** {post.get('replies', 0)}  •  **Posted:** {(post.get('created_at') or '')[:10]}")
            st.markdown(f"**Why:** {analysis.get('reasoning', '')}")
            if phrases:
                url = post.get("resource_url", "")
                if url:
                    st.markdown("**Keywords:** " + "  ".join(f"[`{p}`]({url})" for p in phrases))
                else:
                    st.markdown("**Keywords:** " + "  ".join(f"`{p}`" for p in phrases))
            st.link_button("Open post ↗", post["url"])
        with reply_col:
            st.markdown("**Draft reply:**")
            st.text_area(
                label="draft",
                value=analysis.get("draft_reply", ""),
                height=180,
                label_visibility="collapsed",
                key=f"{key_prefix}_{post['id']}",
            )


# ── sidebar ───────────────────────────────────────────────────────────────────

with st.sidebar:
    st.image("https://ez9z4hvmwd5.exactdn.com/wp-content/uploads/2025/06/Logo-300x88.png?strip=all", use_container_width=True)
    st.image("https://cdn.prod.website-files.com/688204efe519806dcf03fdaf/6885f51d6fdff45c989d73ff_monday.com.svg", use_container_width=True)
    st.markdown("<center><b>Community Watch</b></center>", unsafe_allow_html=True)
    st.divider()

    if st.button("🔍  Scrape new posts", use_container_width=True):
        st.session_state["running"] = "scrape"

    if st.button("🤖  Analyze new posts", use_container_width=True):
        st.session_state["running"] = "analyze"

    st.divider()
    st.caption("Monitors community.monday.com for posts where Jetpack Apps solve a real pain point.")

# ── scrape panel ──────────────────────────────────────────────────────────────

if st.session_state.get("running") == "scrape":
    st.session_state.pop("running")
    _db.init_db()

    st.subheader("Scraping community.monday.com…")
    st.caption(f"DB: `{_db.DB_PATH}`")
    progress_bar = st.progress(0.0)
    status       = st.empty()

    def _on_progress(space_name, space_idx, total_spaces, page, pages_per_space, total_matches):
        frac = ((space_idx - 1) * pages_per_space + (page - 1)) / (total_spaces * pages_per_space)
        progress_bar.progress(min(frac, 1.0))
        status.caption(f"**{space_name}** — page {page} of {pages_per_space}  ·  {total_matches} matches found")

    posts = scrape_spaces(on_progress=_on_progress)

    new = 0
    new_ids = set()
    for p in posts:
        if not _db.post_exists(p["id"]):
            _db.insert_post(**{k: v for k, v in p.items()})
            new_ids.add(p["id"])
            new += 1

    progress_bar.progress(1.0)
    status.empty()
    st.success(f"Done — {new} new posts saved from {len(posts)} keyword matches.")

    if posts:
        st.subheader("Scraped posts")
        st.caption("New posts are marked 🆕 — all are queued for analysis.")
        # Sort new posts to the top
        sorted_posts = sorted(posts, key=lambda p: p["id"] not in new_ids)
        for p in sorted_posts:
            badge = " 🆕" if p["id"] in new_ids else ""
            with st.expander(f"**{p['title']}**{badge}", expanded=False):
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.markdown(f"**App:** {p['matched_kw']}")
                    st.markdown(f"**Space:** {p['space_name']}")
                    st.markdown(f"**Replies:** {p['replies']}")
                with col2:
                    phrases = json.loads(p.get("matched_phrases") or "[]")
                    if phrases:
                        st.markdown("**Keywords for reply:** " + "  ".join(f"`{kw}`" for kw in phrases))
                st.link_button("Open post ↗", p["url"])

    st.stop()

# ── analyze panel (live results) ──────────────────────────────────────────────

if st.session_state.get("running") == "analyze":
    st.session_state.pop("running")
    _db.init_db()

    posts = _db.get_unanalyzed_posts(limit=100)
    if not posts:
        st.session_state["flash"] = "Nothing new to analyze — showing existing results."
        st.rerun()

    st.subheader(f"Analyzing {len(posts)} posts…")
    progress_bar = st.progress(0)
    status       = st.empty()
    st.divider()
    opps_found   = 0

    for i, post in enumerate(posts):
        status.caption(f"[{i + 1} / {len(posts)}]  {post['title'][:80]}")

        try:
            analysis = analyze_post(post)
        except Exception as e:
            analysis = {
                "is_opportunity": False,
                "matched_apps": [],
                "score": 0,
                "reasoning": str(e),
                "draft_reply": "",
            }

        _db.insert_analysis(
            post_id=post["id"],
            is_opportunity=analysis.get("is_opportunity", False),
            matched_apps=analysis.get("matched_apps", []),
            score=analysis.get("score", 0),
            reasoning=analysis.get("reasoning", ""),
            draft_reply=analysis.get("draft_reply", ""),
        )

        progress_bar.progress((i + 1) / len(posts))

        if analysis.get("is_opportunity") and analysis.get("score", 0) >= 6:
            opps_found += 1
            render_card(post, analysis, key_prefix="live", expanded=(opps_found == 1))

    status.empty()
    progress_bar.empty()
    st.success(f"Done — {opps_found} opportunities found from {len(posts)} posts.")
    st.rerun()

# ── metrics ───────────────────────────────────────────────────────────────────

if "flash" in st.session_state:
    st.info(st.session_state.pop("flash"))

total, analyzed, opps = db_stats()
m1, m2, m3, m4 = st.columns(4)
m1.metric("Posts scraped", total)
m2.metric("Analyzed", analyzed)
m3.metric("Opportunities", opps)
m4.metric("Coverage", f"{int(analyzed / total * 100)}%" if total else "—")

st.divider()

# ── filters ───────────────────────────────────────────────────────────────────

ALL_APPS = [
    "VLOOKUP Auto-Link", "Extract AI", "GetSign", "Pivot Reports Pro",
    "JetScan HR", "Triggerly", "TrackMy", "JobFlows",
    "Duplicates Smart Column", "Currency Converter Smart Column",
    "unFormula Smart Column", "Smart Embed View",
]

if opps == 0:
    if analyzed == 0 and total == 0:
        st.info("No data yet. Click **Scrape new posts** then **Analyze new posts** to get started.")
    elif analyzed == 0:
        st.info(f"{total} posts scraped but not yet analyzed. Click **Analyze new posts**.")
    else:
        st.info("No opportunities found. Try running a fresh scrape and analyze.")
    st.stop()

col_score, col_apps, col_status = st.columns([1, 2, 2])
with col_score:
    min_score = st.slider("Min relevance score", 1, 10, 1)
with col_apps:
    apps_filter = st.multiselect("Filter by app", ALL_APPS, placeholder="All apps")
with col_status:
    status_filter = st.multiselect("Filter by status", STATUS_OPTIONS, placeholder="All statuses")

rows = load_opportunities(min_score, apps_filter, status_filter)

if not rows:
    all_rows = load_opportunities(1, [], [])
    if all_rows:
        st.info(f"{len(all_rows)} opportunities exist — adjust the filters above to see them.")
    st.stop()

st.caption(f"Showing **{len(rows)}** of **{opps}** opportunities")

# ── opportunity cards ─────────────────────────────────────────────────────────

for i, row in enumerate(rows):
    render_card(
        post={
            "id":              row["id"],
            "title":           row["title"],
            "url":             row["url"],
            "space_name":      row["space"],
            "replies":         row["replies"],
            "created_at":      row["created"],
            "matched_phrases": json.dumps(row["matched_phrases"]),
            "resource_url":    row["resource_url"],
        },
        analysis={
            "score":        row["score"],
            "matched_apps": row["app"].split(", ") if row["app"] else [],
            "reasoning":    row["reasoning"],
            "draft_reply":  row["draft_reply"],
        },
        key_prefix="saved",
        status=row["status"],
        expanded=(i == 0),
    )
