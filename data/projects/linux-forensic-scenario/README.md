Linux Forensic Scenario Analysis

UAC(Universal Artifact Collector) 기반 Linux 침해 사고 분석

대상 시스템: Linux Worker Host | 분석 도구: UAC, PowerShell, journalctl



📌 개요

본 레포지토리는 SOC로부터 제보된 Linux 워커 시스템의 침해 의심 사고를 분석한 포렌식 시나리오 보고서입니다.



SOC는 TCP 22 포트에서 암호화되지 않은 트래픽과 원인 불명의 높은 CPU 사용률을 감지하였으며, UAC를 통해 수집된 아티팩트를 기반으로 침해 경로, 권한 상승, 루트킷 배포, 지속성 메커니즘을 분석하였습니다.



🔍 분석 결과 요약

항목	내용

초기 침투 경로	Jump Host(192.168.4.35) → 공유 계정 worker 사용

권한 상승	NOPASSWD sudo 설정 악용 → sudo -s root 쉘 획득

페이로드 실행	/dev/shm/kit/top (메모리 기반 파일시스템 실행 후 삭제)

프로세스 은닉	/etc/ld.so.preload 악성 공유 라이브러리 로드

높은 CPU 원인	은닉된 인메모리 페이로드 (크립토마이닝 의심)

아웃바운드 연결	192.168.4.22 → 192.168.5.95:22 (SSH)

🗂️ 파일 구성

Linux-Forensic-Scenario/

├── README.md

└── Linux\_Forensic\_Scenario\_Report.pdf   # 상세 분석 보고서

🔗 공격 흐름 (Attack Chain)

\[Jump Host 192.168.4.35]

&#x20;       │

&#x20;       │ SSH (worker 공유 계정)

&#x20;       ▼

\[Worker Host 192.168.4.22]

&#x20;       │

&#x20;       ├─ sudo -s → root 쉘 획득 (NOPASSWD 악용)

&#x20;       │

&#x20;       ├─ /etc/ld.so.preload 수정

&#x20;       │   └─ 악성 .so 로드 → readdir(), fopen() 후킹

&#x20;       │       └─ ps, top, /proc 디렉토리 은닉

&#x20;       │

&#x20;       ├─ /dev/shm/kit/top 실행 (인메모리)

&#x20;       │   └─ 실행 후 디스크에서 삭제 → 프로세스만 잔존

&#x20;       │

&#x20;       ├─ python3 -c 'import pty; pty.spawn("/bin/bash")'

&#x20;       │   └─ TTY 업그레이드 → 인터랙티브 쉘

&#x20;       │

&#x20;       └─ 아웃바운드 SSH → 192.168.5.95:22

🕵️ 주요 분석 내용

1\. 프로세스 은닉 (Rootkit)

/etc/ld.so.preload에 악성 공유 오브젝트가 등록되어 readdir(), fopen() 함수를 후킹함으로써 ps, top 등 유저랜드 프로세스 목록에서 악성 프로세스를 은닉하였다.



은닉된 PID 목록:



PID	실행 경로

941	/usr/bin/bash

975	/usr/bin/ssh

977	/dev/shm/kit/top (deleted)

2\. 인메모리 페이로드

PID 977은 /dev/shm/kit/top에서 실행된 후 디스크에서 삭제되었으나 프로세스는 계속 실행 상태를 유지하였다. 메모리 스트링 분석 결과 WebAssembly(WASM), Emscripten 런타임, 멀티스레딩 관련 문자열이 확인되어 크립토마이닝 페이로드로 추정된다.



3\. 권한 상승

worker 계정에 NOPASSWD sudo 설정이 되어 있어 패스워드 없이 즉시 root 쉘을 획득하였다.



sudo: worker : USER=root ; COMMAND=/bin/bash

4\. TTY 업그레이드 및 리버스 쉘

python3 -c 'import pty; pty.spawn("/bin/bash")'

루프백 127.0.0.1:3333 리스너 및 127.0.0.1:59182 양방향 연결이 확인되었다.



📅 침해 타임라인

시간 (UTC-4)	이벤트

Mar 24 19:34:32	worker 계정으로 Jump Host에서 SSH 로그인

Mar 24 19:38	sudo -s 실행 → root 쉘 획득

Mar 24 19:38	/etc/ld.so.preload 수정 → 악성 라이브러리 로드

Mar 24 19:38	/dev/shm/kit/top 실행 → 프로세스 은닉 시작

Mar 24 19:38	아웃바운드 SSH 연결 → 192.168.5.95:22

Mar 24 19:38:20	UAC 아티팩트 수집 시점

🛡️ 대응 권고사항

공유 계정의 NOPASSWD sudo 설정 제거

/etc/ld.so.preload 무결성 모니터링 및 변경 시 알림 설정

/dev/shm, /tmp 등 임시 경로에서의 실행 탐지 룰 적용

워커 시스템의 아웃바운드 SSH 연결 모니터링

프로세스 은닉 및 유저랜드 라이브러리 후킹 탐지 체계 구축

영향 받은 호스트 신뢰 기반 이미지로 재구축 및 자격 증명 교체

🔗 참고

UAC (Universal Artifact Collector)

Linux /etc/ld.so.preload 악용 기법

MITRE ATT\&CK — /dev/shm 실행

⚠️ 면책 조항

본 레포지토리는 보안 연구 및 학습 목적으로 작성된 포렌식 시나리오 분석 자료입니다.

모든 분석은 제공된 아티팩트를 기반으로 수행되었습니다.

