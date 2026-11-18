# SPEC — news.png

Goal: generate `news.png`, a single self-contained infographic summarising the world news of **Tuesday, 17 November 2026**.

## Deliverable

- `main.py` — runnable, deterministic Python script (Pillow). Running `python3 main.py` in the repo root writes `news.png` and nothing else. No network access, no randomness without a fixed seed, no wall-clock timestamps baked into the drawing.
- `news.png` — the rendered infographic (dark editorial style, headline + dated masthead "17 November 2026", one card per news item with a category tag and a 1–2 sentence summary, plus small source attribution line).

## News items (cross-checked across multiple sources on 17 Nov 2026)

1. **UKRAINE–RUSSIA / KERCH BRIDGE** — Ukraine struck the Kerch Bridge linking Russia to occupied Crimea for a second consecutive night in what it called an "unprecedented" operation; the bridge partly collapsed and road traffic was suspended. Russia reported downing a record drone barrage (over 2,000 drones) and retaliated with strikes on Kyiv's North and South bridges, cutting water and power in parts of the capital. (Sources: BBC, The Guardian, AP, Al Jazeera, RTE)
2. **TRUMP IN ASIA** — President Trump arrived in Manila at the start of a high-stakes Asia trip: ASEAN summit meetings in the Philippines, then APEC in China and a planned historic trilateral summit with Vladimir Putin and Xi Jinping in Shenzhen — the first three-way meeting of the nuclear-armed powers since the Cold War era. Large protests were held in Manila. (Sources: AP, Reuters, The Guardian, The Washington Post)
3. **US–IRAN ESCALATION** — The US struck targets on Iran's Qeshm Island after Iranian mines set at least five ships ablaze in the Strait of Hormuz; Iran fired drones at a US radar facility in Bahrain — its third attack on US targets there — as a third US aircraft carrier group arrived in the Gulf. Oil shipping through Hormuz was disrupted. (Sources: NPR, Euronews, AP, Reuters, Le Monde)
4. **US AVIATION CRISIS** — Air travel lurched back toward normal after Friday's FAA nationwide ground stop (over 18,000 cancellations, the largest disruption since 9/11); United Airlines then canceled dozens of flights after a 90-minute system outage. The FAA said it will rethink how it does upgrades, and Transportation Secretary Sean Duffy faced Senate questioning. (Sources: NPR, Democracy Now!, Euronews)
5. **TECH OUTAGES / NSA** — A "highly classified NSA network went down", per ABC News, the latest in a string of US technology and government system outages this month; a former NSA hacker told CNN "there's something here". Lawmakers demanded answers about Nvidia chips' role in Chinese access to advanced hardware. (Sources: ABC News, CNN)
6. **MEASLES / PUBLIC HEALTH** — The Pan American Health Organization revoked measles-elimination status from Bolivia, Mexico and the United States after more than 5,700 US infections and continuing domestic transmission for over 12 months. (Sources: PAHO/AFP, France 24, ABC)
7. **MARKETS / AI SLIDE** — Wall Street fell again as AI stocks swung: the S&P 500 sank 0.9%, the Dow dropped 541 points and Nvidia flipped between gains and losses before closing down 2.9%. Separately, Jensen Huang said he would be "honoured" to return as Nvidia's CEO and is set to testify before US Congress committees on 1 December over chip sales to China. (Sources: AP, Euronews)
8. **EU MIGRATION / RWANDA HUBS** — Five EU states (Austria, Denmark, Germany, Greece, the Netherlands) announced plans for migrant "return hubs" in Rwanda, drawing human-rights backlash and criticism from Spain's Sánchez; the EU also cleared the UniCredit takeover of Germany's Commerzbank. (Sources: The Guardian, Euronews, Christian Science Monitor)

## Style

- Dark background (near-black), light text, one accent colour per category tag.
- Masthead: "WORLD NEWS — 17 NOVEMBER 2026" plus subtitle "Eight stories that shaped the day".
- Each item: category label (colored), bold headline, 1–2 sentence body, tiny source line.
- Deterministic output; fixed canvas size; fonts from system DejaVu directory.
