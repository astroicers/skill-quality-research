# G1 Review Summary(Gate G1 — 人工審查用)

- 產生時間:2026-08-16T07:54:50.637106+00:00  mode:offline-seeds-only
- 總 repo 數:32;rubric 樣本(A–D):22
- tier 分布:{'T1': 4, 'T2': 21, 'T3': 7}
- cohort 分布:{None: 32}(切點為提案值,請對照 created_at 分布確認)
- fame 分布:{None: 32}
- taxonomy 分布:{'A': 1, 'B': 6, 'C': 7, 'D': 8, 'E': 6, 'F': 4}
- domain 分布:{'design-ui': 3, 'dev-workflow': 12, 'memory-context': 1, 'meta-tooling': 11, 'research-analysis': 2, 'science': 1, 'security': 1, 'writing-content': 1}
- 純度樣本(F0 且 T2+):0 個 → []

## 待人工定案(TBD / 啟發式標籤)
- 無

## 抽樣方法記錄
```json
{
  "mode": "offline",
  "queries": [],
  "range_samples": []
}
```

## G1 檢查清單(BRIEF §3)
- [ ] 清單完整性(重要 repo 未遺漏;superpowers 現址已確認)
- [ ] taxonomy 分類正確(尤其 E/F 排除是否合理)
- [ ] 純度標籤 domain / fame / cohort 標注正確
- [ ] 四層抽樣分布合理(T0/T1 不可全是同類同域)
- [ ] verdict:approved / rejected(附修改指示)
