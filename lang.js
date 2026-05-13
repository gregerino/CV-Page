// Language switcher for Marcus Hultberg CV site
(function () {
  var translations = {
    // ── NAV ──
    'nav.home': { en: 'Home', sv: 'Hem' },
    'nav.about': { en: 'About', sv: 'Om mig' },
    'nav.cv': { en: 'CV', sv: 'CV' },
    'nav.skills': { en: 'Skills', sv: 'Kompetenser' },
    'nav.education': { en: 'Education', sv: 'Utbildning' },
    'nav.personal': { en: 'Personal', sv: 'Personligt' },
    'nav.contact': { en: 'Contact', sv: 'Kontakt' },

    // ── INDEX ──
    'index.eyebrow': { en: 'People & Culture · HR · Recruitment', sv: 'People & Culture · HR · Rekrytering' },
    'index.subtitle': { en: 'Specialist in Talent Acquisition, Learning & Development and organisational development, with 7+ years of experience in technical environments.', sv: 'Specialist inom Talent Acquisition, Learning & Development och organisationsutveckling, med 7+ års erfarenhet i tekniska miljöer.' },
    'index.location': { en: 'Gothenburg, Sweden', sv: 'Göteborg, Sverige' },
    'index.tag1': { en: 'Talent Acquisition', sv: 'Talent Acquisition' },
    'index.tag2': { en: 'People & Culture', sv: 'People & Culture' },
    'index.tag3': { en: 'L&D', sv: 'L&D' },
    'index.tag4': { en: 'Employer Branding', sv: 'Employer Branding' },
    'index.cta1': { en: 'View CV', sv: 'Se CV' },
    'index.cta2': { en: 'Get in touch', sv: 'Kontakta mig' },
    'index.stat1': { en: 'Years experience', sv: 'Års erfarenhet' },
    'index.stat2': { en: 'Industry focus', sv: 'Branschfokus' },
    'index.badge.title': { en: 'People & Culture · Recruitment', sv: 'People & Culture · Rekrytering' },
    'index.search': { en: 'Ask anything about Marcus', sv: 'Fråga vad som helst om Marcus' },
    'index.thinking': { en: 'Thinking…', sv: 'Tänker…' },
    'index.answer': { en: 'Answer', sv: 'Svar' },
    'index.footer.cta': { en: 'Get in touch →', sv: 'Kontakta mig →' },

    // ── ABOUT ──
    'about.eyebrow': { en: 'Background & motivations', sv: 'Bakgrund & drivkrafter' },
    'about.title': { en: 'About me', sv: 'Om mig' },
    'about.ingress': { en: 'Experienced in working broadly within recruitment, HR, Learning & Development and organisational development, primarily in technical environments.', sv: 'Bred erfarenhet av att arbeta inom rekrytering, HR, Learning & Development och organisationsutveckling, främst i tekniska miljöer.' },
    'about.body1': { en: 'What drives me is the opportunity to work closely with people and business, and to create conditions for both individuals and organisations to grow. Through my roles I have had the chance to build and improve processes within recruitment, onboarding and competence development, always with a focus on creating a great and engaging employee experience.', sv: 'Det som driver mig är möjligheten att arbeta nära människor och verksamhet, och att skapa förutsättningar för både individer och organisationer att växa. Genom mina roller har jag fått bygga och förbättra processer inom rekrytering, onboarding och kompetensutveckling, alltid med fokus på att skapa en fantastisk medarbetarupplevelse.' },
    'about.body2': { en: 'I thrive in collaboration with managers and teams, contributing with structure, perspective and support in how we can work smarter and more sustainably over time.', sv: 'Jag trivs i samarbete med chefer och team, där jag bidrar med struktur, perspektiv och stöd i hur vi kan arbeta smartare och mer hållbart över tid.' },
    'about.drives.title': { en: "What I'm passionate about", sv: 'Det jag brinner för' },
    'about.drive1': { en: 'Matching the right person with the right role, and creating conditions for them to succeed', sv: 'Att matcha rätt person med rätt roll och skapa förutsättningar för dem att lyckas' },
    'about.drive2': { en: 'Building structures and processes that create long-term sustainability', sv: 'Att bygga strukturer och processer som skapar långsiktig hållbarhet' },
    'about.drive3': { en: 'Working closely with the business to understand its needs', sv: 'Att arbeta nära verksamheten för att förstå dess behov' },
    'about.drive4': { en: 'Creating engaging employee experiences from day one', sv: 'Att skapa engagerande medarbetarupplevelser från dag ett' },
    'about.drive5': { en: 'Combining data-driven thinking with a genuine focus on people', sv: 'Att kombinera datadriven tankesätt med ett genuint fokus på människor' },
    'about.card.location': { en: 'Location', sv: 'Plats' },
    'about.card.location.val': { en: 'Gothenburg, Sweden', sv: 'Göteborg, Sverige' },
    'about.card.focus': { en: 'Focus', sv: 'Fokus' },
    'about.card.focus.val': { en: 'People & Culture · Recruitment · L&D', sv: 'People & Culture · Rekrytering · L&D' },

    // ── EXPERIENCE ──
    'exp.eyebrow': { en: 'Career', sv: 'Karriär' },
    'exp.title': { en: 'Work experience', sv: 'Arbetslivserfarenhet' },

    'exp.r1.title': { en: 'Recruitment Consultant', sv: 'Rekryteringskonsult' },
    'exp.r1.about': { en: 'Recruitment and consulting firm specialising in science, technology and engineering.', sv: 'Rekryterings- och konsultföretag specialiserat på vetenskap, teknik och ingenjörskonst.' },
    'exp.r1.desc': { en: 'Matching the right person with the right workplace while acting as an advisor to hiring managers on competence and cultural fit.', sv: 'Matchning av rätt person med rätt arbetsplats, samtidigt som jag agerade rådgivare till rekryterande chefer kring kompetens och kulturell passform.' },
    'exp.r1.b1': { en: 'Drove and managed full recruitment processes from needs analysis to final placement, within technical roles', sv: 'Drev och ledde fullständiga rekryteringsprocesser från behovsanalys till slutlig placering, inom tekniska roller' },
    'exp.r1.b2': { en: 'Advised managers on competence profiles, selection, process and candidate evaluation', sv: 'Rådgav chefer kring kompetenskrav, urval, process och kandidatutvärdering' },
    'exp.r1.b3': { en: 'Ensured a structured and high-quality candidate experience throughout the process', sv: 'Säkerställde en strukturerad kandidatupplevelse av hög kvalitet genom hela processen' },
    'exp.r1.b4': { en: 'Developed and improved recruitment processes and ways of working', sv: 'Utvecklade och förbättrade rekryteringsprocesser och arbetssätt' },
    'exp.r1.b5': { en: 'Worked in ATS systems to ensure quality and structure in candidate data', sv: 'Arbetade i ATS-system för att säkerställa kvalitet och struktur i kandidatdata' },
    'exp.r1.b6': { en: 'Wrote and published job ads based on business needs', sv: 'Skrev och publicerade jobbannonser baserade på verksamhetens behov' },
    'exp.r1.b7': { en: 'Proactively sourced and built candidate pipelines', sv: 'Proaktivt sökte och byggde kandidatpipelines' },

    'exp.r2.title': { en: 'Course Developer', sv: 'Kursutvecklare' },
    'exp.r2.about': { en: 'Leading Nordic HR tech company providing HR systems, payroll solutions and training.', sv: 'Ledande nordiskt HR-techbolag som erbjuder HR-system, lönelösningar och utbildning.' },
    'exp.r2.desc': { en: 'Developed and improved training content in HR, payroll, tax and VAT for a leading HR system with a strong focus on the employee experience.', sv: 'Utvecklade och förbättrade utbildningsinnehåll inom HR, lön, skatt och moms för ett ledande HR-system med starkt fokus på medarbetarupplevelsen.' },
    'exp.r2.b1': { en: 'Developed and improved courses within HR and Learning & Development', sv: 'Utvecklade och förbättrade kurser inom HR och Learning & Development' },
    'exp.r2.b2': { en: 'Ensured content was up to date and aligned with current HR trends and needs', sv: 'Säkerställde att innehållet var aktuellt och i linje med nuvarande HR-trender och behov' },
    'exp.r2.b3': { en: 'Collaborated with subject matter experts to create relevant and high-quality training', sv: 'Samarbetade med ämnesexperter för att skapa relevant utbildning av hög kvalitet' },
    'exp.r2.b4': { en: 'Planned and executed conferences and training sessions focused on participant value', sv: 'Planerade och genomförde konferenser och utbildningar med fokus på deltagarvärde' },
    'exp.r2.b5': { en: 'Improved course materials and pedagogical structures', sv: 'Förbättrade kursmaterial och pedagogiska strukturer' },
    'exp.r2.b6': { en: 'Integrated market insights and research into training content', sv: 'Integrerade marknadsinsikter och forskning i utbildningsinnehållet' },

    'exp.r3.title': { en: 'Business Manager', sv: 'Affärsansvarig' },
    'exp.r3.about': { en: 'IT consulting firm connecting tech talent with companies across Sweden.', sv: 'IT-konsultföretag som kopplar samman techtalanger med företag över hela Sverige.' },
    'exp.r3.desc': { en: 'Responsible for recruitment and matching of IT consultants alongside ongoing HR support in a fast-moving consulting environment.', sv: 'Ansvarig för rekrytering och matchning av IT-konsulter samt löpande HR-stöd i en snabbrörlig konsultmiljö.' },
    'exp.r3.b1': { en: 'Responsible for recruitment and matching of IT consultants', sv: 'Ansvarig för rekrytering och matchning av IT-konsulter' },
    'exp.r3.b2': { en: 'Coordinated dialogue between clients and candidates throughout the process', sv: 'Koordinerade dialogen mellan kunder och kandidater genom hela processen' },
    'exp.r3.b3': { en: 'Worked with onboarding and ongoing HR support to consultants, including invoicing and follow-up', sv: 'Arbetade med onboarding och löpande HR-stöd till konsulter, inklusive fakturering och uppföljning' },
    'exp.r3.b4': { en: 'Developed internal onboarding structures to increase engagement and retention', sv: 'Utvecklade interna onboardingstrukturer för att öka engagemang och retention' },
    'exp.r3.b5': { en: 'Managed multiple parallel processes in a fast-changing environment', sv: 'Hanterade flera parallella processer i en snabbföränderlig miljö' },

    'exp.r4.title': { en: 'Talent Acquisition Lead / Consultant Manager', sv: 'Talent Acquisition Lead / Konsultansvarig' },
    'exp.r4.about': { en: 'Fast-growing IT consulting company focused on web development and digital solutions.', sv: 'Snabbväxande IT-konsultföretag med fokus på webbutveckling och digitala lösningar.' },
    'exp.r4.desc': { en: 'Part of the management team with full responsibility for talent acquisition and a consultant group of 15+ people in a high-growth IT company.', sv: 'Del av ledningsgruppen med fullt ansvar för talent acquisition och en konsultgrupp på 15+ personer i ett snabbväxande IT-företag.' },
    'exp.r4.b1': { en: "Led and developed the company's talent acquisition work", sv: 'Ledde och utvecklade företagets talent acquisition-arbete' },
    'exp.r4.b2': { en: 'Worked with employer branding and improvement of internal processes', sv: 'Arbetade med employer branding och förbättring av interna processer' },
    'exp.r4.b3': { en: 'Implemented and developed ATS workflows', sv: 'Implementerade och utvecklade ATS-arbetsflöden' },
    'exp.r4.b4': { en: 'Managed full recruitment processes from start to onboarding', sv: 'Hanterade fullständiga rekryteringsprocesser från start till onboarding' },
    'exp.r4.b5': { en: 'HR support and development for a consultant group of 15+ people', sv: 'HR-stöd och utveckling för en konsultgrupp på 15+ personer' },
    'exp.r4.b6': { en: 'Developed and implemented onboarding structure for new employees', sv: 'Utvecklade och implementerade onboardingstruktur för nyanställda' },
    'exp.r4.b7': { en: 'Created and ran internal workshops and training initiatives', sv: 'Skapade och drev interna workshops och utbildningsinitiativ' },
    'exp.r4.b8': { en: 'Initiated and built a career programme for junior talent', sv: 'Initierade och byggde ett karriärprogram för juniora talanger' },
    'exp.r4.b9': { en: 'Contributed to organisational development by establishing an internal LMS that was later sold B2B', sv: 'Bidrog till organisationsutveckling genom att etablera ett internt LMS som senare såldes B2B' },

    'exp.r5.title': { en: 'Education Manager / ICT Manager', sv: 'Utbildningsledare / ICT-ansvarig' },
    'exp.r5.about': { en: "One of Sweden's largest providers of vocational higher education within IT and tech.", sv: 'En av Sveriges största aktörer inom yrkeshögskola med fokus på IT och tech.' },
    'exp.r5.desc': { en: "Led education programmes at one of Sweden's largest vocational IT schools and supported students in their transition into the tech industry.", sv: 'Ledde utbildningsprogram på en av Sveriges största yrkeshögskolor inom IT och stöttade studenter i deras övergång till techbranschen.' },
    'exp.r5.b1': { en: 'Led and developed education programmes in close collaboration with the labour market', sv: 'Ledde och utvecklade utbildningsprogram i nära samarbete med arbetsmarknaden' },
    'exp.r5.b2': { en: 'Coached and guided students in their career journey into the IT industry', sv: 'Coachade och vägledde studenter i deras karriärresa in i IT-branschen' },
    'exp.r5.b3': { en: 'Worked with competence supply by matching education to market needs', sv: 'Arbetade med kompetensförsörjning genom att matcha utbildning mot marknadens behov' },
    'exp.r5.b4': { en: 'Participated in recruiting teachers and ensured relevant competence', sv: 'Deltog i rekrytering av lärare och säkerställde relevant kompetens' },
    'exp.r5.b5': { en: 'Built and maintained partnerships with companies and external stakeholders', sv: 'Byggde och underhöll partnerskap med företag och externa intressenter' },
    'exp.r5.b6': { en: 'Secured internship placements and supported students in transitioning to working life', sv: 'Säkrade praktikplatser och stöttade studenter i övergången till arbetslivet' },
    'exp.r5.b7': { en: 'Improved internal communication flows and developed LMS structure', sv: 'Förbättrade interna kommunikationsflöden och utvecklade LMS-struktur' },

    'exp.r6.title': { en: 'First Line Support / Store Sales', sv: 'First Line Support / Butikssäljare' },
    'exp.r6.about': { en: "Sweden's largest telecom operator, providing mobile, broadband and TV services.", sv: 'Sveriges största telekomoperatör som erbjuder mobil, bredband och TV-tjänster.' },
    'exp.r6.desc': { en: "Full-time for three years and part-time for two years at Sweden's largest telecom provider, with a focus on customer service and internal employee support.", sv: 'Heltid i tre år och deltid i två år hos Sveriges största telekomleverantör, med fokus på kundservice och internt medarbetarstöd.' },
    'exp.r6.b1': { en: 'Supported onboarding of new employees through coaching and participating in recruitment', sv: 'Stöttade onboarding av nyanställda genom coachning och deltagande i rekrytering' },
    'exp.r6.b2': { en: 'Contributed to improved knowledge sharing and working methods in support', sv: 'Bidrog till förbättrad kunskapsdelning och arbetssätt inom support' },
    'exp.r6.b3': { en: 'Worked with customer service via phone, chat and email', sv: 'Arbetade med kundservice via telefon, chatt och e-post' },
    'exp.r6.b4': { en: 'Developed strong communication and problem-solving skills', sv: 'Utvecklade stark kommunikations- och problemlösningsförmåga' },

    // ── SKILLS ──
    'skills.eyebrow': { en: 'What I bring', sv: 'Vad jag bidrar med' },
    'skills.title': { en: 'Skills', sv: 'Kompetenser' },
    'skills.core': { en: 'Core competencies', sv: 'Kärnkompetenser' },
    'skills.tools': { en: 'Systems & tools', sv: 'System & verktyg' },
    'skills.s1': { en: 'Talent Acquisition', sv: 'Talent Acquisition' },
    'skills.s1.d': { en: 'Full recruitment process: from needs analysis and sourcing to offer and onboarding', sv: 'Fullständig rekryteringsprocess: från behovsanalys och sourcing till erbjudande och onboarding' },
    'skills.s2': { en: 'People & Culture', sv: 'People & Culture' },
    'skills.s2.d': { en: 'Employee experience, engagement, culture and HR processes in technical environments', sv: 'Medarbetarupplevelse, engagemang, kultur och HR-processer i tekniska miljöer' },
    'skills.s3': { en: 'Learning & Development', sv: 'Learning & Development' },
    'skills.s3.d': { en: 'Course development, education management, LMS and competence development programmes', sv: 'Kursutveckling, utbildningsledning, LMS och kompetensutvecklingsprogram' },
    'skills.s4': { en: 'HR', sv: 'HR' },
    'skills.s4.d': { en: 'Personnel matters, onboarding, retention and support to managers and employees', sv: 'Personalfrågor, onboarding, retention och stöd till chefer och medarbetare' },
    'skills.s5': { en: 'Employer Branding', sv: 'Employer Branding' },
    'skills.s5.d': { en: 'Building and communicating employer brand to attract the right talent', sv: 'Bygga och kommunicera arbetsgivarvarumärke för att attrahera rätt talanger' },
    'skills.s6': { en: 'Project Management', sv: 'Projektledning' },
    'skills.s6.d': { en: 'Driving parallel processes, structuring work and delivering in fast-changing environments', sv: 'Driva parallella processer, strukturera arbete och leverera i snabbföränderliga miljöer' },
    'skills.s7': { en: 'Organisational Development', sv: 'Organisationsutveckling' },
    'skills.s7.d': { en: 'Building structures, processes and programmes that create long-term sustainability', sv: 'Bygga strukturer, processer och program som skapar långsiktig hållbarhet' },
    'skills.s8': { en: 'Stakeholder Management', sv: 'Intressenthantering' },
    'skills.s8.d': { en: 'Advisory collaboration with managers, leadership and external stakeholders', sv: 'Rådgivande samarbete med chefer, ledning och externa intressenter' },
    'skills.s9': { en: 'Communication', sv: 'Kommunikation' },
    'skills.s9.d': { en: 'Clear and adapted communication in candidate meetings, workshops and conferences', sv: 'Tydlig och anpassad kommunikation i kandidatmöten, workshops och konferenser' },
    'skills.s10': { en: 'AI Tools', sv: 'AI-verktyg' },
    'skills.s10.d': { en: 'Practical experience using ChatGPT and Claude to enhance productivity and work quality', sv: 'Praktisk erfarenhet av att använda ChatGPT och Claude för att öka produktivitet och arbetskvalitet' },
    'skills.highlight.title': { en: 'Technical environments as home turf', sv: 'Tekniska miljöer som hemmaplan' },
    'skills.highlight.text': { en: 'The majority of my career has been spent in IT and tech companies, which means I understand the language, needs and challenges of the business. This creates better recruitment processes, more accurate competence profiles and stronger trust from both candidates and hiring managers.', sv: 'Största delen av min karriär har tillbringats i IT- och techföretag, vilket innebär att jag förstår språket, behoven och utmaningarna i verksamheten. Det skapar bättre rekryteringsprocesser, mer träffsäkra kompetenskrav och starkare förtroende från både kandidater och rekryterande chefer.' },

    // ── EDUCATION ──
    'edu.eyebrow': { en: 'Academic background', sv: 'Akademisk bakgrund' },
    'edu.title': { en: 'Education', sv: 'Utbildning' },
    'edu.degree1': { en: 'BSc. Behavioural Science with focus on IT environments', sv: 'Kandidatexamen i beteendevetenskap med inriktning mot IT-miljöer' },
    'edu.school1': { en: 'Umeå University', sv: 'Umeå universitet' },
    'edu.desc1': { en: "Bachelor's degree focused on human behaviour in digital and technical organisations: a solid foundation for People & Culture work in the tech industry.", sv: 'Kandidatexamen med fokus på mänskligt beteende i digitala och tekniska organisationer: en solid grund för People & Culture-arbete i techbranschen.' },
    'edu.degree2': { en: 'Certified Education Manager', sv: 'Certifierad utbildningsledare' },
    'edu.school2': { en: 'Myndigheten för Yrkeshögskolan', sv: 'Myndigheten för Yrkeshögskolan' },
    'edu.desc2': { en: 'Certification in education management focused on vocational higher education, directly applicable in L&D roles with emphasis on pedagogical planning and course design.', sv: 'Certifiering inom utbildningsledning med fokus på yrkeshögskola, direkt tillämpbar i L&D-roller med betoning på pedagogisk planering och kursdesign.' },
    'edu.focus.label': { en: 'The core of the education', sv: 'Kärnan i utbildningen' },
    'edu.focus.title': { en: 'Behavioural science meets technical environments', sv: 'Beteendevetenskap möter tekniska miljöer' },
    'edu.focus.text': { en: 'The combination of behavioural science and an IT perspective provides a unique understanding of how people function in modern, fast-changing organisations, and the ability to bridge the gap between HR and the business.', sv: 'Kombinationen av beteendevetenskap och IT-perspektiv ger en unik förståelse för hur människor fungerar i moderna, snabbföränderliga organisationer, och förmågan att överbrygga klyftan mellan HR och verksamheten.' },
    'edu.areas': { en: 'Relevant knowledge areas', sv: 'Relevanta kunskapsområden' },
    'edu.a1': { en: 'Organisational psychology', sv: 'Organisationspsykologi' },
    'edu.a2': { en: 'Pedagogy & didactics', sv: 'Pedagogik & didaktik' },
    'edu.a3': { en: 'Recruitment & selection', sv: 'Rekrytering & urval' },
    'edu.a4': { en: 'Group dynamics', sv: 'Gruppdynamik' },
    'edu.a5': { en: 'Employment law basics', sv: 'Grundläggande arbetsrätt' },
    'edu.a6': { en: 'Leadership & coaching', sv: 'Ledarskap & coachning' },
    'edu.a7': { en: 'Quality assurance', sv: 'Kvalitetssäkring' },
    'edu.a8': { en: 'Competence supply', sv: 'Kompetensförsörjning' },

    // ── PERSONAL ──
    'personal.eyebrow': { en: 'Beyond work', sv: 'Utanför jobbet' },
    'personal.title': { en: 'Personal', sv: 'Personligt' },
    'personal.intro': { en: "There's more to life than work. Here's a glimpse of who I am outside the office: the things that keep me curious, grounded and energised.", sv: 'Det finns mer i livet än jobb. Här är en glimt av vem jag är utanför kontoret: det som håller mig nyfiken, jordad och energisk.' },
    'personal.hobbies': { en: 'Hobbies', sv: 'Intressen' },
    'personal.hobbies.text': { en: "I'm a creative person at heart. I read a lot of fantasy and channel that into writing D&D adventures as a Game Master. I have a huge passion for food and cooking, and love all food, from street food joints to Michelin restaurants. I also really enjoy getting together over board games, and love watching Critical Role, a live-action D&D series that fuels my creativity as a Game Master.", sv: 'Jag är en kreativ person i grunden. Jag läser mycket fantasy och kanaliserar det till att skriva D&D-äventyr som Game Master. Jag har en enorm passion för mat och matlagning, och älskar all mat, från streetfood till Michelin-restauranger. Jag gillar också att samlas över brädspel och älskar att titta på Critical Role, en live-action D&D-serie som ger bränsle till min kreativitet som Game Master.' },
    'personal.travel': { en: 'Travel', sv: 'Resor' },
    'personal.travel.text': { en: "I love to travel, especially to Spain and Costa del Sol. I also grew up half and half in Thailand, and I've even been stuck on the African savannah. Ask me about it!", sv: 'Jag älskar att resa, särskilt till Spanien och Costa del Sol. Jag växte också upp halva tiden i Thailand, och jag har till och med suttit fast på den afrikanska savannen. Fråga mig om det!' },
    'personal.family': { en: 'Friends & family', sv: 'Vänner & familj' },
    'personal.family.text': { en: 'I live in Gothenburg with my fiancée and our 2.5-year-old son. Time with the people I care about is what matters most: good conversations, dinners and shared experiences.', sv: 'Jag bor i Göteborg med min fästmö och vår 2,5-årige son. Tid med människorna jag bryr mig om är det som betyder mest: bra samtal, middagar och delade upplevelser.' },
    'personal.music': { en: 'Music & podcasts', sv: 'Musik & poddar' },
    'personal.music.text': { en: "I'm a music omnivore, always listening to something. Right now I'm stuck on funk soul. I definitely prefer music over podcasts.", sv: 'Jag är en musikallätare, lyssnar alltid på något. Just nu är jag fast i funk soul. Jag föredrar definitivt musik framför poddar.' },
    'personal.curiosity': { en: 'Curiosity & learning', sv: 'Nyfikenhet & lärande' },
    'personal.curiosity.text': { en: 'I love reading and watching videos to learn new things, especially about AI and how to streamline and optimise the way we work. Being creative in my work is something that genuinely makes me feel good.', sv: 'Jag älskar att läsa och titta på videor för att lära mig nya saker, särskilt om AI och hur man kan effektivisera och optimera sättet vi arbetar. Att vara kreativ i mitt arbete är något som genuint får mig att må bra.' },
    'personal.picks': { en: 'My quick picks', sv: 'Mina snabbval' },
    'personal.drives.title': { en: 'What drives me', sv: 'Det som driver mig' },
    'personal.drives.text': { en: "At the core, I'm someone who genuinely cares about people. Whether it's at work or in my personal life, I believe in building real connections, staying curious and always trying to grow. The best version of me shows up when I balance meaningful work with the things and people that inspire me outside of it.", sv: 'I grunden är jag en person som genuint bryr sig om människor. Oavsett om det är på jobbet eller i privatlivet tror jag på att bygga riktiga relationer, vara nyfiken och alltid försöka växa. Den bästa versionen av mig visar sig när jag balanserar meningsfullt arbete med de saker och människor som inspirerar mig utanför det.' },

    // ── CONTACT ──
    'contact.eyebrow': { en: 'Reach me', sv: 'Nå mig' },
    'contact.title': { en: 'Contact', sv: 'Kontakt' },
    'contact.intro': { en: 'Want to learn more about my background, discuss an opportunity or just have a conversation? Feel free to reach out — I respond quickly and look forward to hearing from you.', sv: 'Vill du veta mer om min bakgrund, diskutera en möjlighet eller bara ha ett samtal? Hör gärna av dig — jag svarar snabbt och ser fram emot att höra från dig.' },
    'contact.email': { en: 'Email', sv: 'E-post' },
    'contact.phone': { en: 'Phone', sv: 'Telefon' },
    'contact.status': { en: 'Available for conversations', sv: 'Tillgänglig för samtal' },
    'contact.avail.title': { en: 'Open to new opportunities', sv: 'Öppen för nya möjligheter' },
    'contact.avail.text': { en: "I'm always interested in hearing about exciting roles within People & Culture, Talent Acquisition and Learning & Development, especially in technical environments.", sv: 'Jag är alltid intresserad av att höra om spännande roller inom People & Culture, Talent Acquisition och Learning & Development, särskilt i tekniska miljöer.' },
    'contact.facts': { en: 'Quick facts', sv: 'Snabbfakta' },
    'contact.location': { en: 'Location', sv: 'Plats' },
    'contact.location.val': { en: 'Gothenburg', sv: 'Göteborg' },
    'contact.experience': { en: 'Experience', sv: 'Erfarenhet' },
    'contact.focus': { en: 'Focus', sv: 'Fokus' },
    'contact.industry': { en: 'Industry', sv: 'Bransch' },
    'contact.education': { en: 'Education', sv: 'Utbildning' },
    'contact.education.val': { en: 'BSc. Behavioural Science', sv: 'Kand. Beteendevetenskap' },

    // ── FOOTER ──
    'footer.cta': { en: 'Get in touch →', sv: 'Kontakta mig →' }
  };

  function getLang() {
    return localStorage.getItem('cv-lang') || 'en';
  }

  function setLang(lang) {
    localStorage.setItem('cv-lang', lang);
    applyLang(lang);
    // Update toggle buttons
    var btns = document.querySelectorAll('.lang-toggle');
    btns.forEach(function (b) {
      b.textContent = lang === 'sv' ? 'EN' : 'SV';
      b.title = lang === 'sv' ? 'Switch to English' : 'Byt till svenska';
    });
  }

  function applyLang(lang) {
    document.documentElement.lang = lang;
    var els = document.querySelectorAll('[data-i18n]');
    els.forEach(function (el) {
      var key = el.getAttribute('data-i18n');
      var t = translations[key];
      if (t && t[lang]) {
        if (el.tagName === 'INPUT' && el.hasAttribute('placeholder')) {
          el.placeholder = t[lang];
        } else {
          el.textContent = t[lang];
        }
      }
    });
  }

  // Create toggle button and insert into nav
  function createToggle() {
    var lang = getLang();
    // Desktop nav
    var navInner = document.querySelector('.nav-inner');
    if (navInner) {
      var btn = document.createElement('button');
      btn.className = 'lang-toggle';
      btn.textContent = lang === 'sv' ? 'EN' : 'SV';
      btn.title = lang === 'sv' ? 'Switch to English' : 'Byt till svenska';
      btn.onclick = function () { setLang(getLang() === 'en' ? 'sv' : 'en'); };
      // Insert before hamburger if it exists, otherwise append
      var hamburger = navInner.querySelector('.nav-hamburger');
      if (hamburger) {
        navInner.insertBefore(btn, hamburger);
      } else {
        navInner.appendChild(btn);
      }
    }
  }

  // Initialize
  createToggle();
  applyLang(getLang());
})();
