# 🚀 PromptHub - Quick Start Guide

Digital Marketplace built with Django, PostgreSQL, and Docker.

---

## ⚡ Chạy ngay (Quick Start)

### 1. Start Project
```bash
docker-compose up -d
```

### 2. Create Admin User
```bash
docker-compose exec web python manage.py createsuperuser
```

### 3. Open Browser
```
🌐 Homepage: http://localhost:8000/
🔐 Admin:    http://localhost:8000/admin
```

**That's it!** 🎉

---

## 📋 Requirements

- Docker Desktop
- Docker Compose

---

## 🛠️ Common Commands

```bash
# Start
docker-compose up -d

# Stop
docker-compose down

# Logs
docker-compose logs -f web

# Restart
docker-compose restart web
```

---

## 📚 Full Documentation

| Guide | Description |
|-------|-------------|
| **[QUICKSTART.md](QUICKSTART.md)** | 📖 Complete setup guide |
| **[COMMANDS_CHEATSHEET.md](COMMANDS_CHEATSHEET.md)** | ⚡ Quick commands |
| **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** | 📁 Directory structure |
| **[ROADMAP.md](ROADMAP.md)** | 🗺️ Development roadmap |
| **[FRONTEND_INTEGRATION.md](FRONTEND_INTEGRATION.md)** | 🎨 Frontend details |

---

## 🎯 What's Working

✅ Homepage with 13 sections  
✅ Responsive design  
✅ Dark/Light mode  
✅ Admin panel  
✅ Database (PostgreSQL)  
✅ Cache (Redis)  
✅ Task queue (Celery)  

---

## 🔄 Next Steps

1. ⏳ Connect database to homepage
2. ⏳ Add product listing page
3. ⏳ Implement user authentication
4. ⏳ Add shopping cart
5. ⏳ Payment integration

See [ROADMAP.md](ROADMAP.md) for full plan.

---

## 🐛 Troubleshooting

**Problem:** Containers won't start
```bash
docker-compose logs
docker-compose down -v
docker-compose up -d --build
```

**Problem:** Static files not loading
```bash
docker-compose exec web python manage.py collectstatic --noinput
docker-compose restart nginx
```

**More help:** See [QUICKSTART.md](QUICKSTART.md) → Troubleshooting section

---

## 📊 Project Status

- ✅ Phase 1: Foundation (100%)
- 🔄 Phase 2: Dynamic Content (0%)
- ⏳ Phase 3: Additional Pages
- ⏳ Phase 4: Authentication
- ⏳ Phase 5: Payment

---

## 📞 Support

- 📖 Documentation: See files above
- 🐛 Issues: Check logs with `docker-compose logs -f web`
- 💡 Tips: See [COMMANDS_CHEATSHEET.md](COMMANDS_CHEATSHEET.md)

---

**Version:** 1.0  
**Status:** ✅ Development Ready  
**Updated:** 2026-01-16

---

**Ready?** Run `docker-compose up -d` and visit http://localhost:8000/ 🚀
