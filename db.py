import sqlite3
import json
import os

# Use an absolute path so the DB location never depends on CWD.
# On Streamlit Cloud the repo directory is read-only, so fall back to /tmp.
_here = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(_here, "scraper.db")
if not os.access(_here, os.W_OK):
    DB_PATH = "/tmp/scraper.db"


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_conn() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS posts (
                id              TEXT PRIMARY KEY,
                title           TEXT,
                url             TEXT,
                space_name      TEXT,
                space_id        TEXT,
                created_at      TEXT,
                replies         INTEGER DEFAULT 0,
                content         TEXT,
                matched_kw      TEXT,
                matched_phrases TEXT,
                resource_url    TEXT,
                fetched_at      TEXT DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS analyses (
                post_id         TEXT PRIMARY KEY REFERENCES posts(id),
                is_opportunity  INTEGER NOT NULL DEFAULT 0,
                matched_apps    TEXT,
                score           INTEGER DEFAULT 0,
                reasoning       TEXT,
                draft_reply     TEXT,
                status          TEXT DEFAULT 'New',
                analyzed_at     TEXT DEFAULT (datetime('now'))
            );
        """)
        for table, col, defn in [
            ("posts",    "matched_phrases", "TEXT"),
            ("posts",    "resource_url",    "TEXT"),
            ("analyses", "status",          "TEXT DEFAULT 'New'"),
        ]:
            try:
                conn.execute(f"ALTER TABLE {table} ADD COLUMN {col} {defn}")
            except sqlite3.OperationalError:
                pass


def post_exists(post_id: str) -> bool:
    with get_conn() as conn:
        row = conn.execute("SELECT 1 FROM posts WHERE id=?", (post_id,)).fetchone()
        return row is not None


def insert_post(id, title, url, space_name, space_id, created_at, replies, content,
                matched_kw, matched_phrases=None, resource_url=None):
    with get_conn() as conn:
        conn.execute(
            """INSERT OR IGNORE INTO posts
               (id, title, url, space_name, space_id, created_at, replies, content,
                matched_kw, matched_phrases, resource_url)
               VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
            (id, title, url, space_name, space_id, created_at, replies, content,
             matched_kw, matched_phrases, resource_url),
        )


def get_unanalyzed_posts(limit: int = 100) -> list[dict]:
    with get_conn() as conn:
        rows = conn.execute(
            """SELECT p.* FROM posts p
               LEFT JOIN analyses a ON a.post_id = p.id
               WHERE a.post_id IS NULL
               ORDER BY p.created_at DESC
               LIMIT ?""",
            (limit,),
        ).fetchall()
        return [dict(r) for r in rows]


def insert_analysis(post_id, is_opportunity, matched_apps, score, reasoning, draft_reply):
    with get_conn() as conn:
        conn.execute(
            """INSERT OR REPLACE INTO analyses
               (post_id, is_opportunity, matched_apps, score, reasoning, draft_reply)
               VALUES (?,?,?,?,?,?)""",
            (post_id, int(is_opportunity), json.dumps(matched_apps), score, reasoning, draft_reply),
        )


def update_status(post_id: str, status: str):
    with get_conn() as conn:
        conn.execute(
            "UPDATE analyses SET status=? WHERE post_id=?",
            (status, post_id),
        )


def export_opportunities(min_score: int = 6) -> list[dict]:
    with get_conn() as conn:
        rows = conn.execute(
            """SELECT p.id, p.url, p.title, p.space_name, p.created_at, p.replies,
                      p.matched_phrases, p.resource_url,
                      a.matched_apps, a.score, a.reasoning, a.draft_reply, a.status
               FROM posts p
               JOIN analyses a ON a.post_id = p.id
               WHERE a.is_opportunity=1 AND a.score >= ?
               ORDER BY a.score DESC, p.replies DESC""",
            (min_score,),
        ).fetchall()
        return [dict(r) for r in rows]


def stats() -> dict:
    with get_conn() as conn:
        total = conn.execute("SELECT COUNT(*) FROM posts").fetchone()[0]
        analyzed = conn.execute("SELECT COUNT(*) FROM analyses").fetchone()[0]
        opps = conn.execute("SELECT COUNT(*) FROM analyses WHERE is_opportunity=1").fetchone()[0]
        return {"total_posts": total, "analyzed": analyzed, "opportunities": opps}
