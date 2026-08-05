# Assumptions register

Assumptions are not facts. Codex must either verify them or keep them explicitly unresolved.

| ID | Assumption | Verification method | Status |
|---|---|---|---|
| A-001 | Android display permits USB APK sideloading | Real device installation | OPEN |
| A-002 | Android display supports USB Host / USB Audio Class | Device enumeration and recording | OPEN |
| A-003 | Development PC has a compatible NVIDIA GPU | `nvidia-smi`, CUDA/PyTorch test | OPEN |
| A-004 | Store network permits WHEP/WebRTC | Real network session test | OPEN |
| A-005 | Existing provider credentials cover required APIs | Provider console and minimal call | OPEN |
| A-006 | Current idle/avatar assets have commercial rights | Provenance and written approval | OPEN |
| A-007 | 10 Mbps is adequate for chosen video profile | Measured stream bandwidth | OPEN |
| A-008 | 4 GB server is stable for the gateway workload | Load/memory test | OPEN |
