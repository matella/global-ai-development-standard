import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
FENCE = re.compile(r"^```.*?^```", re.M | re.S)


def anchors(path):
    """GitHub-style heading anchors of a Markdown file."""
    text = FENCE.sub("", path.read_text(encoding="utf-8"))
    headings = re.findall(r"^#+\s+(.+?)\s*$", text, re.M)
    return {re.sub(r"[^\w\- ]", "", h.lower()).replace(" ", "-") for h in headings}


class DocsLinkTests(unittest.TestCase):
    def test_relative_links_resolve(self):
        broken = []
        for doc in sorted(ROOT.rglob("*.md")):
            if ".git" in doc.parts:
                continue
            for target in LINK.findall(FENCE.sub("", doc.read_text(encoding="utf-8"))):
                if re.match(r"[a-z]+:", target):
                    continue
                path, _, anchor = target.partition("#")
                resolved = (doc.parent / path).resolve() if path else doc
                if not resolved.exists():
                    broken.append(f"{doc.relative_to(ROOT)}: {target}")
                elif anchor and resolved.suffix == ".md" and anchor not in anchors(resolved):
                    broken.append(f"{doc.relative_to(ROOT)}: {target} (missing anchor)")
        self.assertEqual(broken, [])


if __name__ == "__main__":
    unittest.main()
