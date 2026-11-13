# thewittyswan

The witty swan carries knowledge forward — a personal site combining
network security writing, literature, and a bit of playful engineering.
Live at [thewittyswan.space](https://thewittyswan.space).

Built by **Dhawal**.

## What this repository demonstrates

This is a deliberately low-complexity publishing platform with a clear
content pipeline: write Markdown, manage it through Decap CMS, generate a
static site with Jekyll, and deploy immutable output through Vercel. The
portfolio is complemented by the independent Go terminal repository, which
consumes this site's public `posts.json` and `portfolio.json` feeds.

## Why this stack

I'm a backend person at heart. Databases, APIs, servers — that's where
my head naturally goes. Frontend work, especially the modern
React/Next.js/Tailwind kind, has never been where I want to spend my
time — not because I dislike design, but because designing *in code*
feels heavy to me. I actually enjoy design a lot, just visually — Canva,
Figma, moving things around and seeing them change instantly. Writing
`className="flex items-center justify-between px-4"` to get the same
result has never felt like the same activity to me.

So this site is built the way it is on purpose: Jekyll, plain
Markdown, one CSS file, no build tooling to fight with, no component
tree to maintain. I write in Markdown the way I'd write a note, and the
design work — once done — stays done. No repeated frontend decisions
per post, no framework churn to keep up with. Boring, on purpose, and
genuinely comfortable to maintain for someone who'd rather be thinking
about the backend of things.

## Stack

- **Jekyll** — static site generator, Markdown-based, no server or
  database at runtime
- **Decap CMS** — browser-based admin panel at `/admin`, writes directly
  to this GitHub repo
- **Cloudinary** — image hosting for blog post images
- **Vercel** — hosting, auto-deploys on push to `main`
- **daresaydigital/decap-cms-oauth** — separate small Vercel project
  handling GitHub OAuth for the admin panel

This is one of two repos. The other, `thewittyswan-terminal`, is a
Go-based interactive terminal at `/terminal`, self-hosted separately on a
GCP e2-micro VM. The two are independent — this site works standalone even if
the terminal is down.

## Content architecture

```text
Author
  │
  ├── Markdown posts/pages ──► GitHub repository
  │                              │
  │                              ├── Jekyll build
  │                              ├── posts.json
  │                              └── portfolio.json
  │
  └── Decap CMS / GitHub OAuth
             │
             └── Cloudinary media uploads

Vercel
  └── Jekyll site at thewittyswan.space

GCP e2-micro VM
  └── Caddy → Go terminal at thewittyswan.space/terminal
```

The generated JSON feeds are an explicit integration boundary rather than a
shared database. This keeps the portfolio deployable as a static site while
allowing the terminal to provide a dynamic reading and profile experience.

## Local setup

```powershell
git clone https://github.com/DhawalShankar/thewittyswan.git
cd thewittyswan
bundle install
bundle exec jekyll serve
```

Visit `http://127.0.0.1:4000`.

For the admin panel locally, also run (in a separate terminal):
```powershell
npx decap-server
```
Then visit `http://127.0.0.1:4000/admin/` — this uses Decap's local
backend mode, no OAuth needed for local testing.

## Structure

- `_posts/netsec/`, `_posts/literature/` — blog posts, edited via `/admin`
  or directly as Markdown
- `home/`, `about/` (→ `/now/`), `projects/`, `glossary/`, `recommends/`
  — structural pages, editable via `/admin`
- `index.md` — the landing fork ("I'm a dev" / "I'm a homo sapien"),
  intentionally **not** editable via the CMS
- `posts.json` — auto-generated feed of all posts, consumed by the
  terminal repo for its `ls`/`cat`/`grep` commands
- `assets/css/main.scss` — all site styling, single file
- `admin/config.yml` — Decap CMS configuration

## Deployment

Pushing to `main` auto-deploys the Jekyll site via Vercel. The GCP VM is
managed separately through the completed SSH/bash deployment workflow, with
Caddy handling HTTPS and path routing for the terminal.

The `/admin/` workflow uses Decap CMS with GitHub-backed content updates.
`admin/config.yml` defines the editable collections, media library, OAuth
backend, and local development mode. The terminal service does not access the
GitHub repository directly; it reads only the public generated feeds.

## Repository map

| Path | Responsibility |
|---|---|
| `_posts/` | Network-security and literature content |
| `home/`, `about/`, `projects/`, `glossary/`, `recommends/` | Structured site pages |
| `admin/config.yml` | Decap CMS collections and media configuration |
| `posts.json` | Public feed consumed by the terminal |
| `portfolio.json` | Structured profile, projects, skills, and resume metadata |
| `scripts/sync_resume.py` | Automated sync script parsing Drive resume PDF via Gemini API |
| `.github/workflows/` | Monthly automated resume sync GitHub Action |
| `assets/css/main.scss` | Site-wide styling |

## Security and operations

- GitHub OAuth is handled by the dedicated Decap OAuth service.
- Cloudinary stores uploaded editorial media; credentials are not part of the
  static site output.
- The site has no runtime database or public server-side application process.
- The terminal is deployed separately, so a terminal outage does not take down
  the portfolio and blog.

## License

Personal project, all rights reserved.