import os
import sys
import tempfile
import tomllib
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import install  # noqa: E402


class InstallTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.project = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def run_install(self, *args):
        with redirect_stdout(StringIO()):
            return install.main(["--project", str(self.project), *args])

    def read(self, rel):
        return (self.project / rel).read_text(encoding="utf-8")

    def test_all_targets_write_entry_points_that_resolve(self):
        self.assertEqual(self.run_install("--target", "all"), 0)
        for rel in [
            ".tmt/skills/tmt-gap-analysis/SKILL.md",
            ".tmt/skills/tmt-stride-catalog/references/catalog.md",
            ".tmt/agents/tmt-system-mapper.md",
            ".tmt/scripts/tmt_gate.py",
            ".agents/skills/tmt-gap-analysis/SKILL.md",
            ".agents/skills/tmt-gap-analysis/agents/openai.yaml",
            ".gemini/commands/tmt/gap-analysis.toml",
            ".cursor/rules/tmt.mdc",
            ".cursor/commands/tmt-write-tests.md",
            ".github/prompts/tmt-gap-analysis.prompt.md",
            ".opencode/command/tmt-gap-analysis.md",
            ".opencode/agent/tmt-test-writer.md",
            ".claude/skills/tmt-write-tests/SKILL.md",
            ".claude/agents/tmt-gap-analyst.md",
        ]:
            self.assertTrue((self.project / rel).is_file(), rel)
        # Every entry point references a skill file that exists in the installed kit.
        for rel in [".gemini/commands/tmt/write-tests.toml", ".opencode/command/tmt-write-tests.md",
                    ".github/prompts/tmt-write-tests.prompt.md", ".cursor/commands/tmt-write-tests.md"]:
            self.assertIn(".tmt/skills/tmt-write-tests/SKILL.md", self.read(rel))
        self.assertFalse(list(self.project.glob(".tmt/**/__pycache__")))

    def test_gemini_command_is_valid_toml_with_args(self):
        self.run_install("--target", "gemini")
        cmd = tomllib.loads(self.read(".gemini/commands/tmt/gap-analysis.toml"))
        self.assertIn("{{args}}", cmd["prompt"])
        self.assertTrue(cmd["description"])
        self.assertIn("tmt-agent:start", self.read("GEMINI.md"))

    def test_non_claude_targets_add_agents_md(self):
        self.run_install("--target", "cursor")
        self.assertIn(".tmt/skills/tmt-gap-analysis/SKILL.md", self.read("AGENTS.md"))

    def test_claude_only_leaves_agents_md_alone(self):
        self.run_install("--target", "claude")
        self.assertFalse((self.project / "AGENTS.md").exists())

    def test_agents_md_block_is_idempotent_and_keeps_user_content(self):
        (self.project / "AGENTS.md").write_text("# My rules\n\nUse tabs.\n", encoding="utf-8")
        self.run_install("--target", "agents-md")
        self.run_install("--target", "agents-md")
        text = self.read("AGENTS.md")
        self.assertTrue(text.startswith("# My rules\n\nUse tabs.\n"))
        self.assertEqual(text.count(install.BLOCK_START), 1)

    def test_does_not_overwrite_foreign_files_without_force(self):
        foreign = self.project / ".github/prompts/tmt-gap-analysis.prompt.md"
        foreign.parent.mkdir(parents=True)
        foreign.write_text("mine", encoding="utf-8")
        self.run_install("--target", "copilot")
        self.assertEqual(foreign.read_text(encoding="utf-8"), "mine")
        self.run_install("--target", "copilot", "--force")
        self.assertIn(install.MARK, foreign.read_text(encoding="utf-8"))

    def test_reinstall_overwrites_its_own_files(self):
        self.run_install("--target", "opencode")
        self.assertEqual(self.run_install("--target", "opencode"), 0)

    def test_opencode_agents_are_subagents_with_role_body(self):
        self.run_install("--target", "opencode")
        text = self.read(".opencode/agent/tmt-system-mapper.md")
        self.assertIn("mode: subagent", text)
        self.assertIn("## Method", text)
        self.assertNotIn("tools: Read", text)

    def test_unknown_target_rejected(self):
        with self.assertRaises(SystemExit), redirect_stderr(StringIO()):
            install.main(["--project", str(self.project), "--target", "vim"])


if __name__ == "__main__":
    unittest.main()
