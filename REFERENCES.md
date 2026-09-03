# References / 参考资料

**Baseline date:** 2026-09-04. Versions below were current or otherwise explicitly identified as draft on that date. NeoCloud Cyber Security uses these sources as informative inputs; it does not reproduce proprietary control text and does not claim formal equivalence.

## Cybersecurity governance and cloud assurance

1. NIST, *Cybersecurity Framework (CSF) 2.0*, 2024. https://www.nist.gov/cyberframework
2. NIST, *SP 800-207: Zero Trust Architecture*, 2020. https://csrc.nist.gov/publications/detail/sp/800-207/final
3. NIST, *SP 800-207A: A Zero Trust Architecture Model for Access Control in Cloud-Native Applications in Multi-Cloud Environments*, 2023. https://csrc.nist.gov/pubs/sp/800/207/a/final
4. NIST, *SP 800-53 Rev. 5: Security and Privacy Controls for Information Systems and Organizations*. https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final
5. NIST, *SP 800-61 Rev. 3: Incident Response Recommendations and Considerations for Cybersecurity Risk Management*, 2025. https://csrc.nist.gov/pubs/sp/800/61/r3/final
6. Cloud Security Alliance, *Cloud Controls Matrix v4.1*, 2026. https://cloudsecurityalliance.org/artifacts/introductory-guidance-to-ccm
7. Center for Internet Security, *CIS Critical Security Controls v8.1*, 2024. https://www.cisecurity.org/controls/v8-1
8. ISO, *ISO/IEC 27001:2022 Information Security Management Systems*. https://www.iso.org/standard/27001
9. ISO, *ISO/IEC 27002:2022 Information Security Controls*. https://www.iso.org/standard/75652.html
10. CISA, *Secure by Design*. https://www.cisa.gov/securebydesign
11. CISA, *Cloud Security Technical Reference Architecture*. https://www.cisa.gov/resources-tools/resources/cloud-security-technical-reference-architecture

## AI, model, and agent security

12. NIST, *AI Risk Management Framework 1.0*. https://www.nist.gov/itl/ai-risk-management-framework
13. NIST, *AI 600-1: Artificial Intelligence Risk Management Framework—Generative AI Profile*, 2024. https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence
14. NIST, *SP 800-218A: Secure Software Development Practices for Generative AI and Dual-Use Foundation Models*, 2024. https://csrc.nist.gov/pubs/sp/800/218/a/final
15. NIST, *IR 8596: Cybersecurity Framework Profile for Artificial Intelligence*, initial preliminary draft, 2025. https://csrc.nist.gov/pubs/ir/8596/iprd
16. ISO, *ISO/IEC 42001:2023 AI Management Systems*. https://www.iso.org/standard/42001
17. ISO, *ISO/IEC 42005:2025 AI System Impact Assessment*. https://www.iso.org/standard/42005
18. OWASP GenAI Security Project, *Top 10 for LLM Applications 2026*. https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/
19. OWASP GenAI Security Project, *Top 10 for Agentic Applications 2026*. https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/
20. OWASP, *Agentic Skills Top 10*, 2026. https://owasp.org/www-project-agentic-skills-top-10/
21. MITRE, *ATLAS—Adversarial Threat Landscape for Artificial-Intelligence Systems*. https://atlas.mitre.org/

## Cloud-native, workload identity, and orchestration

22. Kubernetes, *Security Checklist*. https://kubernetes.io/docs/concepts/security/security-checklist/
23. Kubernetes, *Pod Security Standards*. https://kubernetes.io/docs/concepts/security/pod-security-standards/
24. Kubernetes, *RBAC Good Practices*. https://kubernetes.io/docs/concepts/security/rbac-good-practices/
25. NSA and CISA, *Kubernetes Hardening Guidance*. https://www.cisa.gov/news-events/alerts/2022/03/15/updated-kubernetes-hardening-guide
26. SPIFFE, *Secure Production Identity Framework for Everyone*. https://spiffe.io/docs/latest/
27. SchedMD, *Slurm Workload Manager Documentation*. https://slurm.schedmd.com/documentation.html

## GPU, accelerator, confidential computing, and fabric isolation

28. NVIDIA, *Multi-Instance GPU (MIG)*. https://www.nvidia.com/en-us/technologies/multi-instance-gpu/
29. NVIDIA GPU Operator, *Time-Slicing GPUs in Kubernetes*. https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/gpu-sharing.html
30. NVIDIA, *Confidential Containers Reference Architecture*. https://docs.nvidia.com/datacenter/cloud-native/confidential-containers/latest/
31. NVIDIA Infra Controller, *Network Isolation*. https://docs.nvidia.com/infra-controller/documentation/operations-day-2/network-isolation
32. NVIDIA Infra Controller, *InfiniBand Partitioning*. https://docs.nvidia.com/infra-controller/documentation/configuration-day-1/infini-band/infini-band-partitioning
33. NVIDIA Infra Controller, *Operational Principles*. https://docs.nvidia.com/infra-controller/documentation/overview/operational-principles

## Threat modeling, software supply chain, and artifact trust

34. MITRE, *ATT&CK Enterprise Matrix*, including Cloud, Containers, IaaS, Identity Provider, ESXi, Linux, Network Devices, and SaaS. https://attack.mitre.org/matrices/enterprise/
35. SLSA, *SLSA Specification v1.2*. https://slsa.dev/spec/v1.2/
36. Sigstore, *Documentation and Transparency Log*. https://docs.sigstore.dev/about/overview/
37. OpenSSF, *Scorecard*. https://securityscorecards.dev/
38. NIST, *SP 800-218 Secure Software Development Framework v1.1*. https://csrc.nist.gov/pubs/sp/800/218/final

## How to use these references

- Use NIST CSF 2.0 as the top-level outcome and governance vocabulary.
- Use CSA CCM and CIS Controls to check cloud-control completeness and implementation priority.
- Use NIST AI RMF, NIST SP 800-218A, ISO/IEC 42001, OWASP GenAI, and MITRE ATLAS for AI/model/agent lifecycle risk.
- Use Kubernetes, SPIFFE/SPIRE, Slurm, NVIDIA, and platform documentation for implementation-specific safeguards.
- Use MITRE ATT&CK/ATLAS to derive detections and validation scenarios.
- Use SLSA, Sigstore, SSDF, SBOM/VEX, and reproducible build evidence for software, model, container, firmware, and infrastructure supply chains.

Always verify the current version and applicability before a formal audit or production change.
