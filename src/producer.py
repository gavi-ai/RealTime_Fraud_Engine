import time
import redis
import random
from faker import Faker
from datetime import datetime
import os

print("Starting the producer...")

r = redis.Redis(os.getenv('REDIS_HOST', 'localhost'), port=6379, decode_responses=True  )
fake = Faker()

merchants = [
    'Siri Fort Golf Pro Shop', 
    'South Delhi Auto Mods', 
    'Big Chill Cafe', 
    'Apple Store Saket', 
    'Under Armour Gym Gear', 
    'Uber Black', 
    'Zomato'
]
print("✅ [REDIS]: Connected to In-Memory Highway. Data Stream initiating...")
print("==================================================================")

try:
    while True:
        # 2. Create a fake transaction
        transaction = {
            "tx_id": fake.uuid4(),
            # Keeping the user pool small (50 users) so we can intentionally trigger "fraud" when one user buys too much!
            "user_id": f"USER_{random.randint(1, 50)}", 
            "amount": str(round(random.uniform(500.0, 150000.0), 2)), # Amount in INR
            "merchant": random.choice(merchants),
            "timestamp": datetime.now().isoformat()
        }
        
        # 3. Push to Redis Stream (The Data Bullet Train)
        # 'live_transactions' is the name of our stream. '*' means auto-generate a Redis ID.
        r.xadd("live_transactions", transaction)
        
        # Flex on the terminal
        print(f"💸 [STREAMING]: TX {transaction['tx_id'][:8]} | {transaction['user_id']} | ₹{transaction['amount']} | 📍 {transaction['merchant']}")
        
        # 4. Wait a fraction of a second before the next order (2 transactions per second)
        time.sleep(0.5)

except KeyboardInterrupt:
    print("\n🛑 [SYSTEM]: Producer shut down gracefully. Taking a breather!")
