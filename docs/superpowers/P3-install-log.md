# P3 安裝紀錄

## ⚠️ 升級會覆蓋(fix round 2 C2 finding,2026-08-17 補記)

**`~/.claude/asp/` 不是原始碼,是安裝產物。** 來源是獨立 git repo
`/home/ubuntu/AI-SOP-Protocol`,其 `scripts/install.sh` 在複製階段會對
`profiles/hooks/templates/levels/config/scripts/advanced` 逐一 `rm -rf` 再整個複製覆蓋
——**含本次改動的 `profiles/pipeline.md` 與 `config/rule-registry.yaml`**。

已查證(2026-08-17):installed `~/.claude/asp/VERSION` = `5.0.0`,repo
`/home/ubuntu/AI-SOP-Protocol/.asp/VERSION` = `5.1.0`——**升級已逾期**。只要之後跑一次
ASP 升級(不論是誰、是否知情),本次加入的 G5 skill 子句與兩條 `GATE-G5-SKILL-*` 規則
會被**無聲清除**,不會有任何錯誤或警告訊息。

**`.bak` 不可用於升級後還原**:`~/.claude/asp/profiles/pipeline.md.bak` 與
`~/.claude/asp/config/rule-registry.yaml.bak` 是 2026-08-16 當時(installed VERSION=5.0.0)的
快照,只反映「加 skill 子句前」的 5.0.0 狀態。升級後如果拿 `.bak` 蓋回去,等於把整個安裝
**降版**回 5.0.0(遺失 5.0.0→5.1.0 之間的所有官方修正),不是安全的還原手段。

**如何重新套用(升級後手動執行)**:

1. 確認升級後 `profiles/pipeline.md` 的 `FUNCTION evaluate_G5` 內沒有 `// P3: skill-reviewer`
   子句(`/usr/bin/grep -n "P3: skill-reviewer" ~/.claude/asp/profiles/pipeline.md`)。
2. 若沒有,依 spec §3.2 的完整 pseudocode(見
   `docs/superpowers/specs/2026-08-16-skill-reviewer-asp-g5-design.md` §3.2)手動貼回
   `evaluate_G5` 函式尾段(`checks.append("Skill packaging 剖面...")` 之前的 `IF issues:` 之上)。
3. 確認 `config/rule-registry.yaml` 有 `GATE-G5-SKILL-HYGIENE` 與 `GATE-G5-SKILL-CRAFT` 兩條
   (`/usr/bin/grep -n "GATE-G5-SKILL" ~/.claude/asp/config/rule-registry.yaml`)。
4. 若沒有,依 spec §3.4 的完整 yaml(同上檔案 §3.4)手動貼回
   `rules:` 清單,放在 `GATE-G6` 之後、`DENY-01` 之前的 G5 skill 品質檢查區塊。
   注意 `GATE-G5-SKILL-HYGIENE` 的 `observed_by` 是 `manual`(非 `gate-log`,見 spec §3.4 說明)。
5. 用 `/usr/bin/diff` 對照 spec §3.2/§3.4 的內容與重新套用後的檔案,確認完全一致。
6. 跑 `cd ~/skill-quality-research && python3 skill-reviewer/scripts/lint_skill.py --selftest`
   確認綠燈。

**長期正解**(未執行,超出本次授權範圍,見 spec §11):應把這兩處改動提交進
`/home/ubuntu/AI-SOP-Protocol` repo 本身,走該 repo 自己的 ADR/gate 流程,而不是留在使用者
本機的安裝副本上。

---

- 2026-08-16 skill-reviewer 全域安裝(symlink)
  `~/.claude/skills/skill-reviewer` → `~/skill-quality-research/skill-reviewer`
- 驗證:全域路徑 selftest 通過;缺席情境 exit=2 可被偵測

- 2026-08-16 Task 2: pipeline.md evaluate_G5 加入 skill 子句(備份 pipeline.md.bak)
- 2026-08-16 Task 3: rule-registry.yaml 登記 GATE-G5-SKILL-HYGIENE / -CRAFT
