---
title: AB Testing & Feature Flag Service
emoji: 🛒
colorFrom: blue
colorTo: gray
sdk: docker
app_port: 7860
pinned: false
---

# AB Testing & Feature Flag Service

## Local Development
```bash
docker build -t ab-testing-feature-flag-service .
docker run -p 7860:7860 ab-testing-feature-flag-service
```
