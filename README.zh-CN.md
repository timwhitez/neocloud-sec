# NeoCloud Cyber Security

简体中文 | [English](README.md)

面向专业 AI/GPU 云的厂商中立安全基线、参考架构、路线图与实践指南。

**基础版本：** `1.0.0-draft.1`  
**公开问题画像：** `1.0.1`  
**最近范围内复核：** 2026-09-09

这是文档与校验工具项目，不是可部署的安全控制平面、认证体系，也不能证明某服务商已经安全。“NeoCloud”是行业工作术语，应明确真实服务和信任边界，不能根据名称推断安全属性。

## 从这里开始

| 目标 | 中文 | English |
|---|---|---|
| 理解风险与运营模型 | [白皮书](docs/zh-CN/WHITEPAPER.md) | [White paper](docs/en/WHITEPAPER.md) |
| 评估 18 个安全域、90 项控制 | [安全基线](docs/zh-CN/SECURITY_BASELINE.md) | [Baseline](docs/en/SECURITY_BASELINE.md) |
| 实施并运营控制 | [实践指南](docs/zh-CN/PRACTICE_GUIDE.md) | [Practice guide](docs/en/PRACTICE_GUIDE.md) |
| 设计身份、租户与执行边界 | [参考架构](docs/zh-CN/REFERENCE_ARCHITECTURE.md) | [Architecture](docs/en/REFERENCE_ARCHITECTURE.md) |
| 分阶段交付 | [路线图](docs/zh-CN/ROADMAP.md) | [Roadmap](docs/en/ROADMAP.md) |
| 定义证据、度量与验证 | [度量与持续证明](docs/zh-CN/METRICS_AND_ASSURANCE.md) | [Assurance](docs/en/METRICS_AND_ASSURANCE.md) |
| 核对公开问题与执行授权验证 | [覆盖审计与验证指南](docs/zh-CN/SEMIANALYSIS_COVERAGE.md) | [SemiAnalysis coverage](docs/en/SEMIANALYSIS_COVERAGE.md) |
| 验证运行态、撤权、存储与遥测边界 | [验证手册](docs/zh-CN/VALIDATION_RUNBOOKS.md) | [Validation runbooks](docs/en/VALIDATION_RUNBOOKS.md) |
| 校验证据与公告记录一致性 | [证据与公告记录校验](docs/EVIDENCE_VALIDATION.md) | [Evidence validation](docs/EVIDENCE_VALIDATION.md) |
| 明确局限 | [范围与局限](docs/zh-CN/SCOPE_AND_LIMITATIONS.md) | [Scope](docs/en/SCOPE_AND_LIMITATIONS.md) |

研究成果直接迭代上述文档和工具。[贡献流程](CONTRIBUTING.md#recurring-research)定义来源复核、缺口判断及先 PR 后合并，[CHANGELOG.md](CHANGELOG.md)记录普通项目变更。日期化决策与测试证据留在对应 PR／Issue，不另建平行周更文档系列；本项目不安装后台任务或调度器。

## 项目包含什么

基础目录保留 90 个稳定控制 ID：T0=32、T1=31、T2=19、T3=7、T4=1。服务画像覆盖 GPU IaaS、裸金属、托管 Kubernetes、Slurm/HPC、模型训练、模型服务、Agent 和主权/受监管部署。

独立的 SemiAnalysis/ClusterMAX 覆盖层包含 **40 项本项目拆分的原子映射**，以及**有日期的公开 Security 页面快照的 20/20 项映射**。映射不等于实施、执行测试、认证、背书或完整复刻专有框架。逐项历史覆盖分类为 **21 项明确覆盖 / 12 项部分覆盖 / 7 项缺口**，而非此前错误摘要；证据见[范围内审计](reviews/2026-09-05-validation-audit.md)。

请结合[核心控制](controls/neocloud-security-baseline.v1.json)、[规范勘误](controls/neocloud-security-baseline.v1.errata.json)、[公开问题画像](controls/semianalysis-public-findings-profile.v1.json)及[模板](templates/README.md)使用，不能导入原始目录却静默忽略适用勘误。

## 运营规则

每个适用 T0 都必须独立验证为 `VERIFIED`。失败、未知、过期、无法判断或未测试的 T0 仍为 `NO_GO_NONCONFORMANT`，业务风险决定不能改变控制结果。实现与验证是不同阶段：

```text
PROPOSED → READY → IMPLEMENTED → CANDIDATE_DONE → VERIFIED
```

服务商独占的控制面、Host/GPU Reset、Fabric Manager、BMC/OOB 和签名/密钥根仍由服务商负责。计算、存储、Fabric、可观测性和支持路径要分别验证。Agent 输出不能授予权限。恢复必须重建身份、完整性和租户隔离，而不仅是恢复可用性。

## 本地校验——不依赖 Actions

使用完整检出及 Python 3.10+。前两项旧仓库校验器使用标准库；严格 Schema 校验依赖声明的包。安装是独立准备步骤，不会隐藏在校验程序的网络操作中。

```bash
python3 -m pip install -r requirements-validation.txt
python3 scripts/check_local.py
```

本地入口运行三项仓库校验并发现单元/负向测试。缺依赖或缺文件会失败，不会跳过后显示绿色；也不会探测基础设施。离线环境应通过组织批准的流程预置依赖。Actions 额度受限期间，工作流保持仅手动触发，不得调度或重跑。

在不修改源文件的情况下生成应用勘误后的目录：

```bash
python3 scripts/compile_catalog.py > /tmp/neocloud-effective-catalog.json
```

输出含 `catalog` 和 SHA-256 来源标识，不是部署安全证明。可选离线[证据与公告校验器](docs/EVIDENCE_VALIDATION.md)只验证元数据，不证明实际修复；历史 `--as-of` 示例仅作回放，不是当前评估。仓库示例保持未验证，真实资产和证据在独立私有系统中保存。

## 治理与来源

[参考资料](REFERENCES.md) · [治理](GOVERNANCE.md) · [贡献](CONTRIBUTING.md) · [安全报告](SECURITY.md) · [变更记录](CHANGELOG.md) · [仓库设置建议](.github/REPOSITORY_SETTINGS.md)

设置建议文档不会自动修改 GitHub About、Topics、可见性或权限。当前未授予开源 License。本轮不改变可见性、License、分支保护或第三方关联声明。
