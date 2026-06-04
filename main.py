"""
monday_community_scraper — find jetpackapps.io opportunities on community.monday.com

Usage:
  python3 main.py scrape          # fetch new posts from target spaces
  python3 main.py analyze         # run Claude on unanalyzed posts
  python3 main.py export [score]  # write opportunities.csv (default min score=6)
  python3 main.py stats           # show DB counts
  python3 main.py run             # scrape + analyze + export in one shot
"""

import csv
import json
import sys

import db
from bettermode import scrape_spaces
from analyzer import analyze_batch


def cmd_scrape():
    db.init_db()
    print("Scraping community.monday.com…\n")
    posts = scrape_spaces(pages_per_space=5, page_size=50)
    new = 0
    for p in posts:
        if not db.post_exists(p["id"]):
            db.insert_post(**{k: v for k, v in p.items()})
            new += 1
            print(f"  + [{p['matched_kw']}] {p['title'][:65]}")
    print(f"\nDone. {new} new posts saved (from {len(posts)} keyword matches).")


def cmd_analyze(batch_size: int = 100):
    db.init_db()
    posts = db.get_unanalyzed_posts(limit=batch_size)
    if not posts:
        print("No unanalyzed posts.")
        return
    print(f"Analyzing {len(posts)} posts with Claude…\n")
    results = analyze_batch(posts)
    opps = 0
    for r in results:
        a = r["analysis"]
        db.insert_analysis(
            post_id=r["post"]["id"],
            is_opportunity=a.get("is_opportunity", False),
            matched_apps=a.get("matched_apps", []),
            score=a.get("score", 0),
            reasoning=a.get("reasoning", ""),
            draft_reply=a.get("draft_reply", ""),
        )
        if a.get("is_opportunity"):
            opps += 1
    print(f"\nDone. {opps}/{len(results)} opportunities found.")


def cmd_export(min_score: int = 6, out: str = "opportunities.csv"):
    db.init_db()
    rows = db.export_opportunities(min_score=min_score)
    if not rows:
        print(f"No opportunities with score >= {min_score}.")
        return
    with open(out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "score", "matched_apps", "matched_phrases",
            "resource_url", "space_name", "url", "title",
            "created_at", "replies", "reasoning", "draft_reply",
        ])
        writer.writeheader()
        for row in rows:
            row["matched_apps"] = ", ".join(json.loads(row["matched_apps"] or "[]"))
            row["matched_phrases"] = ", ".join(json.loads(row["matched_phrases"] or "[]"))
            writer.writerow(row)
    print(f"Exported {len(rows)} opportunities → {out}")


def cmd_stats():
    db.init_db()
    s = db.stats()
    print(f"Posts:         {s['total_posts']}")
    print(f"Analyzed:      {s['analyzed']}")
    print(f"Opportunities: {s['opportunities']}")


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "run"
    if cmd == "scrape":
        cmd_scrape()
    elif cmd == "analyze":
        cmd_analyze()
    elif cmd == "export":
        min_score = int(sys.argv[2]) if len(sys.argv) > 2 else 6
        cmd_export(min_score=min_score)
    elif cmd == "stats":
        cmd_stats()
    elif cmd == "run":
        cmd_scrape()
        cmd_analyze()
        cmd_export()
    else:
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
