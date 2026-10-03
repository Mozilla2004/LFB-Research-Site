# Experiment design

唯一实验变量为 source experience representation（Track M）。Canonical source 保存原始 task/environment/attempt/correction/state/applicability 以及 12 个独立审计文本 atoms。Raw 按 Observation→Action→Failure→Correction→Revised Action→Outcome 展开，附源记录中的适用条件等 notes；不添加因果解释标签。Summary 将同样 sentences 连成普通自然语言，删除标题换行；这是保守、轻量的格式压缩，不是自由生成摘要。State-Change 用规定的八类标题组织同样事实。每条 C 信息在 B 完整出现。由于 Raw 在 matched 条件也需含边界记录，它不是未经整理的真实机器人日志。

Track P 的 A/B 删去五条 extracted annotations（variable、failure_state、change、positive、negative）；C 全保留。删除内容中部分已由 trajectory 隐含，因此 package 差异不能直接量化 extraction 的纯效应。两条 track 的 source 内容和全部 evaluation oracle 在调用前冻结。

Canonical evaluation 不含正确答案；下一动作四个候选 shuffled；Q1 候选去重后数量可不同，Q2 始终四个候选。Q3 YES/PARTIAL/NO 的 operational definition 固定在 prompt。Q4 只保存短说明，不索取隐藏 chain of thought。

Near 更换同类 target；medium 更换 object/task context；far 用同类约束关系到检查桅杆、结构部件、滑轨、虚拟界面等领域。当前 far 是人工指定的结构代理，无经验标定。T3/T4 明示要适配当前尺寸，故 Q3 的 PARTIAL 具有任务提示，不能把这个指标解释为自主发现迁移距离。T5 是明确禁止机械复用的约束反例。

数据生成是人工目录+确定性 generator，未让被测模型生成数据/oracle。生成规则假定 positive 条件使 correction 成功，negative 条件要求 alternative；这属于 synthetic world stipulation，不是物理规律证明。所有源成功都只有一次示范，不能推出单一变量因果性。

一次 call 固定四个问题；模型可利用候选与 Q3 定义，该 shared cue 对各组相同，但可能导致 ceiling、shortcut 和弱 representation 差异。没有 no-experience baseline；v0.1 不能独立估计经验相对无经验的绝对效用。

盲评分只保证 case-level 不依赖组标签。Raw 留下全文和 runtime；failed request 同样持久化。每次运行独立目录，禁止覆盖；失败无自动重试，crash 留已写 records 和 planned index，audit 判 incomplete。
