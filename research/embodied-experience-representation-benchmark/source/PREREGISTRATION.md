# PREREGISTRATION — v0.1

本文件在所有调用之前冻结。禁止看到结果后新增 H4/H5、修改 oracle 或调整 λ/阈值。第一次 freeze 的 UTC 时间及 SHA256 见 FROZEN_INPUTS.json；本地时区 Asia/Shanghai。所有发现的错误写 INVALID_CASES.csv，并另存说明；旧版本保留。

## 冻结竞争假设

- H0 Trajectory Sufficiency：Raw ≈ Summary ≈ State-Change；完整轨迹足够，显式表示无独立增量。
- H1 Compression Hypothesis：Summary ≈ State-Change > Raw；压缩/去噪产生收益。
- H2 State-Change Hypothesis：State-Change > Summary/Raw；预期尤其见于 medium/far、失败恢复与 applicability boundary。
- H3 Overgeneralization Tradeoff：State-Change transfer ↑，Boundary refusal ↓；保留错误迁移风险。

不以 v0.1 显著性检验“证明”机制。

## 范围与规模

Track M 为唯一主 track，匹配事实；Track P 是 representation + extraction package diagnostic。T0 是源经验，不计为 evaluation；T1/T2 near、T3 medium、T4 structural/far、T5 boundary。20 families，100 evaluation cases。一次请求回答四个问题，因此 M 三重复为 900 calls。P 三重复另为 900；四组 controls 各 300，需单独授权预算。

本次仅 construction + 5-family smoke，每条件一重复。Smoke families F01、F04、F06、F15、F20 在运行前冻结。fixture 是软件验证，无资格支持 H0-H3。真实模型 smoke 必须固定同一 model/system/temperature/max output/question/oracle。temperature=0、seed=20261002（provider若不支持应在新预注册版本明确修订），max_output_tokens=600；不尝试不兼容接口后悄悄更换参数。

## 指标和分母

唯一 Primary：Q2 Transfer Action Accuracy，仅 T3/T4，正确动作数/有效且 API 成功的 T3/T4 condition 数。API 成功但 malformed 的输出计错；API failure 单独列出，绝不算成功，也不当作错误的模型行为。另报告 planned valid 条件数、API coverage、malformed 和 missing；任一正式组 coverage <100% 则决策 UNDETERMINED，避免剔除失败后美化结论。

Secondary：T1/T2 Q2、Q1 diagnosis、T5 Q3=NO 的 Boundary Refusal、全案例 Q3、T5 中 YES/PARTIAL 的 False Transfer、provider 返回的 input/output tokens、客户端延迟。Invalid output 在 refusal/judgment 中计错，无法确定 false transfer，因此 false-transfer 分母只纳入有效 response，并另报 boundary response coverage 与 malformed 数，不能视为安全拒绝。U=Primary−0.5×FalseTransferRate 只作 diagnostic。Q4 原文留存、不按流畅度评分。

所有比较按相同 case/repeat 配对，family 为 bootstrap 重采样单位（5000 draws、seed=20261002）。报告 paired mean difference 和 percentile 95% CI。Near 不进入 primary。重复不视为独立 family。

## 决策规则（正式 Track M 才有资格）

预先固定 practical difference δ=0.05；≈ 要求 paired 95% CI 完全落在 [-0.05,0.05]，> 要求点估计≥0.05且 CI 下限>0。单纯“不显著”不算等价。稳定要求 3 次 repeat 方向一致、family bootstrap 支持；样本不足归 UNDETERMINED。

优先判断：审计失败、oracle ambiguity、未完成真实模型 smoke、人类 Gate 缺失、run 不完整、coverage<100% → UNDETERMINED（工程 Gate 可 BLOCKED）。

- Continue A：C>B>A，并且 C−A 在 T3/T4 的 gain 大于 near 的 gain。
- Continue B：C>B≈A，并且 C 的 Boundary Refusal 与 B/A 差值 CI 下限≥−0.05。
- Continue C：C 的 transfer gain≥0.05且 CI 下限>0，同时相对 B 的 false transfer 增量≥0.05且 CI 下限>0；3 repeats 方向一致。视为稳定 tradeoff，进入 v0.2 专门研究风险，不称纯正向收益。
- Downgrade：B≈C>A，只允许结论“Experience compression matters.”
- Stop：A≈B≈C，三重复无≥0.05稳定 gain，停止把显式 State-Change 作为当前优先研究变量。
- 其他、不精确、冲突：UNDETERMINED。

C>B 但 boundary 恶化且 tradeoff 不稳定不能触发 Continue B。Track P/control 不得覆写 M 决策。

## 盲评分与 controls

同一 seeded randomization 打乱 condition/repeat 顺序，输出匿名 run IDs，映射单独存 BLIND_MAPPING.json。case-level scorer 只接收解析结果、case 和 oracle，不读表示映射；aggregate 才揭示组。开发者并非对渲染文本双盲。

C1 删除所有 typed headings（包含 Failure-State、Relevant Variable、State Change）保留顺序/事实；C2 seed=818+family number 打乱完整事实；C3 只反转显式 recorded change，保留其余内容，检验矛盾错误是否造成伤害；C4 给第+7（循环）family 的结构化经验，目标 oracle 不变。Controls 仅独立 M diagnostic，C3/C4 不要求 matched 正确事实。Harm 定义为同 case/repeat 的正确 C 动作准确率减 wrong-state 准确率，正值表示伤害；另列有害翻转（C对→wrong错）和修复翻转。

## 研究纪律

不删除负结果、boundary failure、失败请求；不修改 H0-H3，不用 Q4、tokens 或 U 替代 primary，不偷换 oracle，不用 P 冒充 M，不外推真机、AS-IR、Current State 或“表征塑造计算空间”。Report、Negative、Audit、Decision 独立展示；最大 claim 见 CLAIM_BOUNDARY.md。


## v0.1.1 pre-model-run repair amendment

本版本是在正式模型实验开始之前，由 F20_T5 oracle ambiguity 触发的 benchmark repair。没有看到任何真实模型实验结果，没有根据模型行为修改 benchmark。Repair is pre-model-run. H0/H1/H2/H3、Primary metric、Secondary metrics、λ、decision rules、randomization、smoke families 与 full-run规模均不变。原 PREREGISTRATION 内容逐字保留在本段之前，原文件另存 history/v0.1/PREREGISTRATION.md。

仅 F20_T5 的当前情景/动作与相应oracle理由改为新用户偏好未知时先获取偏好；不改源经验、A/B/C renderer或prompt。全量行为唯一性审核是额外 Gate，发现的非 F20 blocker只登记，不在本次越界修复。固定 fixture 只用于软件验证，不能支持任何研究假设。

本次禁止真实模型调用。Zcode下阶段只能提供 execution backend；模型snapshot与provider执行配置须执行前单独冻结且保持既有预算600、temperature0、seed20261002、1repeat。配置示例含占位符，不是可运行批准。Ready for real-model smoke 不代表 ready for full run；任何新blocker保持BLOCKED。


## v0.1.2 pre-model-run action-space repair amendment

Repair the action space, not the hypothesis. 本版本在任何真实模型实验之前修复Q2行为等效/多解。只见过离线固定fixture，未看过任何真实模型输出，未按模型表现修改数据或oracle。H0/H1/H2/H3、Primary/Secondary、λ/δ/CI、Continue/Downgrade/Stop/Undetermined规则、source experience、20families/120objects、Track M/P、representations、controls、smoke F01/F04/F06/F15/F20与75-call/900-call设计不变。

允许范围为100个evaluation的Q2候选、判别所需显式当前场景约束、对应oracle动作wording、新semantic tags/tests/audits。Source对象与source rendered facts不变；共享task_constraints含公开几何/阈值/顺序/用户状态，与任何representation无关。Q1、Q3、case goal、transfer level不改。Oracle新增correct_next_action_text，key沿用seeded slot，不改冻结理由/label。

34个原P0 case通过重写/显式条件消除动作多解；F11_T5按Option C公开invalid，原因是源关系along-guide可涵盖curved local following，不能仅改Q2保证NO解释唯一。它的canonical/oracle保留，外部INVALID_CASES记录；不修改源语义或NO标签，不按有效结果计分。当前99有效eval、1invalid，Primary40个T3/T4全部有效；Boundary有效19。所有报告显式展示数量，不宣称100个案例都已科学验证。

原5-family smoke不含F11，因此仍25有效eval×3representations×1repeat=75。Full设计仍900planned calls；若未来获准，F11对应9条件保留planned记录并排除评分，必须公开invalid，不改变valid-case分母定义。当前只有Ready for real-model smoke only, NOT ready for full run的工程资格；不代替人工授权。

typed audit以公开的synthetic constraints判断动作兼容性，不以oracle key或预填correct标签判定。标准包括参数/操作行为、contextual normalization、执行前失败后未执行后缀、无成本extra step、真实goal reversal与未知参数。不同binary成功率不是behavioral distinctness的必要条件；关键指令变量/可观测trace必须可区分。

显式约束可能让题目更容易，数值/场景事实只为消歧，真实性与难度未经实证；不得把修复解释为representation增益或维持难度的证据。所有新增信息对A/B/C相同。Research Decision继续UNDETERMINED。模型配置仍未执行，GLM/API/full/真机均禁止在本任务调用。


## Explicit v0.1.3 compatibility and measurement erratum

The preceding text remains the historical preregistration. Before any v0.1.3 rerun, the malformed-as-incorrect implementation is superseded by SCORING_DENOMINATOR_SPEC.md: only API-success, provider-complete, schema-valid final answers of eligible cases enter scientific denominators. This corrects measurement, not Primary/Secondary definitions. HTTP 200 length/empty-final and format failures are execution failures, never scientific incorrectness. Zero valid responses means NONE/null.

Historical 600-token cap and zero retries are superseded for this execution release by PROVIDER_QUALIFICATION_SPEC.md: independent non-benchmark cap qualification, one frozen uniform cap, <=2 API-only retries, no malformed/completion retries. No benchmark content was tuned from model outputs. No valid scientific model result exists. H0/H1/H2/H3, Primary T3/T4 Q2, secondary metrics, lambda and Continue/Downgrade/Stop/Undetermined rules remain unchanged. Resource readiness plus separate human approval are required for the same 75-call smoke; no full run authorized.
