#!/usr/bin/env python3
"""
sync_resume.py
Automated synchronization script that:
1. Downloads the latest resume PDF from Google Drive.
2. Checks SHA-256 hash against .resume_hash to detect actual changes.
3. If changed (or --force), extracts resume text and updates the portfolio
   with Groq, falling back to Gemini if Groq fails.
4. Generates updated portfolio.json and syncs projects/index.md.
5. Updates .resume_hash so future runs skip when unchanged.
"""

import io
import os
import sys
import json
import hashlib
import argparse
import time
from datetime import datetime
import urllib.request
import urllib.error
from dotenv import load_dotenv
from pypdf import PdfReader

load_dotenv()

DEFAULT_DRIVE_FILE_ID = "1zodZ1AqMNmWbzGSzmJerYLQGAHMEUwTa"
HASH_FILE = ".resume_hash"
PORTFOLIO_FILE = "portfolio.json"
PROJECTS_FILE = os.path.join("projects", "index.md")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")
GEMINI_MODELS = ["gemini-flash-lite-latest", "gemini-flash-latest"]
USER_AGENT = "thewittyswan-resume-sync/1.0"

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

def extract_resume_text(pdf_bytes: bytes) -> str:
    """Extract selectable text from the downloaded resume PDF."""
    reader = PdfReader(io.BytesIO(pdf_bytes))
    text = "\n".join(page.extract_text() or "" for page in reader.pages).strip()
    if not text:
        raise RuntimeError("Resume PDF contains no extractable text; scanned PDFs require OCR.")
    return text


def build_portfolio_prompt(resume_text: str, current_portfolio: dict) -> str:
    current_json_str = json.dumps(current_portfolio, indent=2)
    today_str = datetime.now().strftime("%Y-%m-%d")

    prompt = f"""
You are an expert technical portfolio updater.
You are given:
1. The user's latest resume as extracted text.
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

RESUME TEXT:
{resume_text}

CURRENT PORTFOLIO.JSON:
{current_json_str}
"""
    return prompt


def call_groq_with_resume(api_key: str, resume_text: str, current_portfolio: dict) -> dict:
    """Send extracted resume text and portfolio JSON to Groq's chat API."""
    prompt = build_portfolio_prompt(resume_text, current_portfolio)
    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": "Update the portfolio JSON using only the supplied resume and current portfolio."},
            {"role": "user", "content": prompt}
        ],
        "response_format": {"type": "json_object"},
        "temperature": 0.1,
        "max_completion_tokens": 16000
    }

    req_data = json.dumps(payload).encode("utf-8")
    last_err = None
    for attempt in range(3):
        try:
            req = urllib.request.Request(
                GROQ_API_URL,
                data=req_data,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                    "User-Agent": USER_AGENT
                }
            )
            with urllib.request.urlopen(req, timeout=60) as resp:
                resp_json = json.loads(resp.read().decode("utf-8"))
            content = resp_json["choices"][0]["message"]["content"]
            if not content:
                raise RuntimeError("Groq response did not contain any textual output.")
            result = json.loads(content)
            if not isinstance(result, dict):
                raise RuntimeError("Groq response was valid JSON but not a JSON object.")
            return result
        except urllib.error.HTTPError as exc:
            response_body = exc.read().decode("utf-8", errors="replace")
            last_err = f"HTTP {exc.code}: {response_body[:500]}"
            if exc.code not in (429, 500, 502, 503, 504):
                break
            if attempt < 2:
                time.sleep(2 ** attempt)
        except (urllib.error.URLError, TimeoutError) as exc:
            last_err = str(exc)
            if attempt < 2:
                time.sleep(2 ** attempt)
        except Exception as exc:
            last_err = exc
            break

    raise RuntimeError(f"Groq API request failed after retries. Last error: {last_err}")


def call_gemini_with_resume(api_key: str, resume_text: str, current_portfolio: dict) -> dict:
    """Send extracted resume text and portfolio JSON to Gemini as a fallback."""
    prompt = build_portfolio_prompt(resume_text, current_portfolio)
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseMimeType": "application/json",
            "temperature": 0.1
        }
    }
    req_data = json.dumps(payload).encode("utf-8")
    last_err = None

    for model in GEMINI_MODELS:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        for attempt in range(2):
            try:
                req = urllib.request.Request(
                    url,
                    data=req_data,
                    headers={
                        "Content-Type": "application/json",
                        "User-Agent": USER_AGENT
                    }
                )
                with urllib.request.urlopen(req, timeout=60) as resp:
                    resp_json = json.loads(resp.read().decode("utf-8"))
                parts = resp_json["candidates"][0]["content"]["parts"]
                content = "".join(part.get("text", "") for part in parts).strip()
                if not content:
                    raise RuntimeError("Gemini response did not contain any textual output.")
                result = json.loads(content)
                if not isinstance(result, dict):
                    raise RuntimeError("Gemini response was valid JSON but not a JSON object.")
                return result
            except urllib.error.HTTPError as exc:
                response_body = exc.read().decode("utf-8", errors="replace")
                last_err = f"HTTP {exc.code}: {response_body[:500]}"
                if exc.code not in (429, 500, 502, 503, 504):
                    break
                if attempt < 1:
                    time.sleep(2 ** attempt)
            except (urllib.error.URLError, TimeoutError) as exc:
                last_err = str(exc)
                if attempt < 1:
                    time.sleep(2 ** attempt)
            except Exception as exc:
                last_err = exc
                break

    raise RuntimeError(f"Gemini API request failed after retries. Last error: {last_err}")


def update_portfolio_with_fallback(
    pdf_bytes: bytes,
    current_portfolio: dict,
    groq_api_key: str | None,
    gemini_api_key: str | None
) -> dict:
    """Try Groq first, then Gemini when configured and Groq fails."""
    if not groq_api_key and not gemini_api_key:
        raise RuntimeError("Set GROQ_API_KEY, GEMINI_API_KEY, or both to update the portfolio.")

    resume_text = extract_resume_text(pdf_bytes)
    errors = []

    if groq_api_key:
        try:
            return call_groq_with_resume(groq_api_key, resume_text, current_portfolio)
        except RuntimeError as exc:
            errors.append(f"Groq: {exc}")
            if gemini_api_key:
                print(f"Groq failed ({exc}); trying Gemini fallback.", file=sys.stderr)

    if gemini_api_key:
        try:
            if not groq_api_key:
                print("GROQ_API_KEY is not set; using Gemini.", file=sys.stderr)
            return call_gemini_with_resume(gemini_api_key, resume_text, current_portfolio)
        except RuntimeError as exc:
            errors.append(f"Gemini: {exc}")

    raise RuntimeError("All configured AI providers failed. " + " | ".join(errors))


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

    groq_api_key = os.getenv("GROQ_API_KEY")
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not groq_api_key and not gemini_api_key:
        print("ERROR: Set GROQ_API_KEY, GEMINI_API_KEY, or both.", file=sys.stderr)
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

    providers = []
    if groq_api_key:
        providers.append(f"Groq ({GROQ_MODEL})")
    if gemini_api_key:
        providers.append("Gemini fallback")
    print(f"Resume update detected (or --force). Updating portfolio using {' then '.join(providers)}...")
    with open(PORTFOLIO_FILE, "r", encoding="utf-8") as f:
        current_portfolio = json.load(f)

    updated_portfolio = update_portfolio_with_fallback(
        pdf_bytes,
        current_portfolio,
        groq_api_key,
        gemini_api_key
    )
    
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
