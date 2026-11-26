"""The soundtrack of the demo video, made in code so it is ours to use: an original piece of music plus interface
sounds, timed to what happens on screen. record.py saves when each click, highlight, zoom and card happens next to
each clip (.json); this joins the clips and adds the sound.

    .venv/bin/python demo/sound.py   # mixes the sound again from the clips already filmed

The music follows the usual shape of product videos: quiet at the start, a light beat once the results are shown,
a rise into the closing figures, and a final chord on the name. Clicks tick, highlights chime in the music's key.
"""

import json
import subprocess
import sys
import tempfile
import wave
from pathlib import Path

import numpy as np

SR = 48000
CLIPS = Path(__file__).parent / "clips"
OUT = Path(__file__).parent / "knowledge-hub-demo.mp4"
SCENES = ["1-title", "2-upload", "3-result", "4-assistant", "5-similar", "6-patents", "7-research", "8-sector", "9-end"]
BEAT = 0.5  # 120 beats a minute
BAR = 4 * BEAT
CHORDS = [[57, 60, 64], [57, 60, 65], [55, 60, 64], [55, 59, 62]]  # A minor, F, C, G (MIDI notes), one a bar
ROOTS = [45, 41, 48, 43]
C_MAJOR = [55, 60, 64, 67]
LOUDNESS = -29  # average level of the scenes in dBFS: quiet, to talk over
ENDING = 0.6  # the closing figures and name stand out, but not by much
CALM = 0.45  # the music under the scenes, relative to the sounds and the ending
rng = np.random.default_rng(7)


def hz(note):
    return 440 * 2 ** ((note - 69) / 12)


def ts(seconds):
    return np.arange(int(seconds * SR)) / SR


def shape(sig, attack, release):
    """Smooth fade in and out (seconds), so nothing clicks."""
    a, r = int(attack * SR), int(release * SR)
    sig = sig.copy()
    if a:
        sig[:a] *= 0.5 - 0.5 * np.cos(np.linspace(0, np.pi, a))
    if r:
        sig[-r:] *= 0.5 + 0.5 * np.cos(np.linspace(0, np.pi, r))
    return sig


def band(sig, low, high):
    spectrum = np.fft.rfft(sig)
    freqs = np.fft.rfftfreq(len(sig), 1 / SR)
    spectrum[(freqs < low) | (freqs > high)] = 0
    return np.fft.irfft(spectrum, len(sig))


def noise(seconds):
    return rng.normal(0, 1, int(seconds * SR))


# Instruments

def pad(note, seconds, release=0.9):
    """A soft, slightly detuned saw: three voices, returned apart so they can be spread left to right."""
    t = ts(seconds)
    voices = []
    for cents in (-9, 0, 9):
        f = hz(note) * 2 ** (cents / 1200)
        voice = sum(np.sin(2 * np.pi * k * f * t + rng.uniform(0, 6.3)) / k ** 1.7 for k in range(1, 6))
        voices.append(shape(voice, 0.6, release))
    return voices


def pluck(note, seconds=0.7, bright=6):
    t = ts(seconds)
    f = hz(note)
    return shape(sum(np.sin(2 * np.pi * k * f * t) * np.exp(-t * (4 + 3.5 * k)) / k for k in range(1, bright)), 0.003, 0.05)


def bass(note):
    t = ts(0.24)
    f = hz(note)
    return shape((np.sin(2 * np.pi * f * t) + 0.25 * np.sin(4 * np.pi * f * t)) * np.exp(-t * 6), 0.006, 0.04)


def kick(seconds=0.45):
    t = ts(seconds)
    phase = 2 * np.pi * np.cumsum(48 + 95 * np.exp(-t * 30)) / SR
    return shape(np.sin(phase) * np.exp(-t * 7), 0.001, 0.05)


def hat():
    t = ts(0.06)
    return np.diff(noise(0.06), prepend=0) * np.exp(-t * 75)


def bell(note, seconds=1.8):
    t = ts(seconds)
    f = hz(note)
    return shape(sum(a * np.sin(2 * np.pi * f * m * t) * np.exp(-t * d) for m, a, d in ((1, 1, 2.6), (2.76, 0.35, 5), (5.4, 0.15, 9))),
                 0.002, 0.2)


def glow(note, seconds=1.4):
    """A soft, round tone for a highlight: a slow start and almost no overtones, so it does not ping."""
    t = ts(seconds)
    f = hz(note)
    return shape((np.sin(2 * np.pi * f * t) + 0.18 * np.sin(4 * np.pi * f * t)) * np.exp(-t * 2.2), 0.03, 0.3)


def tick(pitch=2600, body=1.0):
    """An interface click: a short high tick with a little body."""
    t = ts(0.045)
    return (np.sin(2 * np.pi * pitch * t) * np.exp(-t * 380) * 0.6 + body * np.sin(2 * np.pi * 170 * t) * np.exp(-t * 95) * 0.5
            + noise(0.045) * np.exp(-t * 1200) * 0.15)


def whoosh(seconds=0.8, peak=0.55):
    t = ts(seconds)
    env = np.where(t < peak, (t / peak) ** 2, np.exp(-(t - peak) * 9))
    return band(noise(seconds), 250, 2800) * env


def riser(seconds):
    """Noise that opens up and grows into the closing figures, with a rising tone under it."""
    parts = 24
    chunks = np.array_split(noise(seconds), parts)
    sig = np.concatenate([band(c, 300, 700 + 9000 * (i / parts) ** 2) for i, c in enumerate(chunks)])
    t = ts(seconds)[:len(sig)]
    tone = np.sin(2 * np.pi * np.cumsum(180 + 520 * (t / seconds) ** 2) / SR)
    return (sig * 0.8 + tone * 0.25) * (t / seconds) ** 2.2


def crash(seconds=2.2):
    t = ts(seconds)
    return band(noise(seconds), 3500, 15000) * np.exp(-t * 2.4)


def reverb(bus, seconds=2.2):
    t = ts(seconds)
    out = np.zeros_like(bus)
    size = 1 << int(np.ceil(np.log2(bus.shape[1] + len(t))))
    for ch in range(2):
        ir = band(noise(seconds), 150, 7000) * np.exp(-t * 3.0)
        ir /= np.sqrt(np.sum(ir ** 2))
        out[ch] = np.fft.irfft(np.fft.rfft(bus[ch], size) * np.fft.rfft(ir, size), size)[:bus.shape[1]]
    return out


# Arrangement

def compose(length, starts, events):
    n = int(length * SR)
    dry, duck, wet = (np.zeros((2, n)) for _ in range(3))  # duck: pads and bass, which dip on each kick; wet: sent to the reverb

    def put(bus, at, sig, gain=1.0, pan=0.0, send=0.0):
        i = int(round(at * SR))
        if i < 0:
            sig, i = sig[-i:], 0
        sig = sig[:max(0, n - i)] * gain
        left, right = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
        for target, amount in ((bus, 1.0), (wet, send)):
            if amount:
                target[0, i:i + len(sig)] += sig * left * amount
                target[1, i:i + len(sig)] += sig * right * amount

    cards = [at for at, kind in events if kind == "card"]
    figures, logo = cards[0], cards[-1]  # the closing figures, then the name
    on_beat = lambda at: figures + np.ceil((at - figures) / BEAT) * BEAT
    on_bar = lambda at: figures + np.ceil((at - figures) / BAR) * BAR
    arp_from, groove_from, groove_to = on_beat(starts["2-upload"]), on_bar(starts["3-result"]), figures - BAR
    lift = on_bar(starts["5-similar"])  # halfway: softer in-between hi-hats come in

    # The progression runs up to the closing figures, so its last bar (G) leads into them
    for bar in range(int(np.floor(-figures / BAR)), 0):
        at = figures + bar * BAR
        chord, root = CHORDS[bar % 4], ROOTS[bar % 4]
        level = CALM * (0.09 if at >= groove_from else 0.07)
        for note in chord:
            for voice, pan in zip(pad(note, BAR + 0.9), (-0.6, 0, 0.6)):
                put(duck, at, voice, level / 3, pan, send=0.5)
        pattern = sorted(chord + [c + 12 for c in chord])
        for step, index in enumerate((0, 2, 4, 2)):  # one note a beat
            when = at + step * BEAT
            if when >= arp_from:
                put(dry, when, pluck(pattern[index] + 12, bright=4), CALM * 0.06, 0.35 if step % 2 else -0.35, send=0.4)
        if groove_from <= at < groove_to:
            for beat in range(4):
                when = at + beat * BEAT
                put(dry, when, kick(), CALM * 0.3)
                put(dry, when + BEAT / 2, hat(), CALM * 0.04, 0.25)
                if at >= lift:
                    put(dry, when + BEAT / 4, hat(), CALM * 0.018, -0.25)
                    put(dry, when + 3 * BEAT / 4, hat(), CALM * 0.018, -0.25)
                for half in (0, 0.5):
                    put(duck, when + half * BEAT, bass(root), CALM * 0.12)

    # Pads and bass dip a little on every kick, so the beat breathes
    curve = np.ones(n)
    for k in np.arange(groove_from, groove_to, BEAT):
        i = int(k * SR)
        seg = 1 - 0.38 * np.exp(-ts(BEAT) / 0.12)
        curve[i:i + len(seg)] *= seg[:max(0, n - i)]
    dry += duck * curve

    put(dry, figures - BAR, riser(BAR), 0.11, send=0.3)

    # The closing figures: a hit, a bright C major, a note for each figure; then the name on a full chord
    put(dry, figures, kick(0.8), 0.55)
    put(dry, figures, crash(), 0.06, send=0.4)
    for note in C_MAJOR:
        for voice, pan in zip(pad(note, logo - figures + 0.8), (-0.6, 0, 0.6)):
            put(dry, figures, voice, 0.1 / 3, pan, send=0.5)
    pops = [at for at, kind in events if kind == "pop"]
    for at, note in zip(pops, (72, 76, 79, 84)):
        put(dry, at, pluck(note, 0.9, 7), 0.12, send=0.5)
        put(dry, at, tick(3200, 0.3), 0.08)
    put(dry, logo, kick(0.9), 0.5)
    put(dry, logo, crash(3), 0.05, send=0.5)
    for note in (36, 48, 55, 60, 64, 67, 74):
        for voice, pan in zip(pad(note, length - logo, release=length - logo - 0.8), (-0.6, 0, 0.6)):  # rings out to silence
            put(dry, logo, voice, 0.12 / 3, pan, send=0.6)
    put(dry, logo, bell(84, 3), 0.06, send=0.7)

    # Interface sounds
    chord_at = lambda at: C_MAJOR if at >= figures else CHORDS[int(np.floor((at - figures) / BAR)) % 4]
    for at, kind in events:
        if kind == "click":
            put(dry, at, tick(), 0.22, send=0.08)
        elif kind == "key":
            put(dry, at, tick(rng.uniform(3200, 4200), 0.2)[:int(0.03 * SR)], 0.05)
        elif kind == "drop":
            put(dry, at, tick(1400, 2.0), 0.25, send=0.2)
        elif kind == "spot":
            put(dry, at, glow(max(chord_at(at)) + 12), 0.045, 0.2, send=0.5)
        elif kind == "zoom":
            put(dry, at, whoosh(1.0, 0.7), 0.035, -0.3, send=0.3)
        elif kind == "done":  # an agent finishes its part
            put(dry, at, tick(1900, 1.4), 0.16, send=0.25)

    mix = dry + 0.32 * reverb(wet)
    mix = np.array([band(ch, 35, 20000) for ch in mix])  # no rumble below what speakers play
    rise = int((figures - BAR) * SR)
    mix *= 10 ** (LOUDNESS / 20) / np.sqrt(np.mean(mix[:, :rise] ** 2))
    mix[:, rise:] *= np.minimum(1, np.linspace(1, ENDING, int(BAR * SR)).tolist() + [ENDING] * (n - rise - int(BAR * SR)))
    end = int(0.3 * SR)
    mix[:, -end:] *= np.linspace(1, 0, end)  # the last chord fades as the video ends
    return 0.97 * np.tanh(mix / 0.97)  # soft limit: no harsh peaks


def mix(names=SCENES):
    """Join the clips into OUT with the soundtrack."""
    missing = [n for n in names if not (CLIPS / f"{n}.mp4").exists() or not (CLIPS / f"{n}.json").exists()]
    if missing:
        sys.exit(f"Not joined yet, these clips are missing or have no timings: {', '.join(missing)} (film them with record.py)")
    starts, events, length = {}, [], 0.0
    for name in names:
        info = json.loads((CLIPS / f"{name}.json").read_text())
        starts[name] = length
        events += [(length + at, kind) for at, kind in info["events"]]
        length += info["length"]
    audio = compose(length, starts, sorted(events))
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        with wave.open(str(tmp / "sound.wav"), "wb") as w:
            w.setnchannels(2)
            w.setsampwidth(2)
            w.setframerate(SR)
            w.writeframes((audio.T * 32767).astype("<i2").tobytes())
        (tmp / "clips.txt").write_text("".join(f"file '{CLIPS / name}.mp4'\n" for name in names))
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(tmp / "clips.txt"),
                        "-i", str(tmp / "sound.wav"), "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                        "-shortest", "-movflags", "+faststart", str(OUT)], check=True)
    print(f"Saved {OUT} ({length:.1f} s, with sound)")


if __name__ == "__main__":
    mix()
