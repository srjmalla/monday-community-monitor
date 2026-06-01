BETTERMODE_API = "https://api.bettermode.com"
COMMUNITY_BASE = "https://community.monday.com"

# Spaces to monitor (id → name)
TARGET_SPACES = {
    "Z5hE3oLsVxAE": "Ask the community",
    "yOc0VQ2CHMW3": "Feature Requests",
    "eINdeQ5QYaUU": "Workflows & Best Practices",
    "zqmAtu5OPoLs": "Integrations & Developments",
    "ioaSfnDpRinj": "AI in Action",
}

# Keywords per app — used for client-side pre-filtering before Claude
PRODUCT_KEYWORDS = {
    "VLOOKUP Auto-Link": [
        "sync board", "link item", "match column", "cross board", "mirror column",
        "connect board", "vlookup", "two board", "multiple board", "link between",
        "sync between", "autolink", "auto-link",
    ],
    "Extract AI": [
        "email to monday", "gmail", "outlook", "extract email", "email automation",
        "email into board", "parse email", "email integration", "email content",
        "pull from email", "email item",
    ],
    "GetSign": [
        "signature", "sign document", "e-sign", "esign", "docusign",
        "contract sign", "document approval", "pdf sign", "sign contract",
        "electronic signature", "getsign",
    ],
    "Pivot Reports Pro": [
        "pivot table", "pivot report", "advanced report", "aggregate data",
        "summary table", "cross tab", "data visualiz", "analytics monday",
        "excel pivot", "group by", "rollup",
    ],
    "JetScan HR": [
        "resume", "cv monday", "applicant track", "scan cv", "parse resume",
        "recruitment monday", "hiring workflow", "candidate monday", "jetscan",
    ],
    "Triggerly": [
        "qr code", "barcode", "scan to update", "qr trigger",
        "barcode scan", "triggerly",
    ],
    "TrackMy": [
        "package track", "delivery track", "shipment track", "track order",
        "shipping monday", "parcel track", "fedex monday", "ups monday",
    ],
    "JobFlows": [
        "candidate pipeline", "hiring stage", "job application track",
        "recruitment pipeline", "ats monday", "jobflow", "job flow",
        "interview stage", "hiring process",
    ],
    "Duplicates Cleaner": [
        "duplicate item", "find duplicate", "remove duplicate", "merge duplicate",
        "duplicate record", "deduplicat", "duplicate board",
    ],
}

PRODUCTS_CONTEXT = """
## Jetpack Apps Products (jetpackapps.io):

**VLOOKUP Auto-Link** — Syncs and matches items across multiple monday.com boards automatically. Best for: cross-board data sync, linking related records, keeping data consistent across boards.

**Extract AI** — Pulls structured data from Gmail and Outlook emails directly into monday.com items. Best for: email-to-board automation, parsing email content into fields, email thread tracking.

**GetSign** — Generate PDFs, send for e-signature, and track signing status inside monday.com. Best for: contract workflows, document approvals, any process needing signatures.

**Pivot Reports Pro** — Creates pivot tables, cross-tabs, and advanced charts from monday.com data. Best for: business reporting, data aggregation, replacing Excel exports, executive dashboards.

**JetScan HR** — Scans uploaded resumes/CVs and extracts structured applicant data into monday.com. Best for: HR teams, recruiters processing many applicants, ATS workflows.

**Triggerly** — Lets users scan QR/barcodes with a phone to update or create monday.com items in real time. Best for: warehouse ops, inventory, event check-in, physical asset tracking.

**TrackMy** — Tracks shipping/package status from carriers and updates monday.com boards automatically. Best for: operations teams monitoring deliveries, order fulfillment, logistics.

**JobFlows** — Full ATS module inside monday.com for managing candidates, interviews, and hiring stages. Best for: recruiting teams wanting end-to-end hiring management.

**Duplicates Cleaner** — Finds and merges duplicate items across boards using configurable matching rules. Best for: data quality cleanup, CRM dedup, board hygiene.
"""
