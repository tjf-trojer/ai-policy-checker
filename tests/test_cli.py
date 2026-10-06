#!/usr/bin/env python3
"""Run the scripts the way a user does, from outside the repository.

  python3 -m unittest discover tests

Standard library, offline. Each test copies what it needs into a temporary folder and runs the
script there, so nothing in the repository is written.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VERIFY = os.path.join(ROOT, "scripts", "verify.py")


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return fh.read()


def example(n):
    """Example n of examples.md, from its Source heading on."""
    part = re.split(r"(?m)^(?=# Example )", read("examples.md"))[n]
    return part[part.index("## Source"):].rstrip("\n-").rstrip() + "\n"


def run(args, cwd):
    p = subprocess.run([sys.executable] + args, cwd=cwd, stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT, universal_newlines=True)
    return p.returncode, p.stdout


class InputOutsideTheRepository(unittest.TestCase):
    """A register names its input relative to where the user runs the checker."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        reg = example(2).replace("| Input | `inputs/wikipedia-bot-policy.txt` |",
                                 "| Input | `my-policy.txt` |")
        with open(os.path.join(self.tmp, "my-register.md"), "w", encoding="utf-8") as fh:
            fh.write(reg)
        shutil.copy(os.path.join(ROOT, "inputs", "wikipedia-bot-policy.txt"),
                    os.path.join(self.tmp, "my-policy.txt"))

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_with_input(self):
        rc, out = run([VERIFY, "my-register.md", "--input", "my-policy.txt"], self.tmp)
        self.assertEqual(rc, 0, out)

    def test_without_input(self):
        rc, out = run([VERIFY, "my-register.md"], self.tmp)
        self.assertEqual(rc, 0, out)

    def test_input_that_is_another_file(self):
        shutil.copy(os.path.join(self.tmp, "my-policy.txt"), os.path.join(self.tmp, "other.txt"))
        rc, out = run([VERIFY, "my-register.md", "--input", "other.txt"], self.tmp)
        self.assertEqual(rc, 1, out)
        self.assertIn("names my-policy.txt, but --input is", out)


if __name__ == "__main__":
    unittest.main()
