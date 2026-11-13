# Range Calculator: paste your Wardogs map position and the target's (from Mark Coordinates in chat), press
# Enemy range, and it shows the RNG and compass heading (Face) to set on the L81 mortar or SPH-2 artillery sight.
# Styled to Jadan Duffin's design system (ink ground, one orange, Schibsted Grotesk + JetBrains Mono).
import ctypes, json, os, shutil, subprocess, sys, threading, tkinter as tk, tkinter.font as tkfont, urllib.request, webbrowser

from pill import pill_image
from rangecalc import calculate, compass_point

VERSION = os.environ.get("RANGECALC_VERSION", "1.8")  # build.ps1 reads this number; the env override only lets the update test pretend to be old
REPO = "jadanduffin/range-calculator"  # GitHub releases are checked on launch for a newer RangeCalculator-Setup.exe
REPO_URL = f"https://github.com/{REPO}"
WINDOWS = sys.platform == "win32"

INK, INK2, INK3, LINE = "#08090A", "#0E0F11", "#131417", "#1E1F21"
FG, MUTED, MUTED2, ACCENT = "#F4F5F4", "#9A9DA3", "#83868C", "#FB4B1D"  # MUTED2 lifted from #696C72 so small text passes 4.5:1
HERE = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))  # PyInstaller unpacks bundled files to _MEIPASS
SETTINGS = os.path.join(os.environ.get("APPDATA", os.path.expanduser("~")), "RangeCalculator.json")

# the brand fonts ship inside the exe; load them for this process only, so nothing is installed on the user's PC
if WINDOWS:
    for f in os.listdir(os.path.join(HERE, "fonts")):
        if f.endswith(".ttf"):
            ctypes.windll.gdi32.AddFontResourceExW(os.path.join(HERE, "fonts", f), 0x10, 0)  # FR_PRIVATE
SANS, SANS_MED, SANS_BLACK = "Schibsted Grotesk", "Schibsted Grotesk Medium", "Schibsted Grotesk ExtraBold"
MONO, MONO_MED = "JetBrains Mono", "JetBrains Mono Medium"

settings = {"a": "x98.42, y110.38", "b": "x94.53, y109.03", "weapon": "mortar"}  # example points until you paste your own
try:
    settings.update(json.load(open(SETTINGS)))
except Exception:
    pass

def save_settings():
    try:
        json.dump(settings, open(SETTINGS, "w"))
    except Exception:
        pass  # shortcut: unsaved settings still work for this run

root = tk.Tk()
root.title("Range Calculator")
root.configure(bg=INK)
root.attributes("-topmost", True)
root.resizable(False, False)
if WINDOWS and os.path.exists(os.path.join(HERE, "RangeCalculator.ico")):
    root.iconbitmap(os.path.join(HERE, "RangeCalculator.ico"))
root.update()
if WINDOWS:
    ctypes.windll.dwmapi.DwmSetWindowAttribute(ctypes.windll.user32.GetParent(root.winfo_id()), 20, ctypes.byref(ctypes.c_int(1)), 4)  # dark title bar

WIDTH = 380  # text wraps to this
APP_W = 460  # the window is this wide on every view and weapon, so nothing jumps when you switch

def label(parent, text, **kw):
    kw = {"font": (MONO, 9), "fg": MUTED2, "bg": parent.cget("bg"), "anchor": "w", "justify": "left", **kw}
    return tk.Label(parent, text=text, **kw)

def rule(parent, top=20, bottom=12):
    tk.Frame(parent, bg=LINE, height=1).pack(fill="x", pady=(top, bottom))

class Button(tk.Canvas):  # the design system's pill button: raised fill, hairline (or orange) stroke; tk.Label cannot round corners
    def __init__(self, parent, text, cmd, fg=MUTED, bg=INK2, outline=LINE, font=(MONO, 9), height=26, full=False):
        super().__init__(parent, bg=parent.cget("bg"), highlightthickness=0, cursor="hand2")
        self.text, self.cmd, self.fg, self.fill, self.outline = text, cmd, fg, bg, outline
        self.font, self.h, self.full = font, height, full
        self.bind("<Button-1>", lambda _: self.cmd and self.cmd())
        self.bind("<Enter>", lambda _: self.hover(ACCENT))  # the stroke goes orange under the pointer
        self.bind("<Leave>", lambda _: self.hover(self.outline))
        if full:
            self.bind("<Configure>", lambda _: self.draw())
        self.draw()
    def hover(self, color):  # swap to the pill drawn with that stroke colour
        self.hovering = color == ACCENT
        self.itemconfig("pill", image=self.imgs[self.hovering])
    def config(self, **kw):  # text / fg / fill / outline / cursor
        self.text, self.fg = kw.pop("text", self.text), kw.pop("fg", self.fg)
        self.fill, self.outline = kw.pop("bg", self.fill), kw.pop("outline", self.outline)
        tk.Canvas.config(self, **kw)
        self.draw()
    def draw(self):
        self.delete("all")
        h = self.h
        w = max(self.winfo_width(), 40) if self.full else tkfont.Font(font=self.font).measure(self.text) + 30
        tk.Canvas.config(self, height=h, **({} if self.full else {"width": w}))
        ground = self.cget("bg")
        self.imgs = [smooth_pill(w, h, fill=self.fill, bg=ground, stroke=edge) for edge in (self.outline, ACCENT)]  # normal, hover
        self.create_image(0, 0, image=self.imgs[getattr(self, "hovering", False)], anchor="nw", tags="pill")
        self.create_text(w / 2, h / 2, text=self.text, font=self.font, fill=self.fg)
button = Button

def open_repo():
    webbrowser.open(REPO_URL)

images = []  # tk drops an image that nothing in Python references, so keep every one
def header(parent, name, right_text, right_cmd):
    head = tk.Frame(parent, bg=INK)
    head.pack(fill="x")
    try:
        images.append(tk.PhotoImage(file=os.path.join(HERE, "icon-56.png")).subsample(2))
        tk.Label(head, image=images[-1], bg=INK).pack(side="left", padx=(0, 10))  # just the mark; VIEW SOURCE on How to opens GitHub
    except Exception:
        pass  # shortcut: no icon file, skip the mark
    label(head, name, font=(SANS_BLACK, 14), fg=FG).pack(side="left")  # the view's title: brand display face, sentence case
    button(head, right_text, right_cmd).pack(side="right")

pill_cache = {}  # a pill is only drawn once per size and colours; tk needs a reference kept to every image anyway
def smooth_pill(w, h, **kw):
    key = (w, h, tuple(sorted(kw.items())))
    if key not in pill_cache:
        pill_cache[key] = pill_image(tk, w, h, **kw)
    return pill_cache[key]

class GlowButton(tk.Canvas):  # the one orange fill per view: AutoClicker's primary pill with its orange-tinted glow
    GLOW, H = 20, 60  # glow reach, pill height (same as AutoClicker's state bar)
    def __init__(self, parent, text, cmd):
        super().__init__(parent, width=100, height=self.H + 2 * self.GLOW, bg=INK, highlightthickness=0, cursor="hand2")
        self.text, self.cmd = text, cmd
        self.bind("<Configure>", lambda _: self.draw())
        self.bind("<Button-1>", lambda _: self.cmd())
    def draw(self):
        self.delete("all")
        g, w = self.GLOW, self.winfo_width()
        if w < 2 * g + self.H:
            return  # not laid out yet
        # orange pill with a glow fading out over g px: peaks near 24% orange right at the edge
        self.img = smooth_pill(w, self.H + 2 * g, fill=ACCENT, bg=INK, glow=(ACCENT, 0.24, g), inset=g)
        self.create_image(0, 0, image=self.img, anchor="nw")
        self.create_text(w / 2, g + self.H / 2, text=self.text, font=(SANS_BLACK, 22), fill=INK)  # ink text on orange

# ---------- main view ----------
main = tk.Frame(root, bg=INK, padx=24, pady=20)
header(main, "Range Calculator", "HOW TO", lambda: show(guide))

chips = []  # (weapon, button) on both views, so the switch reads the same everywhere
def weapon_row(parent):
    row = tk.Frame(parent, bg=INK)
    row.pack(fill="x", pady=(22, 0))
    label(row, "WEAPON").pack(side="left")
    for key in ("artillery", "mortar"):  # packed right to left
        chip = button(row, key.upper(), lambda k=key: pick_weapon(k))
        chip.pack(side="right", padx=(6, 0))
        chips.append((key, chip))

def pick_weapon(key):
    settings["weapon"] = key
    for k, chip in chips:
        on = k == key
        chip.config(fg=INK if on else MUTED, bg=ACCENT if on else INK2, outline=ACCENT if on else LINE)  # the picked weapon is brand orange
    save_settings()
    if current is guide:
        build_guide()
    if result_shown:
        work()
    fit()

weapon_row(main)

rule(main, 18, 14)

def field(parent, caption, key):
    label(parent, caption).pack(fill="x")
    frame = tk.Frame(parent, bg=INK2, highlightthickness=1, highlightbackground=LINE)
    frame.pack(fill="x", pady=(6, 14))
    box = tk.Entry(frame, font=(SANS, 12), fg=FG, bg=INK2, insertbackground=FG, relief="flat", bd=0, highlightthickness=0)
    box.pack(fill="x", padx=12, pady=9)
    box.frame = frame
    box.bind("<FocusOut>", lambda _: frame.config(highlightbackground=getattr(box, "edge", LINE)))
    box.insert(0, settings[key])
    box.bind("<Return>", lambda _: work())
    box.bind("<FocusIn>", lambda _: (box.select_range(0, "end"), frame.config(highlightbackground=ACCENT)))  # click once, paste over the old point
    return box

box_a = field(main, "A · YOUR POSITION · X, Y", "a")
box_b = field(main, "B · TARGET · X, Y", "b")

go = GlowButton(main, "Enemy range  →", lambda: work())
go.pack(fill="x", pady=(0, 0))

# result: hidden until the first calculation
result = tk.Frame(main, bg=INK)
rule(result, 20, 14)
readouts = tk.Frame(result, bg=INK)
readouts.pack(fill="x")
readouts.columnconfigure((0, 1), weight=1, uniform="half")

def readout(col, caption, weight_font):
    cell = tk.Frame(readouts, bg=INK)
    cell.grid(row=0, column=col, sticky="w")
    label(cell, caption).pack(anchor="w")
    line = tk.Frame(cell, bg=INK)
    line.pack(anchor="w", pady=(4, 0))
    big = tk.Label(line, font=(weight_font, 34), fg=FG, bg=INK)
    big.pack(side="left")
    unit = tk.Label(line, font=(SANS, 13), fg=MUTED, bg=INK)
    unit.pack(side="left", anchor="s", pady=(0, 7), padx=(4, 0))
    return big, unit

rng_big, rng_unit = readout(0, "SET RNG", SANS_BLACK)
face_big, face_unit = readout(1, "FACE", SANS_MED)  # lighter than RNG: one bold value per card, and Face is untested in game
arc_line = label(result, "", fg=FG, font=(MONO_MED, 9))
note_line = tk.Label(result, font=(SANS, 10), fg=MUTED, bg=INK, anchor="w", justify="left", wraplength=WIDTH)
working = label(result, "")
error_line = tk.Label(main, font=(SANS_MED, 11), fg=ACCENT, bg=INK, anchor="w", justify="left", wraplength=WIDTH)

result_shown = False
def work():
    global result_shown
    settings.update(a=box_a.get(), b=box_b.get())
    save_settings()
    r = calculate(box_a.get(), box_b.get(), settings["weapon"])
    for box in (box_a, box_b):
        box.edge = LINE
        box.frame.config(highlightbackground=ACCENT if box is root.focus_get() else LINE)
    result.pack_forget(); error_line.pack_forget()
    if r.error:
        bad = box_a if r.error.startswith("Your") else box_b
        bad.edge = ACCENT
        bad.frame.config(highlightbackground=ACCENT)
        error_line.config(text=r.error)
        error_line.pack(fill="x", pady=(18, 0))
        result_shown = False
        fit()
        return
    rng_big.config(text=str(r.rng)); rng_unit.config(text="m")
    face_big.config(text=f"{r.face}°"); face_unit.config(text=compass_point(r.bearing))
    for w in (arc_line, note_line, working):
        w.pack_forget()
    if r.arc and not r.range_note:
        arc_line.config(text=r.arc.upper()); arc_line.pack(fill="x", pady=(10, 0))
    if r.range_note:
        note_line.config(text="●  " + r.range_note, fg=MUTED); note_line.pack(fill="x", pady=(10, 0))
    working.config(text=f"{r.meters:.2f} m = √({r.dx:.2f}² + {r.dy:.2f}²) × 100")
    working.pack(fill="x", pady=(8, 0))
    result.pack(fill="x")
    result_shown = True
    fit()

# ---------- how-to view (only the notes for the weapon you picked) ----------
guide = tk.Frame(root, bg=INK, padx=24, pady=20)
header(guide, "How to", "BACK", lambda: show(main))
weapon_row(guide)  # switch weapons here too; the steps below follow
guide_body = tk.Frame(guide, bg=INK)
guide_body.pack(fill="x")

COMMON_START = [
    ("01", "Mark both points", "On the map, zoom all the way in, right-click where you are and choose Mark Coordinates. Copy them from chat (Ctrl A, Ctrl C) into A. Do the same on the target for B."),
    ("02", "Enemy range", "Press Enemy range (or Enter). One map unit is 100 m, so A² + B² = C² gives the range in meters."),
]
GUIDES = {
    "mortar": {
        "steps": COMMON_START + [
            ("03", "Dial the range", "Zoom into the mortar sight. Move the barrel with W A S D for big moves and the mouse for small ones until RNG matches SET RNG. Take the nearest tick."),
            ("04", "Face and fire", "Turn until the compass at the top reads FACE. Watch the first round land and walk the next one in."),
        ],
        "reach": "Reach about 130 to 684 m.",
    },
    "artillery": {
        "steps": [
            ("01", "Crew and shells", "Three seats: driver, gunner, roof gunner. Park on flat ground and press B for 155 mm HE shells."),
            ("02", "Stabilize", "Scroll down at your firing spot until it no longer reads Unstabilized."),
        ] + [(f"0{int(n) + 2}", h, b) for n, h, b in COMMON_START] + [
            ("05", "Dial and face", "In the gunner's sight, set RNG to SET RNG and turn the compass to FACE. Under about 1,070 m only the high arc reaches."),
            ("06", "Fire and reload", "Press R right after firing, then press the W A S D prompts in the order shown. Walk the next shell in."),
        ],
        "reach": "Reach about 745 to 2,660 m. Unlocks at career level 90.",
    },
}
SIGHT = [  # one line each: where it sits in the sight, what it means
    ("RNG", "left · range in meters, match SET RNG"),
    ("MIL", "right · barrel tilt, follows RNG by itself"),
    ("N°", "top · compass heading, match FACE"),
]

def section(title, steps, top=20):
    rule(guide_body, top, 10)
    label(guide_body, title).pack(fill="x", pady=(0, 6))
    for num, head, body in steps:
        row = tk.Frame(guide_body, bg=INK)
        row.pack(fill="x", pady=(6, 0))
        label(row, num, width=4).pack(side="left", anchor="n", pady=(2, 0))
        text = tk.Frame(row, bg=INK)
        text.pack(side="left", fill="x", expand=True)
        tk.Label(text, text=head, font=(SANS_MED, 10), fg=FG, bg=INK, anchor="w").pack(fill="x")
        tk.Label(text, text=body, font=(SANS, 10), fg=MUTED, bg=INK, anchor="w", justify="left", wraplength=WIDTH - 44).pack(fill="x")

def build_guide():
    for w in guide_body.winfo_children():
        w.destroy()
    g = GUIDES[settings["weapon"]]
    section("MORTAR · L81" if settings["weapon"] == "mortar" else "ARTILLERY · SPH-2", g["steps"])
    rule(guide_body, 20, 10)
    label(guide_body, "READING THE SIGHT").pack(fill="x", pady=(0, 6))
    for key, text in SIGHT:
        row = tk.Frame(guide_body, bg=INK)
        row.pack(fill="x", pady=(4, 0))
        label(row, key, width=4, fg=FG).pack(side="left")
        tk.Label(row, text=text, font=(SANS, 10), fg=MUTED, bg=INK, anchor="w").pack(side="left")
    rule(guide_body, 16, 10)
    label(guide_body, g["reach"] + " From player guides. If a round lands on the wrong side, aim by eye.",
          wraplength=WIDTH).pack(fill="x")
    src_row = tk.Frame(guide_body, bg=INK)
    src_row.pack(fill="x", pady=(14, 0))
    label(src_row, f"v{VERSION} · open source").pack(side="left")
    button(src_row, "VIEW SOURCE", open_repo).pack(side="right")

# ---------- update stripe (bottom of main view, hidden until a newer release exists) ----------
upd_row = tk.Frame(root, bg=ACCENT, padx=24, pady=12)
upd_label = tk.Label(upd_row, text="", font=(MONO, 9), fg=FG, bg=ACCENT, anchor="w")
upd_label.pack(side="left", fill="x", expand=True)
upd_btn = button(upd_row, "UPDATE", lambda: install_update(), fg=FG, bg=INK)
upd_btn.pack(side="right")
latest = {}

# version, bottom-right corner, 9px; placed on top so nothing moves; show() hides it under the stripe
ver = tk.Label(root, text=f"v{VERSION}", font=(MONO, -9), fg=MUTED2, bg=INK, bd=0, padx=0, pady=0)

def install_update():
    upd_btn.config(text="DOWNLOADING", fg=MUTED, cursor="arrow")
    upd_btn.cmd = None
    def go():
        path = os.path.join(os.environ.get("TEMP", os.path.expanduser("~")), "RangeCalculator-Setup.exe")
        try:
            req = urllib.request.Request(latest["url"], headers={"User-Agent": "RangeCalculator"})
            with urllib.request.urlopen(req, timeout=30) as r, open(path, "wb") as f:
                shutil.copyfileobj(r, f)
            # the installer takes over; it closes this copy and replaces it. Drop PyInstaller's _PYI_* variables: the
            # installer would hand them to the new exe, which then takes itself for our child and refuses to start.
            subprocess.Popen([path], env={k: v for k, v in os.environ.items() if not k.startswith("_PYI_")})
            root.after(0, root.destroy)
        except Exception:
            root.after(0, lambda: (upd_btn.config(text="FAILED · RETRY", fg=FG, cursor="hand2"), setattr(upd_btn, "cmd", install_update)))
    threading.Thread(target=go, daemon=True).start()

def show_update():
    upd_label.config(text=f"v{latest['tag']} available")
    show(current)

def check_update():
    try:
        req = urllib.request.Request(f"https://api.github.com/repos/{REPO}/releases/latest", headers={"User-Agent": "RangeCalculator"})
        rel = json.load(urllib.request.urlopen(req, timeout=5))
        tag = rel["tag_name"].lstrip("v")
        if tuple(map(int, tag.split("."))) > tuple(map(int, VERSION.split("."))):
            latest.update(tag=tag, url=next(a["browser_download_url"] for a in rel["assets"] if a["name"].endswith("Setup.exe")))
            root.after(0, show_update)
    except Exception:
        pass  # offline, rate-limited, private repo or no release yet: say nothing

current = main
def show(view):
    global current
    current = view
    for w in (main, guide, upd_row):
        w.pack_forget()
    if view is guide:
        build_guide()
    view.pack(fill="x")
    if view is main and latest:
        upd_row.pack(side="bottom", fill="x")
        ver.place_forget()  # the stripe already names the versions
    else:
        ver.place(relx=1, rely=1, anchor="se", x=-14, y=-8)
        ver.lift()
    fit()

def fit():  # fixed width, height follows the content
    root.update_idletasks()
    root.geometry(f"{APP_W}x{root.winfo_reqheight()}")

pick_weapon(settings["weapon"])
show(main)
work()
threading.Thread(target=check_update, daemon=True).start()
root.mainloop()
