#!/usr/bin/env python3
"""Install TMT-Agent into a project for coding agents other than the native plugins.

Copies the kit (skills, role files, templates, scripts) to <project>/.tmt/ and writes the
thin per-tool entry points that point back at it, so every tool runs the same instructions.

Usage:
    install.py --project ../my-app --target codex,gemini
    install.py --project . --target all

Targets:
    agents-md  AGENTS.md block (Codex, Cursor, Copilot, OpenCode, Zed, Windsurf, Amp, ...)
    codex      .agents/skills/ wrappers           ($tmt-gap-analysis)
    gemini     .gemini/commands/tmt/ + GEMINI.md  (/tmt:gap-analysis)
    cursor     .cursor/rules + .cursor/commands   (/tmt-gap-analysis)
    copilot    .github/prompts/                   (/tmt-gap-analysis in VS Code chat)
    opencode   .opencode/command + .opencode/agent (/tmt-gap-analysis, @tmt-system-mapper)
    claude     .claude/skills + .claude/agents    (for teams not using the plugin)

Every non-claude target also writes the AGENTS.md block. Generated files carry the marker
"tmt-agent:generated"; existing files without it are left alone unless --force is given.
"""
import argparse
import re
import shutil
import sys
from pathlib import Path

KIT_SRC = Path(__file__).resolve().parent.parent
KIT_DIRS = ("agents", "skills", "templates", "scripts")
KIT = ".tmt"
MARK = "tmt-agent:generated"
BLOCK_START = "<!-- tmt-agent:start -->"
BLOCK_END = "<!-- tmt-agent:end -->"
TARGETS = ("agents-md", "codex", "gemini", "cursor", "copilot", "opencode", "claude")

# name -> (skill directory, short description for command menus)
COMMANDS = {
    "gap-analysis": ("tmt-gap-analysis", "Find STRIDE threats with no test proving the control works"),
    "write-tests": ("tmt-write-tests", "Write the missing TMT security tests and report findings"),
}

AGENTS_BLOCK = f"""{BLOCK_START}
## TMT-Agent (Threat Modeling Testing)

This repo has the TMT-Agent kit in `{KIT}/`. When asked which security tests are missing,
to check tests against a threat model or STRIDE, or to write security tests for TMT IDs
(e.g. `T-API-01`), read and follow the matching skill. Its `KIT` path is `{KIT}`.

- Gap analysis: `{KIT}/skills/tmt-gap-analysis/SKILL.md` (writes `tmt-report/`)
- Write missing tests: `{KIT}/skills/tmt-write-tests/SKILL.md`
- Scenario catalog: `{KIT}/skills/tmt-stride-catalog/SKILL.md`
- CI gate: `python3 {KIT}/scripts/tmt_gate.py tmt-report/gaps.json --fail-on high`
{BLOCK_END}
"""


def frontmatter(path):
    """Return (fields, body) for a Markdown file with simple `key: value` front matter."""
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        return {}, text
    fields = {}
    for line in m.group(1).splitlines():
        key, sep, value = line.partition(":")
        if sep:
            fields[key.strip()] = value.strip()
    return fields, m.group(2)


def run_skill(skill, args_placeholder=None):
    text = (f"Read `{KIT}/skills/{skill}/SKILL.md` and follow it exactly. "
            f"Its `KIT` path is `{KIT}`; resolve every path it mentions from there.")
    if args_placeholder:
        text += f"\n\nArguments: {args_placeholder}"
    return text


class Installer:
    def __init__(self, project, force=False):
        self.project = project
        self.force = force
        self.written, self.skipped = [], []

    def write(self, rel, content):
        path = self.project / rel
        if path.exists() and MARK not in path.read_text(encoding="utf-8") and not self.force:
            self.skipped.append(rel)
            return
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        self.written.append(rel)

    def block(self, rel, block=AGENTS_BLOCK):
        """Insert or replace the marked block in a shared instructions file."""
        path = self.project / rel
        text = path.read_text(encoding="utf-8") if path.exists() else ""
        pattern = re.compile(re.escape(BLOCK_START) + ".*?" + re.escape(BLOCK_END) + r"\n?", re.S)
        if pattern.search(text):
            text = pattern.sub(lambda _: block, text)
        else:
            text = (text.rstrip() + "\n\n" if text.strip() else "") + block
        path.write_text(text, encoding="utf-8")
        self.written.append(rel)

    def kit(self):
        for name in KIT_DIRS:
            dest = self.project / KIT / name
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(KIT_SRC / name, dest,
                            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        self.written.append(f"{KIT}/")

    def skills(self):
        return sorted(p.parent for p in (KIT_SRC / "skills").glob("*/SKILL.md"))

    def roles(self):
        return sorted((KIT_SRC / "agents").glob("*.md"))

    # --- targets ---------------------------------------------------------------

    def agents_md(self):
        self.block("AGENTS.md")

    def codex(self):
        for skill_dir in self.skills():
            fields, _ = frontmatter(skill_dir / "SKILL.md")
            name = skill_dir.name
            self.write(f".agents/skills/{name}/SKILL.md",
                       f"---\nname: {name}\ndescription: {fields['description']}\n---\n"
                       f"<!-- {MARK} -->\n\n{run_skill(name)}\n")
            yaml = skill_dir / "agents" / "openai.yaml"
            if yaml.exists():
                self.write(f".agents/skills/{name}/agents/openai.yaml",
                           f"# {MARK}\n" + yaml.read_text(encoding="utf-8"))

    def gemini(self):
        for cmd, (skill, desc) in COMMANDS.items():
            prompt = run_skill(skill, "{{args}}")
            self.write(f".gemini/commands/tmt/{cmd}.toml",
                       f'# {MARK}\ndescription = "{desc}"\nprompt = """\n{prompt}\n"""\n')
        self.block("GEMINI.md")

    def cursor(self):
        self.write(".cursor/rules/tmt.mdc",
                   "---\ndescription: Threat Modeling Testing. Use when asked about missing security "
                   "tests, STRIDE coverage, threat models, or TMT IDs like T-API-01.\nalwaysApply: false\n---\n"
                   f"<!-- {MARK} -->\n\n" + AGENTS_BLOCK.replace(BLOCK_START + "\n", "").replace(BLOCK_END + "\n", ""))
        for cmd, (skill, _) in COMMANDS.items():
            self.write(f".cursor/commands/tmt-{cmd}.md",
                       f"<!-- {MARK} -->\n{run_skill(skill)}\n\nUse any text after the command as the skill's arguments.\n")

    def copilot(self):
        for cmd, (skill, desc) in COMMANDS.items():
            self.write(f".github/prompts/tmt-{cmd}.prompt.md",
                       f"---\nagent: 'agent'\ndescription: '{desc}'\n---\n<!-- {MARK} -->\n\n"
                       f"{run_skill(skill, '${input:args:optional arguments}')}\n")

    def opencode(self):
        for cmd, (skill, desc) in COMMANDS.items():
            self.write(f".opencode/command/tmt-{cmd}.md",
                       f"---\ndescription: {desc}\n---\n<!-- {MARK} -->\n\n{run_skill(skill, '$ARGUMENTS')}\n")
        for role in self.roles():
            fields, body = frontmatter(role)
            self.write(f".opencode/agent/{role.name}",
                       f"---\ndescription: {fields['description']}\nmode: subagent\n---\n<!-- {MARK} -->\n{body}")

    def claude(self):
        for skill_dir in self.skills():
            fields, _ = frontmatter(skill_dir / "SKILL.md")
            name = skill_dir.name
            self.write(f".claude/skills/{name}/SKILL.md",
                       f"---\nname: {name}\ndescription: {fields['description']}\n---\n"
                       f"<!-- {MARK} -->\n\n{run_skill(name)}\n")
        for role in self.roles():
            self.write(f".claude/agents/{role.name}",
                       role.read_text(encoding="utf-8").replace("\n---\n", f"\n---\n<!-- {MARK} -->\n", 1))


def parse_targets(value):
    targets = list(TARGETS) if value == "all" else [t.strip() for t in value.split(",") if t.strip()]
    unknown = sorted(set(targets) - set(TARGETS))
    if unknown:
        raise argparse.ArgumentTypeError(f"unknown target(s): {', '.join(unknown)}")
    if any(t != "claude" for t in targets) and "agents-md" not in targets:
        targets.insert(0, "agents-md")
    return targets


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--project", type=Path, required=True, help="project to install into")
    parser.add_argument("--target", type=parse_targets, required=True,
                        help=f"comma-separated: {', '.join(TARGETS)}, or 'all'")
    parser.add_argument("--force", action="store_true", help="overwrite files not created by TMT-Agent")
    args = parser.parse_args(argv)

    project = args.project.resolve()
    if not project.is_dir():
        print(f"install: {project} is not a directory", file=sys.stderr)
        return 2
    if project == KIT_SRC:
        print("install: refusing to install TMT-Agent into itself", file=sys.stderr)
        return 2

    inst = Installer(project, args.force)
    inst.kit()
    for target in args.target:
        getattr(inst, target.replace("-", "_"))()

    print(f"TMT-Agent installed into {project} for: {', '.join(args.target)}")
    for rel in inst.written:
        print(f"  wrote   {rel}")
    for rel in inst.skipped:
        print(f"  skipped {rel} (exists and wasn't created by TMT-Agent; use --force)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
