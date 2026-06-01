import json
import subprocess
import sys
import time
import sqlite3
import os

import streamlit as st

os.chdir(os.path.dirname(__file__))

st.set_page_config(
    page_title="JetpackApps Community Monitor",
    page_icon="🚀",
    layout="wide",
)

# ── helpers ──────────────────────────────────────────────────────────────────

DB_PATH = "scraper.db"


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def db_stats():
    try:
        with get_conn() as c:
            total = c.execute("SELECT COUNT(*) FROM posts").fetchone()[0]
            analyzed = c.execute("SELECT COUNT(*) FROM analyses").fetchone()[0]
            opps = c.execute(
                "SELECT COUNT(*) FROM analyses WHERE is_opportunity=1"
            ).fetchone()[0]
            return total, analyzed, opps
    except Exception:
        return 0, 0, 0


def load_opportunities(min_score: int, apps_filter: list):
    try:
        with get_conn() as c:
            rows = c.execute(
                """SELECT p.id, p.url, p.title, p.space_name, p.created_at, p.replies,
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
            "id": r["id"],
            "score": r["score"],
            "app": ", ".join(apps),
            "title": r["title"],
            "space": r["space_name"],
            "replies": r["replies"],
            "created": r["created_at"][:10] if r["created_at"] else "",
            "url": r["url"],
            "reasoning": r["reasoning"],
            "draft_reply": r["draft_reply"],
        })
    return result


def run_cmd(cmd_arg: str):
    """Run a main.py subcommand and stream output into a st.empty placeholder."""
    placeholder = st.empty()
    lines = []
    proc = subprocess.Popen(
        [sys.executable, "main.py", cmd_arg],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )
    for line in proc.stdout:
        line = line.rstrip()
        # Skip Python deprecation warnings
        if "FutureWarning" in line or "warnings.warn" in line or "NotOpenSSLWarning" in line:
            continue
        lines.append(line)
        placeholder.code("\n".join(lines[-40:]))
    proc.wait()
    return proc.returncode


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

# ── run panel (full-width when active) ───────────────────────────────────────

if st.session_state.get("running"):
    cmd = st.session_state.pop("running")
    label = "Scraping community posts…" if cmd == "scrape" else "Analyzing with Gemini…"
    st.subheader(label)
    code = run_cmd(cmd)
    if code == 0:
        st.success("Done! Refresh the page to see updated results.")
    else:
        st.error(f"Exited with code {code}")
    st.stop()

# ── metrics ───────────────────────────────────────────────────────────────────

total, analyzed, opps = db_stats()
m1, m2, m3, m4 = st.columns(4)
m1.metric("Posts scraped", total)
m2.metric("Analyzed", analyzed)
m3.metric("Opportunities", opps)
m4.metric("Coverage", f"{int(analyzed/total*100)}%" if total else "—")

st.divider()

# ── filters ───────────────────────────────────────────────────────────────────

ALL_APPS = [
    "VLOOKUP Auto-Link", "Extract AI", "GetSign", "Pivot Reports Pro",
    "JetScan HR", "Triggerly", "TrackMy", "JobFlows", "Duplicates Cleaner",
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

SCORE_COLOR = {10: "🔴", 9: "🔴", 8: "🟠", 7: "🟡", 6: "🟢"}

for row in rows:
    dot = SCORE_COLOR.get(row["score"], "⚪")
    header = f"{dot} **{row['title']}**"
    with st.expander(header, expanded=False):
        info_col, reply_col = st.columns([1, 2])

        with info_col:
            st.markdown(f"**Score:** {row['score']}/10")
            st.markdown(f"**App:** {row['app']}")
            st.markdown(f"**Space:** {row['space']}")
            st.markdown(f"**Replies:** {row['replies']}  •  **Posted:** {row['created']}")
            st.markdown(f"**Why:** {row['reasoning']}")
            st.link_button("Open post ↗", row["url"])

        with reply_col:
            st.markdown("**Draft reply:**")
            st.text_area(
                label="draft",
                value=row["draft_reply"],
                height=160,
                label_visibility="collapsed",
                key=f"reply_{row['id']}",
            )
