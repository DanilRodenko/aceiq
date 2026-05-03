# AceIQ Roadmap

## Phase 1 — Data & Infrastructure ✅
- [x] Django project structure
- [x] Models: Player, Match, Prediction, CustomUser
- [x] Admin panel
- [x] load_players.py (65k players)
- [x] load_matches.py (195k matches)

## Phase 2 — Player Analytics (START HERE)
- [ ] K-Means clustering: Defender / Aggressive / All-Court / Serve-Volley
- [ ] Player stats dashboard (aces, df, 1st serve %, bp saved)
- [ ] H2H history page
- [ ] Player performance vs cluster type
      (e.g. "Sinner is 2-8 vs Defenders last 10 matches")
- [ ] Player ranking page with filters

## Phase 3 — ML Pipeline (MLflow + MLOps)
- [ ] MLflow tracking setup
- [ ] Feature engineering pipeline (Elo, Surface Elo, H2H, Form, Cluster)
- [ ] 3 XGBoost models per surface (Hard / Clay / Grass)
- [ ] Model versioning and registry (MLflow)
- [ ] pytest — unit tests for feature functions
- [ ] Model metrics dashboard (accuracy, ROC-AUC, calibration)
- [ ] Challenger data → better Elo calibration
- [ ] Round as feature
- [ ] Betting odds as feature (The Odds API)

## Phase 4 — Predictions
- [ ] FastAPI /predict endpoint
- [ ] Match prediction page
- [ ] Probability display with key factors
- [ ] Value bets (our probability vs bookmaker implied probability)

## Phase 5 — Betting & Monetization
- [ ] The Odds API integration
- [ ] Arbitrage scanner
- [ ] Live odds (APScheduler → every 30s → DB snapshot)
- [ ] Alert system (Telegram bot / email)
- [ ] Stripe subscriptions (Free / Pro / Enterprise)
- [ ] Bookmaker referral links

## Phase 6 — Scale
- [ ] WTA support
- [ ] Futures model
- [ ] Challenger model
- [ ] Mobile app
- [ ] CI/CD pipeline
- [ ] Docker + Railway deploy

## Tech Debt / Always On
- [ ] pytest coverage > 80%
- [ ] MLflow experiment tracking
- [ ] Model retraining pipeline (monthly)
- [ ] Data quality monitoring