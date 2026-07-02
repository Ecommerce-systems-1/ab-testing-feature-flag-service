1.  mkdir ab-testing-feature-flag-service && cd ab-testing-feature-flag-service
2.  git init && git checkout -b main
3.  Create requirements.txt: fastapi uvicorn[standard] pytest httpx python-multipart
4.  Write backend/database.py: init_db() creates all 3 tables; get_db() yields connection
5.  Write backend/schemas.py: ExperimentCreate, ExperimentOut, AssignResponse, TrackEvent,
    VariantResultOut, ResultsResponse, FlagOut
6.  Run: python -m pytest backend/tests/test_assignment.py — expect FAIL
7.  Write backend/services/assignment.py — tests must pass
8.  Run: python -m pytest backend/tests/test_results.py — expect FAIL
9.  Write backend/services/results.py — tests must pass
10. Run: python -m pytest backend/tests/test_flags.py — expect FAIL
11. Write backend/services/flags.py — tests must pass
12. Run: python -m pytest backend/tests/test_experiments_router.py — expect FAIL
13. Write backend/routers/experiments.py (CRUD + assign + results endpoints)
14. Write backend/routers/tracking.py (POST /track with upsert-safe insert)
15. Write backend/routers/flags.py (GET /flags?user_id=X)
16. Write backend/main.py: lifespan→init_db+seed; include routers under /api prefix
17. Write backend/seed.py: 5 experiments + 2000 events with realistic conversion rates
18. Run: python -m pytest backend/tests/ — ALL must pass
19. cd frontend && npx create-next-app@14 . --typescript --tailwind --app
20. Write frontend/src/lib/api.ts with typed fetch wrappers
21. Write ExperimentBuilder.tsx, ResultsTable.tsx, VariantBar.tsx, SignificanceBadge.tsx
22. Write page.tsx (experiment list + builder) and experiments/[id]/page.tsx (results)
23. Set next.config.js: output: 'export', distDir: '../backend/static'
24. Run: npm run build — verify no TypeScript errors
25. Write Dockerfile: python:3.11-slim; install deps; copy static; uvicorn on port 7860
26. Write .github/workflows/ci.yml: pytest + npm test on push to main
27. docker build -t ab-service . && docker run -p 7860:7860 ab-service
28. Verify: create experiment, start it, call GET /assign 10x same user_id → always same variant
29. Verify: POST /track 500 impressions + 100 conversions for control, 75 for treatment
30. Verify: GET /experiments/{id}/results shows p_value and significant flag
31. Verify: GET /flags?user_id=X returns JSON map of flag booleans
32. git add -A && git commit -m "feat: ab testing and feature flag service"
33. gh repo create ab-testing-feature-flag-service --public && git push -u origin main