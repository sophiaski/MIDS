#!/bin/sh 

while true
	do
	docker-compose exec mids ab -n $(($RANDOM%25+6)) -H "Host: user1.comcast.com" http://localhost:5000/
	docker-compose exec mids ab -n $(($RANDOM%25+6)) -H "Host: user1.comcast.com" http://localhost:5000/purchase_a_sword
	docker-compose exec mids ab -n $(($RANDOM%25+6)) -H "Host: user1.comcast.com" http://localhost:5000/join_a_guild
	docker-compose exec mids ab -n $(($RANDOM%50+1)) -H "Host: user2.att.com" http://localhost:5000/
	docker-compose exec mids ab -n $(($RANDOM%50+1)) -H "Host: user2.att.com" http://localhost:5000/purchase_a_sword
	docker-compose exec mids ab -n $(($RANDOM%50+1)) -H "Host: user2.att.com" http://localhost:5000/join_a_guild
	sleep 3
done
