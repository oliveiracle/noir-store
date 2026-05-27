"""
Forensic analysis: AI-generated vs student-written code.
Checks multiple dimensions that distinguish AI output from human code.
Run with: python check_ai_traces.py
"""

import os
import re
import ast
from collections import defaultdict

SKIP_DIRS = {'migrations', '.git', '__pycache__', 'venv', 'staticfiles', '.claude'}
SKIP_FILES = {'check_ai_traces.py'}

# ── Vocabulary frequently used by LLMs in comments/strings ──────────────────
AI_VOCAB = [
    r'\bensure\b', r'\brobust\b', r'\bleverage[sd]?\b', r'\bfacilitate[sd]?\b',
    r'\bseamlessly\b', r'\bstraightforward\b', r'\bcomprehensive\b',
    r'\befficiently\b', r'\belegant(ly)?\b', r'\boptimal(ly)?\b',
    r'\bsophisticated\b', r'\bsimply\b', r'\bintuitively\b',
    r'\bseemlessly\b', r'\bpowerful\b', r'\bflexible\b',
    r'\bconveniently\b', r'\baccordingly\b', r'\bnotably\b',
    r'\bmoreover\b', r'\bfurthermore\b', r'\badditionally\b',
    r'\bnevertheless\b', r'\bconsequently\b', r'\bultimately\b',
]

# ── Structural patterns typical of AI ────────────────────────────────────────
STRUCTURAL_PATTERNS = [
    r'""".*?"""',                        # triple-quoted docstrings
    r'# -{3,}',                          # separator comment lines
    r'# [A-Z][A-Z\s]{5,}:',             # ALL CAPS section headers
    r'# (Step|Phase|Part) \d+',          # numbered steps
    r'# (Note|TODO|FIXME|HACK|XXX):',   # tagged comments (OK but flag for review)
]

ai_vocab_pattern = re.compile('|'.join(AI_VOCAB), re.IGNORECASE)
struct_pattern = re.compile('|'.join(STRUCTURAL_PATTERNS), re.IGNORECASE | re.DOTALL)


def collect_py_files():
    files = []
    for root, dirs, filenames in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in filenames:
            if f.endswith('.py') and f not in SKIP_FILES:
                files.append(os.path.join(root, f))
    return files


def collect_js_files():
    files = []
    for root, dirs, filenames in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in filenames:
            if f.endswith('.js') and f not in SKIP_FILES:
                files.append(os.path.join(root, f))
    return files


def analyse_python(filepath):
    issues = []
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        source = f.read()
        lines = source.splitlines()

    # ── 1. Docstring on every function (AI tends to do this) ──────────────
    try:
        tree = ast.parse(source)
        funcs = [n for n in ast.walk(tree)
                 if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
        docstrings = sum(1 for f in funcs if ast.get_docstring(f))
        if funcs and docstrings / len(funcs) >= 0.9:
            issues.append(
                f"  [DOCSTRINGS] {docstrings}/{len(funcs)} functions have docstrings "
                f"({int(docstrings/len(funcs)*100)}%) — very high, typical of AI"
            )
    except SyntaxError:
        pass

    # ── 2. Comment-to-code ratio ──────────────────────────────────────────
    comment_lines = sum(1 for l in lines if l.strip().startswith('#'))
    code_lines = sum(1 for l in lines if l.strip() and not l.strip().startswith('#'))
    if code_lines > 0:
        ratio = comment_lines / code_lines
        if ratio > 0.4:
            issues.append(
                f"  [COMMENT DENSITY] {comment_lines} comment lines / {code_lines} "
                f"code lines = {ratio:.0%} — unusually high"
            )

    # ── 3. AI vocabulary in comments ─────────────────────────────────────
    ai_hits = []
    for i, line in enumerate(lines, 1):
        if line.strip().startswith('#') or '"""' in line:
            match = ai_vocab_pattern.search(line)
            if match:
                ai_hits.append(f"    line {i}: {line.strip()[:100]}")
    if ai_hits:
        issues.append(f"  [AI VOCAB] {len(ai_hits)} occurrence(s):")
        issues.extend(ai_hits[:5])
        if len(ai_hits) > 5:
            issues.append(f"    ... and {len(ai_hits)-5} more")

    return issues


def analyse_js(filepath):
    issues = []
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    comment_lines = sum(1 for l in lines if l.strip().startswith('//') or l.strip().startswith('/*'))
    code_lines = sum(1 for l in lines if l.strip() and not l.strip().startswith('//') and not l.strip().startswith('/*') and not l.strip().startswith('*'))

    if code_lines > 0:
        ratio = comment_lines / code_lines
        if ratio > 0.4:
            issues.append(
                f"  [COMMENT DENSITY] {comment_lines} comment lines / {code_lines} "
                f"code lines = {ratio:.0%} — unusually high"
            )

    ai_hits = []
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith('//') or stripped.startswith('/*') or stripped.startswith('*'):
            match = ai_vocab_pattern.search(stripped)
            if match:
                ai_hits.append(f"    line {i}: {stripped[:100]}")
    if ai_hits:
        issues.append(f"  [AI VOCAB] {len(ai_hits)} occurrence(s):")
        issues.extend(ai_hits[:5])

    return issues


def check_git_commits():
    """Check git log for co-authored-by or AI mentions."""
    import subprocess
    try:
        result = subprocess.run(
            ['git', 'log', '--pretty=%B'],
            capture_output=True, text=True
        )
        log = result.stdout.lower()
        hits = []
        for term in ['co-authored-by', 'claude', 'chatgpt', 'openai', 'anthropic', 'copilot']:
            if term in log:
                hits.append(term)
        return hits
    except Exception:
        return []


# ── MAIN ─────────────────────────────────────────────────────────────────────
print("\n" + "="*65)
print("  FORENSIC AI CODE ANALYSIS — NOIR STORE")
print("="*65)

total_flags = 0

# Python files
py_files = collect_py_files()
print(f"\n📂 Analysing {len(py_files)} Python files...\n")
for filepath in sorted(py_files):
    issues = analyse_python(filepath)
    if issues:
        total_flags += len(issues)
        print(f"⚠️  {filepath}")
        for issue in issues:
            print(issue)
        print()

# JS files
js_files = collect_js_files()
print(f"📂 Analysing {len(js_files)} JavaScript files...\n")
for filepath in sorted(js_files):
    issues = analyse_js(filepath)
    if issues:
        total_flags += len(issues)
        print(f"⚠️  {filepath}")
        for issue in issues:
            print(issue)
        print()

# Git commits
print("📂 Checking git commit history...\n")
git_hits = check_git_commits()
if git_hits:
    total_flags += len(git_hits)
    print(f"⚠️  Git log contains: {', '.join(git_hits)}\n")
else:
    print("✅ No AI mentions in git commit history.\n")

# Summary
print("="*65)
if total_flags == 0:
    print("✅ CLEAN — No significant AI patterns detected.")
elif total_flags <= 5:
    print(f"⚠️  LOW RISK — {total_flags} minor flags. Review individually.")
elif total_flags <= 15:
    print(f"🔶 MEDIUM RISK — {total_flags} flags. Some patterns worth cleaning.")
else:
    print(f"🔴 HIGH RISK — {total_flags} flags. Code has strong AI characteristics.")
print("="*65 + "\n")
