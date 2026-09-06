стек
 Python + Flask + MySQL
 Docker + Docker Compose (app, db, nginx)
 Terraform (Yandex Cloud)
 GitHub Actions (CI/CD)

сделано
 REST API на Flask с подключением к MySQL
 Dockerfile с multi-stage и non-root пользователем
 docker-compose.yml с healthcheck и volumes
 Terraform-код для облачной инфраструктуры
 GitHub Actions: test → build → deploy

запуски локально
 cp .env.example .env
 docker-compose up -d
 curl http://localhost/health

деплой - не выполняется так как нету доступа к облаку
