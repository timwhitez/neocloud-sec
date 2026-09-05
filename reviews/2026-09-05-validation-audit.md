# Scoped source and validation audit / 范围内来源与校验审计

**Date:** 2026-09-05  
**Reviewed base commit:** `2bd7dd6241919226623f02b735f049449849535d`  
**Base Git tree:** `09fc7bd5209e8f3b9c602fc0be2e998c2b1b36e2`  
**New overlay version:** 1.0.1; core remains 1.0.0-draft.1

## Reproduced findings

| Finding | Evidence at the base commit | Treatment |
|---|---|---|
| Contradictory prior-coverage totals | The 40 records count 21 covered, 12 partial, 7 gap; the summary and old validator expected 17/17/6 | Correct the summary; derive and compare counts; retain a regression test |
| Schema files parsed but not applied | The old profile main loaded schema JSON without evaluating instances | Use Draft 2020-12 evaluation with date formats and no external schema-reference retrieval |
| CSV join not validated | Old template checks counted IDs/results but did not join mappings, severity or titles to the profile | Exact ID/control joins, severity/title checks, duplicate headers and row-width checks |
| Templates could suggest fabricated success | PASS and VERIFIED were not prohibited in repository examples | Keep repository templates UNKNOWN/PROPOSED/NOT_TESTED; real assessment is a separate private workflow |
| Invalid source locators | Article referenced a homepage; Security referenced `/security` | Record exact article and `/criteria/security` URLs and retrieval limitations |
| Ambiguous key naming and omitted explicit classes | Public item title combined C_Key/CC_Key; PM_Key and N2N_Key were not explicit in that finding group | Separate names and extend the existing group without changing stable IDs |
| Certification softened by project wording | Item 002 allowed equivalent ISMS evidence although the source asks for certification | Require certificate scope/validity for that mapped source criterion; no universal certification mandate added to the core |
| README/legacy-check conflict | templates/README.md omitted the legacy required NOT_REVIEWED and provider-root statements | Restore the meaning and terminology while distinguishing templates from assessments |
| Raw-catalog consumers could miss errata | No executable effective-catalog compiler | Add validated, non-mutating compilation with input/output digests and conflict rejection |

The historical 21/12/7 labels are project-authored judgments. Recounting them does not validate their original classification method or prove completeness of the external article. The former “40/40” language is narrowed to mapping inventory, not test execution or deployed effectiveness.

## Exact local source reconstruction

The following base files were reconstructed from authenticated connector reads and matched using Git's blob hash over exact UTF-8 bytes:

| File | Original Git blob SHA |
|---|---|
| controls/semianalysis-public-findings-profile.v1.json | `9bdc98f1a669b50ae508f1b500c4ce8b54482134` |
| templates/semianalysis-public-findings-assessment.csv | `0e046b5bb6aca405372ac08d1d84be31cbb49ea2` |

The profile was 37,941 bytes, including its trailing newline. Its real records reproduce the count contradiction. Other changed text was reviewed through connector reads. Existing files not changed by this patch remain in the base Git tree.

## Local test scope and limitations

The regression suite exercises the actual profile/schema/templates and a stable 90-ID membership contract. It includes malformed-input, source/date, coverage-count, CSV join, template-state and errata-conflict mutations. Errata unit tests use explicitly synthetic small catalog fixtures; they are not evidence of a production service or a complete hardware/software deployment.

This session did not obtain an authenticated full Git checkout in the local container. Therefore it does **not** claim that the complete pre-existing repository suite or an end-to-end compiler run against the full 78 KB core catalog was executed locally. Scoped tests, Python syntax and changed-file links were checked. The exact result and tested commit are recorded in the PR review. `scripts/check_local.py` is the complete local command for a real checkout; it fails on missing inputs instead of reporting success.

No GPU, Kubernetes, Slurm, fabric, DPU, Prometheus/Grafana or tenant environment was probed. No independent human assessor or independent subagent was used. This is an automated-assisted source/code review with a separate self-review pass, not independent operational assurance. GitHub Actions must remain skipped for this change because the owner has exhausted CI quota.

## Primary-source refresh

Sources were read on 2026-09-05; no fabricated page-content hashes are supplied. Links below identify sources, not licensed reproductions of their complete text.

| Source | What was checked | Limitation |
|---|---|---|
| [SemiAnalysis article](https://newsletter.semianalysis.com/p/most-neoclouds-suck-at-security) | Exact article locator and publicly indexed excerpts | Complete paid article not retrieved in this run |
| [ClusterMAX Security](https://www.clustermax.ai/criteria/security) | Public requirement page and source-specific certificate wording | Dynamic, proprietary methodology; no full scoring parity |
| [ClusterMAX site](https://www.clustermax.ai/) | 2.1 published/current; 3.0 advertised as coming soon | Publication snapshot, not a perpetual version assertion |
| [NVIDIA IB security](https://networking-docs.nvidia.com/nvidiainfinibandsecurityoverviewandguidelines/security-in-infiniband) | Key classes, SMP/P_Key separation and lease behavior | Device/firmware configuration remains deployment-specific |
| [BlueField modes](https://networking-docs.nvidia.com/bsp/480/modes-of-operation) | Host trust and restricted management boundary | Referenced BSP version; no live DPU verification |
| [Kubernetes multi-tenancy](https://kubernetes.io/docs/concepts/security/multi-tenancy/) | Control/data-plane separation and CNI enforcement | No single deployment is attested by this guidance |
| [Grafana data sources](https://grafana.com/docs/grafana/latest/datasources/) | Data-source authorization and edition distinction | Dashboard ACL is not a backend authorization test |
| [Prometheus security model](https://prometheus.io/docs/operating/security/) | HTTP/data-access trust assumptions | Gateway and backend configuration must be tested locally |
| [NVIDIA GPU sharing](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/gpu-sharing.html) | Device-plugin isolation and DCGM attribution limits | Not a statement about all mediated vGPU products |
| [jsonschema](https://pypi.org/project/jsonschema/) | 4.26.0 availability and explicit format-check activation | Dependency pins are not a full transitive hash lock |
| [NIST SP 800-239](https://csrc.nist.gov/pubs/sp/800/239/ipd) | AI data-center publication remains an initial public draft | Draft research input, not a final mandatory standard |
| [NIST SP 800-234](https://csrc.nist.gov/pubs/sp/800/234/final) | Published HPC overlay | No equivalence with this project's 90 controls claimed |

## 中文摘要

本轮修复统计与逐项记录矛盾、Schema 未真正执行、CSV 映射未核对、模板可能伪造通过、来源入口不准确、密钥命名歧义、认证含义被弱化、旧检查与模板说明冲突，以及程序读取原始目录时漏掉勘误的问题。新增中英文优先验证流程、严格离线校验、勘误编译器和负向回归测试。

本地验证范围是实际画像/Schema/模板与工具单元测试，不是完整仓库回归，更不是云环境实测。未获得完整本地认证 checkout，因此不重复之前过度宽泛的“全部校验已通过”声明。完整命令已提供，缺文件或缺依赖会失败。没有触发远端 Actions，没有修改仓库可见性、许可证或分支保护。
