from http.server import BaseHTTPRequestHandler
import json, os, urllib.request, urllib.error

MARCUS_CONTEXT = """
Marcus Hultberg — People & Culture, Recruitment & Learning and Development

PROFILE:
Experienced in working broadly within recruitment, HR, Learning & Development and organisational development,
primarily in technical environments. Driven by working closely with people and business, and by creating
conditions for both individuals and organisations to develop. Has built and improved processes within
recruitment, onboarding and competence development, always with a focus on creating a great employee experience.
Thrives collaborating with managers and teams, contributing with structure, perspective and support.

CONTACT:
Email: marcus.hultberg@live.se
Phone: 0703445947
Location: Hedåsgatan 10, 412 53 Gothenburg, Sweden
LinkedIn: https://www.linkedin.com/in/marcus-hultberg-505b386a/

WORK EXPERIENCE:

1. Recruitment Consultant — Mpya Sci & Tech, Gothenburg (June 2024 – June 2026)
   Company: Recruitment and consulting firm specialising in science, technology and engineering.
   - Drove and managed full recruitment processes (need analysis to final placement) for technical roles
   - Advised managers on competence profiles, selection, process and candidate evaluation
   - Ensured a structured and high-quality candidate experience throughout the process
   - Developed and improved recruitment processes and ways of working
   - Worked in ATS systems to ensure quality and structure in candidate data
   - Wrote and published job ads based on business needs
   - Proactively sourced and built candidate pipelines

2. Course Developer — Simployer, Gothenburg (Sep 2023 – June 2024)
   Company: Leading Nordic HR tech company providing HR systems, payroll solutions and training.
   - Developed and improved training courses within HR and Learning & Development
   - Ensured content was up to date and aligned with current HR trends and needs
   - Collaborated with subject matter experts to create relevant and high-quality training
   - Planned and executed conferences and training sessions focused on participant value
   - Improved course materials and pedagogical structures
   - Integrated market insights and research into training content

3. Business Manager — A Society, Gothenburg (April 2022 – Sep 2023)
   Company: IT consulting firm connecting tech talent with companies across Sweden.
   - Responsible for recruitment and matching of IT consultants
   - Coordinated dialogue between clients and candidates throughout the process
   - Worked with onboarding and ongoing HR support to consultants, including invoicing and follow-up
   - Developed internal onboarding structures to increase engagement and retention
   - Managed multiple parallel processes in a fast-changing environment

4. Talent Acquisition Lead / Consultant Manager — ZoCom, Gothenburg (Nov 2020 – April 2022)
   Company: Fast-growing IT consulting company focused on web development and digital solutions.
   - Led and developed the company's talent acquisition work (part of management team)
   - Worked with employer branding and improvement of internal processes
   - Implemented and developed ATS workflows
   - Managed full recruitment processes from start to onboarding
   - HR support and development for a consultant group of 15+ people
   - Developed and implemented onboarding structure for new employees
   - Created and ran internal workshops and training initiatives
   - Initiated and built a career programme for junior talent
   - Contributed to organisational development by establishing an internal LMS that was later sold B2B

5. Education Manager / ICT Manager — IT-Högskolan, Gothenburg (June 2019 – Oct 2020)
   Company: One of Sweden's largest providers of vocational higher education within IT and tech.
   - Led and developed education programmes in close collaboration with the labour market
   - Coached and guided students in their career journey into the IT industry
   - Worked with competence supply by matching education to market needs
   - Participated in recruiting teachers and ensured relevant competence
   - Built and maintained partnerships with companies and external stakeholders
   - Secured internship placements and supported students in their transition to working life
   - Improved internal communication flows and developed LMS structure

6. First Line Support / Store Sales — Telia Company, Gothenburg/Umeå (May 2013 – Aug 2018)
   Company: Sweden's largest telecom operator, providing mobile, broadband and TV services.
   - Supported onboarding of new employees through coaching and participating in recruitment
   - Contributed to improved knowledge sharing and working methods in support
   - Worked with customer service via phone, chat and email
   - Developed strong communication and problem-solving skills

SKILLS:
- Talent Acquisition: Full recruitment process, from needs analysis and sourcing to offer and onboarding
- People & Culture: Employee experience, engagement, culture and HR processes in technical environments
- Learning & Development (L&D): Course development, education management, LMS and competence development programmes
- HR: Personnel matters, onboarding, retention and support to managers and employees
- Employer Branding: Building and communicating employer brand to attract the right talent
- Project Management: Driving parallel processes, structuring work and delivering in fast-changing environments
- Organisational Development: Building structures, processes and programmes that create long-term sustainability
- Stakeholder Management: Advisory collaboration with managers, leadership and external stakeholders
- Communication: Clear and adapted communication in candidate meetings, workshops and conferences
- AI Tools: Practical experience using ChatGPT and Claude to enhance productivity and work quality

SYSTEMS & TOOLS:
Teamtailor, Workbuster, Slack, Notion, Google Workspace, LinkedIn Recruiter, ChatGPT, Claude

EDUCATION:
- BSc. Behavioural Science with focus on IT environments — Umeå University, 2016–2019
  Focused on human behaviour in digital and technical organisations, a solid foundation for People & Culture work in the tech industry.
  Relevant areas: Organisational psychology, Pedagogy & didactics, Recruitment & selection, Group dynamics, Employment law basics, Leadership & coaching, Quality assurance, Competence supply.
- Certified Education Manager — Myndigheten för Yrkeshögskolan, 2020
  Certification in education management focused on vocational higher education, directly applicable in L&D roles.

LANGUAGES:
Swedish (native), English (professional fluency)

PERSONAL LIFE:
- Lives in Gothenburg with his fiancée and their 2.5-year-old son.
- Hobbies: Creative person who reads a lot of fantasy and writes D&D adventures as a Game Master. Huge passion for food and cooking, loves all food from street food joints to Michelin restaurants. Enjoys board games. Loves watching Critical Role, a live-action D&D series.
- Travel: Loves travelling, especially to Spain and Costa del Sol. Grew up half and half in Thailand. Has been stuck on the African savannah.
- Music: Music omnivore, currently stuck on funk soul. Favourite track right now: "Beirut" by Wanda Wonderful. Prefers music over podcasts.
- Curiosity & learning: Loves reading and watching videos to learn new things, especially about AI and how to streamline and optimise work. Being creative at work is something that makes him feel good.
- Quick picks: Burger over Pizza, Wine over Beer, Beach over Mountains, Night over Morning, Series over Movie, Slack over Teams, iPhone over Android, Spicy over Mild food, Marvel over Star Wars, Claude over ChatGPT.
- What drives him: Genuinely cares about people. Believes in building real connections, staying curious and always trying to grow.

AVAILABILITY:
Open to new opportunities within People & Culture, Talent Acquisition and Learning & Development, especially in technical environments.
"""

SYSTEM_PROMPT = (
    "You are a helpful assistant on Marcus Hultberg's personal CV website. "
    "Answer questions about Marcus professionally and concisely, based strictly on the information provided. "
    "Always answer in the same language the question is asked in (Swedish or English). "
    "Keep answers under 120 words. If asked something not covered by the provided info, say so politely."
)


class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length))
        question = body.get("question", "").strip()

        api_key = os.environ.get("ANTHROPIC_API_KEY", "")
        if not api_key:
            self._json(400, {"error": "API key not configured."})
            return
        if not question:
            self._json(400, {"error": "No question provided."})
            return

        payload = json.dumps({
            "model": "claude-haiku-4-5-20251001",
            "max_tokens": 300,
            "system": SYSTEM_PROMPT,
            "messages": [{"role": "user", "content": f"CV context:\n{MARCUS_CONTEXT}\n\nQuestion: {question}"}]
        }).encode()

        req = urllib.request.Request(
            "https://api.anthropic.com/v1/messages",
            data=payload,
            headers={
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                result = json.loads(resp.read())
                answer = result["content"][0]["text"]
            self._json(200, {"answer": answer})
        except urllib.error.HTTPError as e:
            err = e.read().decode()
            self._json(500, {"error": f"API error: {err}"})
        except Exception as e:
            self._json(500, {"error": str(e)})

    def _json(self, code, data):
        body = json.dumps(data).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
