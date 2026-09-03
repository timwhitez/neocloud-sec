# NeoCloud incident severity matrix / 事件分级矩阵

The highest applicable criterion determines severity. Privacy, legal, contractual, safety, and customer-notification duties may override the operational targets below.

| Severity | Typical NeoCloud criteria | Initial acknowledgement | Incident command | Customer/legal assessment | Target containment |
|---|---|---:|---:|---:|---:|
| **SEV-0 Critical** | Confirmed cross-tenant data/model exposure; provider signing/root key compromise; broad control-plane takeover; hostile firmware/BMC/DPU control; active destructive agent outside scope; systemic secure-erase failure; material safety or sovereign-boundary breach | 5 min | 10 min | Immediate | 30 min or emergency shutdown |
| **SEV-1 High** | Single-tenant sensitive-data exposure; privileged account takeover; production cluster compromise; exploitable escape with evidence of use; major ransomware; widespread API outage caused by attack; critical supply-chain compromise | 10 min | 15 min | 30 min | 2 h |
| **SEV-2 Medium** | Contained compromise without confirmed sensitive-data access; important control disabled; repeated abuse affecting capacity; high-risk vulnerability with reachable path; partial logging blind spot during active threat | 30 min | 60 min as needed | 4 h | 8 h |
| **SEV-3 Low** | Low-impact policy violation, blocked attack, non-sensitive misconfiguration, isolated malware, minor abuse, or vulnerability without a practical production path | 4 h | Business owner | Next business day | Risk based |
| **SEV-4 Observation** | Suspicious or anomalous event requiring triage but no established security impact | 1 business day | No | As needed | Not applicable |

## Mandatory escalation triggers

Escalate immediately for any of the following regardless of current severity:

- possible cross-tenant or cross-region boundary failure;
- loss of integrity in audit/evidence systems;
- compromise of root, signing, attestation, KMS, identity, or break-glass credentials;
- hostile control of BMC, DPU, fabric manager, scheduler controller, hypervisor, or Kubernetes control plane;
- AI agent action that exceeded approved goal, scope, tool set, budget, or stop condition;
- inability to prove secure deletion or hardware sanitization between tenants;
- credible public disclosure, extortion, regulator contact, or law-enforcement request;
- safety impact or prohibited-use activity with imminent harm.

## First-response checklist

1. Establish incident commander, scribe, secure communications, and decision log.
2. Preserve volatile and durable evidence without spreading tenant data.
3. Identify affected tenants, regions, clusters, fabrics, identities, data classes, and service dependencies.
4. Revoke/rotate credentials and stop unsafe automation through approved break-glass procedures.
5. Contain at the strongest reliable boundary: API, identity, tenant, namespace, node, GPU, fabric, rack, region, or service.
6. Assess notification, privacy, contractual, legal, safety, and evidence-retention obligations.
7. Validate recovery and tenant-isolation state independently before reopening service.
8. Produce root cause, control-gap mapping, corrective actions, and verified closure evidence.
