#!/usr/bin/env python3
"""v56 빌드: GitHub main의 docs/index.html(base_index.html) → 인쇄 양식(print_patch) → 화면(ui_patch) → docs/index.html.
test/index.html은 미리 보기용(구글 글꼴 대신 이 컴퓨터의 Noto CJK를 씀)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import print_patch, ui_patch
s = open(os.path.join(HERE, 'base_index.html'), encoding='utf-8').read()
s = print_patch.patch(s)
s = ui_patch.patch(s)
open(os.path.join(HERE, 'docs/index.html'), 'w', encoding='utf-8').write(s)
t = s.replace('<style>[hidden]{display:none!important}</style>', '<style>[hidden]{display:none!important}</style><link rel="stylesheet" href="/testfonts/testfonts.css">', 1)
assert t != s
open(os.path.join(HERE, 'docs/test.html'), 'w', encoding='utf-8').write(t)
print('ok', len(s.encode()))
