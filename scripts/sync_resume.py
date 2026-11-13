#!/usr/bin/env python3
"""
sync_resume.py
Automated synchronization script that:
1. Downloads the latest resume PDF from Google Drive.
2. Checks SHA-256 hash against .resume_hash to detect actual changes.
3. If changed (or --force), sends the resume PDF to Google's Gemini API
   together with the current portfolio.json.
4. Generates updated portfolio.json and syncs projects/index.md.
5. Updates .resume_hash so future runs skip when unchanged.
"""

import os
import sys
import json
import base64
import hashlib
import argparse
from datetime import datetime
import urllib.request
import urllib.error

DEFAULT_DRIVE_FILE_ID = "1zodZ1AqMNmWbzGSzmJerYLQGAHMEUwTa"
HASH_FILE = ".resume_hash"
PORTFOLIO_FILE = "portfolio.json"
PROJECTS_FILE = os.path.join("projects", "index.md")

GEMINI_MODELS = [
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-1.5-flash"
]

def compute_sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def download_google_drive_pdf(file_id: str) -> bytes:
    """Download public PDF from Google Drive using direct export URLs."""
    urls = [
        f"https://drive.usercontent.google.com/download?id={file_id}&export=download&authuser=0",
        f"https://drive.google.com/uc?export=download&id={file_id}"
    ]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    last_err = None
    for url in urls:
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=30) as resp:
                content = resp.read()
                # Validate it's actually a PDF file
                if content.startswith(b"%PDF"):
                    return content
                # Handle possible Google Drive redirect HTML or confirmation page
                if b"confirm=" in content:
                    import re
                    match = re.search(r'confirm=([a-zA-Z0-9_\-]+)', content.decode('utf-8', errors='ignore'))
                    if match:
                        confirm_token = match.group(1)
                        confirm_url = f"https://drive.google.com/uc?export=download&id={file_id}&confirm={confirm_token}"
                        req_conf = urllib.request.Request(confirm_url, headers=headers)
                        with urllib.request.urlopen(req_conf, timeout=30) as resp_conf:
                            conf_content = resp_conf.read()
                            if conf_content.startswith(b"%PDF"):
                                return conf_content
        except Exception as e:
            last_err = e
            continue
            
    raise RuntimeError(f"Could not download valid PDF from Google Drive for file ID {file_id}. Last error: {last_err}")

def call_gemini_with_pdf(api_key: str, pdf_bytes: bytes, current_portfolio: dict) -> dict:
    """Send resume PDF directly to Gemini API alongside current portfolio.json."""
    pdf_b64 = base64.b64encode(pdf_bytes).decode("utf-8")
    current_json_str = json.dumps(current_portfolio, indent=2)
    today_str = datetime.now().strftime("%Y-%m-%d")

    prompt = f"""
You are an expert technical portfolio updater.
You are given:
1. The user's latest resume as an attached PDF document.
2. The user's current 'portfolio.json' file content.

Today's date is: {today_str}

YOUR TASK:
Carefully analyze the resume PDF and update 'portfolio.json' with high precision:
1. 'meta':
   - Set 'last_updated' to '{today_str}'.
   - Increment or keep 'portfolio_version' and 'resume_version'.
2. 'profile':
   - Update 'summary', 'title', 'tagline', 'location', 'education_short' based on the resume.
3. 'contact' & 'profiles':
   - Update email, phone, location, github, linkedin, leetcode URLs if any have changed.
4. 'resume':
   - Update 'summary' to concisely reflect the candidate's latest focus.
   - Keep 'pdf_url' unchanged.
5. 'education':
   - Update institutions, degrees, grades (CGPA/percentage), dates.
6. 'experience':
   - Update companies, roles, locations, dates, descriptions, and bullet highlights with exact technical details, metrics, and tech stacks from the resume.
7. 'projects':
   - Update existing projects with latest metrics, users, architecture points, and tech stacks.
   - Add any newly featured projects from the resume.
   - Retain existing self-hosted projects (like 'thewittyswan Terminal') even if omitted from a 1-page resume.
8. 'skills' & 'skills_by_category':
   - Update both the flat array and categorized dictionary (languages, backend_and_apis, databases, authentication_and_security, ai_and_integrations, cs_fundamentals, devops_and_cloud) to include all technologies listed on the resume.
9. 'timeline' & 'achievements':
   - Add any new honors, contest ranks, certifications, hackathons, or milestones from the resume.

IMPORTANT FORMATTING RULES:
- Return ONLY a valid JSON object matching the portfolio.json schema.
- Do NOT wrap in markdown fences (e.g. ```json). Just the raw JSON.
- Maintain valid JSON syntax.

CURRENT PORTFOLIO.JSON:
{current_json_str}
"""

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "inline_data": {
                            "mime_type": "application/pdf",
                            "data": pdf_b64
                        }
                    },
                    {
                        "text": prompt
                    }
                ]
            }
        ],
        "generationConfig": {
            "response_mime_type": "application/json",
            "temperature": 0.1
        }
    }

    req_data = json.dumps(payload).encode("utf-8")
    
    last_err = None
    for model in GEMINI_MODELS:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        try:
            req = urllib.request.Request(
                url,
                data=req_data,
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=90) as resp:
                resp_json = json.loads(resp.read().decode("utf-8"))
                candidate = resp_json["candidates"][0]["content"]["parts"][0]["text"]
                cleaned_text = candidate.strip()
                if cleaned_text.startswith("```json"):
                    cleaned_text = cleaned_text[7:]
                if cleaned_text.startswith("```"):
                    cleaned_text = cleaned_text[3:]
                if cleaned_text.endswith("```"):
                    cleaned_text = cleaned_text[:-3]
                parsed = json.loads(cleaned_text.strip())
                return parsed
        except Exception as e:
            last_err = e
            continue

    raise RuntimeError(f"Gemini API request failed across all models. Last error: {last_err}")

def render_projects_markdown(portfolio: dict) -> str:
    """Deterministically render projects/index.md from portfolio.json data."""
    summary = portfolio.get("profile", {}).get("summary", "")
    
    lines = [
        "---",
        "layout: default",
        "title: Projects",
        "permalink: /projects/",
        "---",
        "",
        "# projects & engineering",
        "",
        summary if summary else "Backend Software Engineer focused on Go, Node.js, and Python. Founder of [GolangForAll](https://golangforall.in).",
        "",
        "[featured systems](#featured-systems) · [work experience](#work-experience) · [technical skills](#technical-skills) · [achievements](#achievements)",
        "",
        "---",
        "",
        "<h2 id=\"featured-systems\">featured systems</h2>",
        ""
    ]

    for p in portfolio.get("projects", []):
        name = p.get("name", "")
        link = p.get("link", "")
        desc = p.get("description", "")
        highlights = p.get("highlights", [])
        stack = p.get("stack", [])

        if link:
            lines.append(f"### [{name}]({link})")
        else:
            lines.append(f"### {name}")
        lines.append("")
        
        if desc:
            lines.append(desc)
            lines.append("")

        for h in highlights:
            lines.append(f"- {h}")

        impact = p.get("impact", "")
        if impact:
            lines.append(f"- **impact:** {impact}")

        if stack:
            lines.append(f"- **built with:** {' · '.join(stack)}")

        lines.append("")
        lines.append("---")
        lines.append("")

    lines.append("<h2 id=\"work-experience\">work experience</h2>")
    lines.append("")

    for exp in portfolio.get("experience", []):
        role = exp.get("role", "")
        company = exp.get("company", "")
        location = exp.get("location", "")
        duration = exp.get("duration", "")
        highlights = exp.get("highlights", [])
        stack = exp.get("stack", [])

        loc_str = f" · {location}" if location else ""
        lines.append(f"### {role} — {company}")
        lines.append(f"*{duration}{loc_str}*")
        lines.append("")

        for h in highlights:
            lines.append(f"- {h}")

        if stack:
            lines.append(f"- **Tech:** {' · '.join(stack)}")

        lines.append("")
        lines.append("---")
        lines.append("")

    lines.append("<h2 id=\"technical-skills\">technical skills</h2>")
    lines.append("")

    cat_map = {
        "languages": "Languages",
        "backend_and_apis": "Backend & APIs",
        "databases": "Databases",
        "authentication_and_security": "Authentication & Security",
        "ai_and_integrations": "AI & Integrations",
        "cs_fundamentals": "CS Fundamentals",
        "devops_and_cloud": "DevOps & Cloud"
    }

    skills_by_cat = portfolio.get("skills_by_category", {})
    if skills_by_cat:
        for cat_key, cat_label in cat_map.items():
            if cat_key in skills_by_cat and skills_by_cat[cat_key]:
                lines.append(f"- **{cat_label}:** {' · '.join(skills_by_cat[cat_key])}")
    else:
        all_skills = portfolio.get("skills", [])
        if all_skills:
            lines.append(f"- **Skills:** {' · '.join(all_skills)}")

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("<h2 id=\"achievements\">achievements & honors</h2>")
    lines.append("")

    for ach in portfolio.get("achievements", []):
        title = ach.get("title", "")
        desc = ach.get("description", "")
        year = ach.get("year", "")
        year_str = f" ({year})" if year and not year in desc else ""
        lines.append(f"- **{title}:** {desc}{year_str}")

    lines.append("")
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="Sync portfolio with latest resume from Google Drive.")
    parser.add_argument("--force", action="store_true", help="Force sync even if resume hash is unchanged.")
    parser.add_argument("--render-only", action="store_true", help="Only re-render projects/index.md from existing portfolio.json.")
    parser.add_argument("--file-id", default=os.getenv("DRIVE_FILE_ID", DEFAULT_DRIVE_FILE_ID), help="Google Drive file ID.")
    args = parser.parse_args()

    # Mode: Render only
    if args.render_only:
        print("Re-rendering projects/index.md from existing portfolio.json...")
        with open(PORTFOLIO_FILE, "r", encoding="utf-8") as f:
            portfolio = json.load(f)
        rendered_md = render_projects_markdown(portfolio)
        with open(PROJECTS_FILE, "w", encoding="utf-8") as f:
            f.write(rendered_md)
        print("Render complete!")
        return

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY environment variable is required.", file=sys.stderr)
        sys.exit(1)

    print(f"Checking Google Drive for resume file ID: {args.file_id}...")
    pdf_bytes = download_google_drive_pdf(args.file_id)
    pdf_hash = compute_sha256(pdf_bytes)
    print(f"Downloaded PDF size: {len(pdf_bytes)} bytes | SHA256: {pdf_hash[:16]}...")

    prev_hash = ""
    if os.path.exists(HASH_FILE):
        with open(HASH_FILE, "r", encoding="utf-8") as f:
            prev_hash = f.read().strip()

    if not args.force and prev_hash and prev_hash == pdf_hash:
        print("No changes detected in resume PDF since last sync. Portfolio is up to date!")
        return

    print("Resume update detected (or --force). Updating portfolio using Gemini...")
    with open(PORTFOLIO_FILE, "r", encoding="utf-8") as f:
        current_portfolio = json.load(f)

    updated_portfolio = call_gemini_with_pdf(api_key, pdf_bytes, current_portfolio)
    
    # Save updated portfolio.json
    with open(PORTFOLIO_FILE, "w", encoding="utf-8") as f:
        json.dump(updated_portfolio, f, indent=2, ensure_ascii=False)
    print(f"Updated {PORTFOLIO_FILE}")

    # Re-render projects/index.md
    updated_md = render_projects_markdown(updated_portfolio)
    with open(PROJECTS_FILE, "w", encoding="utf-8") as f:
        f.write(updated_md)
    print(f"Updated {PROJECTS_FILE}")

    # Record new hash
    with open(HASH_FILE, "w", encoding="utf-8") as f:
        f.write(pdf_hash)
    print(f"Saved new hash to {HASH_FILE}")

    print("Sync successfully completed!")

if __name__ == "__main__":
    main()
