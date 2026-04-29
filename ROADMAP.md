# AceIQ Roadmap

## In Progress
- [ ] load_players.py
- [ ] load_matches.py
- [ ] ML model (XGBoost)

## Next Up
- [ ] The Odds API integration
- [ ] Arbitrage scanner
- [ ] Value bets

## Ideas / Later
- [ ] Live odds (in-play)
- [ ] WTA support
- [ ] Challenger level matches
- [ ] Telegram bot / alerts
- [ ] Mobile app

Scheduler (APScheduler или Celery Beat)
→ каждые 30 сек делает запрос
→ сохраняет снапшот коэффов в БД
→ пересчитывает вилки
→ если вилка найдена → уведомление юзеру