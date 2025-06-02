# message-service
Simple message service prototype built using FastAPI + uvicorn, using local db with SQLAlchemy, uv for package management. Docker + docker compose for building.

# Assumptions/Delimitations
- Assumes small volume (local DB) and low traffic (SQLite).
- No authentication/authorization
- Recipient is arbitrary string, not confined to anything specific
- Message-ids are simple auto_incremented for ease of testing
- Have assumed interest is in fetching/deleting messages for one recipient at a time and not all of them. This however could be easily added as a functionality.

# Build Guide
git clone https://github.com/antonschulz/message-service
cd message-service
docker compose up --build
---> REST-API should be available at localhost:8000

# Example Usage (or see localhost:8000/docs)
1. Send plain-text message
curl -v -X POST "http://127.0.0.1:8000/messages/foo@bar.com" \
     -H "Content-Type: text/plain" \
     --data "Hello, this is a test message!"

2. Fetch unread messages (for specific user)
curl -v "http://127.0.0.1:8000/messages/unread?recipient_id=foo@bar.com"

3. Delete a single message (by message id)
curl -v -X DELETE "http://127.0.0.1:8000/messages/2"

4. Delete multiple messages
curl -v -X DELETE "http://127.0.0.1:8000/messages/" \
     -H "Content-Type: application/json" \
     --data '{
       "message_ids": [1, 2, 3]
     }'

5. Fetch messaged ordered by time, according to start and/or stop index
curl -v "http://127.0.0.1:8000/messages/?recipient_id=foo@bar.com&skip=0&limit=10"



