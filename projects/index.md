---
layout: default
title: Projects
permalink: /projects/
---

# projects & engineering

Backend Software Engineer focused on **Go**, **Node.js**, and **Python**. My work spans distributed systems, microservices, sandboxed execution runtimes, real-time messaging, and cloud infrastructure. Founder of [GolangForAll](https://golangforall.in).

[featured systems](#featured-systems) · [work experience](#work-experience) · [technical skills](#technical-skills) · [achievements](#achievements)

---

<h2 id="featured-systems">featured systems</h2>

### [GoLab — Sandboxed Go Code Execution Playground](https://golab.golangforall.in)

What happens if a Go learning platform doesn't just show code, but lets anyone execute it safely in the browser? The challenge: **executing arbitrary user code without trusting the person submitting it.**

- Launched GoLab for **60+ users** in GolangForAll’s **80+ member** WhatsApp community: Next.js/Monaco frontend, Go runner on AWS EC2.
- Isolated compilation and execution in separate Docker containers with dropped Linux capabilities, disabled networking, non-root users, and strict per-request CPU, memory, and PID limits.
- Configured read-only container root filesystems and cached compiler builds to slash latency; mounted the runtime workspace strictly read-only.
- Created GolangForAll’s companion Docusaurus documentation and community platform for **200+ users** with Go APIs, Neon PostgreSQL, and Cloudinary.
- **impact:** Created a live, publicly accessible sandboxed Go execution environment engineered for hostile workloads.
- **built with:** Go · Docker · AWS EC2 · Caddy · systemd · Next.js · Monaco Editor · PostgreSQL · Cloudinary

---

### [VartaLang — Language Exchange & LMS](https://vartalang.in)

What if learning a language meant finding another person rather than opening another lesson? VartaLang connects reciprocal language partners and extends that into real-world career opportunities and learning courses.

- Engineered VartaLang microservices with Node.js/Express, MongoDB, and Socket.IO for reciprocal matching and real-time chat; deployed at `api.vartalang.in` with GitHub Actions checks. Reached **60+ sign-ups and 500+ visitors**.
- Launched `learn.vartalang.in` with freemium courses in **33 languages**, instructor onboarding, sales reports, and live Razorpay payment processing; implemented SSO between VartaLang and the LMS with shared MongoDB user accounts and LMS state in Neon PostgreSQL.
- Added Sarvam Translate and Google Cloud translation APIs for Indic and foreign-language chat, plus Sarvam Bulbul TTS, read receipts, blocking, reporting, and per-user soft deletion.
- Marked 7-day job listings as expired with node-cron; public queries check expiry dates, and expired listings are kept in the admin panel for manual paid extensions before automated cleanup with MongoDB TTL.
- Selected for the **Sarvam Startup Program**; advanced to **RideHack JIIT Round 2** for funding.
- **impact:** Combined language exchange, real-time messaging, reciprocal matching, and LMS course monetization into a production platform.
- **built with:** Next.js · Node.js · Express.js · Socket.IO · MongoDB · Neon PostgreSQL · JWT · Sarvam AI · Razorpay · Vercel · Render

---

### [Cosmo India Prakashan — E-Commerce & AI Inventory Platform](https://cosmoindiaprakashan.in)

Built for a family publishing house — bridging digital book retail with secure payment processing, polyglot persistence, and natural-language inventory management.

- Deployed a live storefront on Vercel with serverless APIs and MongoDB orders; verified Razorpay payments with HMAC-SHA256 signatures and served **400+ visits**.
- Designed an Express admin API with JWT RBAC and polyglot persistence: PostgreSQL for book inventory and MongoDB for customer orders.
- Integrated staff-reviewed Gemini product entry and conversational inventory querying for non-technical operations staff.
- Protected administrative operations with JWT and RBAC while designing AI prompt interactions to prevent prompt-injection attacks.
- **impact:** Transformed a traditional publishing business into an active digital storefront with cryptographic payment verification and an AI-assisted operational layer.
- **built with:** React · TypeScript · Node.js · Express.js · MongoDB · Supabase (PostgreSQL) · Razorpay · Gemini API · JWT · Nodemailer SMTP · Vercel · Render

---

### [thewittyswan — Personal Writing & Interactive Go Terminal](https://thewittyswan.space)

A personal publishing space and engineering lab combining network security writing, literature, and self-hosted systems.

- Built a Jekyll publishing engine for essays, reflections, and technical notes deployed immutably to Vercel.
- Built an independent interactive terminal (`/terminal`) powered by a Go backend and xterm.js frontend, self-hosted on a GCP e2-micro VM behind Caddy with systemd process supervision.
- Added a live network security lab (TLS inspection, DNS diagnostics, HTTP security header auditing, port reachability checks, and OSV.dev dependency vulnerability lookups), strictly protected against SSRF via host/IP validation on every outbound check.
- Publishes public `posts.json` and `portfolio.json` feeds consumed as explicit API boundaries by the terminal.
- **impact:** A personal corner of the internet where writing and engineering don't have to live in separate rooms.
- **built with:** Go · xterm.js · Jekyll · GCP Compute Engine · Caddy · systemd · OSV.dev API · Linux

---

### [GolangForAll — Go Developer Community & Learning Platform](https://golangforall.in)

A grassroots developer community and learning hub designed to make Go approachable for developers of all levels.

- Built the platform from the ground up using Docusaurus, React, a custom Go backend, PostgreSQL, and Cloudinary.
- Created an authenticated publishing workflow for technical writing, build logs, meetups, announcements, and community updates for **200+ users**.
- Built a lightweight content-management console with protected administrative operations and cloud-backed media uploads.
- Integrated **GoLab** directly into the ecosystem, allowing developers to move from reading documentation to executing code instantly.
- **impact:** Connected learning, writing, and hands-on coding for a growing Go developer community.
- **built with:** Go · React · Docusaurus · Neon PostgreSQL · Cloudinary · Docker · AWS · Caddy · systemd

---

### [Cape Comorin School Records — Digitisation & Multimodal OCR](https://capecomorinschool.com)

Decades of handwritten student records shouldn't require someone to spend an afternoon digging through cupboards. Built to modernize a heritage school established in 1984.

- Built an OCR pipeline using Gemini Multimodal API to extract information from scanned handwritten student records.
- Implemented RapidFuzz-ranked fuzzy searching to resolve imperfect OCR output against student registries, reducing record lookup time from **hours to ~30 seconds**.
- Built authenticated administrative panels with Firebase JWT authentication and RBAC for **10+ staff members** across Turso, Neon PostgreSQL, and Cloudinary.
- Created calendar-grounded, staff-reviewed AI notices with Groq’s Llama API and WeasyPrint PDFs; gated frontend merges on GitHub Actions lint, TypeScript checks, and production builds.
- **impact:** Converted decades of paper archives into an instantaneous, searchable digital workflow for school administrators.
- **built with:** Next.js · Flask · FastAPI · Gemini API · Groq (Llama API) · RapidFuzz · Firebase Auth · Turso · Neon PostgreSQL · Cloudinary · WeasyPrint · GitHub Actions

---

### [Churn — AI-Powered Developer CLI](https://pypi.org/project/churn-cli/)

An open-source command-line tool that brings repository intelligence and interview preparation directly to the developer terminal.

- Built a CLI that mines git history for high-churn hotspots, generates leveled interview Q&A in Markdown or JSON, produces documentation, and scores repository health across local and GitHub repositories.
- Integrated multi-provider LLM support across **Gemini, Groq, and OpenAI** rather than coupling to a single model provider.
- Published to PyPI (`churn-cli`), reaching approximately **144 monthly downloads**.
- **impact:** Brought LLM repository analysis into native command-line developer workflows.
- **built with:** Python · Gemini API · Groq API · OpenAI API · PyPI · CLI

---

### [AuralAce — Audio Processing Playground](https://auralace.vercel.app)

An interactive platform for sound shaping and audio signal processing.

- Built an interface for experimenting with FFT equalisation, convolution reverb, time stretching, and smoothing.
- Designed around immediate before-and-after playback and live waveform visualisations rather than slow batch pipelines.
- Implemented audio processing algorithms using Python, FastAPI, NumPy, SciPy, and librosa alongside the Web Audio API.
- **built with:** Python · FastAPI · NumPy · SciPy · librosa · JavaScript · Web Audio API · Next.js · Vercel

---

<h2 id="work-experience">work experience</h2>

### IT Operations Support Intern — Cape Comorin Children School
*Kanpur (Hybrid) · Jun 2026 – Jul 2026*

- Delivered a deployed Next.js demo with separately deployed Flask school and FastAPI Vritukul microservices; used Gemini to extract 100+ handwritten records and RapidFuzz-ranked search for about 30-second lookup.
- Implemented Firebase-verified auth and RBAC for student and register workflows; designed the admin system for 10+ staff accounts using Turso, Neon PostgreSQL, and Cloudinary.
- Created calendar-grounded, staff-reviewed AI notices with Groq’s Llama API and WeasyPrint PDFs; gated Cape Comorin frontend merges on GitHub Actions lint, TypeScript checks and production builds.
- **Tech:** Next.js · Flask · FastAPI · Gemini API · Groq (Llama API) · RapidFuzz · Firebase Auth · Turso · Neon PostgreSQL · Cloudinary · WeasyPrint · GitHub Actions

---

### Backend Developer Intern — Codingo Forge
*Noida (Remote) · Apr 2026 – Jun 2026*

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
- **Adobe Education Summit:** Selected among the top 300 of 19,000+ nationwide applicants for Adobe’s Education Summit at its Noida HQ, focused on Adobe Firefly and developer communities (2026).
- **Churn (PyPI):** CLI for interview prep, doc generation, and repo health scoring; 144 downloads/month.
- **UAV Certification, CDAC Noida:** Certified UAV Pilot by C-DAC, Noida (2024) in ArduPilot/Pixhawk flight control and DGCA drone regulations.
- **LeetCode:** Peak contest rating of 1617 and earned the 50 Days Badge.
