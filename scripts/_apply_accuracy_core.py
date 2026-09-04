#!/usr/bin/env python3
"""One-shot core accuracy migration for the review branch."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OLD_VERSION = "1.0.0-draft.1"
NEW_VERSION = "1.0.0-draft.2"


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")


def replace(path: str, old: str, new: str, expected: int = 1) -> None:
    text = read(path)
    count = text.count(old)
    if count != expected:
        raise RuntimeError(f"{path}: expected {expected}, found {count}: {old!r}")
    write(path, text.replace(old, new))


def bump_versions() -> None:
    paths = [
        "README.md",
        "README.zh-CN.md",
        "docs/en/WHITEPAPER.md",
        "docs/zh-CN/WHITEPAPER.md",
        "docs/en/SECURITY_BASELINE.md",
        "docs/zh-CN/SECURITY_BASELINE.md",
        "docs/en/PRACTICE_GUIDE.md",
        "docs/zh-CN/PRACTICE_GUIDE.md",
        "docs/en/REFERENCE_ARCHITECTURE.md",
        "docs/zh-CN/REFERENCE_ARCHITECTURE.md",
        "docs/en/METRICS_AND_ASSURANCE.md",
        "docs/zh-CN/METRICS_AND_ASSURANCE.md",
        "controls/README.md",
    ]
    for path in paths:
        text = read(path)
        if OLD_VERSION not in text:
            raise RuntimeError(f"{path}: missing {OLD_VERSION}")
        write(path, text.replace(OLD_VERSION, NEW_VERSION))
    write("VERSION", NEW_VERSION + "\n")


def patch_readmes() -> None:
    replace(
        "README.md",
        """NeoCloud Cyber Security is an open, evidence-driven security architecture and operating model for AI-first cloud infrastructure.

> **NeoCloud Cyber Security is a unified cybersecurity control plane for AI-native organizations and specialized AI clouds. It treats identity as the root of trust, policy as the decision core, and agents plus workloads as first-class security subjects. It coordinates endpoint, cloud-native runtime, network and fabric, data, software/model supply chain, and security operations controls to close the loop from visibility to real-time enforcement and continuous assurance.**""",
        """NeoCloud Cyber Security is a vendor-neutral, bilingual, evidence-oriented reference baseline and implementation guide for AI-first cloud infrastructure.

> **This repository defines a security reference model, control catalog, assurance method, and implementation roadmap. It is not a deployed security product or a claim that one universal “control plane” can secure every NeoCloud. The model coordinates identity and authorization, platform and workload integrity, cryptographic roots, policy enforcement, tenant isolation, and independently protected evidence across the service lifecycle.**""",
    )
    replace(
        "README.md",
        "The project covers the full NeoCloud trust surface: people, tenants, AI agents, workload identities, APIs, control planes, Kubernetes and Slurm, bare-metal hosts, hypervisors, GPUs and accelerators, Ethernet and InfiniBand/RDMA fabrics, datasets, models, checkpoints, secrets, firmware, BMCs, facilities, and third-party dependencies.",
        """The project covers the full NeoCloud trust surface: people, tenants, AI agents, workload identities, APIs, control planes, Kubernetes and Slurm, bare-metal hosts, hypervisors, GPUs and accelerators, Ethernet and InfiniBand/RDMA fabrics, datasets, models, checkpoints, secrets, firmware, BMCs, facilities, and third-party dependencies.

“NeoCloud” is used here as an operational term for specialized AI/GPU cloud services, not as a formally standardized industry category. See [Scope and Limitations](docs/en/SCOPE_AND_LIMITATIONS.md) before adopting or citing the baseline.""",
    )
    replace(
        "README.md",
        "| Standards and research | [References](REFERENCES.md) | [参考资料](REFERENCES.md) |",
        """| Standards and research | [References](REFERENCES.md) | [参考资料](REFERENCES.md) |
| Scope and limitations | [Scope & Limitations](docs/en/SCOPE_AND_LIMITATIONS.md) | [范围与局限](docs/zh-CN/SCOPE_AND_LIMITATIONS.md) |
| Accuracy review | [Accuracy Review](ACCURACY_REVIEW.md) | [准确性审计](ACCURACY_REVIEW.md) |
| Repository metadata | [Project Metadata](PROJECT_METADATA.md) | [项目元数据](PROJECT_METADATA.md) |
| Security reporting | [Security Policy](SECURITY.md) | [安全报告](SECURITY.md) |""",
    )
    replace(
        "README.md",
        """- **T3 — Assured:** higher-assurance controls for sensitive, regulated, sovereign, or dedicated environments.
- **T4 — Adaptive:** continuous verification, high-confidence automation, confidential computing, and guarded AI-assisted defense.""",
        """- **T3 — Assured:** higher-assurance controls for sensitive, regulated, sovereign, or dedicated environments, including independently tested and threat-model-justified attestation or confidential-computing patterns.
- **T4 — Adaptive:** continuous verification and guarded AI-assisted security automation whose authority, rollback, and independent verification are proven.""",
    )
    replace(
        "README.md",
        "- **Secure by design, not by tenant expertise.** Safe defaults, MFA, logging, isolation, and update mechanisms are provider responsibilities, not paid add-ons.",
        "- **Secure by design and accurately scoped.** Provider-controlled baseline safeguards should be secure by default; customer-controlled duties and higher-assurance offerings must be explicit and must not conceal the limitations of baseline service tiers.",
    )
    replace(
        "README.md",
        "## Status and scope\n",
        """## Accuracy and scope

The baseline distinguishes scheduler-level GPU oversubscription from mediated vGPU and hardware-partitioned modes; treats InfiniBand P_Keys and Slurm labels as partial mechanisms rather than complete isolation proofs; and makes attestation, confidential computing, sanitization, and public control-plane claims product-, version-, configuration-, and threat-model specific.

See the [accuracy review](ACCURACY_REVIEW.md), [scope and limitations](docs/en/SCOPE_AND_LIMITATIONS.md), and [source register](REFERENCES.md). Project-defined targets are planning defaults, not externally validated industry benchmarks.

## Status and scope
""",
    )
    replace(
        "README.md",
        "This is an implementation-oriented community baseline, not a certification, legal opinion, or substitute for jurisdiction-specific obligations. Mappings to external frameworks are informative. Organizations remain responsible for determining applicability and obtaining qualified legal, privacy, safety, and audit advice.",
        "This is a project-defined implementation draft and reference baseline—not an adopted industry standard, deployed product, certification, legal opinion, or substitute for jurisdiction-specific obligations. External-framework mappings are informative. Organizations remain responsible for applicability decisions and qualified legal, privacy, safety, engineering, and audit review.",
    )

    replace(
        "README.zh-CN.md",
        """NeoCloud Cyber Security 是一套面向 AI-first 云基础设施的开放、证据驱动的安全架构与运营模型。

> **NeoCloud Cyber Security 是 NeoCloud 面向 AI-native 组织和专业 AI 云构建的统一网络安全控制平面：以身份为信任根、以策略为决策核心、以 Agent 与工作负载为重点保护对象，通过端点、云原生运行时、网络与高性能互联、数据、软件/模型供应链和安全运营协同，实现从“看见风险”到“实时阻断”和“持续证明”的闭环。**""",
        """NeoCloud Cyber Security 是一套面向 AI-first 云基础设施、保持厂商中立的中英文证据导向参考基线与实施指南。

> **本仓库定义安全参考模型、控制目录、持续证明方法和建设路线图；它不是已经部署的软件产品，也不主张一个通用“控制平面”可以覆盖所有 NeoCloud。该模型在完整服务生命周期中协同身份与授权、平台/工作负载完整性、密码信任根、策略执行、租户隔离以及独立保护的证据。**""",
    )
    replace(
        "README.zh-CN.md",
        "本项目覆盖完整的 NeoCloud 信任面：人员、租户、AI Agent、工作负载身份、API、控制面、Kubernetes、Slurm、裸金属、虚拟化、GPU/加速器、以太网、InfiniBand/RDMA、数据集、模型、Checkpoint、密钥、固件、BMC、机房以及第三方依赖。",
        """本项目覆盖完整的 NeoCloud 信任面：人员、租户、AI Agent、工作负载身份、API、控制面、Kubernetes、Slurm、裸金属、虚拟化、GPU/加速器、以太网、InfiniBand/RDMA、数据集、模型、Checkpoint、密钥、固件、BMC、机房以及第三方依赖。

本文将 “NeoCloud” 作为专业 AI/GPU 云服务的操作性术语使用，并不声称它是已经标准化的行业类别。采用或引用前请先阅读[范围与局限](docs/zh-CN/SCOPE_AND_LIMITATIONS.md)。""",
    )
    replace(
        "README.zh-CN.md",
        "| 标准与研究资料 | [参考资料](REFERENCES.md) | [References](REFERENCES.md) |",
        """| 标准与研究资料 | [参考资料](REFERENCES.md) | [References](REFERENCES.md) |
| 范围与局限 | [范围与局限](docs/zh-CN/SCOPE_AND_LIMITATIONS.md) | [Scope & Limitations](docs/en/SCOPE_AND_LIMITATIONS.md) |
| 准确性审计 | [准确性审计](ACCURACY_REVIEW.md) | [Accuracy Review](ACCURACY_REVIEW.md) |
| GitHub 项目元数据 | [项目元数据](PROJECT_METADATA.md) | [Project Metadata](PROJECT_METADATA.md) |
| 安全问题报告 | [安全报告规则](SECURITY.md) | [Security Policy](SECURITY.md) |""",
    )
    replace(
        "README.zh-CN.md",
        """- **T3—可信级：** 面向敏感、受监管、主权或专属环境的高保证控制。
- **T4—自适应级：** 持续验证、可控自动化、机密计算和带护栏的 AI 辅助防御。""",
        """- **T3—可信级：** 面向敏感、受监管、主权或专属环境的高保证控制，包括经过独立测试、由威胁模型证明必要的证明或机密计算模式。
- **T4—自适应级：** 持续验证，以及权限、回滚和独立验证均已证明的受控 AI 辅助安全自动化。""",
    )
    replace(
        "README.zh-CN.md",
        "- **安全默认，而非依赖客户专家能力。** MFA、日志、隔离、安全更新和安全默认配置应由服务提供方内建，而不是收费选件。",
        "- **安全默认且声明精确。** 服务商控制的基础安全措施应默认安全；客户控制的责任和更高保证服务必须明确，不能用高阶付费能力掩盖基础 SKU 的限制。",
    )
    replace(
        "README.zh-CN.md",
        "## 状态与边界\n",
        """## 准确性与适用范围

本基线区分调度器级 GPU 超卖、受 Hypervisor 仲裁的 vGPU 与硬件分区；不把 InfiniBand P_Key 或 Slurm Label 当成完整隔离证明；并要求 Attestation、Confidential Computing、Sanitization 及公网控制面声明绑定具体产品、版本、配置与威胁模型。

详见[准确性审计](ACCURACY_REVIEW.md)、[范围与局限](docs/zh-CN/SCOPE_AND_LIMITATIONS.md)和[参考资料](REFERENCES.md)。本文给出的目标值是项目定义的规划默认值，不是经外部验证的行业 Benchmark。

## 状态与边界
""",
    )
    replace(
        "README.zh-CN.md",
        "本项目是面向实施的行业基线，不是认证、法律意见，也不能替代特定司法辖区的强制要求。外部框架映射仅供参考；组织仍需自行判断适用性，并获得合格的法律、隐私、安全和审计意见。",
        "本项目是项目自定义的实施草案与参考基线，不是已被行业采纳的正式标准、已部署产品、认证或法律意见，也不能替代特定司法辖区的强制要求。外部框架映射仅供参考；组织仍需自行判断适用性，并获得合格的法律、隐私、安全工程和审计意见。",
    )


def patch_whitepapers() -> None:
    replace("docs/en/WHITEPAPER.md", "**Status:** Implementation-oriented public draft", "**Status:** Project-defined implementation draft")
    replace(
        "docs/en/WHITEPAPER.md",
        "NeoCloud Cyber Security defines a unified cybersecurity control plane for this environment. Identity is the root of trust; policy is the decision core; people, tenants, workloads, devices, and AI agents are first-class security subjects.",
        "NeoCloud Cyber Security proposes a unified security reference model and operating architecture for this environment. Identity and authorization, platform and workload integrity, cryptographic roots, policy enforcement, tenant isolation, and independently protected evidence are complementary trust inputs; no single input is sufficient.",
    )
    replace(
        "docs/en/WHITEPAPER.md",
        "The companion [Security Baseline](SECURITY_BASELINE.md), [Practice Guide](PRACTICE_GUIDE.md), [Reference Architecture](REFERENCE_ARCHITECTURE.md), [Roadmap](ROADMAP.md), and [Metrics and Assurance Guide](METRICS_AND_ASSURANCE.md) convert the model into deployable work.",
        "The companion [Security Baseline](SECURITY_BASELINE.md), [Practice Guide](PRACTICE_GUIDE.md), [Reference Architecture](REFERENCE_ARCHITECTURE.md), [Roadmap](ROADMAP.md), and [Metrics and Assurance Guide](METRICS_AND_ASSURANCE.md) convert the model into deployable work. [Scope and Limitations](SCOPE_AND_LIMITATIONS.md) defines what this project does not claim.",
    )
    replace(
        "docs/en/WHITEPAPER.md",
        "**NeoCloud Cyber Security is a unified cybersecurity control plane for AI-native organizations and specialized AI clouds. It treats identity as the root of trust, policy as the decision core, and agents plus workloads as first-class security subjects. It coordinates endpoint, cloud-native runtime, network and fabric, data, software/model supply chain, and security operations controls to close the loop from visibility to real-time enforcement and continuous assurance.**",
        "**NeoCloud Cyber Security is a project-defined security reference model and control baseline for AI-native organizations and specialized AI/GPU clouds. It coordinates identity and authorization, platform and workload integrity, cryptographic roots, policy enforcement, compute/fabric/data isolation, security operations, and independent evidence. It is an architecture and assurance model—not a claim that one product or one universal control plane can secure every deployment.**",
    )
    replace("docs/en/WHITEPAPER.md", "A hardened Kubernetes cluster cannot compensate for a shared InfiniBand partition.", "A hardened Kubernetes cluster cannot compensate for an inadequately isolated or misconfigured high-performance fabric.")
    replace("docs/en/WHITEPAPER.md", "documented SKU isolation, dedicated/MIG-class options, reset verification, adversarial testing", "documented SKU isolation; dedicated, hardware-partitioned, or mediated-virtualization options validated for the deployed stack; reset verification; adversarial testing")
    replace("docs/en/WHITEPAPER.md", "4. **Secure defaults are provider responsibilities.** MFA, audit, safe isolation modes, encryption, updates, and secure deletion cannot be optional premium features.", "4. **Provider-controlled safeguards are secure by default and accurately scoped.** Customer-controlled duties and higher-assurance service options must be explicit; they must not be used to obscure weaker baseline properties or ambiguous responsibility.")
    replace("docs/en/WHITEPAPER.md", "| **T0 Guardrails** | non-negotiable conditions before tenant data or production capacity is exposed | release blocked until passed or an exceptional executive emergency process is invoked |", "| **T0 Guardrails** | non-negotiable conditions before tenant data or production capacity is exposed | release blocked while the service remains in scope; an emergency deviation remains explicitly nonconformant and time-bounded |")
    replace("docs/en/WHITEPAPER.md", "| **T4 Adaptive** | continuous verification, guarded automation, advanced attestation/confidentiality | adopted only where failure modes and rollback are understood |", "| **T4 Adaptive** | continuous verification and guarded security automation | adopted only where authority, failure modes, rollback and independent verification are understood |")
    replace(
        "docs/en/WHITEPAPER.md",
        "## Disclaimer\n",
        """## Source basis and limitations

The control set is a project-defined synthesis informed by authoritative and primary sources in [`REFERENCES.md`](../../REFERENCES.md); it is not a normative transcription or formally validated crosswalk. Hardware and platform claims must be revalidated against the exact GPU, virtualization mode, driver, firmware, hypervisor, fabric controller, Slurm/Kubernetes configuration, and service contract in use. See [Scope and Limitations](SCOPE_AND_LIMITATIONS.md) and the repository [Accuracy Review](../../ACCURACY_REVIEW.md).

## Disclaimer
""",
    )
    replace("docs/en/WHITEPAPER.md", "This white paper is an implementation-oriented industry baseline.", "This white paper is a project-defined implementation draft and reference baseline. It is not an adopted industry standard or deployed product.")

    replace("docs/zh-CN/WHITEPAPER.md", "**状态：** 面向实施的公开草案", "**状态：** 项目自定义的实施草案")
    replace(
        "docs/zh-CN/WHITEPAPER.md",
        "NeoCloud Cyber Security 为该环境定义统一的网络安全控制平面：以身份为信任根，以策略为决策核心，把人员、租户、工作负载、设备和 AI Agent 都视为一等安全主体。",
        "NeoCloud Cyber Security 为该环境提出统一的安全参考模型与运营架构。身份与授权、平台和工作负载完整性、密码信任根、策略执行、租户隔离以及独立保护的证据是相互补充的信任输入，任何单一输入都不充分。",
    )
    replace(
        "docs/zh-CN/WHITEPAPER.md",
        "配套的[安全基线](SECURITY_BASELINE.md)、[实践指南](PRACTICE_GUIDE.md)、[参考架构](REFERENCE_ARCHITECTURE.md)、[发展路线图](ROADMAP.md)和[度量与持续证明](METRICS_AND_ASSURANCE.md)将其转换为可执行工作。",
        "配套的[安全基线](SECURITY_BASELINE.md)、[实践指南](PRACTICE_GUIDE.md)、[参考架构](REFERENCE_ARCHITECTURE.md)、[发展路线图](ROADMAP.md)和[度量与持续证明](METRICS_AND_ASSURANCE.md)将其转换为可执行工作；[范围与局限](SCOPE_AND_LIMITATIONS.md)明确本项目不作出的声明。",
    )
    replace(
        "docs/zh-CN/WHITEPAPER.md",
        "**NeoCloud Cyber Security 是 NeoCloud 面向 AI-native 组织和专业 AI 云构建的统一网络安全控制平面：以身份为信任根、以策略为决策核心、以 Agent 与工作负载为重点保护对象，通过端点、云原生运行时、网络与高性能互联、数据、软件/模型供应链和安全运营协同，实现从“看见风险”到“实时阻断”和“持续证明”的闭环。**",
        "**NeoCloud Cyber Security 是面向 AI-native 组织和专业 AI/GPU 云、由本项目定义的安全参考模型与控制基线。它协同身份与授权、平台/工作负载完整性、密码信任根、策略执行、计算/Fabric/数据隔离、安全运营和独立证据；它是一套架构与持续证明模型，并不主张一个产品或一个通用控制平面可以覆盖所有部署。**",
    )
    replace("docs/zh-CN/WHITEPAPER.md", "4. **安全默认属于服务商责任。** MFA、审计、安全隔离模式、加密、安全更新和删除能力不能成为额外付费选项。", "4. **服务商控制的基础措施应默认安全且声明精确。** 客户控制的责任和更高保证服务必须明确，不能用于掩盖基础服务属性不足或责任边界含糊。")
    replace("docs/zh-CN/WHITEPAPER.md", "| **T0 硬门槛** | 在处理租户数据或开放生产能力前不可妥协的条件 | 未通过则阻断发布，除非触发高管批准的紧急例外流程 |", "| **T0 硬门槛** | 在处理租户数据或开放生产能力前不可妥协的条件 | 服务仍在适用范围内时必须阻断；紧急偏离仍保持“不符合”状态且必须限时 |")
    replace("docs/zh-CN/WHITEPAPER.md", "| **T4 自适应级** | 持续验证、受控自动化、进阶证明和机密性 | 仅在理解失败模式和回滚后采用 |", "| **T4 自适应级** | 持续验证与受控安全自动化 | 仅在权限、失败模式、回滚和独立验证均明确后采用 |")
    replace(
        "docs/zh-CN/WHITEPAPER.md",
        "## 免责声明\n",
        """## 来源依据与局限

控制集是本项目参考 [`REFERENCES.md`](../../REFERENCES.md) 中权威资料与一手资料形成的综合结果，不是对外部标准的规范性转录，也不是经过正式验证的 Crosswalk。所有硬件和平台声明都必须针对实际 GPU、虚拟化模式、Driver、Firmware、Hypervisor、Fabric Controller、Slurm/Kubernetes 配置及服务合同重新验证。详见[范围与局限](SCOPE_AND_LIMITATIONS.md)和仓库[准确性审计](../../ACCURACY_REVIEW.md)。

## 免责声明
""",
    )
    replace("docs/zh-CN/WHITEPAPER.md", "本白皮书是面向实施的行业基线，", "本白皮书是项目自定义的实施草案与参考基线，不是已被行业采纳的标准或已部署产品，")


def patch_baselines_and_governance() -> None:
    replace("docs/en/SECURITY_BASELINE.md", "This document explains how to assess and apply it.", "This document explains how to assess and apply it. The tiers, gates, counts, and targets are project-defined normative rules for this repository, not claims of universal industry consensus; see [Scope and Limitations](SCOPE_AND_LIMITATIONS.md).")
    replace("docs/en/SECURITY_BASELINE.md", "A score never compensates for a failed T0. T0 exceptions are emergency-only, executive and security approved, time-bounded, customer/legal-impact assessed, protected by compensating controls, and tied to a remediation deadline.", "A score never compensates for a failed T0. An accountable executive and security owner may authorize a time-bounded emergency deviation to continue a service, but the failed or unknown T0 remains `NO-GO` for conformity: it cannot be marked `PASS` or `VERIFIED`, cannot be represented as baseline-compliant, and must retain explicit customer/legal impact, compensating controls, rollback conditions, and a remediation deadline.")
    replace("docs/en/SECURITY_BASELINE.md", "7. **End-to-end isolation:** tenant identity is preserved across API, scheduler, host, GPU, storage, Ethernet, InfiniBand/RDMA, DPU, telemetry, and support operations.", "7. **End-to-end isolation:** tenant and authorization context is preserved across control-plane translations and enforced through authoritative bindings at scheduler, host, GPU, storage, Ethernet, InfiniBand/RDMA, DPU, telemetry, and support boundaries.")
    replace("docs/en/SECURITY_BASELINE.md", "10. **Secure orchestration:** Kubernetes/Slurm control planes are private, patched, strongly authenticated, separated from tenants, backed up, and recoverable.", "10. **Secure orchestration:** provider-only Kubernetes/Slurm controllers and databases are private, patched, strongly authenticated, separated from tenants, backed up, and recoverable. Any customer-facing management API is private by default or explicitly approved, hardened, restricted, protected from abuse, and fully audited.")
    replace("docs/en/SECURITY_BASELINE.md", "| NCS-IAM-03 | T2 | Attested workload and service identity |", "| NCS-IAM-03 | T2 | Short-lived workload and service identity |")
    replace("docs/en/SECURITY_BASELINE.md", "| NCS-ORC-01 | T0 | Hardened and private orchestrator control planes |", "| NCS-ORC-01 | T0 | Hardened and access-restricted orchestrator control planes |")
    replace("docs/en/SECURITY_BASELINE.md", "T0/T1 controls should be reviewed at least quarterly and after material change. T2/T3 should be reviewed at least semi-annually with continuous monitoring where feasible. T4 automation requires continuous metrics and quarterly adversarial/failure-mode review.", "Default minimum revalidation is: T0—continuous monitoring where feasible plus independent verification at least quarterly and after material change; T1—at least quarterly and after material change; T2—at least semi-annually and after material change; T3—control-owner review at least semi-annually, independent assessment at least annually, and review after material change; T4—continuous metrics plus quarterly adversarial/failure-mode review and review after material change. A service-specific threat model, contract, incident, or regulator may require a shorter interval.")

    replace("docs/zh-CN/SECURITY_BASELINE.md", "本文解释如何评估和应用。", "本文解释如何评估和应用。等级、硬门、数量和目标值是本仓库定义的规范规则，并不代表普遍行业共识；详见[范围与局限](SCOPE_AND_LIMITATIONS.md)。")
    replace("docs/zh-CN/SECURITY_BASELINE.md", "任何分数都不能抵消 T0 失败。T0 例外只能用于紧急情况，必须由高管与安全 Owner 批准、限时、评估客户/法律影响、具备补偿控制，并绑定整改截止时间。", "任何分数都不能抵消 T0 失败。可追责高管和安全 Owner 可以批准限时紧急偏离以维持服务，但失败或未知 T0 在符合性判定上仍然是 `NO-GO`：不得标记为 `PASS` 或 `VERIFIED`，不得对外声称符合本基线，并必须明确客户/法律影响、补偿控制、回滚条件和整改截止时间。")
    replace("docs/zh-CN/SECURITY_BASELINE.md", "7. **端到端隔离：** Tenant Identity 贯穿 API、Scheduler、Host、GPU、Storage、Ethernet、InfiniBand/RDMA、DPU、Telemetry 和 Support。", "7. **端到端隔离：** Tenant/Authorization Context 在控制面对象转换中保持，并通过权威绑定在 Scheduler、Host、GPU、Storage、Ethernet、InfiniBand/RDMA、DPU、Telemetry 和 Support 边界执行。")
    replace("docs/zh-CN/SECURITY_BASELINE.md", "10. **编排安全：** Kubernetes/Slurm Control Plane 私有、补丁及时、强认证、与租户分离、可备份和恢复。", "10. **编排安全：** 服务商专用 Kubernetes/Slurm Controller 与 Database 私有、补丁及时、强认证、与租户分离、可备份和恢复。任何面向客户的管理 API 默认私有，或经过显式批准并实施加固、来源/权限限制、抗滥用保护和完整审计。")
    replace("docs/zh-CN/SECURITY_BASELINE.md", "| NCS-IAM-03 | T2 | 经过证明的工作负载与服务身份 |", "| NCS-IAM-03 | T2 | 短期工作负载与服务身份 |")
    replace("docs/zh-CN/SECURITY_BASELINE.md", "| NCS-ORC-01 | T0 | 加固且私有的编排控制面 |", "| NCS-ORC-01 | T0 | 加固且访问受限的编排控制面 |")
    replace("docs/zh-CN/SECURITY_BASELINE.md", "T0/T1 至少每季度及重大变更后 Review；T2/T3 至少每半年，技术可行时持续监控；T4 自动化需要持续指标和每季度对抗/失败模式 Review。", "默认最低重验证频率为：T0 在可行时持续监控、至少每季度独立验证并在重大变更后复验；T1 至少每季度及重大变更后；T2 至少每半年及重大变更后；T3 至少每半年由 Control Owner 复核、至少每年独立评估，并在重大变更后复验；T4 持续度量、每季度对抗/失败模式复核，并在重大变更后复验。服务威胁模型、合同、事件或监管要求可以缩短周期。")

    replace(
        "GOVERNANCE.md",
        """When requirements conflict, use the following order:

1. Applicable law, regulator, contract, or customer commitment.
2. Explicit organizational risk decisions approved by accountable owners.
3. T0 production guardrails in this baseline.
4. Service-specific threat models and shared-responsibility decisions.
5. T1–T4 controls and informative framework mappings.

A mapping to an external framework never proves compliance by itself.""",
        """When requirements conflict, use the following order:

1. Applicable law, regulator, contract, or customer commitment.
2. Explicit service boundary and applicability decisions approved by accountable owners.
3. T0 production guardrails for the in-scope service.
4. Service-specific threat models and shared-responsibility decisions.
5. Explicit residual-risk decisions for T1–T4 and explicitly nonconformant emergency deviations.
6. Informative framework mappings.

A risk decision may authorize a time-bounded operational deviation, but it cannot relabel a failed or unknown T0 as `PASS`, `VERIFIED`, or baseline-conformant. A mapping to an external framework never proves compliance by itself.""",
    )
    replace(
        "GOVERNANCE.md",
        """T0 exceptions are prohibited unless an accountable executive and security owner approve a time-bounded emergency exception with compensating controls, customer/legal impact analysis, and a rollback or remediation deadline. Exceptions must never silently become permanent architecture.

All exceptions require an owner, reason, affected assets/tenants, residual risk, compensating controls, approval, expiration date, and verification after closure.""",
        """A T0 failure or unknown state cannot receive a conforming exception. An accountable executive and security owner may approve a time-bounded **emergency deviation** with compensating controls, customer/legal impact analysis, explicit nonconformant status, rollback conditions, and a remediation deadline. The affected control remains failed or unverified until an independent validator returns `PASS`.

All deviations and other exceptions require an owner, reason, affected assets/tenants, residual risk, compensating controls, approval, expiration date, customer-facing claim treatment, and verification after closure. They must never silently become permanent architecture.""",
    )
    replace("GOVERNANCE.md", "- a declared goal, immutable scope, and authorized tool set;", "- a declared goal, a policy-controlled authorization envelope that the agent or untrusted content cannot expand, and an authorized tool set;")
    replace(
        "GOVERNANCE.md",
        """- T0/T1: at least quarterly and after material architecture or threat changes.
- T2/T3: at least semi-annually, with continuous monitoring where technically feasible.
- T4 automation: continuous telemetry plus quarterly adversarial and failure-mode review.
- Full baseline: annual version review or earlier when a major standard, platform, accelerator, isolation mechanism, or threat class changes.""",
        """- T0: continuous monitoring where feasible, independent verification at least quarterly, and review after material architecture or threat change.
- T1: at least quarterly and after material change.
- T2: at least semi-annually and after material change.
- T3: control-owner review at least semi-annually, independent assessment at least annually, and review after material change.
- T4 automation: continuous telemetry plus quarterly adversarial/failure-mode review and review after material change.
- Full baseline: annual version review or earlier when a major standard, platform, accelerator, isolation mechanism, or threat class changes.""",
    )


def patch_catalog() -> None:
    path = ROOT / "controls/neocloud-security-baseline.v1.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["version"] = NEW_VERSION
    data["status"] = "project-defined implementation draft"
    data["normative_rules"]["t0_gate"] = "Every applicable T0 control must be independently VERIFIED. Failed, unknown, inconclusive, untested, or stale T0 evidence produces NO-GO. An approved emergency deviation may authorize time-bounded continuity, but it never converts the control to PASS or VERIFIED and never establishes baseline conformity."
    data["normative_rules"]["t0_gate_zh_CN"] = "每个适用 T0 控制都必须被独立验证为 VERIFIED；失败、未知、无法判定、未测试或证据过期均产生 NO-GO。经批准的紧急偏离可以限时维持服务，但绝不能把控制转换为 PASS/VERIFIED，也不建立基线符合性。"
    data["tiers"]["T3"]["frequency"] = "control-owner review at least semi-annually, independent verification at least annually, and review after material change"
    data["tiers"]["T3"]["frequency_zh_CN"] = "至少每半年由 Control Owner 复核、至少每年独立验证，并在重大变更后复验"
    controls = {c["id"]: c for c in data["controls"]}
    controls["NCS-IAM-03"]["title"] = {"en": "Short-lived workload and service identity", "zh-CN": "短期工作负载与服务身份"}
    controls["NCS-IAM-03"]["requirement"] = {"en": "The provider MUST issue scoped, audience-restricted, short-lived workload and service identities, avoid embedded credentials, and bind identity or key release to attested state where the product supports it and the threat model justifies it.", "zh-CN": "服务商必须签发范围受限、Audience 受限、短期的工作负载和服务身份，避免嵌入式凭据，并在产品支持且威胁模型证明必要时将身份或密钥释放绑定到 Attested State。"}
    controls["NCS-NET-02"]["requirement"] = {"en": "The provider MUST preserve tenant and authorization context across control-plane translations and enforce tenant-aware isolation through authoritative bindings across Ethernet, storage, InfiniBand/RDMA, DPU/NIC, support, and NVLink/NVSwitch-aware placement. P_Keys, labels, or topology metadata alone do not prove complete isolation.", "zh-CN": "服务商必须在控制面对象转换中保持 Tenant/Authorization Context，并通过权威绑定在 Ethernet、Storage、InfiniBand/RDMA、DPU/NIC、Support 与 NVLink/NVSwitch 感知放置中实施租户隔离。P_Key、Label 或 Topology Metadata 不能单独证明完整隔离。"}
    controls["NCS-CMP-02"]["requirement"] = {"en": "The provider MUST distinguish dedicated, hardware-partitioned, hypervisor-mediated vGPU, and scheduler-level sharing modes; select them by threat model; prevent sensitive placement on insufficient boundaries; and verify product/version/configuration-specific memory, cache, DMA/IOMMU, fault, reset, telemetry, performance-interference, quarantine, and inter-tenant cleanup properties.", "zh-CN": "服务商必须区分 Dedicated、Hardware-partitioned、Hypervisor-mediated vGPU 与 Scheduler-level Sharing，按威胁模型选择，禁止敏感工作负载进入不足边界，并验证具体 Product/Version/Configuration 的 Memory、Cache、DMA/IOMMU、Fault、Reset、Telemetry、Performance Interference、Quarantine 与跨租户 Cleanup 属性。"}
    controls["NCS-CMP-05"]["requirement"] = {"en": "For assured services, the provider MUST implement service-specific dedicated, confidential, attested, topology-aware, and side-channel controls justified by the threat model and validated on the exact hardware, firmware, driver, hypervisor, and service configuration. Attestation or a confidential-computing label alone does not prove end-to-end confidentiality or eliminate side channels.", "zh-CN": "对可信级服务，服务商必须按威胁模型实施服务特定的 Dedicated、Confidential、Attested、Topology-aware 与 Side-channel Control，并在准确 Hardware、Firmware、Driver、Hypervisor 与服务配置上验证。Attestation 或 Confidential Computing 标签本身不能证明端到端机密性，也不能消除侧信道。"}
    controls["NCS-ORC-01"]["title"] = {"en": "Hardened and access-restricted orchestrator control planes", "zh-CN": "加固且访问受限的编排控制面"}
    controls["NCS-ORC-01"]["requirement"] = {"en": "Provider-only Kubernetes, Slurm, scheduler, controller, and database management planes MUST be private, strongly authenticated, patched, separated, backed up, and recoverable. A customer-facing management API MUST be private by default or explicitly approved, hardened, access-restricted, abuse-protected, and fully audited.", "zh-CN": "服务商专用 Kubernetes、Slurm、Scheduler、Controller 与 Database 管理面必须私有、强认证、已修补、隔离、备份且可恢复。面向客户的管理 API 必须默认私有，或经过显式批准并实施加固、访问限制、抗滥用保护和完整审计。"}
    controls["NCS-ORC-03"]["requirement"] = {"en": "The provider MUST enforce tenant-aware namespace/account/partition/queue, quota, priority, reservation, topology, node, GPU, fabric, and data placement boundaries. Slurm accounts, partitions, QOS, MCS labels, Kubernetes namespaces, and similar scheduler/visibility constructs are not complete isolation boundaries without OS/runtime, credential, storage, and network/fabric enforcement.", "zh-CN": "服务商必须执行租户感知的 Namespace/Account/Partition/Queue、Quota、Priority、Reservation、Topology、Node、GPU、Fabric 与 Data Placement 边界。Slurm Account/Partition/QOS/MCS Label、Kubernetes Namespace 等调度或可见性机制，如果没有 OS/Runtime、Credential、Storage 与 Network/Fabric Enforcement，就不是完整隔离边界。"}
    controls["NCS-KMS-04"]["requirement"] = {"en": "For assured services, admission and sensitive key release MUST evaluate current identity, measured state, policy, nonce/freshness, tenant, workload, and revocation context. Attestation claims MUST be product/version/configuration specific and MUST NOT be treated as proof of application behavior, end-to-end confidentiality, or absence of side channels.", "zh-CN": "对可信级服务，准入与敏感密钥释放必须评估当前 Identity、Measured State、Policy、Nonce/Freshness、Tenant、Workload 与 Revocation Context。Attestation Claim 必须绑定具体 Product/Version/Configuration，不得被视为 Application Behavior、端到端机密性或无侧信道的证明。"}
    controls["NCS-PHY-04"]["requirement"] = {"en": "Before tenant reassignment or release, the provider MUST revoke credentials and apply vendor-documented, device/mode-specific reset or sanitization to accelerator state, local storage/media, host provisioning, and network/fabric assignments; validate the result; and quarantine or dedicate resources when a defensible cross-tenant cleanup claim cannot be established.", "zh-CN": "在租户重分配或释放前，服务商必须撤销凭据，对 Accelerator State、本地 Storage/Media、Host Provisioning 与 Network/Fabric Assignment 执行厂商文档支持、绑定 Device/Mode 的 Reset 或 Sanitization，验证结果；如果无法建立可辩护的跨租户清理声明，则必须隔离或专属化资源。"}
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def patch_contributing_validator_changelog() -> None:
    old = """## Local validation

This repository intentionally does not require a GitHub Actions workflow. Run the checks locally before review:

```bash
python -m json.tool controls/neocloud-security-baseline.v1.json >/dev/null
python - <<'PY'
import json
from pathlib import Path
p = Path('controls/neocloud-security-baseline.v1.json')
data = json.loads(p.read_text())
ids = [c['id'] for c in data['controls']]
assert len(ids) == len(set(ids)), 'duplicate control IDs'
assert all(c['tier'] in {'T0','T1','T2','T3','T4'} for c in data['controls'])
print(f"validated {len(ids)} controls")
PY

grep -RInE 'TODO|TBD|FIXME|PLACEHOLDER' README* docs controls templates GOVERNANCE.md CONTRIBUTING.md REFERENCES.md && exit 1 || true
```

Review all relative Markdown links manually or with a local link checker. Mermaid diagrams must render in GitHub Markdown.
"""
    new = """## Local and CI validation

Run the repository contract locally before review:

```bash
python3 scripts/validate_repository.py
```

The validator checks catalog structure, exact control IDs/counts/tier distribution, bilingual baseline parity, cross-references, release versions, required deliverables, intended repository metadata, and relative Markdown links. GitHub Actions runs the same validator for pull requests and `main`; local success does not replace independent review, and CI success does not prove the substantive correctness of a security claim. Mermaid diagrams should also be visually reviewed in GitHub Markdown.
"""
    replace("CONTRIBUTING.md", old, new)
    replace("CONTRIBUTING.md", "Use the repository owner's private disclosure channel. Redact evidence before committing it.", "Follow [`SECURITY.md`](SECURITY.md), use GitHub private vulnerability reporting when enabled or another established private maintainer channel, and redact evidence before committing it.")
    replace("CONTRIBUTING.md", "所有校验和 Review 应在本地完成，只有独立验证通过后才能宣称控制已完成。", "提交前运行 `python3 scripts/validate_repository.py`，Pull Request 还会执行相同 CI；只有独立验证返回 `PASS` 后才能宣称控制已完成。")

    replace("scripts/validate_repository.py", '    "REFERENCES.md",\n    "VERSION",', '    "REFERENCES.md",\n    "ACCURACY_REVIEW.md",\n    "PROJECT_METADATA.md",\n    "SECURITY.md",\n    ".github/repository-metadata.json",\n    "docs/en/SCOPE_AND_LIMITATIONS.md",\n    "docs/zh-CN/SCOPE_AND_LIMITATIONS.md",\n    "VERSION",')

    text = read("CHANGELOG.md")
    marker = "## 1.0.0-draft.1 — 2026-09-04\n"
    if marker not in text:
        raise RuntimeError("CHANGELOG prior marker missing")
    entry = """## 1.0.0-draft.2 — 2026-09-04

### Corrected

- Reframed the repository as a project-defined, vendor-neutral reference baseline rather than an open project, deployed product, adopted industry standard, or universal security control plane.
- Reconciled T0 emergency handling with the hard `NO-GO` algorithm: a time-bounded emergency deviation remains explicitly nonconformant and cannot become `PASS` or `VERIFIED`.
- Reconciled T3 cadence as semi-annual control-owner review plus annual independent verification and material-change review.
- Distinguished scheduler-level Kubernetes GPU time-slicing from mediated vGPU, hardware partitioning, and full-GPU dedication; made isolation and cleanup claims deployment specific.
- Clarified that InfiniBand P_Keys, Slurm scheduling constructs, Kubernetes namespaces, attestation, confidential computing, and signatures are partial mechanisms rather than complete proof.
- Replaced universally private customer API wording with a provider-private/customer-endpoint risk model.
- Corrected `CONTRIBUTING.md` to describe the actual local and GitHub Actions validation workflow.

### Added

- Bilingual scope and limitations documents, a source-backed accuracy review, intended GitHub metadata, and a security-reporting policy.

"""
    write("CHANGELOG.md", text.replace(marker, entry + marker, 1))


def main() -> None:
    bump_versions()
    patch_readmes()
    patch_whitepapers()
    patch_baselines_and_governance()
    patch_catalog()
    patch_contributing_validator_changelog()
    print(f"Applied core corrections: {OLD_VERSION} -> {NEW_VERSION}")


if __name__ == "__main__":
    main()
