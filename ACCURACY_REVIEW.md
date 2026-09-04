# Accuracy Review / 准确性审计

**Review date / 审计日期:** 2026-09-04  
**Reviewed version / 审计版本:** 1.0.0-draft.2  
**Scope / 范围:** repository positioning, normative consistency, primary-source currency, GPU/fabric/orchestrator claims, assurance semantics, contribution workflow, and GitHub metadata intent

## Result / 结论

The repository is structurally coherent and suitable as a **project-defined implementation draft** after the corrections below. It must not be presented as an adopted industry standard, deployed security product, certification, or openly licensed project. The machine-readable catalog remains internally complete at 18 domains and 90 controls.

修订后，仓库在结构上保持一致，可作为**项目自定义的实施草案**使用；不得将其描述为已被行业采纳的标准、已部署产品、认证体系或已开放许可的项目。机器可读目录仍保持 18 个安全域和 90 项控制完整性。

## Corrections made / 已修复问题

| Area | Previous risk | Correction |
|---|---|---|
| Project identity / 项目定位 | “Open” and “unified control-plane” wording overstated a private, unlicensed documentation/control project | Reframed as a vendor-neutral reference baseline and explicitly stated that it is not a deployed product |
| T0 governance | Emergency exception wording contradicted the hard `NO-GO` algorithm | Defined a nonconformant emergency deviation that cannot create `PASS`, `VERIFIED`, or conformity |
| Review cadence | T3 was semi-annual in prose but annual in the catalog | Set semi-annual control-owner review plus annual independent verification and material-change review |
| GPU sharing | “Time-slicing” was treated too generically | Distinguished scheduler-level Kubernetes oversubscription from mediated vGPU, hardware partitioning, and dedication |
| GPU cleanup | Reset/sanitization language risked implying universal device guarantees | Required vendor-documented, device/mode/version-specific procedures, validation, and quarantine/dedication when a defensible claim is unavailable |
| InfiniBand/RDMA | P_Key and VPC terminology could be read as complete isolation proof | Treated P_Key as one mechanism and required membership/default-partition/controller/topology/negative-path validation |
| Kubernetes control plane | “Private API server” was too categorical for some managed service designs | Kept provider-only controllers/databases private while permitting an explicitly approved, hardened customer-facing endpoint |
| Slurm isolation | Scheduler constructs risked being read as security boundaries | Clarified that Account/Partition/QOS/MCS need OS/runtime, credential, storage, and fabric enforcement |
| Attestation/confidential computing | Wording risked treating an attestation label as end-to-end proof | Made claims product/version/configuration/threat-model specific and retained independent validation |
| Evidence independence | Could imply mandatory physical separation | Defined administrative and observational independence appropriate to risk |
| MFA | Risked implying NIST universally mandates phishing resistance for every private tenant owner | Kept phishing-resistant MFA as this project's privileged-access baseline and clarified NIST applicability |
| Contributions | CONTRIBUTING incorrectly stated that the repository did not require GitHub Actions | Replaced with the actual local/CI validator workflow |
| Publication | No License, Security Policy, description, homepage, or topics were documented | Added scope, security reporting, and intended repository-metadata documents; license remains explicitly undecided |

## Primary-source checks / 一手资料核对

- NIST SP 800-234 is final (May 2026); SP 800-239 and SP 800-209 Rev. 1 were drafts at the baseline date.
- CSA CCM v4.1 contains 207 controls across 17 domains; CSA AICM v1.1 contains 247 control objectives across 18 domains.
- NVIDIA GPU Operator scheduler-level time-slicing states that replicas have no memory or fault isolation, while supported mediated vGPU modes can have different hardware isolation properties.
- Slurm MCS documentation shows that labels and plugins require careful configuration and are not a complete multi-layer isolation boundary.
- NIST SP 800-88 Rev. 2 is the current final media-sanitization guide; conventional media guidance must not be overextended to volatile accelerator state without device evidence.
- NIST SP 800-63 Revision 4 is current; AAL- and federal-specific phishing-resistance requirements should not be generalized without an applicability decision.
- OWASP Agent Control Standard was released on 2026-09-01; it is treated as an emerging informative source, not a certification standard.

Authoritative links and publication status are maintained in [`REFERENCES.md`](REFERENCES.md).

## Remaining limitations / 剩余局限

1. No production NeoCloud deployment was tested. Control effectiveness still requires service-specific implementation and independent verification.
2. No formal crosswalk or legal analysis was performed. External mappings remain informative.
3. Hardware isolation and cleanup claims vary by product, generation, firmware, driver, hypervisor, topology, and configuration.
4. Roadmap dates and numerical metrics are planning defaults, not validated industry benchmarks.
5. The repository is private and has no selected license. Public release and reuse terms remain unresolved.
6. GitHub sidebar metadata is represented in [`.github/repository-metadata.json`](.github/repository-metadata.json) but requires manual synchronization because the available repository integration does not expose a metadata-update operation.

See [Scope and Limitations](docs/en/SCOPE_AND_LIMITATIONS.md) / [范围与局限](docs/zh-CN/SCOPE_AND_LIMITATIONS.md).
