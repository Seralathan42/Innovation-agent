# Demo video script (80 seconds, with sound)

The video is [demo/knowledge-hub-demo.mp4](../demo/knowledge-hub-demo.mp4). It has music and interface sounds but no voice: you talk over it live, so each scene has a caption on screen and a short line for you to say. The demo disclosure is fictional: [disclosures/demo-sleep-radar.md](../disclosures/demo-sleep-radar.md), a bedside radar that screens for sleep apnea.

Each scene starts exactly where the one before it ended, and moves to the next part of the app by clicking its tab. The important part of each scene is highlighted: the camera zooms in and a spotlight dims everything else.

| Time | Scene | What is shown and highlighted | Caption on screen | What you can say |
|---|---|---|---|---|
| 0:00 to 0:03 | Title | Aalto Innovation Knowledge Hub | (title card) | "This is the Knowledge Hub we built for Aalto Innovation's advisors." |
| 0:03 to 0:11 | Upload | The disclosure file is dragged onto the Brief tab. The brief opens and the real run plays 30 times faster: each agent ticks off as it finishes, its score appears, and the checker finishes last. | Drop in an invention disclosure / 2 minutes of research, sped up | "An advisor drops in an invention disclosure, and about two minutes later the research is done." |
| 0:11 to 0:23 | Result | Zoom on the four steps: spotlight on the four research agents, then on the overall score. Then zoom on a score card where the checker disagrees, and the patent report opens. | Four AI agents research it at the same time / Each part is scored from 1 to 5 / A second AI checks every score | "Four agents research the market, patents and funding and write a summary, using our own patent database and the web. Each part is scored from 1 to 5, and a second AI checks the scores against the sources." |
| 0:23 to 0:35 | Assistant | A question typed into the assistant and its answer (sped up). A company it names is clicked; one spotlight on its name, summary and key people. | Ask the assistant follow-up questions / One click opens a company profile | "The advisor can ask follow-up questions, and any company it names opens as a profile with its key people." |
| 0:35 to 0:44 | Similar patents | A description typed in; spotlight on who files most in the area, from the closest stored patents. | Find similar patents in our local patent database | "Similar patents are found in our own patent database, so nothing is sent out." |
| 0:44 to 0:53 | Patents | Health technology selected in the filters; spotlight on the count; the list sorted by applicant. | Search through 460,000 patents | "Every European and international patent in Aalto's fields from the last five years, kept up to date." |
| 0:53 to 1:06 | Past research | "lithium recovery" is typed and the list narrows to 20 papers. The 2018 paper opens; zoom and spotlight on its verdict at a glance: Partly missed, first patented in 2014 by JX Nippon Mining & Metals, sold today by 7 companies, 51 searches. | Spot missed opportunities in past Aalto research | "We also check past Aalto research against today's patents and companies, to find opportunities we missed." |
| 1:06 to 1:12 | Sector | The health technology sector; spotlight on key figures, then on open funding calls. | Market news, figures and funding calls | "And each research area has its own market news, figures and funding calls, updated in the background." |
| 1:12 to 1:20 | End | The key figures count up (4 AI agents, about 460,000 patents, about 25,700 Aalto papers, 8 research areas), then the name and the slogan, held while the last chord rings out | Less background research. More time advising. | "Less background research, more time advising." |

## Sound

The music and sounds are our own, made in code by [demo/sound.py](../demo/sound.py), so there is no licence to worry about. They follow what product videos usually do: quiet music that builds, and small sounds tied to what happens on screen.

- 0:00: a soft pad. Plucked notes, one a beat, come in with the upload.
- 0:11: a light beat starts when the results appear.
- 0:35: soft in-between hi-hats come in as the patent scenes begin.
- 1:10: a riser leads into the closing figures, which land on a hit, with a note for each figure. The name lands on a full final chord.
- Every click ticks, typing clicks softly, and every highlight has a soft, low tone in the music's key. Zooms have a soft whoosh, and each agent that finishes during the upload gives a soft tick.

The music under the scenes is kept quiet (about -27 LUFS, well below normal video loudness) so it stays in the background; the ending is a little louder (about -24 LUFS). Turn the room volume up from low until you can just hear it under your voice. To mix the sound again without filming: `.venv/bin/python demo/sound.py`.

## Recording again

- Start the Knowledge Hub (`.venv/bin/python terminal.py`). The demo brief, the company profiles and the lithium paper's analysis are already stored, so nothing in the video waits.
- `.venv/bin/python demo/record.py` films every scene in a hidden Chrome window, saves each as its own clip in `demo/clips/`, and joins them into `demo/knowledge-hub-demo.mp4`.
- To redo one part, name its scenes: `.venv/bin/python demo/record.py research sector`. Only those are filmed again, each starting where the scene before it ends, and all the clips are joined again. The scenes are title, upload, result, assistant, similar, patents, research, sector and end.
- The assistant scene asks the chat a real question, so it uses a little subscription usage and its answer differs each time. The scenes after it show that answer in the chat panel, so film them again too after filming the assistant scene.
