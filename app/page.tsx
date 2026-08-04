"use client";

import { useState } from "react";

const examples = [
  {
    title: "杯子 — 抓取任务",
    domain: "具身智能",
    vector: "物体 / 容器 / 可抓取",
    fibers: ["几何：圆柱形开口", "功能：盛装液体", "约束：保持竖直", "动作：从把手侧接近"],
    invariant: "容器功能与重力约束，在不同材质、尺寸与视角下保持可追踪。",
  },
  {
    title: "合同 — 风险审阅",
    domain: "知识工作",
    vector: "条款 / 义务 / 风险",
    fibers: ["角色：甲乙双方", "机制：交付—验收", "约束：违约责任", "关系：权利与义务映射"],
    invariant: "责任归属与条件触发关系，不应因措辞变化而丢失。",
  },
  {
    title: "治疗 — 方案迁移",
    domain: "科学与医疗研究",
    vector: "症状 / 干预 / 效果",
    fibers: ["因果：干预→响应", "条件：人群与剂量", "机制：靶点路径", "边界：证据等级"],
    invariant: "因果主张必须携带适用条件和证据边界。",
  },
];

const conceptCards = [
  ["01", "对象不只是位置", "语言对象可被理解为：一个 Base 上，随上下文激活的一组 Fiber。"],
  ["02", "结构需要可见", "机制、约束、角色与不变量，可能需要在推理时保持显式表达。"],
  ["03", "比较机制而非表面", "关注两个对象是否共享同一结构机制，而不只比较词面或向量距离。"],
  ["04", "面向可检验研究", "提出接口、基准与工程原型，让假设可以被形式化、验证与反驳。"],
];

export default function Home() {
  const [active, setActive] = useState(0);
  const item = examples[active];

  return (
    <main>
      <header className="topbar wrap">
        <a className="brand" href="#top" aria-label="LFB 首页"><span className="brand-mark">•••</span> LFB / OPEN RESEARCH</a>
        <nav aria-label="主导航"><a href="#idea">概念</a><a href="#example">示例</a><a href="#program">研究计划</a><a href="#collaborate">协作</a></nav>
      </header>

      <section className="hero wrap" id="top">
        <div className="hero-copy">
          <p className="eyebrow">VISUAL INTRODUCTION · V0.5</p>
          <h1>语言纤维束 <span>Language Fiber Bundle</span></h1>
          <p className="kicker">从向量表示到结构表示</p>
          <p className="thesis">向量定位语义。<br />纤维展开结构。<small>Vectors locate meaning. Fibers expose structure.</small></p>
          <p className="lead">LFB 是一项开放研究计划：探索在 Token / Vector 表示与高阶推理之间，是否需要一个显式的结构表示层。</p>
          <a className="button" href="#idea">探索研究假设 <span>↓</span></a>
        </div>
        <div className="hero-model" aria-label="向量表示和 LFB 结构表示的比较">
          <div className="model-head"><span>CONVENTIONAL</span><b>Vector representation</b></div>
          <div className="model-flow"><i>Token</i><em>↓</em><i>Embedding</i><em>↓</em><i>Similarity</i></div>
          <div className="model-head lfb"><span>LFB HYPOTHESIS</span><b>Structural representation</b></div>
          <div className="model-flow structural"><i>Base</i><em>↓</em><i className="fiber">Active fibers</i><em>↓</em><i>Mechanism & constraints</i></div>
          <p>不是替代既有表征；而是提出一个可研究、形式化与验证的结构层接口。</p>
        </div>
      </section>

      <section id="idea"><div className="wrap">
        <p className="eyebrow">THE CENTRAL QUESTION</p><h2>当推理依赖机制与约束，<br />结构是否应保持显式？</h2>
        <p className="section-intro">Embedding 擅长捕获大规模语义规律。LFB 假设，面向推理、记忆、迁移与治理的关键结构，或许需要一层能被直接表达、比较与操作的接口。</p>
        <div className="concept-grid">{conceptCards.map(([n, title, text]) => <article className="concept-card" key={n}><span>{n}</span><h3>{title}</h3><p>{text}</p></article>)}</div>
      </div></section>

      <section className="tint"><div className="wrap fiber-section">
        <div><p className="eyebrow">A MINIMAL INTERFACE</p><h2>Base 与 Fiber</h2><p className="section-intro">一个对象不是静止的标签，而是在特定上下文下，由稳定的基础坐标与被激活的结构维度共同描述。</p><p className="formula">L(x, c) = (B(x), F(x, c))</p></div>
        <div className="fiber-board"><div className="base-label">BASE</div><div className="fiber-cells"><div><b>身份</b><span>对象是什么</span></div><div><b>机制</b><span>如何发生</span></div><div><b>约束</b><span>什么必须成立</span></div><div><b>关系</b><span>与谁相关</span></div><div><b>不变量</b><span>什么保持不变</span></div><div><b>上下文</b><span>何时被激活</span></div></div></div>
      </div></section>

      <section id="example"><div className="wrap"><p className="eyebrow">INTERACTIVE EXAMPLE</p><h2>从“相似”走向“共享机制”</h2><p className="section-intro">切换对象，观察 LFB 如何把一个模糊的语义对象展开成可讨论的结构面。</p>
        <div className="example-panel"><div className="tabs" role="tablist">{examples.map((e, i) => <button role="tab" aria-selected={active === i} className={active === i ? "active" : ""} onClick={() => setActive(i)} key={e.title}>{e.domain}</button>)}</div>
          <div className="example-content"><div><p className="eyebrow">{item.domain}</p><h3>{item.title}</h3><p className="muted">传统向量视角可能浓缩为：</p><code>{item.vector}</code><p className="invariant"><b>可检验的不变量</b>{item.invariant}</p></div><div className="active-fibers"><p>ACTIVE FIBERS</p>{item.fibers.map((f) => <div key={f}>{f}</div>)}<p className="outcome">可进一步用于：结构比较 · 条件追踪 · 失败归因 · 迁移评估</p></div></div>
        </div>
      </div></section>

      <section id="program"><div className="wrap"><p className="eyebrow">OPEN RESEARCH PROGRAM</p><h2>LFB 不是完成的理论产品。<br />它是一套待检验的研究程序。</h2>
        <div className="program-grid"><article><span>TRACK 01</span><h3>形式化</h3><p>明确对象、映射、等价关系与可证明的边界条件。</p></article><article><span>TRACK 02</span><h3>验证</h3><p>构建 LFB-Struct20 Pilot、专家标注与结构相似性评价。</p></article><article><span>TRACK 03</span><h3>工程</h3><p>探索 Fiber 提取、结构记忆与 Fiber-enhanced RAG 原型。</p></article><article><span>TRACK 04</span><h3>治理</h3><p>研究结构可解释性、可审计性及跨域协作规范。</p></article></div>
      </div></section>

      <section className="tint" id="collaborate"><div className="wrap collaborate"><p className="eyebrow">COLLABORATIVE INFRASTRUCTURE</p><h2>开放的结构研究基础设施</h2><p className="section-intro">理论、实验与工程以独立且可连接的角色协作，形成可被检验的共同研究程序。</p><div className="ecosystem"><div>理论研究者</div><span>↘</span><div>AI Labs</div><strong>LFB<br />RESEARCH</strong><div>工程伙伴</div><span>↙</span><div>领域专家</div></div><div className="contribution"><b>欢迎贡献：</b>概念框架　·　形式化定义　·　基准设计　·　原型实现　·　领域案例　·　治理实验</div></div></section>

      <section className="closing wrap"><p className="eyebrow">AN OPEN INVITATION</p><blockquote>让结构成为<br />可被看见、讨论和检验的对象。</blockquote><p>LFB 是开放研究假设，不宣称替代 Transformer、Embedding、RAG 或既有 LLM 架构。</p></section>
      <footer className="wrap"><span>LANGUAGE FIBER BUNDLE · OPEN RESEARCH</span><span>Visual Introduction v0.5</span></footer>
    </main>
  );
}
