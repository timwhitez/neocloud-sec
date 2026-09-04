# NeoCloud service threat model / 服务威胁建模模板

## 1. Document control

- Service:
- Version / architecture commit:
- Service profile:
- Business owner:
- Technical owner:
- Security reviewer:
- Data/privacy reviewer:
- Date / next review:
- Production regions and jurisdictions:

## 2. Security objectives

State confidentiality, integrity, availability, privacy, tenant-isolation, safety, sovereignty, and recoverability objectives. Include explicit non-goals.

## 3. Assets and crown jewels

| Asset | Owner | Data class | Tenant scope | Integrity need | Availability need | Recovery need |
|---|---|---|---|---|---|---|
| | | | | | | |

At minimum consider credentials, API tokens, signing keys, images, infrastructure code, scheduler state, datasets, models, checkpoints, inference inputs/outputs, KV caches, GPU/HBM contents, storage snapshots, audit evidence, billing and quota state, BMC/DPU/firmware configuration, and customer contact data.

## 4. Actors

- Anonymous internet user
- Authenticated tenant administrator
- Tenant workload or AI agent
- Malicious or compromised tenant
- Provider support engineer
- Provider privileged administrator
- CI/CD and automation identity
- Third-party supplier or managed-service operator
- Compromised node, container, model, dependency, firmware, or control-plane component
- Lawful authority or jurisdictional actor where relevant

## 5. Architecture and trust boundaries

Attach a current data-flow diagram. Mark at least:

- public edge and API boundary;
- identity and policy boundary;
- provider control plane;
- tenant management plane;
- workload/data plane;
- Kubernetes or Slurm control plane;
- host/hypervisor/container boundary;
- GPU/accelerator sharing boundary;
- Ethernet, storage, InfiniBand/RDMA, NVLink, and management fabrics;
- BMC/DPU/out-of-band management;
- observability and support tooling;
- external model, package, image, data, and SaaS dependencies;
- cross-region and cross-jurisdiction flows.

## 6. Data flows

| Flow | Source | Destination | Protocol | Identity | Authorization | Encryption | Tenant boundary | Logged | Retention |
|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | |

## 7. Abuse cases and failure modes

Evaluate at minimum:

1. Public API abuse, credential theft, account takeover, and privilege escalation.
2. Cross-tenant compute, storage, cache, telemetry, or fabric exposure.
3. Container/VM escape, privileged workload, host compromise, and control-plane takeover.
4. GPU memory remanence, time-slicing without isolation, side channels, and device reset failure.
5. InfiniBand PKey, VRF/VXLAN, network-policy, or DPU misassignment.
6. Dataset or model poisoning, malicious model formats, unsafe deserialization, and checkpoint theft.
7. Build, image, driver, operator, firmware, model, package, and IaC supply-chain compromise.
8. Prompt injection, tool misuse, excessive agency, skill poisoning, memory poisoning, and confused-deputy behavior.
9. Exfiltration through egress, logs, metrics, support channels, snapshots, or model outputs.
10. GPU capacity hoarding, queue manipulation, denial of wallet, DDoS, cryptomining abuse, or prohibited workloads.
11. Malicious insider, support impersonation, break-glass abuse, and audit-log tampering.
12. Ransomware, destructive automation, regional outage, dependency failure, and failed recovery.

## 8. Risk analysis

| Threat | Preconditions | Existing controls | Detection | Likelihood | Impact | Residual risk | Owner | Treatment |
|---|---|---|---|---|---|---|---|---|
| | | | | | | | | |

Do not average away catastrophic tenant-isolation or T0 failures. Record uncertainty and missing evidence.

## 9. Required controls and evidence

Map threats to NeoCloud control IDs. Define implementation, scope, evidence, validator, test frequency, and exception handling.

## 10. Validation plan

Include positive, negative, adversarial, recovery, and misconfiguration tests. Active tests require written authorization and a safe rollback/containment plan. External content must not alter test scope or tool permissions.

## 11. Residual-risk decision

Record accepted risks, approvers, affected tenants, customer disclosures, expiration dates, and re-review triggers.
