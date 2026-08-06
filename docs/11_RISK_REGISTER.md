# Risk register

| ID | Risk | Impact | Mitigation | Owner/status |
|---|---|---|---|---|
| R-001 | Android screen does not support USB Audio Class | Voice input blocked | Real-device test; fallback mic/USB audio adapter | Open |
| R-002 | No compatible GPU for LiveTalking | No real-time lipsync | Keep idle-video mode; use separate GPU node later | Open |
| R-003 | Small server memory pressure | Gateway instability | Lightweight stack, limits, swap/upgrade decision | Open |
| R-004 | WebRTC blocked by NAT/firewall | No remote digital stream | WHEP tests, TURN/proxy plan, local GPU option | Open |
| R-005 | Echo between speakers and microphone | Poor ASR | AEC-capable hardware, push-to-talk/VAD, layout test | Open |
| R-006 | Provider API or pricing changes | Integration/cost failure | Adapters, current official docs, cost caps | Open |
| R-007 | Unverified knowledge causes false claims | Trust/compliance harm | Small reviewed FAQ and transfer rules | Open |
| R-008 | Secrets committed to public repo | Critical credential exposure | Ignore rules, secret checks, rotation playbook | Open |
| R-009 | Avatar/voice commercial rights unclear | Legal/brand risk | Provenance register and approval before release | Open |
| R-010 | Upstream updates break patches | Maintenance risk | Commit lock, adapter-first, patch ledger | Open |
