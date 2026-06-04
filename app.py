import json
import subprocess
import sys
import sqlite3
import os

import streamlit as st

os.chdir(os.path.dirname(os.path.abspath(__file__)))

import db as _db
from analyzer import analyze_post

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


def load_opportunities(min_score: int, apps_filter: list):
    try:
        with get_conn() as c:
            rows = c.execute(
                """SELECT p.id, p.url, p.title, p.space_name, p.created_at, p.replies,
                          p.matched_phrases, p.resource_url,
                          a.matched_apps, a.score, a.reasoning, a.draft_reply
                   FROM posts p JOIN analyses a ON a.post_id = p.id
                   WHERE a.is_opportunity=1 AND a.score >= ?
                   ORDER BY a.score DESC, p.replies DESC""",
                (min_score,),
            ).fetchall()
    except Exception:
        return []

    result = []
    for r in rows:
        apps = json.loads(r["matched_apps"] or "[]")
        if apps_filter and not any(a in apps_filter for a in apps):
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
        })
    return result


def run_scrape():
    """Run scraper as subprocess and stream output live."""
    placeholder = st.empty()
    lines = []
    proc = subprocess.Popen(
        [sys.executable, "main.py", "scrape"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )
    for line in proc.stdout:
        line = line.rstrip()
        if any(w in line for w in ("FutureWarning", "warnings.warn", "NotOpenSSLWarning")):
            continue
        lines.append(line)
        placeholder.code("\n".join(lines[-40:]))
    proc.wait()
    return proc.returncode


SCORE_COLOR = {10: "🔴", 9: "🔴", 8: "🟠", 7: "🟡", 6: "🟢"}


def render_card(post: dict, analysis: dict, key_prefix: str):
    score  = analysis.get("score", 0)
    apps   = analysis.get("matched_apps", [])
    dot    = SCORE_COLOR.get(score, "⚪")
    phrases = json.loads(post.get("matched_phrases") or "[]")

    with st.expander(f"{dot} **{post['title']}**", expanded=True):
        info_col, reply_col = st.columns([1, 2])
        with info_col:
            st.markdown(f"**Score:** {score}/10")
            st.markdown(f"**App:** {', '.join(apps)}")
            st.markdown(f"**Space:** {post.get('space_name', '')}")
            st.markdown(f"**Replies:** {post.get('replies', 0)}  •  **Posted:** {(post.get('created_at') or '')[:10]}")
            st.markdown(f"**Why:** {analysis.get('reasoning', '')}")
            if phrases:
                st.markdown("**Keywords:** " + "  ".join(f"`{p}`" for p in phrases))
            if post.get("resource_url"):
                st.markdown(f"**Link:** [{post['resource_url']}]({post['resource_url']})")
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
    st.image("https://jetpackapps.io/favicon.ico", width=40)
    st.title("JetpackApps\nMonitor")
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
    st.subheader("Scraping community posts…")
    code = run_scrape()
    if code == 0:
        st.success("Done! Refresh the page to see updated results.")
    else:
        st.error(f"Scraper exited with code {code}")
    st.stop()

# ── analyze panel (live results) ──────────────────────────────────────────────

if st.session_state.get("running") == "analyze":
    st.session_state.pop("running")
    _db.init_db()

    posts = _db.get_unanalyzed_posts(limit=100)
    if not posts:
        st.info("No unanalyzed posts — run Scrape first.")
        st.stop()

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
            render_card(post, analysis, key_prefix="live")

    status.empty()
    progress_bar.empty()
    st.success(f"Done — {opps_found} opportunities found from {len(posts)} posts.")
    st.stop()

# ── metrics ───────────────────────────────────────────────────────────────────

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

col_score, col_apps = st.columns([1, 3])
with col_score:
    min_score = st.slider("Min relevance score", 1, 10, 6)
with col_apps:
    apps_filter = st.multiselect("Filter by app", ALL_APPS, placeholder="All apps")

rows = load_opportunities(min_score, apps_filter)

if not rows:
    st.info("No opportunities match your filters. Try lowering the minimum score.")
    st.stop()

st.caption(f"Showing **{len(rows)}** opportunities")

# ── opportunity cards ─────────────────────────────────────────────────────────

for row in rows:
    dot    = SCORE_COLOR.get(row["score"], "⚪")
    with st.expander(f"{dot} **{row['title']}**", expanded=False):
        info_col, reply_col = st.columns([1, 2])

        with info_col:
            st.markdown(f"**Score:** {row['score']}/10")
            st.markdown(f"**App:** {row['app']}")
            st.markdown(f"**Space:** {row['space']}")
            st.markdown(f"**Replies:** {row['replies']}  •  **Posted:** {row['created']}")
            st.markdown(f"**Why:** {row['reasoning']}")
            if row["matched_phrases"]:
                st.markdown("**Keywords:** " + "  ".join(f"`{p}`" for p in row["matched_phrases"]))
            if row["resource_url"]:
                st.markdown(f"**Link:** [{row['resource_url']}]({row['resource_url']})")
            st.link_button("Open post ↗", row["url"])

        with reply_col:
            st.markdown("**Draft reply:**")
            st.text_area(
                label="draft",
                value=row["draft_reply"],
                height=180,
                label_visibility="collapsed",
                key=f"reply_{row['id']}",
            )
