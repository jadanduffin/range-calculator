# Fundamentals: the cheat sheet

Look terms up here, or ask Claude:
"Using docs/FUNDAMENTALS.md, explain <term> with an example from my project."

You don't need to memorize any of this. You need to recognize it, so you can
direct an agent and notice when it is wrong.

---

## 1. The five principles

Every decision in a project traces back to these. Agents ignore all five by
default unless you ask for them.

| Principle | In one line | Why it matters more with AI | Say this to your agent |
|---|---|---|---|
| **Simplicity** | The smallest thing that solves the problem | Agents over-build: extra features, extra libraries, extra layers | "What is the simplest version that meets the spec? Remove anything else." |
| **Separation of concerns** | Each part does one job | Small, focused parts fit in context and can be fixed alone | "Which module owns this job? Don't put it anywhere else." |
| **Clarity and readability** | Code and plans a human can follow | You can't supervise what you can't read | "Explain this as if I've never coded. Rename anything unclear." |
| **Testability** | Every behavior can be checked automatically | Tests are how you know the agent is right, not just confident | "Write the test first. It must fail before you build." |
| **Defensive programming** | Check inputs where they enter; fail clearly | Agents write the happy path and forget the messy real world | "List every way the input could be wrong, and handle each one." |

---

## 2. Core vocabulary

| Term | Plain meaning |
|---|---|
| Program | Instructions a computer follows: input, processing, output |
| Function | A named, reusable step |
| Module | A file of related functions with one job |
| Variable | A named box holding a value |
| Data type | What kind of value: text (string), number, true/false (boolean), list, dictionary |
| Path | A file's address, like `renders/shot010_v003.exr` |
| Terminal | Typing commands to your computer instead of clicking |
| Virtual environment (venv) | A private toolbox for one project, so projects don't clash |
| Dependency / library | Code someone else wrote that your project borrows |
| Interface | What goes into a module and what comes out |
| Invariant | Something that must always be true |
| Test | A small program that checks your program |
| Bug / regression | Something wrong / something that used to work and broke |
| Log | A program's diary of what it did, for diagnosing problems |

---

## 3. How the web works

**Client and server.** The client (your browser) asks; the server answers.
A static HTML page needs no server: the browser opens the file directly.

**A web page in three layers**

| Layer | Job | CG analogy |
|---|---|---|
| HTML | Structure: what's on the page | The geometry |
| CSS | Look: colors, layout, type | The shading and lighting |
| JavaScript | Behavior: what happens when you click | The rig and animation |

**HTTP** is the language clients and servers speak. Each request has a method:

| Method | Meaning | Example |
|---|---|---|
| GET | Give me something | Load a page |
| POST | Here is something new | Add an item |
| PUT / PATCH | Change something | Update an item |
| DELETE | Remove something | Delete an item |

Each answer has a status code: **200** OK, **404** not found, **500** the server broke.

**API** (application programming interface): the menu of requests a system
accepts and what it returns. Usually JSON over HTTP.

---

## 4. Data and storage

| Format | Good for | Example |
|---|---|---|
| CSV | Simple tables people edit in a spreadsheet | A shot list |
| JSON | Nested data that programs pass around | An API response, a config file |
| SQLite | A real database in a single file; no server | A personal tool that outgrew its CSV |
| PostgreSQL | A database server for many users at once | A studio-wide tool |

Rule of thumb: files until it hurts, then SQLite, then a database server.

---

## 5. Architecture patterns

| Pattern | Shape | CG analogy | When to use |
|---|---|---|---|
| Pipeline | Data flows through steps in order | A Nuke comp tree | Batch tools: scan, process, write |
| Layered | Interface on top, logic in the middle, storage at the bottom; each layer only talks to its neighbor | Department handoffs: layout, anim, lighting, comp | Most apps that will grow |
| Client-server | A shared server, many clients | A render farm and its submitters | Anything multi-user or on the web |
| MVC (model, view, controller) | Data, display and input handling kept separate | The scene, the viewport and the tools | Interactive apps and web frameworks |

Many tools start as a pipeline. Keeping the output step separate lets them
become layered or client-server later without a rewrite.

---

## 6. Languages

| Language | What it's for | Where you'll see it |
|---|---|---|
| Python | General purpose, data, automation, servers | Maya, Houdini, Nuke, Blender and Unreal scripting |
| JavaScript | Anything that runs in a browser; also servers (Node.js) | Interactive web pages |
| TypeScript | JavaScript with types that catch mistakes early | Most serious web frontends |
| SQL | Asking questions of a database | Any tool with a database |
| C++ | Speed-critical code | Unreal Engine, renderers, plugins |
| HTML and CSS | Page structure and style (not programming languages) | Any web page |

---

## 7. Frameworks rundown

A framework is a prebuilt skeleton for one kind of app. It saves weeks, and costs
you its rules. **Pick one only when your project gives you a reason.**

| Category | Framework | Good for | Watch out for |
|---|---|---|---|
| Command-line tools | argparse (built into Python) | Small tools | Verbose for big CLIs |
| | Typer, Click | Larger CLIs with many commands | An extra dependency |
| Python web backends | Flask | Small, simple servers; easy to learn | You assemble the pieces yourself |
| | FastAPI | Modern APIs, automatic docs, type checking | Slightly more concepts up front |
| | Django | Big apps with users, admin pages and a database | Heavy for small tools |
| Quick Python interfaces | Streamlit, Gradio | Internal tools and demos in an afternoon | Hard to customize; not for products |
| Web frontends | React | The most common; huge ecosystem; agents know it best | Lots of concepts; easy to over-build |
| | Vue, Svelte | Gentler learning curves | Smaller ecosystems |
| Full stack | Next.js | React plus a server in one project | Many moving parts |
| Desktop apps | PySide / Qt | Native tools; also how Maya, Houdini and Nuke build their UIs | Desktop packaging is fiddly |
| | Electron, Tauri | Desktop apps built with web tech | Electron apps are large |
| Styling | Tailwind CSS | Fast, consistent styling with utility classes | Busy-looking HTML |
| Testing | pytest | Python tests | |
| | Vitest, Jest | JavaScript tests | |
| | Playwright | Testing a real browser end to end | Slower tests |
| Data | pandas | Tables, analysis, spreadsheets in code | Overkill for a small CSV |
| Databases from code | SQLAlchemy | Talking to SQL databases from Python | Learning curve |

### How to choose a stack

1. **Boring beats novel.** Popular, stable tools have the best docs, and agents know them best.
2. **Fewest moving parts.** Every framework and library is something to learn, update and debug.
3. **Choose for the next version, not version five.** v0.1 needs no framework; v1.0 might.
4. **Write the decision down.** An architecture decision record (ADR) says what you chose, what you rejected, and why.
5. **Signals you need a framework:** many users, a server, a database, an interactive UI, or you're rebuilding something a framework already does well.

---

## 8. Version control vocabulary

| Term | Plain meaning |
|---|---|
| Repository (repo) | A project folder with a memory |
| Commit | A save point with a message |
| Branch | A parallel version to try something safely |
| Merge | Bring a branch's changes back |
| Push / pull | Send to / fetch from GitHub |
| Pull request (PR) | "Please review and merge my branch" |
| Worktree | A second working copy of the same repo, for experiments or parallel agents |
| CI | GitHub runs your tests on every push |

---

## 9. Working with agents

- **Context is a budget.** Every file and message the agent reads costs time,
  money and accuracy. Keep CLAUDE.md short, point at files instead of pasting
  them, and start a fresh session for each task.
- **Value over volume.** Spend the agent on high-impact work: tests, risky
  modules, reviews. Don't burn hours polishing what nobody asked for.
- **Plans are cheap, code is expensive.** Argue with the plan, not the code.
- **The reviewer is not the author.** Critique in a fresh session.
- **Sustainable pace.** Short focused sessions beat marathons. When you are
  fighting the agent instead of directing it, stop and write down why.
