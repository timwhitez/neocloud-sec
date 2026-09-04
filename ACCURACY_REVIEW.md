# Accuracy Review / 准确性审计

**Review date / 审计日期:** 2026-09-04  
**Reviewed release / 审计版本:** 1.0.0-draft.1  
**Scope / 范围:** project positioning, normative consistency, source currency, GPU/fabric/orchestrator claims, AI-agent controls, assurance semantics, metrics, contribution workflow, and GitHub metadata

## Result / 结论

After the corrections recorded below, the repository is structurally coherent and suitable as a **project-authored implementation draft and reference baseline**. It must not be presented as an adopted industry standard, deployed security product, certification, legal determination, or proof that a provider is secure. The normative catalog remains internally complete at 18 domains and 90 stable control IDs.

完成下列修订后，仓库在结构上保持一致，可作为**项目编制的实施草案与参考基线**使用；不得将其描述为已被行业采纳的标准、已部署产品、认证、法律结论或服务商已经安全的证明。规范控制目录仍保持 18 个安全域与 90 个稳定 Control ID。

## Material corrections / 重大修订

| Area | Previous risk | Corrected treatment |
|---|---|---|
| Project identity / 项目定位 | “Open” and “unified control plane” language overstated a private, unlicensed documentation/control project | Described it as a vendor-neutral bilingual baseline and implementation guide, not a deployed product or adopted standard |
| T0 governance | Emergency exception language conflicted with the hard `NO-GO` algorithm | A time-bounded emergency business decision remains `NO_GO_NONCONFORMANT` and cannot create `PASS`, `VERIFIED`, or conformity |
| Verification cadence | Higher-assurance T3 cadence was unclear or less frequent than owner review expectations | T3 uses at least semi-annual owner review, annual independent assessment, and material-change revalidation |
| Identity semantics | Persistent identity, credentials, sessions, privilege, and delegation were conflated | Identity remains stable enough for attribution; credentials, sessions, grants, and delegated authority are short-lived where feasible |
| API ingress | Initial anonymous requests were implicitly required to be authenticated | Anonymous/untrusted status is explicit; authentication is mandatory before tenant-specific, privileged, state-changing, costly, or sensitive actions |
| GPU sharing | “Time-slicing” was treated as one universal virtualization property | Scheduler-level Kubernetes time-slicing is separated from mediated vGPU, hardware partitioning, and full-device dedication |
| GPU cleanup | Reset/sanitization language could imply universal device guarantees | Claims must be vendor-documented and device/mode/version/configuration specific; quarantine, retirement, or dedication is used when defensible cleanup cannot be shown |
| InfiniBand/RDMA | P_Key could be read as complete isolation proof | P_Key is one partitioning mechanism; membership type, default partition, controller authority, DPU/NIC/storage state, topology, reconciliation, and deployed-path tests remain necessary |
| Kubernetes | “Private API server” was too categorical for managed customer endpoints | Provider-only controllers/databases stay private; an explicitly approved customer-facing endpoint can use a protected public edge |
| Slurm | Accounts, partitions, QOS, and MCS labels risked being read as complete isolation | Scheduler/visibility mechanisms require OS/runtime, credential, storage, network/fabric, and node enforcement |
| Attestation and confidential computing | Labels or reports risked being treated as end-to-end proof | Claims are product/version/configuration/threat-model specific and do not alone prove application behavior, key release, end-to-end confidentiality, or absence of side channels |
| Supply-chain signatures | Signature was treated too close to proof of artifact safety | Signature is evaluated with source, provenance, key custody, compatibility, policy, vulnerability, admission, revocation, and recall |
| Evidence independence | “Separate evidence” could imply mandatory physical separation | Sufficient administrative and observational independence is required; physical separation depends on risk and architecture |
| Metrics | Unknown critical scope could fall out of denominators; 95% targets could mask gates | Critical unknowns remain failures; applicable T0, critical ownership, and required T0 telemetry remain 100% gates; 95% is only a disclosed reference target for non-gate coverage |
| AI agents | Uniform full-autonomy controls could overburden low-impact assistants | Controls now scale with authority and impact; high-impact/adaptive workflows receive stronger approval, stop, trace, rollback, and verifier requirements |
| GitHub presentation | Description/topics/license/security-reporting status was absent or ambiguous | Added concise metadata, public-topic warning, publication checklist, no-license warning, and correct private/public reporting guidance |
| Evidence template state | The example used `NOT_REVIEWED`, which is outside the catalog verification-result enum | Replaced it with `NOT_TESTED` and explicitly separated control lifecycle state from verification result |
| Shared-responsibility template | Combined rows could make provider-exclusive Kubernetes/Slurm control planes and fabric roots appear jointly owned | Split provider-owned roots from customer-controlled workload, job, network, and agent configuration |
| Threat-model template | `time-slicing without isolation`, `PKey`, and MCS wording could be read as categorical or complete isolation claims | Bound the risk to an absent justified memory/fault boundary, standardized `P_Key`, and stated that scheduler/visibility controls are not complete isolation |
| Version consistency | New review and scope documents referred to an unissued next-draft version | Aligned them with the repository contract and `VERSION` value `1.0.0-draft.1` |

## Primary-source checks / 一手资料核对

The review checked current or authoritative sources through the 2026-09-04 evidence cut-off, including:

- NIST CSF 2.0, SP 800-53 Rev. 5, SP 800-63 Revision 4, SP 800-88 Rev. 2, SP 800-193, SP 800-207/207A, SP 800-218/218A, SP 800-223, SP 800-228, SP 800-234, the draft SP 800-209 Rev. 1 and SP 800-239, AI RMF, and related NIST material;
- CSA CCM v4.1, AICM v1.1, AI-CAIQ, and AISMM;
- Kubernetes, SchedMD Slurm, SPIFFE, NVIDIA MIG/GPU sharing/vGPU/DCGM/Infrastructure Controller documentation;
- OWASP API Security and GenAI/agent material, MITRE ATT&CK/ATLAS, SLSA, Sigstore, OpenSSF, CIS, ISO, and CISA guidance;
- GitHub repository-topic, CLI/API metadata, and vulnerability-reporting documentation.

Publication status is recorded in [`REFERENCES.md`](REFERENCES.md). Final standards, drafts, public-review material, living projects, vendor guidance, and research do not carry the same authority.

## Remaining limitations / 剩余局限

1. No production NeoCloud service was assessed or tested; control effectiveness still requires service-specific implementation and independent verification.
2. No formal legal analysis, certification, or framework crosswalk was performed. External mappings remain informative.
3. Hardware isolation and cleanup vary by accelerator generation, device, firmware, driver, hypervisor, scheduler, topology, mode, error state, and configuration.
4. Roadmap dates and numerical targets are project planning defaults, not independently validated industry benchmarks.
5. The repository is private and no license has been selected. Public release and reuse terms remain unresolved.
6. GitHub About description, topics, homepage, visibility, merge settings, rulesets, and security settings are administrative state. Documentation does not prove they were applied. Topic names are public even on a private repository.
7. While private, the repository requires an already established trusted reporting channel. GitHub researcher-facing Private Vulnerability Reporting should be enabled and documented after public release if supported.

See [Scope and Limitations](docs/en/SCOPE_AND_LIMITATIONS.md) / [范围与局限](docs/zh-CN/SCOPE_AND_LIMITATIONS.md), [Repository Settings](.github/REPOSITORY_SETTINGS.md), and [Security Policy](SECURITY.md).
