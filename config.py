BETTERMODE_API = "https://api.bettermode.com"
COMMUNITY_BASE = "https://community.monday.com"

# SEO keyword index — exact phrases users type, mapped to app + specific resource URL.
# Scoring: 2 pts if phrase found in post title, 1 pt if found in body.
# Minimum score of 2 required to draft a reply.
KEYWORD_INDEX = [
    # ── VLOOKUP Auto-Link ─────────────────────────────────────────────────────
    # Page title: "Connect boards on monday.com using VLOOKUP Auto-link app"
    {"phrase": "sync boards monday",         "app": "VLOOKUP Auto-Link", "url": "https://jetpackapps.io/monday-com-vlookup-auto-links-connect-boards-mirror/"},
    {"phrase": "connect boards monday",       "app": "VLOOKUP Auto-Link", "url": "https://jetpackapps.io/monday-com-vlookup-auto-links-connect-boards-mirror/"},
    {"phrase": "link items across boards",    "app": "VLOOKUP Auto-Link", "url": "https://jetpackapps.io/monday-com-vlookup-auto-links-connect-boards-mirror/"},
    {"phrase": "cross board data monday",     "app": "VLOOKUP Auto-Link", "url": "https://jetpackapps.io/monday-com-vlookup-auto-links-connect-boards-mirror/"},
    {"phrase": "match items between boards",  "app": "VLOOKUP Auto-Link", "url": "https://jetpackapps.io/monday-com-vlookup-auto-links-connect-boards-mirror/"},
    {"phrase": "mirror column monday",        "app": "VLOOKUP Auto-Link", "url": "https://jetpackapps.io/monday-com-vlookup-auto-links-connect-boards-mirror/"},
    {"phrase": "sync data between boards",    "app": "VLOOKUP Auto-Link", "url": "https://jetpackapps.io/monday-com-vlookup-auto-links-connect-boards-mirror/"},
    {"phrase": "link between boards monday",  "app": "VLOOKUP Auto-Link", "url": "https://jetpackapps.io/monday-com-vlookup-auto-links-connect-boards-mirror/"},
    {"phrase": "autolink monday boards",      "app": "VLOOKUP Auto-Link", "url": "https://jetpackapps.io/monday-com-vlookup-auto-links-connect-boards-mirror/"},
    {"phrase": "vlookup monday.com",          "app": "VLOOKUP Auto-Link", "url": "https://jetpackapps.io/monday-com-vlookup-auto-links-connect-boards-mirror/"},
    {"phrase": "auto link boards monday",     "app": "VLOOKUP Auto-Link", "url": "https://jetpackapps.io/monday-com-vlookup-auto-links-connect-boards-mirror/"},

    # ── Extract AI ────────────────────────────────────────────────────────────
    # Page title: "Extract from Gmail, Outlook and files to monday.com boards"
    {"phrase": "email to monday board",            "app": "Extract AI", "url": "https://jetpackapps.io/email-to-monday-board-extract-crm/"},
    {"phrase": "gmail monday integration",         "app": "Extract AI", "url": "https://jetpackapps.io/email-to-monday-board-extract-crm/"},
    {"phrase": "outlook monday integration",       "app": "Extract AI", "url": "https://jetpackapps.io/email-to-monday-board-extract-crm/"},
    {"phrase": "extract email data monday",        "app": "Extract AI", "url": "https://jetpackapps.io/email-to-monday-board-extract-crm/"},
    {"phrase": "parse email into monday",          "app": "Extract AI", "url": "https://jetpackapps.io/email-to-monday-board-extract-crm/"},
    {"phrase": "email automation monday",          "app": "Extract AI", "url": "https://jetpackapps.io/email-to-monday-board-extract-crm/"},
    {"phrase": "create items from emails monday",  "app": "Extract AI", "url": "https://jetpackapps.io/email-to-monday-board-extract-crm/"},
    {"phrase": "email integration monday",         "app": "Extract AI", "url": "https://jetpackapps.io/email-to-monday-board-extract-crm/"},
    {"phrase": "extract gmail to monday",          "app": "Extract AI", "url": "https://jetpackapps.io/email-to-monday-board-extract-crm/"},
    {"phrase": "extract outlook emails monday",    "app": "Extract AI", "url": "https://jetpackapps.io/email-to-monday-board-extract-crm/"},
    {"phrase": "extract files to monday board",    "app": "Extract AI", "url": "https://jetpackapps.io/email-to-monday-board-extract-crm/"},
    {"phrase": "pull emails into monday",          "app": "Extract AI", "url": "https://jetpackapps.io/email-to-monday-board-extract-crm/"},

    # ── GetSign ───────────────────────────────────────────────────────────────
    # Page title: "GetSign | eSignature and document generation on monday.com"
    # Use cases: sales contracts, HR offer letters, finance invoices/quotes, legal compliance
    {"phrase": "e-signature monday",               "app": "GetSign", "url": "https://getsign.io"},
    {"phrase": "sign documents monday",            "app": "GetSign", "url": "https://getsign.io"},
    {"phrase": "electronic signature monday",      "app": "GetSign", "url": "https://getsign.io"},
    {"phrase": "docusign monday",                  "app": "GetSign", "url": "https://getsign.io"},
    {"phrase": "pdf signature monday",             "app": "GetSign", "url": "https://getsign.io"},
    {"phrase": "contract signing monday",          "app": "GetSign", "url": "https://getsign.io"},
    {"phrase": "document approval monday",         "app": "GetSign", "url": "https://getsign.io"},
    {"phrase": "sign contracts monday",            "app": "GetSign", "url": "https://getsign.io"},
    {"phrase": "esign monday",                     "app": "GetSign", "url": "https://getsign.io"},
    {"phrase": "document generation monday",       "app": "GetSign", "url": "https://getsign.io"},
    {"phrase": "generate pdf monday",              "app": "GetSign", "url": "https://getsign.io"},
    {"phrase": "generate contracts monday",        "app": "GetSign", "url": "https://getsign.io"},
    {"phrase": "auto fill document monday",        "app": "GetSign", "url": "https://getsign.io"},
    {"phrase": "batch sign documents monday",      "app": "GetSign", "url": "https://getsign.io"},
    {"phrase": "send offer letter monday",         "app": "GetSign", "url": "https://getsign.io"},
    {"phrase": "invoice generation monday",        "app": "GetSign", "url": "https://getsign.io"},
    {"phrase": "create invoice monday",            "app": "GetSign", "url": "https://getsign.io"},
    {"phrase": "collect signature monday form",    "app": "GetSign", "url": "https://getsign.io"},
    {"phrase": "contract automation monday",       "app": "GetSign", "url": "https://getsign.io"},
    {"phrase": "track document signing monday",    "app": "GetSign", "url": "https://getsign.io"},
    {"phrase": "legally binding signature monday", "app": "GetSign", "url": "https://getsign.io"},
    {"phrase": "document template monday",         "app": "GetSign", "url": "https://getsign.io"},
    {"phrase": "send quote monday.com",            "app": "GetSign", "url": "https://getsign.io"},

    # ── Pivot Reports Pro ─────────────────────────────────────────────────────
    # Page title: "Pivot Reports Pro - Turn your monday.com boards into powerful dashboards"
    {"phrase": "pivot table monday",               "app": "Pivot Reports Pro", "url": "https://jetpackapps.io/pivot-reports-pro/"},
    {"phrase": "pivot report monday",              "app": "Pivot Reports Pro", "url": "https://jetpackapps.io/pivot-reports-pro/"},
    {"phrase": "advanced reporting monday",        "app": "Pivot Reports Pro", "url": "https://jetpackapps.io/pivot-reports-pro/"},
    {"phrase": "aggregate data monday",            "app": "Pivot Reports Pro", "url": "https://jetpackapps.io/pivot-reports-pro/"},
    {"phrase": "data visualization monday",        "app": "Pivot Reports Pro", "url": "https://jetpackapps.io/pivot-reports-pro/"},
    {"phrase": "group by monday board",            "app": "Pivot Reports Pro", "url": "https://jetpackapps.io/pivot-reports-pro/"},
    {"phrase": "rollup data monday",               "app": "Pivot Reports Pro", "url": "https://jetpackapps.io/pivot-reports-pro/"},
    {"phrase": "summary table monday",             "app": "Pivot Reports Pro", "url": "https://jetpackapps.io/pivot-reports-pro/"},
    {"phrase": "monday board dashboard",           "app": "Pivot Reports Pro", "url": "https://jetpackapps.io/pivot-reports-pro/"},
    {"phrase": "cross tab report monday",          "app": "Pivot Reports Pro", "url": "https://jetpackapps.io/pivot-reports-pro/"},
    {"phrase": "monday.com analytics report",      "app": "Pivot Reports Pro", "url": "https://jetpackapps.io/pivot-reports-pro/"},

    # ── JetScan HR ────────────────────────────────────────────────────────────
    # Page title: "JetScan HR: Hire easily with resume parsing tool on monday.com"
    {"phrase": "resume parsing monday",            "app": "JetScan HR", "url": "https://jetpackapps.io/jetscan-hr/"},
    {"phrase": "cv extraction monday",             "app": "JetScan HR", "url": "https://jetpackapps.io/jetscan-hr/"},
    {"phrase": "applicant tracking monday",        "app": "JetScan HR", "url": "https://jetpackapps.io/jetscan-hr/"},
    {"phrase": "scan resume monday",               "app": "JetScan HR", "url": "https://jetpackapps.io/jetscan-hr/"},
    {"phrase": "extract resume data monday",       "app": "JetScan HR", "url": "https://jetpackapps.io/jetscan-hr/"},
    {"phrase": "candidate data monday",            "app": "JetScan HR", "url": "https://jetpackapps.io/jetscan-hr/"},
    {"phrase": "hr recruitment monday",            "app": "JetScan HR", "url": "https://jetpackapps.io/jetscan-hr/"},
    {"phrase": "resume parsing tool monday",       "app": "JetScan HR", "url": "https://jetpackapps.io/jetscan-hr/"},
    {"phrase": "extract applicant info monday",    "app": "JetScan HR", "url": "https://jetpackapps.io/jetscan-hr/"},
    {"phrase": "hire with resume parser monday",   "app": "JetScan HR", "url": "https://jetpackapps.io/jetscan-hr/"},

    # ── Triggerly ─────────────────────────────────────────────────────────────
    # Page title: "Track inventory, orders, and assets on monday.com with Triggerly"
    {"phrase": "qr code monday",                   "app": "Triggerly", "url": "https://jetpackapps.io/qr-tracking-monday-triggerly/"},
    {"phrase": "barcode scan monday",              "app": "Triggerly", "url": "https://jetpackapps.io/qr-tracking-monday-triggerly/"},
    {"phrase": "scan to update monday",            "app": "Triggerly", "url": "https://jetpackapps.io/qr-tracking-monday-triggerly/"},
    {"phrase": "qr trigger monday",                "app": "Triggerly", "url": "https://jetpackapps.io/qr-tracking-monday-triggerly/"},
    {"phrase": "barcode monday.com",               "app": "Triggerly", "url": "https://jetpackapps.io/qr-tracking-monday-triggerly/"},
    {"phrase": "inventory scan monday",            "app": "Triggerly", "url": "https://jetpackapps.io/qr-tracking-monday-triggerly/"},
    {"phrase": "inventory tracking monday",        "app": "Triggerly", "url": "https://jetpackapps.io/qr-tracking-monday-triggerly/"},
    {"phrase": "asset tracking monday",            "app": "Triggerly", "url": "https://jetpackapps.io/qr-tracking-monday-triggerly/"},
    {"phrase": "track assets monday.com",          "app": "Triggerly", "url": "https://jetpackapps.io/qr-tracking-monday-triggerly/"},
    {"phrase": "scan item create monday",          "app": "Triggerly", "url": "https://jetpackapps.io/qr-tracking-monday-triggerly/"},

    # ── TrackMy ───────────────────────────────────────────────────────────────
    # Page title: "1500+ Global Package Courier tracking on monday.com - TrackMy"
    {"phrase": "track shipping monday",            "app": "TrackMy", "url": "https://jetpackapps.io/trackmy-package-tracking-on-monday-com/"},
    {"phrase": "package tracking monday",          "app": "TrackMy", "url": "https://jetpackapps.io/trackmy-package-tracking-on-monday-com/"},
    {"phrase": "delivery tracking monday",         "app": "TrackMy", "url": "https://jetpackapps.io/trackmy-package-tracking-on-monday-com/"},
    {"phrase": "shipment tracking monday",         "app": "TrackMy", "url": "https://jetpackapps.io/trackmy-package-tracking-on-monday-com/"},
    {"phrase": "order tracking monday",            "app": "TrackMy", "url": "https://jetpackapps.io/trackmy-package-tracking-on-monday-com/"},
    {"phrase": "fedex monday integration",         "app": "TrackMy", "url": "https://jetpackapps.io/trackmy-package-tracking-on-monday-com/"},
    {"phrase": "ups monday.com",                   "app": "TrackMy", "url": "https://jetpackapps.io/trackmy-package-tracking-on-monday-com/"},
    {"phrase": "courier tracking monday",          "app": "TrackMy", "url": "https://jetpackapps.io/trackmy-package-tracking-on-monday-com/"},
    {"phrase": "shipping status monday",           "app": "TrackMy", "url": "https://jetpackapps.io/trackmy-package-tracking-on-monday-com/"},
    {"phrase": "parcel tracking monday",           "app": "TrackMy", "url": "https://jetpackapps.io/trackmy-package-tracking-on-monday-com/"},

    # ── JobFlows ──────────────────────────────────────────────────────────────
    # Page title: "Jobflows - The all in one recruiting software for monday.com"
    {"phrase": "hiring pipeline monday",           "app": "JobFlows", "url": "https://jetpackapps.io/jobflows-recruiting-software-for-mondaycom/"},
    {"phrase": "ats monday.com",                   "app": "JobFlows", "url": "https://jetpackapps.io/jobflows-recruiting-software-for-mondaycom/"},
    {"phrase": "candidate tracking monday",        "app": "JobFlows", "url": "https://jetpackapps.io/jobflows-recruiting-software-for-mondaycom/"},
    {"phrase": "recruitment pipeline monday",      "app": "JobFlows", "url": "https://jetpackapps.io/jobflows-recruiting-software-for-mondaycom/"},
    {"phrase": "job application monday",           "app": "JobFlows", "url": "https://jetpackapps.io/jobflows-recruiting-software-for-mondaycom/"},
    {"phrase": "interview scheduling monday",      "app": "JobFlows", "url": "https://jetpackapps.io/jobflows-recruiting-software-for-mondaycom/"},
    {"phrase": "hiring workflow monday",           "app": "JobFlows", "url": "https://jetpackapps.io/jobflows-recruiting-software-for-mondaycom/"},
    {"phrase": "recruiting software monday",       "app": "JobFlows", "url": "https://jetpackapps.io/jobflows-recruiting-software-for-mondaycom/"},
    {"phrase": "manage hiring stages monday",      "app": "JobFlows", "url": "https://jetpackapps.io/jobflows-recruiting-software-for-mondaycom/"},
    {"phrase": "candidate pipeline monday",        "app": "JobFlows", "url": "https://jetpackapps.io/jobflows-recruiting-software-for-mondaycom/"},

    # ── Duplicates Smart Column ───────────────────────────────────────────────
    # Page title: "Duplicates Smart Column - Identify duplicate data on your board"
    {"phrase": "find duplicates monday",           "app": "Duplicates Smart Column", "url": "https://jetpackapps.io/duplicates-smart-column/"},
    {"phrase": "merge duplicate items monday",     "app": "Duplicates Smart Column", "url": "https://jetpackapps.io/duplicates-smart-column/"},
    {"phrase": "remove duplicates monday",         "app": "Duplicates Smart Column", "url": "https://jetpackapps.io/duplicates-smart-column/"},
    {"phrase": "duplicate records monday",         "app": "Duplicates Smart Column", "url": "https://jetpackapps.io/duplicates-smart-column/"},
    {"phrase": "deduplication monday",             "app": "Duplicates Smart Column", "url": "https://jetpackapps.io/duplicates-smart-column/"},
    {"phrase": "clean duplicates monday",          "app": "Duplicates Smart Column", "url": "https://jetpackapps.io/duplicates-smart-column/"},
    {"phrase": "identify duplicate data monday",   "app": "Duplicates Smart Column", "url": "https://jetpackapps.io/duplicates-smart-column/"},
    {"phrase": "clean board data monday",          "app": "Duplicates Smart Column", "url": "https://jetpackapps.io/duplicates-smart-column/"},
    {"phrase": "duplicate items monday board",     "app": "Duplicates Smart Column", "url": "https://jetpackapps.io/duplicates-smart-column/"},

    # ── Currency Converter Smart Column ──────────────────────────────────────
    # Page title: "Currency Converter Smart Column - Run your multi-currency workflows easily"
    {"phrase": "currency conversion monday",       "app": "Currency Converter Smart Column", "url": "https://jetpackapps.io/currency-converter-smart-column/"},
    {"phrase": "multi-currency monday",            "app": "Currency Converter Smart Column", "url": "https://jetpackapps.io/currency-converter-smart-column/"},
    {"phrase": "currency column monday",           "app": "Currency Converter Smart Column", "url": "https://jetpackapps.io/currency-converter-smart-column/"},
    {"phrase": "convert currency monday",          "app": "Currency Converter Smart Column", "url": "https://jetpackapps.io/currency-converter-smart-column/"},
    {"phrase": "exchange rate monday",             "app": "Currency Converter Smart Column", "url": "https://jetpackapps.io/currency-converter-smart-column/"},
    {"phrase": "foreign currency monday board",    "app": "Currency Converter Smart Column", "url": "https://jetpackapps.io/currency-converter-smart-column/"},
    {"phrase": "currency workflow monday",         "app": "Currency Converter Smart Column", "url": "https://jetpackapps.io/currency-converter-smart-column/"},

    # ── unFormula Smart Column ────────────────────────────────────────────────
    # Page title: "unFormula Smart Column - Copy your formula values to a standard number column"
    {"phrase": "copy formula values monday",       "app": "unFormula Smart Column", "url": "https://jetpackapps.io/unformula-smart-column/"},
    {"phrase": "formula to number column monday",  "app": "unFormula Smart Column", "url": "https://jetpackapps.io/unformula-smart-column/"},
    {"phrase": "unformula monday",                 "app": "unFormula Smart Column", "url": "https://jetpackapps.io/unformula-smart-column/"},
    {"phrase": "convert formula column monday",    "app": "unFormula Smart Column", "url": "https://jetpackapps.io/unformula-smart-column/"},
    {"phrase": "formula result monday board",      "app": "unFormula Smart Column", "url": "https://jetpackapps.io/unformula-smart-column/"},
    {"phrase": "extract formula value monday",     "app": "unFormula Smart Column", "url": "https://jetpackapps.io/unformula-smart-column/"},

    # ── Smart Embed View ──────────────────────────────────────────────────────
    # Page title: "Smart Embed View" — embed external content inside monday.com views
    {"phrase": "embed view monday",                "app": "Smart Embed View", "url": "https://jetpackapps.io/smart-embed-view/"},
    {"phrase": "embed website monday",             "app": "Smart Embed View", "url": "https://jetpackapps.io/smart-embed-view/"},
    {"phrase": "iframe monday board",              "app": "Smart Embed View", "url": "https://jetpackapps.io/smart-embed-view/"},
    {"phrase": "embed external content monday",    "app": "Smart Embed View", "url": "https://jetpackapps.io/smart-embed-view/"},
    {"phrase": "embed url monday.com",             "app": "Smart Embed View", "url": "https://jetpackapps.io/smart-embed-view/"},
    {"phrase": "embed dashboard monday",           "app": "Smart Embed View", "url": "https://jetpackapps.io/smart-embed-view/"},
]

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
    "Duplicates Smart Column": [
        "duplicate item", "find duplicate", "remove duplicate", "merge duplicate",
        "duplicate record", "deduplicat", "duplicate board",
    ],
    "Currency Converter Smart Column": [
        "currency", "multi-currency", "exchange rate", "foreign currency", "convert currency",
    ],
    "unFormula Smart Column": [
        "formula value", "unformula", "formula to number", "convert formula",
    ],
    "Smart Embed View": [
        "embed view", "embed website", "iframe monday", "embed external", "embed url",
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

**Duplicates Smart Column** — Identifies and cleans duplicate items on monday.com boards using configurable matching rules. Best for: data quality cleanup, CRM dedup, board hygiene.

**Currency Converter Smart Column** — Converts currencies inside a monday.com column automatically. Best for: multi-currency workflows, international pricing, finance teams handling multiple currencies.

**unFormula Smart Column** — Copies formula column results into a standard number column. Best for: using formula outputs in automations, exporting calculated values, avoiding recalculation issues.

**Smart Embed View** — Embeds external websites and content directly inside monday.com board views. Best for: accessing external dashboards, tools, or documents without leaving monday.com.
"""
