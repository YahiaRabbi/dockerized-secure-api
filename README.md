# Noorzaah Secure API Engine

> An enterprise-grade, Dockerized RESTful API backend designed for the real-world fashion brand **Noorzaah**. 

This project demonstrates a fully scalable microservices architecture built with **FastAPI**, secured with **JWT Authentication**, and highly optimized using **Redis Caching** and **PostgreSQL**.

## Tech Stack
* **Core Framework:** FastAPI (Python)
* **Database:** PostgreSQL (with SQLAlchemy ORM)
* **Performance/Caching:** Redis
* **Security:** JWT (JSON Web Tokens) & passlib (bcrypt)
* **DevOps:** Docker, Docker Compose
* **CI/CD:** GitHub Actions
* **Automation:** Linux Bash Scripting

## ✨ Key Enterprise Features
1. **Blazing Fast Response:** Built on ASGI standards for high-concurrency performance.
2. **Redis Caching Architecture:** Drastically reduces database load by serving frequent product requests (like catalog views) directly from in-memory cache.
3. **Containerized Environment:** Fully isolated microservices (API, DB, Cache) running seamlessly via `docker-compose`.
4. **Robust Security:** Passwords are never saved in plain text. Features complete JWT-based route protection for user profiles.
5. **Automated CI/CD Pipeline:** Integrated GitHub Actions workflow for continuous testing upon every new push.
6. **Automated Backups:** Custom Bash script (`backup.sh`) for quick, one-click PostgreSQL database backups.

## 📸 Proof of Work (Architecture Showcase)

<img width="1464" height="881" alt="db1" src="https://github.com/user-attachments/assets/e4ad607b-8400-48c4-8016-076d821745da" />
<img width="1210" height="884" alt="db2" src="https://github.com/user-attachments/assets/e0459652-25cc-4186-8a3e-3a1b34d18734" />
<img width="1214" height="881" alt="db3" src="https://github.com/user-attachments/assets/956021b8-c676-43ca-829f-b052aa0f1d70" />
<img width="1624" height="982" alt="db4" src="https://github.com/user-attachments/assets/75e97505-5a6f-4858-a415-deeec0ac374e" />


## 🛠️ How to Run Locally

You don't need to install Python or databases on your local machine. Just install **Docker** and run the following commands:

```bash
# 1. Clone the repository
git clone [https://github.com/YahiaRabbi/dockerized-secure-api.git](https://github.com/YahiaRabbi/dockerized-secure-api.git)
cd dockerized-secure-api

# 2. Run the entire microservices stack
docker compose up --build -d

# 3. Access the interactive API Documentation
Navigate to: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
