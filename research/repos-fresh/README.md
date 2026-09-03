# repos-fresh/ —— 波語料(gitignored)

三波語料共存:fresh(2026-09-02,`../clone-manifest-fresh-wave.json`)、
DIRTY__*(dirty 波,`../clone-manifest-dirty-wave.json`)、
W370__*(rubric370 波,`../clone-manifest-rubric370-wave.json`)+ SECDOC__*.md(S-101 對抗語料)。

⚠️ untrusted clone,只做靜態分析,**絕不執行任何檔案**(Iron Rule 7)。

**2026-09-03 已修剪**(950M→18M,比照 inter-rater corpus 前例):每目錄只留
`**/SKILL.md` + repo 根 `README.md`(報告的行號錨仍可逐字驗)+ SECDOC 檔;
`.git`、腳本、資產全刪。**重建**:依各 manifest 的 commit 做**完整** clone
(shallow 只拿得到上游 HEAD;修剪後本地檔已不足以重跑 lint 的 packaging 面,
craft 行號錨不受影響)。
