
docker-compose down -v
docker-compose up -d

clear
echo "building"
sleep 2

firefox "http://localhost:8080"
clear
docker exec -itw /escape docker-escapefromlinux-efl-1 bash
