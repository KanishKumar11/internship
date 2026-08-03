#!/usr/bin/env bash
# setup_merge_conflict_demo.sh
# Sets up BOTH merge conflict demos (slides 12 & 13) in a clean folder.
#
# Usage:
#   chmod +x setup_merge_conflict_demo.sh
#   ./setup_merge_conflict_demo.sh
#
# After running, you'll have two folders:
#   demo1_different_lines/   — for slide 12 (easy: auto-merge succeeds)
#   demo2_same_line/         — for slide 13 (hard: true conflict, markers shown)
#
# Each folder is a fresh git repo with two branches set up:
#   - main          (the starting point)
#   - teammate-branch (the "other person's" changes, already committed)
#
# To demo: switch to `main`, make YOUR edit, commit, then `git merge teammate-branch`
# and walk through what happens. Reset with `git merge --abort` if needed.
#
# Source: Day 3 slides 12 & 13 of the Zlaark Python Internship program.

set -e  # Exit on any error

echo "=========================================="
echo "  Day 3 · Merge Conflict Demo Setup"
echo "=========================================="
echo ""

# ─── DEMO 1: Different lines, same file (slide 12) ──────────────────────
echo "→ Setting up Demo 1: Different lines, same file..."
DEMO1="demo1_different_lines"
rm -rf "$DEMO1"
mkdir -p "$DEMO1"
cd "$DEMO1"

git init -q --initial-branch=main 2>/dev/null || git init -q && git branch -m main 2>/dev/null || true
git config user.name "Instructor"
git config user.email "instructor@zlaark.com"

# Create the starting README.md
cat > README.md << 'EOF'
# Day 3 Practice

Notes go here.

TODO:
- Add more notes
- Add contact info
EOF

git add README.md
git commit -q -m "Initial README with notes and TODO"

# Create the "teammate" branch with their edit (line 7)
git checkout -q -b teammate-branch
# Use sed to replace line 7 ("- Add contact info" → teammate's version)
sed -i 's/^- Add contact info$/- Add contact info (teammate marked this)/' README.md
git add README.md
git commit -q -m "Mark contact info line as mine"

# Back to main — instructor will edit line 3 live during the demo
git checkout -q main

cd ..
echo "  ✓ Demo 1 ready in $DEMO1/"
echo "    → During demo: edit line 3 of README.md, commit, then:"
echo "      git merge teammate-branch"
echo "    → Auto-merge should SUCCEED (different lines, no conflict)"
echo ""

# ─── DEMO 2: Same line, different content (slide 13) ────────────────────
echo "→ Setting up Demo 2: Same line, different content..."
DEMO2="demo2_same_line"
rm -rf "$DEMO2"
mkdir -p "$DEMO2"
cd "$DEMO2"

git init -q --initial-branch=main 2>/dev/null || git init -q && git branch -m main 2>/dev/null || true
git config user.name "Instructor"
git config user.email "instructor@zlaark.com"

# Create the starting README.md — line 3 is the contested line
cat > README.md << 'EOF'
# Day 3 Practice

Notes go here.

TODO:
- Add more notes
EOF

git add README.md
git commit -q -m "Initial README with placeholder notes line"

# Create the "teammate" branch — they change line 3 to their version
git checkout -q -b teammate-branch
cat > README.md << 'EOF'
# Day 3 Practice

My personal Day 3 notes.

TODO:
- Add more notes
EOF
git add README.md
git commit -q -m "Update notes line with personal version"

# Back to main — instructor will change line 3 to THEIR version live
git checkout -q main

cd ..
echo "  ✓ Demo 2 ready in $DEMO2/"
echo "    → During demo: edit line 3 of README.md to YOUR version, commit, then:"
echo "      git merge teammate-branch"
echo "    → Auto-merge should FAIL (same line, different content)"
echo "    → Show the <<<<<<< HEAD / ======= / >>>>>>> markers in VS Code"
echo "    → Use the Accept Current / Accept Incoming / Accept Both buttons"
echo "    → Then: git add README.md && git commit -m 'Resolve conflict'"
echo ""

# ─── Done ────────────────────────────────────────────────────────────────
echo "=========================================="
echo "  Setup complete."
echo "=========================================="
echo ""
echo "Two demo folders are ready. cd into either one to start."
echo ""
echo "  cd $DEMO1   # for slide 12 (easy: different lines)"
echo "  cd $DEMO2   # for slide 13 (hard: same line, true conflict)"
echo ""
echo "Tip: To reset either demo and try again, just re-run this script."
echo "     It deletes and recreates both folders from scratch."
