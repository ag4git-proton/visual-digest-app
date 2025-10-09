#!/bin/bash
docker-compose build
docker-compose up -d
sleep 15
docker-compose logs
docker-compose exec magazine-compiler python /app/compile_magazine.py
docker-compose down

