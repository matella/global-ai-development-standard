import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INTEGRATION = ROOT / "integrations" / "paperclip"
SKILLS = INTEGRATION / "skills"
ROLES = INTEGRATION / "roles"
EXPECTED_ROLES = {
    "software-engineer", "senior-software-engineer", "tech-lead", "software-architect",
    "qa-engineer", "security-reviewer", "documentation-specialist", "release-manager",
}
EXPECTED_SKILLS = {
    "gads-core", "gads-development", "gads-architecture", "gads-code-review",
    "gads-testing-qa", "gads-security-review", "gads-documentation", "gads-release-management",
}
# Backticked references to GADS files, for example `standard/WORKFLOW_AND_GATES.md`.
GADS_REF = re.compile(r"`((?:standard|templates|agents|scripts|docs|pilot)/[^`\s]+|AGENTS\.md)`")
SKILL_REF = re.compile(r"`(gads-[a-z-]+)`")
ROLE_SECTIONS = ["## Mission", "## Authority and limits", "## Expected deliverables",
                 "## Escalation conditions", "## Definition of Done"]


def frontmatter(text):
    if not text.startswith("---\n"):
        return {}
    head = text[4:].partition("\n---\n")[0]
    return {k.strip(): v.strip() for k, v in (line.split(":", 1) for line in head.splitlines() if ":" in line)}


class SkillTests(unittest.TestCase):
    def test_all_expected_skills_exist(self):
        self.assertEqual({p.name for p in SKILLS.iterdir() if p.is_dir()}, EXPECTED_SKILLS)

    def test_skill_frontmatter_matches_directory(self):
        for name in EXPECTED_SKILLS:
            with self.subTest(skill=name):
                fields = frontmatter((SKILLS / name / "SKILL.md").read_text(encoding="utf-8"))
                self.assertEqual(fields.get("name"), name)
                self.assertTrue(fields.get("description"), "description must not be empty")

    def test_skill_references_resolve_in_repository(self):
        for name in EXPECTED_SKILLS:
            text = (SKILLS / name / "SKILL.md").read_text(encoding="utf-8")
            refs = GADS_REF.findall(text)
            self.assertTrue(refs, f"{name} must reference canonical policies")
            for ref in refs:
                with self.subTest(skill=name, ref=ref):
                    self.assertTrue((ROOT / ref).is_file(), f"missing {ref}")

    def test_skills_declare_inputs_outputs_and_constraints(self):
        for name in EXPECTED_SKILLS:
            text = (SKILLS / name / "SKILL.md").read_text(encoding="utf-8")
            for section in ["## Purpose", "## Canonical policies", "## Inputs", "## Outputs", "## Constraints"]:
                with self.subTest(skill=name, section=section):
                    self.assertIn(section, text)


class RoleTests(unittest.TestCase):
    def role_files(self):
        return {p.stem: p for p in ROLES.glob("*.md")}

    def test_expected_roles_exist(self):
        self.assertEqual(set(self.role_files()), EXPECTED_ROLES)

    def test_roles_point_to_canonical_definitions_and_skills(self):
        for name, path in self.role_files().items():
            text = path.read_text(encoding="utf-8")
            with self.subTest(role=name):
                canonical = re.search(r"\*\*Canonical role:\*\* `(agents/[^`]+\.md)`", text)
                self.assertIsNotNone(canonical, "role must name its canonical agents/*.md file")
                self.assertTrue((ROOT / canonical.group(1)).is_file())
                skills = set(SKILL_REF.findall(text))
                self.assertTrue(skills, "role must list skills")
                self.assertLessEqual(skills, EXPECTED_SKILLS)
                for section in ROLE_SECTIONS:
                    self.assertIn(section, text)

    def test_roles_do_not_duplicate_canonical_definitions(self):
        for name, path in self.role_files().items():
            with self.subTest(role=name):
                # A thin wrapper stays short; the canonical procedure lives in agents/.
                self.assertLess(len(path.read_text(encoding="utf-8").splitlines()), 60)


class ExampleTests(unittest.TestCase):
    def test_example_hire_request_is_well_formed(self):
        path = INTEGRATION / "examples" / "hire-qa-engineer.example.json"
        request = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(request["adapterType"], "claude_local")
        self.assertEqual(request["instructionsBundle"]["entryFile"], "AGENTS.md")
        self.assertLessEqual(set(request["desiredSkills"]), EXPECTED_SKILLS)
        self.assertNotIn("dangerouslySkipPermissions", path.read_text(encoding="utf-8"))


class PlatformIndependenceTests(unittest.TestCase):
    def test_core_standard_does_not_mention_paperclip(self):
        core = [ROOT / "AGENTS.md", ROOT / "CLAUDE.md"]
        core += list((ROOT / "standard").glob("*.md")) + list((ROOT / "agents").glob("*.md"))
        core += list((ROOT / "templates").glob("*.md"))
        for path in core:
            with self.subTest(path=path.relative_to(ROOT).as_posix()):
                self.assertNotIn("paperclip", path.read_text(encoding="utf-8").lower())


if __name__ == "__main__":
    unittest.main()
