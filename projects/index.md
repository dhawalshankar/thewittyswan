---
layout: default
title: Projects
permalink: /projects/
---

# projects & engineering

Backend Software Engineer focused on Go, Node.js and Python. My projects include distributed systems, microservices, real-time chat, payment flows and a Docker-isolated Go runner. I also founded GolangForAll to share Go learning resources and bring developers together.

[featured systems](#featured-systems) · [work experience](#work-experience) · [technical skills](#technical-skills) · [achievements](#achievements)

---

<h2 id="featured-systems">featured systems</h2>

### [GoLab - Sandboxed Go Code Execution Playground](https://golab.golangforall.in)

Browser-to-container code execution playground for GolangForAll. Isolated compilation and execution in separate Docker containers with no network, non-root users, resource limits, and cached builds.

- Launched GoLab for 60+ users in GolangForAll’s 80+ member WhatsApp community: Next.js/Monaco frontend, Go runner on AWS EC2.
- Isolated compilation and execution in separate Docker containers with no network, non-root users and resource limits.
- Used read-only container root filesystems and cached compiler builds; mounted the runtime workspace read-only.
- Created GolangForAll’s Docusaurus platform for 200+ users with Go APIs, Neon PostgreSQL and Cloudinary.
- **impact:** Created a live, publicly accessible sandboxed Go execution environment engineered for hostile workloads.
- **built with:** Next.js · Monaco · Go · Docker · AWS EC2 · Docusaurus · PostgreSQL · Cloudinary

---

### [VartaLang - Language Exchange and LMS](https://vartalang.in)

Language exchange and learning platform featuring real-time chat, reciprocal multilingual matching across 33 languages, LMS with Razorpay payment processing, and Sarvam AI Indic translation & TTS integrations.

- Engineered VartaLang microservices with Node.js/Express, MongoDB and Socket.IO for reciprocal matching and real-time chat; deployed at api.vartalang.in with GitHub Actions checks. Reached 60+ sign-ups and 500+ visitors.
- Launched learn.vartalang.in with freemium courses in 33 languages, instructor onboarding, sales reports and live Razorpay; implemented SSO between VartaLang and the LMS, with shared MongoDB user accounts and LMS data in Neon PostgreSQL.
- Added Sarvam Translate and Google Cloud translation APIs for Indic and foreign-language chat, plus Sarvam Bulbul TTS, read receipts, blocking, reporting and per-user soft deletion.
- Marked 7-day job listings as expired with node-cron; public queries also check the expiry date.
- Kept expired listings in the admin panel for manual paid extensions, then automated cleanup with MongoDB TTL.
- Selected for the Sarvam Startup Program; advanced to RideHack JIIT Round 2 for funding.
- **impact:** Combined language exchange, real-time messaging, reciprocal matching, and LMS course monetization into a production platform.
- **built with:** Next.js · Node.js · Express.js · Socket.IO · MongoDB · PostgreSQL · JWT · Sarvam AI · Google Cloud · Razorpay · Vercel · Render · GitHub Actions

---

### [Cosmo India Prakashan - E-Commerce and AI Inventory Platform](https://cosmoindiaprakashan.in)

AI-powered publishing and e-commerce platform for a family publishing house with polyglot persistence, cryptographic Razorpay payment verification, and staff-reviewed Gemini product catalog workflows.

- Deployed a live storefront on Vercel with serverless APIs and MongoDB orders; verified Razorpay payments with HMAC-SHA256 and served 400+ visits.
- Designed an Express admin API with JWT RBAC and polyglot persistence: PostgreSQL inventory and MongoDB orders; added staff-reviewed Gemini product entry.
- **impact:** Transformed a traditional publishing business into an active digital storefront with cryptographic payment verification and an AI-assisted operational layer.
- **built with:** React · Node.js · MongoDB · Supabase (PostgreSQL) · Razorpay · Gemini API · JWT · Nodemailer SMTP · Vercel · Render

---

### [thewittyswan Terminal](https://thewittyswan.space/terminal)

Self-hosted, browser-based developer terminal built with a Go backend and xterm.js frontend, running on a GCP e2-micro VM behind a Caddy reverse proxy under systemd. Includes a live network security lab, all guarded against SSRF via strict host/IP validation on every outbound check.

- **impact:** A personal corner of the internet where writing and engineering don't have to live in separate rooms.
- **built with:** Go · xterm.js · GCP Compute Engine · Caddy · systemd · GitHub Actions

---

### [GolangForAll](https://golangforall.in)

Community and learning platform for Go developers with authenticated technical writing, community updates, and interactive sandbox integration for 200+ users.

- **impact:** Connected learning, writing, and hands-on coding for a growing Go developer community.
- **built with:** Go · React · Docusaurus · PostgreSQL · Cloudinary · Docker · AWS · Caddy · systemd

---

### [Cape Comorin School Records](https://capecomorinschool.com)

Digitisation platform modernising school records. Multimodal Gemini OCR for 100+ handwritten records, RapidFuzz-ranked search for ~30s lookup, Firebase auth and RBAC for 10+ staff, and calendar-grounded AI notice generation with Groq Llama and WeasyPrint.

- **impact:** Converted decades of paper archives into an instantaneous, searchable digital workflow for school administrators.
- **built with:** Next.js · Flask · FastAPI · Gemini API · Groq (Llama API) · RapidFuzz · Neon PostgreSQL · Turso · Firebase · Cloudinary · WeasyPrint

---

### [Churn](https://pypi.org/project/churn-cli/)

CLI published on PyPI (churn-cli) for interview prep, automated documentation generation, and repo health scoring across local and GitHub repositories using Gemini, Groq, and OpenAI models. 144 downloads/month.

- **impact:** Brought LLM repository analysis into native command-line developer workflows.
- **built with:** Python · Gemini API · Groq API · OpenAI API · PyPI · CLI

---

### [AuralAce](https://auralace.vercel.app)

Audio signal processing platform implementing FFT equalisation, convolution reverb, waveform visualisation and interactive before-and-after playback.

- **impact:** Turned abstract audio-processing operations into an interactive experiment that can be heard rather than merely described.
- **built with:** Python · FastAPI · NumPy · SciPy · librosa · Next.js · Web Audio API

---

### ElectiveXchange

Two-way elective course matcher with priority-ranked preferences, real-time updates, and Firebase authentication. 300+ organic signups.

- **built with:** React · Tailwind CSS · Firebase Auth · Firestore · Vercel

---

<h2 id="work-experience">work experience</h2>

### IT Operations Support Intern — Cape Comorin Children School
*Jun 2026 – Jul 2026 · Kanpur (Hybrid)*

- Delivered a deployed Next.js demo with separately deployed Flask school and FastAPI Vritukul microservices; used Gemini to extract 100+ handwritten records and RapidFuzz-ranked search for about 30-second lookup.
- Implemented Firebase-verified auth and RBAC for student and register workflows; designed the admin system for 10+ staff accounts using Turso, Neon PostgreSQL, and Cloudinary.
- Created calendar-grounded, staff-reviewed AI notices with Groq’s Llama API and WeasyPrint PDFs; gated Cape Comorin frontend merges on GitHub Actions lint, TypeScript checks and production builds.
- **Tech:** Next.js · Flask · FastAPI · Gemini API · Groq (Llama API) · RapidFuzz · Firebase · Turso · Neon PostgreSQL · Cloudinary · WeasyPrint · GitHub Actions · TypeScript

---

### Backend Developer Intern — Codingo Forge
*Apr 2026 – Jun 2026 · Noida (Remote)*

- Dockerized backend services with a 3-engineer team, resolving environment and dependency-version mismatches; configured Clerk RBAC for employees, users, and super-admins in place of shared credentials.
- Implemented Node.js/Express.js REST APIs with MongoDB for a startup’s local-business digital-storefront workflows.
- **Tech:** Node.js · Express.js · MongoDB · Clerk Auth · RBAC · Docker · REST APIs

---

<h2 id="technical-skills">technical skills</h2>

- **Languages:** Python · Java · SQL · JavaScript · Go
- **Backend & APIs:** Node.js · Express.js · FastAPI · Flask · REST APIs · WebSocket · CRON Jobs · Microservices
- **Databases:** MongoDB · PostgreSQL · Turso (LibSQL) · Supabase · Neon
- **Authentication & Security:** JWT · OAuth 2.0 · Clerk · Firebase · HMAC-SHA256 · RBAC
- **AI & Integrations:** Gemini API (Multimodal) · Payment Gateway (Razorpay) · RapidFuzz · Cloudinary · Groq API · Sarvam AI · Nodemailer SMTP
- **CS Fundamentals:** Computer Networks · Operating Systems
- **DevOps & Cloud:** Docker · Git · Linux · Caddy · systemd · AWS (EC2) · GCP Compute Engine · Render · Shell Scripting · CI/CD · Vercel

---

<h2 id="achievements">achievements & honors</h2>

- **Google BigCode:** Ranked in the top 1,500 globally (2026).
- **HirePro HackVega 2.0:** Round 3 Finalist (2026).
- **Adobe Education Summit:** Selected among the top 300 of 19,000+ nationwide applicants for Adobe’s Education Summit at its Noida HQ, focused on Adobe Firefly and developer communities. (2026)
- **Churn (PyPI):** CLI for interview prep, doc generation, and repo health scoring; 144 downloads/month. (2026)
- **UAV Certification, CDAC Noida:** Certified UAV Pilot by C-DAC, Noida (2024). ArduPilot/Pixhawk flight control and DGCA drone rules.
- **LeetCode:** Peak contest rating of 1713 and earned the 50 Days Badge. (2026)
