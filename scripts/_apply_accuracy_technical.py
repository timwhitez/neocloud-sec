#!/usr/bin/env python3
"""One-shot technical accuracy migration for the review branch."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    (ROOT / path).write_text(text, encoding="utf-8")


def replace(path: str, old: str, new: str, expected: int = 1) -> None:
    text = read(path)
    count = text.count(old)
    if count != expected:
        raise RuntimeError(f"{path}: expected {expected}, found {count}: {old!r}")
    write(path, text.replace(old, new))


def patch_practice_guides() -> None:
    replace(
        "docs/en/PRACTICE_GUIDE.md",
        "It is vendor-neutral. Product names are examples, not requirements.",
        "It is vendor-neutral. Product names are examples, not requirements. Apply the [Scope and Limitations](SCOPE_AND_LIMITATIONS.md) to every implementation claim.",
    )
    replace("docs/en/PRACTICE_GUIDE.md", "| Executive risk owner | risk appetite, production exception, crisis priorities | monthly critical-risk review |", "| Executive risk owner | risk appetite, nonconformant emergency deviation, crisis priorities | monthly critical-risk review |")
    replace("docs/en/PRACTICE_GUIDE.md", "- phishing-resistant MFA for provider privilege and tenant owners;", "- phishing-resistant MFA for provider privilege and high-impact tenant administrative roles according to service risk;")
    replace("docs/en/PRACTICE_GUIDE.md", "| ABU | tenant trust tiers, AUP, quota/rate/cost/capacity, egress, cases and appeal | quota bypass, cryptomining, denial-of-wallet, prohibited egress | onboarding decision, enforcement reason, case and restoration |", "| ABU | tenant trust tiers, AUP, quota/rate/cost/capacity, egress, cases and appeal | quota bypass, unauthorized cryptomining or other policy-prohibited workload, denial-of-wallet, prohibited egress | onboarding decision, enforcement reason, case and restoration |")
    replace("docs/en/PRACTICE_GUIDE.md", "- private API server and etcd; strong administrator and workload identity;", "- provider-only controllers and etcd are private; a customer-facing API endpoint is private by default or explicitly approved, strongly authenticated, source/rate restricted, DDoS-protected, and audited; strong administrator and workload identity;")
    replace("docs/en/PRACTICE_GUIDE.md", "- controller/database backup, accounting integrity, failover, and recovery.", "- controller/database backup, accounting integrity, failover, and recovery.\n- Slurm accounts, associations, partitions, QOS, and MCS labels support scheduling and information controls but are not a complete tenant-isolation boundary without OS/runtime, storage, network/fabric, and credential enforcement.")
    replace(
        "docs/en/PRACTICE_GUIDE.md",
        "Treat dedication, hardware partitioning, virtualization, and time slicing as different products. Document memory, cache, DMA, fault, reset, telemetry, and topology properties. Do not use time slicing as a substitute for a hardware security boundary. Sensitive workloads use an isolation mode justified by the threat model and tested on the deployed hardware/driver/firmware stack.",
        "Treat dedication, hardware partitioning, mediated virtualization, and scheduler-level sharing as different products. Scheduler-level Kubernetes GPU time-slicing/oversubscription does not by itself provide memory or fault isolation; a supported hypervisor-mediated vGPU mode can have different properties. Never infer isolation from the phrase ‘time-sliced.’ Document and test memory, cache, DMA/IOMMU, fault, reset, telemetry, topology, performance-interference, hardware, hypervisor, driver, firmware, and configuration properties against the service threat model.",
    )
    replace(
        "docs/en/PRACTICE_GUIDE.md",
        "A VPC or Kubernetes NetworkPolicy does not prove the high-performance data path. Test P_Key membership and enforcement, RDMA reachability, fabric-manager authority, DPU assignment, storage access, stale-controller state, and reallocation cleanup. Protect fabric and DPU controllers as provider roots.",
        "A VPC or Kubernetes NetworkPolicy does not prove the high-performance data path. InfiniBand P_Key membership is one partitioning mechanism—not evidence of complete tenant isolation by itself. Test membership type and enforcement, default-partition policy, RDMA reachability, fabric-manager authority, DPU assignment, storage access, stale-controller state, and reallocation cleanup on the deployed topology. Protect fabric and DPU controllers as provider roots.",
    )
    replace("docs/en/PRACTICE_GUIDE.md", "Critical logs and evidence must be exported to a boundary that ordinary source administrators cannot silently alter.", "Critical logs and evidence must be exported to a boundary with administrative and observational separation sufficient to prevent ordinary source administrators from silently altering the record; this does not universally require a separate physical system.")
    replace("docs/en/PRACTICE_GUIDE.md", "9. tenant fraud, cryptomining, prohibited workload, quota bypass, or denial of wallet;", "9. tenant fraud, unauthorized cryptomining or another policy-prohibited workload, quota bypass, or denial of wallet;")
    replace("docs/en/PRACTICE_GUIDE.md", "- time-sliced GPUs marketed as hardware-separated tenants;", "- scheduler-level shared GPU replicas—or any sharing mode lacking deployment-specific evidence—marketed as hardware-separated tenants;")

    replace("docs/zh-CN/PRACTICE_GUIDE.md", "本文保持厂商中立；出现的产品类别仅作能力示例，不构成采购建议。", "本文保持厂商中立；出现的产品类别仅作能力示例，不构成采购建议。所有实施声明都应同时应用[范围与局限](SCOPE_AND_LIMITATIONS.md)。")
    replace("docs/zh-CN/PRACTICE_GUIDE.md", "| 高管风险 Owner | 风险偏好、生产例外、危机优先级 | 每月审阅关键风险 |", "| 高管风险 Owner | 风险偏好、不符合基线的紧急偏离、危机优先级 | 每月审阅关键风险 |")
    replace("docs/zh-CN/PRACTICE_GUIDE.md", "- 服务商特权身份及租户 Owner 使用抗钓鱼 MFA；", "- 服务商特权身份及按服务风险判定的高影响租户管理角色使用抗钓鱼 MFA；")
    replace("docs/zh-CN/PRACTICE_GUIDE.md", "| ABU | 租户信任分级、AUP、配额/速率/成本/容量、出网、Case 与申诉 | 配额绕过、挖矿、Denial-of-wallet、禁止出网 | 准入判定、执行原因、Case 和恢复记录 |", "| ABU | 租户信任分级、AUP、配额/速率/成本/容量、出网、Case 与申诉 | 配额绕过、未经授权的挖矿或其他 Policy 禁止工作负载、Denial-of-wallet、禁止出网 | 准入判定、执行原因、Case 和恢复记录 |")
    replace("docs/zh-CN/PRACTICE_GUIDE.md", "- 私有 API Server 和 etcd，强管理员及工作负载身份；", "- 服务商专用 Controller 与 etcd 私有；面向客户的 API Endpoint 默认私有，或经过显式批准并实施强认证、来源/速率限制、DDoS 防护与完整审计；使用强管理员及工作负载身份；")
    replace("docs/zh-CN/PRACTICE_GUIDE.md", "- Controller/Database Backup、Accounting Integrity、Failover 与 Recovery。", "- Controller/Database Backup、Accounting Integrity、Failover 与 Recovery。\n- Slurm Account、Association、Partition、QOS 和 MCS Label 可约束调度和信息可见性，但如果缺少 OS/Runtime、Storage、Network/Fabric 与 Credential Enforcement，就不是完整租户隔离边界。")
    replace(
        "docs/zh-CN/PRACTICE_GUIDE.md",
        "将专属、硬件分区、虚拟化与 Time-slicing 视为不同产品。分别声明显存、Cache、DMA、Fault、Reset、Telemetry 和 Topology 属性。Time-slicing 不能替代硬件安全边界；敏感工作负载只能使用经威胁模型证明且在真实 Hardware/Driver/Firmware Stack 上通过测试的隔离模式。",
        "将专属、硬件分区、受 Hypervisor 仲裁的虚拟化和调度器级共享视为不同产品。Kubernetes GPU 调度器级 Time-slicing/超卖本身不提供显存或故障隔离；受支持的 vGPU 模式可能具有不同属性。绝不能仅根据 ‘Time-sliced’ 名称推断隔离。应针对服务威胁模型，逐项声明并测试显存、Cache、DMA/IOMMU、Fault、Reset、Telemetry、Topology、性能干扰、Hardware、Hypervisor、Driver、Firmware 与 Configuration。",
    )
    replace(
        "docs/zh-CN/PRACTICE_GUIDE.md",
        "VPC 或 Kubernetes NetworkPolicy 不能证明高性能数据路径已经隔离。必须测试 P_Key Membership/Enforcement、RDMA Reachability、Fabric Manager Authority、DPU Assignment、Storage Access、Controller Stale State 和重新分配清理。Fabric 和 DPU Controller 应按服务商 Root 保护。",
        "VPC 或 Kubernetes NetworkPolicy 不能证明高性能数据路径已经隔离。InfiniBand P_Key Membership 只是分区机制之一，不能单独证明完整租户隔离。必须在真实拓扑上测试 Membership Type/Enforcement、Default Partition Policy、RDMA Reachability、Fabric Manager Authority、DPU Assignment、Storage Access、Controller Stale State 和重新分配清理。Fabric 和 DPU Controller 应按服务商 Root 保护。",
    )
    replace("docs/zh-CN/PRACTICE_GUIDE.md", "关键日志与证据必须导出到普通源系统管理员无法静默修改的边界。", "关键日志与证据必须导出到具有足够管理与观察分离的边界，使普通源系统管理员无法静默修改记录；这并不普遍要求单独的物理系统。")
    replace("docs/zh-CN/PRACTICE_GUIDE.md", "9. 租户欺诈、挖矿、禁止工作负载、配额绕过或 Denial-of-wallet；", "9. 租户欺诈、未经授权的挖矿或其他 Policy 禁止工作负载、配额绕过或 Denial-of-wallet；")
    replace("docs/zh-CN/PRACTICE_GUIDE.md", "- 将 Time-sliced GPU 宣传为硬件级租户隔离；", "- 将调度器级共享 GPU Replica，或任何缺乏部署特定证据的 Sharing Mode，宣传为硬件级租户隔离；")


def patch_architectures() -> None:
    replace("docs/en/REFERENCE_ARCHITECTURE.md", "It is vendor neutral. A NeoCloud may implement components differently, but it must preserve the security invariants and evidence outcomes.", "It is vendor neutral. A NeoCloud may implement components differently, but it must preserve the security invariants and evidence outcomes. Read [Scope and Limitations](SCOPE_AND_LIMITATIONS.md) before treating a logical component as a product or a hardware-specific guarantee.")
    replace("docs/en/REFERENCE_ARCHITECTURE.md", "- the evidence plane must be protected independently from the systems being evaluated.", "- the evidence plane needs administrative and observational independence appropriate to risk; this is a logical trust requirement and does not always require separate physical infrastructure.")
    replace("docs/en/REFERENCE_ARCHITECTURE.md", "- workload identity using attested, short-lived credentials rather than embedded secrets;", "- short-lived workload identity rather than embedded secrets, with attestation binding where supported and justified by the threat model;")
    replace("docs/en/REFERENCE_ARCHITECTURE.md", "- hardened and privately reachable control planes;", "- provider-only controllers and databases kept private; customer-facing API endpoints private by default or explicitly approved, strongly authenticated, restricted, abuse-protected, and audited;")
    replace("docs/en/REFERENCE_ARCHITECTURE.md", "A compromised BMC or fabric controller is a root-level incident.", "A compromised BMC or fabric controller is a provider-root or fleet-impacting incident whose scope depends on the deployed authority and topology.")
    replace("docs/en/REFERENCE_ARCHITECTURE.md", "Traffic between zones is not automatically trusted. Every crossing requires an authenticated identity, an allowed purpose, an explicit policy, protected transport where appropriate, logging, and a tested failure behavior.", "Traffic between zones is not automatically trusted. Every crossing requires an authenticated endpoint identity or an authoritative identity-to-resource binding where the protocol permits, an allowed purpose, explicit policy, protected transport where appropriate, logging, and tested failure behavior. Low-level physical or L2 paths must not be assumed to carry an application tenant identifier.")
    replace("docs/en/REFERENCE_ARCHITECTURE.md", "1. A tenant identifier is carried and validated at every object, message, controller and storage boundary.", "1. Tenant and authorization context is carried and validated at every control-plane object/message boundary and enforced through an authoritative binding at storage, compute, accelerator, and fabric resources.")
    replace("docs/en/REFERENCE_ARCHITECTURE.md", "12. AI agents and security automation cannot expand their own goal, scope, tools, credentials, approval authority or verifier.", "12. AI agents and security automation cannot expand their own authorization envelope, tools, credentials, approval authority or verifier; goal or task changes require a separately authorized transition.")
    replace("docs/en/REFERENCE_ARCHITECTURE.md", "Use strong VM/container isolation; declare full-GPU, hardware partition or other sharing mode; isolate device management; validate reset and memory clearing; provide tenant network/storage controls; preserve allocation topology and host/GPU lineage.", "Use strong VM/container isolation; distinguish full-GPU dedication, hardware partitioning, hypervisor-mediated vGPU, and scheduler-level sharing; isolate device management; validate the product/version/configuration-specific memory, fault, reset, performance-interference, and cleanup properties; provide tenant network/storage controls; preserve allocation topology and host/GPU lineage.")
    replace("docs/en/REFERENCE_ARCHITECTURE.md", "Protect controller/database/REST/authentication; enforce accounts, partitions, QOS and associations; secure prolog/epilog and modules; isolate shared storage and fabric; prevent users from modifying controller state; collect job/accounting and privileged activity evidence.", "Protect controller/database/REST/authentication; govern accounts, partitions, QOS, associations, and MCS where used; secure prolog/epilog and modules; isolate shared storage and fabric; prevent users from modifying controller state; collect job/accounting and privileged activity evidence. Slurm scheduling labels and MCS controls do not replace OS/runtime, credential, storage, and network/fabric isolation.")

    replace("docs/zh-CN/REFERENCE_ARCHITECTURE.md", "它不绑定特定厂商；不同 NeoCloud 可以采用不同组件，但必须保持同样的安全不变量和可证明结果。", "它不绑定特定厂商；不同 NeoCloud 可以采用不同组件，但必须保持同样的安全不变量和可证明结果。将逻辑组件解释为具体产品或硬件保证前，应先阅读[范围与局限](SCOPE_AND_LIMITATIONS.md)。")
    replace("docs/zh-CN/REFERENCE_ARCHITECTURE.md", "- 证据平面必须独立于被评估系统进行保护。", "- 证据平面需要具备与风险相匹配的管理和观察独立性；这是逻辑信任要求，并不总是要求单独物理基础设施。")
    replace("docs/zh-CN/REFERENCE_ARCHITECTURE.md", "- 基于证明的短期工作负载身份，替代嵌入式 Secret；", "- 使用短期工作负载身份替代嵌入式 Secret，并在产品支持且威胁模型证明必要时绑定 Attestation；")
    replace("docs/zh-CN/REFERENCE_ARCHITECTURE.md", "最低能力：私有并加固的控制面；", "最低能力：服务商专用 Controller/Database 保持私有；面向客户的 API Endpoint 默认私有，或经过显式批准并实施强认证、访问限制、抗滥用和完整审计；")
    replace("docs/zh-CN/REFERENCE_ARCHITECTURE.md", "BMC 或 Fabric Controller 失陷属于信任根级事件。", "BMC 或 Fabric Controller 失陷属于服务商信任根或全局影响事件，具体范围取决于实际权限与拓扑。")
    replace("docs/zh-CN/REFERENCE_ARCHITECTURE.md", "区域间流量永不自动可信。每次跨区都要求已认证身份、允许的目的、显式策略、适当的传输保护、日志和经过测试的失败行为。", "区域间流量永不自动可信。每次跨区都要求已认证 Endpoint Identity，或在协议允许时使用权威 Identity-to-Resource Binding，并具备允许目的、显式策略、适当的传输保护、日志和经过测试的失败行为。底层物理或 L2 路径不能被假定会携带应用层 Tenant ID。")
    replace("docs/zh-CN/REFERENCE_ARCHITECTURE.md", "1. 每个 Object、Message、Controller 和 Storage Boundary 都携带并验证 Tenant ID。", "1. 每个控制面 Object/Message Boundary 都携带并验证 Tenant/Authorization Context，并通过权威绑定在 Storage、Compute、Accelerator 与 Fabric Resource 上执行。")
    replace("docs/zh-CN/REFERENCE_ARCHITECTURE.md", "12. AI Agent/安全自动化不能自行扩大 Goal、Scope、Tool、Credential、Approval Authority 或 Verifier。", "12. AI Agent/安全自动化不能自行扩大 Authorization Envelope、Tool、Credential、Approval Authority 或 Verifier；Goal/Task 变化必须经过独立授权的状态转换。")
    replace("docs/zh-CN/REFERENCE_ARCHITECTURE.md", "实施强 VM/Container 隔离；声明 Full GPU、Hardware Partition 或其他 Sharing；隔离设备管理；验证 Reset/Memory Clear；提供 Tenant Network/Storage Control；保留 Allocation Topology 和 Host/GPU Lineage。", "实施强 VM/Container 隔离；区分 Full-GPU Dedication、Hardware Partition、Hypervisor-mediated vGPU 与 Scheduler-level Sharing；隔离设备管理；针对具体 Product/Version/Configuration 验证 Memory、Fault、Reset、Performance Interference 与 Cleanup；提供 Tenant Network/Storage Control；保留 Allocation Topology 和 Host/GPU Lineage。")
    replace("docs/zh-CN/REFERENCE_ARCHITECTURE.md", "保护 Controller/Database/REST/Auth；执行 Account、Partition、QOS 和 Association；保护 Prolog/Epilog 与 Module；隔离 Shared Storage/Fabric；阻止普通用户改变 Controller State；收集 Job/Accounting 和高权限证据。", "保护 Controller/Database/REST/Auth；治理 Account、Partition、QOS、Association 以及采用时的 MCS；保护 Prolog/Epilog 与 Module；隔离 Shared Storage/Fabric；阻止普通用户改变 Controller State；收集 Job/Accounting 和高权限证据。Slurm Scheduling Label 与 MCS 不能替代 OS/Runtime、Credential、Storage 和 Network/Fabric Isolation。")


def patch_roadmaps_metrics_references() -> None:
    replace("docs/en/ROADMAP.md", "Progress is measured by independently verified outcomes and reduced exposure, not documents produced or tools purchased.", "Progress is measured by independently verified outcomes and reduced exposure, not documents produced or tools purchased. Dates, percentages, and phase targets are project-defined planning defaults—not externally validated industry benchmarks—and must be adapted using [Scope and Limitations](SCOPE_AND_LIMITATIONS.md).")
    replace("docs/en/ROADMAP.md", "- phishing-resistant and just-in-time human access plus attested, short-lived workload/agent identity;", "- phishing-resistant and just-in-time human access plus short-lived workload/agent identity, bound to attestation where supported and justified;")
    replace("docs/en/ROADMAP.md", "1. **Workload identity:** issue short-lived, attested identities to services, jobs, nodes and agents; remove embedded cloud/API credentials.", "1. **Workload identity:** issue short-lived identities to services, jobs, nodes and agents; bind them to attested state where supported and justified; remove embedded cloud/API credentials.")
    replace("docs/en/ROADMAP.md", "- At least 80% of production workloads use short-lived or brokered credentials.", "- An organization-defined target for production workloads using short-lived or brokered credentials is met; 80% by month six is an illustrative planning target, not an industry benchmark.")
    replace("docs/en/ROADMAP.md", "- T0 exception authority and maximum lifetime;", "- authority, maximum lifetime, rollback criteria, and explicitly nonconformant status for any T0 emergency deviation;")

    replace("docs/zh-CN/ROADMAP.md", "进展应以独立验证的安全结果和真实暴露下降衡量，而不是文档数量或采购工具数量。", "进展应以独立验证的安全结果和真实暴露下降衡量，而不是文档数量或采购工具数量。日期、百分比和阶段目标是本项目定义的规划默认值，不是经外部验证的行业 Benchmark，必须结合[范围与局限](SCOPE_AND_LIMITATIONS.md)调整。")
    replace("docs/zh-CN/ROADMAP.md", "- 人员使用抗钓鱼/JIT 权限，Workload/Agent 使用经过证明的短期身份；", "- 人员使用抗钓鱼/JIT 权限，Workload/Agent 使用短期身份，并在产品支持且威胁模型证明必要时绑定 Attestation；")
    replace("docs/zh-CN/ROADMAP.md", "1. **Workload Identity：** 为 Service、Job、Node、Agent 颁发短期、经过证明的 Identity，逐步消除嵌入 Credential。", "1. **Workload Identity：** 为 Service、Job、Node、Agent 颁发短期 Identity，在产品支持且威胁模型证明必要时绑定 Attested State，逐步消除嵌入 Credential。")
    replace("docs/zh-CN/ROADMAP.md", "- 至少 80% 生产 Workload 使用短期或 Brokered Credential；", "- 达到组织自定的生产 Workload 短期/Brokered Credential 目标；‘第六个月 80%’仅为示例规划值，不是行业 Benchmark；")
    replace("docs/zh-CN/ROADMAP.md", "T0 Exception Authority/Maximum Lifetime", "T0 紧急偏离的 Authority、Maximum Lifetime、Rollback Criteria 和明确‘不符合’状态")

    replace("docs/en/METRICS_AND_ASSURANCE.md", "the [Practice Guide](PRACTICE_GUIDE.md), and the repository templates.", "the [Practice Guide](PRACTICE_GUIDE.md), the [Scope and Limitations](SCOPE_AND_LIMITATIONS.md), and the repository templates.")
    replace("docs/en/METRICS_AND_ASSURANCE.md", "Critical evidence should be exported to a protected boundary and linked to stable service, tenant, subject, workload, host, GPU, fabric, data/model, artifact, request, and policy identifiers.", "Critical evidence should be exported to a protected boundary with administrative and observational separation appropriate to risk and linked to stable service, tenant, subject, workload, host, GPU, fabric, data/model, artifact, request, and policy identifiers. Physical separation is not universally required.")
    replace("docs/en/METRICS_AND_ASSURANCE.md", "Targets below are reference starting points. Each organization must set targets based on service commitments and risk, while preserving all T0 hard gates.", "Targets below are project-defined reference starting points, not externally validated industry benchmarks. Each organization must set targets based on service commitments, deployed technology, threat model, and risk, while preserving all applicable T0 hard gates.")

    replace("docs/zh-CN/METRICS_AND_ASSURANCE.md", "[实践指南](PRACTICE_GUIDE.md)及仓库模板共同使用。", "[实践指南](PRACTICE_GUIDE.md)、[范围与局限](SCOPE_AND_LIMITATIONS.md)及仓库模板共同使用。")
    replace("docs/zh-CN/METRICS_AND_ASSURANCE.md", "关键证据应导出到受保护边界，并使用稳定标识关联 Service、Tenant、Subject、Workload、Host、GPU、Fabric、Data/Model、Artifact、Request 和 Policy。", "关键证据应导出到具有与风险相匹配的管理和观察分离的受保护边界，并使用稳定标识关联 Service、Tenant、Subject、Workload、Host、GPU、Fabric、Data/Model、Artifact、Request 和 Policy；这并不普遍要求物理隔离。")
    replace("docs/zh-CN/METRICS_AND_ASSURANCE.md", "下列目标是参考起点。组织应根据服务承诺和风险调整目标，但不得削弱 T0 硬门槛。", "下列目标是本项目定义的参考起点，不是经外部验证的行业 Benchmark。组织应根据服务承诺、实际技术栈、威胁模型和风险调整目标，但不得削弱适用的 T0 硬门槛。")

    replace("REFERENCES.md", "23. NIST NCCoE, *Accelerating the Adoption of Software and AI Agent Identity and Authorization*, concept paper, 2026-02-05.", "23. NIST NCCoE, *Accelerating the Adoption of Software and AI Agent Identity and Authorization*, concept paper, 2026-02-05; project status was ‘Reviewing Comments’ at the baseline date and this is not a final standard.")
    replace("REFERENCES.md", "49. NVIDIA GPU Operator, *Time-Slicing GPUs in Kubernetes*.", "49. NVIDIA GPU Operator, *Time-Slicing GPUs in Kubernetes*; the documented scheduler-level replicas do not provide memory or fault isolation from each other.")
    replace("REFERENCES.md", "55. NVIDIA, *DCGM Health and Diagnostics*. https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/feature-overview.html", "55. NVIDIA, *DCGM Health and Diagnostics*. https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/feature-overview.html\n56. NVIDIA AI Enterprise, *vGPU for Compute Overview*; supported mediated vGPU modes have product- and configuration-specific memory, fault, and scheduling properties distinct from scheduler-level Kubernetes time-slicing. https://docs.nvidia.com/ai-enterprise/release-8/latest/infra-software/vgpu/overview.html")
    # Keep numbering unique after adding the vGPU reference.
    for old, new in [(61, 62), (60, 61), (59, 60), (58, 59), (57, 58), (56, 57)]:
        replace("REFERENCES.md", f"\n{old}. ", f"\n{new}. ")
    replace("REFERENCES.md", "62. NIST, *SP 800-204D: Strategies for the Integration of Software Supply Chain Security in DevSecOps CI/CD Pipelines*. https://csrc.nist.gov/pubs/sp/800/204/d/final", """62. NIST, *SP 800-204D: Strategies for the Integration of Software Supply Chain Security in DevSecOps CI/CD Pipelines*. https://csrc.nist.gov/pubs/sp/800/204/d/final

## Identity, platform integrity, and sanitization

63. NIST, *SP 800-63-4: Digital Identity Guidelines*, final, 2025. https://pages.nist.gov/800-63-4/
64. NIST, *SP 800-63B-4: Digital Identity Guidelines—Authentication and Authenticator Management*, final, 2025. At AAL2 verifiers must offer a phishing-resistant option; requirements for specific populations and assurance levels depend on applicability. https://pages.nist.gov/800-63-4/sp800-63b.html
65. NIST, *SP 800-88 Rev. 2: Guidelines for Media Sanitization*, final, 2025; it supersedes Rev. 1 and emphasizes a risk-based sanitization program and validation. https://csrc.nist.gov/pubs/sp/800/88/r2/final
66. NIST, *SP 800-193: Platform Firmware Resiliency Guidelines*, final, 2018. https://csrc.nist.gov/pubs/sp/800/193/final
67. NIST, *SP 800-160 Vol. 1 Rev. 1: Engineering Trustworthy Secure Systems*, final, 2022. https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final""")
    replace("REFERENCES.md", "- Use Kubernetes, SPIFFE/SPIRE, Slurm, NVIDIA, and deployed platform documentation for implementation-specific safeguards and negative-test design.", "- Use NIST SP 800-63-4/-63B-4 to scope identity-assurance and authenticator decisions; do not generalize federal or AAL-specific requirements to every private service.\n- Use Kubernetes, SPIFFE/SPIRE, Slurm, NVIDIA, and deployed platform documentation for implementation-specific safeguards and negative-test design. Distinguish scheduler-level GPU sharing from mediated vGPU and hardware partitioning.\n- Use NIST SP 800-88 Rev. 2 for media-sanitization program and validation; use vendor/device evidence and the service threat model for volatile accelerator state that is not conventional storage media.\n- Use NIST SP 800-193 and SP 800-160 Vol. 1 Rev. 1 for firmware resilience and trustworthy-system engineering.")


def main() -> None:
    patch_practice_guides()
    patch_architectures()
    patch_roadmaps_metrics_references()
    print("Applied technical accuracy corrections")


if __name__ == "__main__":
    main()
