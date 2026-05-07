import redis

print("🛡️ [GAVI VAULT]: Initializing Real-Time Fraud Detection Sniper...")
print("==================================================================")

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# We are listening to the 'live_transactions' stream.
# The '$' symbol is crucial: It tells Redis "Only give me NEW messages that come AFTER I start listening". 
# If we put '0', it would read from the beginning of time.
last_id = '$'

# Threshold Logic: More than 3 transactions in 60 seconds = Fraud
MAX_SWIPES = 3
TIME_WINDOW_SEC = 60

print("🎯 [SNIPER ACTIVE]: Listening to live transaction stream...")

try:
    while True:
        # block=0 means "Wait forever until a new message arrives". It doesn't waste CPU.
        # count=1 means we read 1 transaction at a time.
        response = r.xread({'live_transactions': last_id}, count=1, block=0)
        
        if response:
            # Redis returns a nested list structure. We extract the exact data payload.
            stream_name, messages = response[0]
            message_id, data_dict = messages[0]
            
            user = data_dict['user_id']
            amount = float(data_dict['amount'])
            merchant = data_dict['merchant']
            
            # --- THE FRAUD LOGIC (Gavi's Mastermind) ---
            # Create a unique key for this user's current shopping spree
            redis_key = f"fraud_window:{user}"
            
            # Increment the counter. If key doesn't exist, Redis makes it 1.
            current_swipes = r.incr(redis_key)
            
            # If this is the FIRST swipe, set a self-destruct timer (60 seconds) on this memory
            if current_swipes == 1:
                r.expire(redis_key, TIME_WINDOW_SEC)
            
            # --- THE Malkin EXCEPTION (The CEO Override) ---
            # Let's say user 'USER_7' is Maalkin . She gets VIP treatment.
            if user == "USER_7":
                print(f"💖 [VIP APPROVED]: Maalkin just spent ₹{amount} at {merchant}. Vault balance is infinite for her! ✨")
                
            # --- THE FRAUD CATCHER ---
            elif current_swipes > MAX_SWIPES:
                print(f"🚨 [FRAUD BLOCKED]: {user} tried to swipe at {merchant} (Swipe #{current_swipes} in 60s). Card Frozen! 🥶")
            
            else:
                # Normal transaction logic
                print(f"✅ [CLEARED]: {user} paid ₹{amount} at {merchant}. (Swipe {current_swipes}/{MAX_SWIPES})")
            
            # Update last_id so we don't read the same message twice
            last_id = message_id

except KeyboardInterrupt:
    print("\n🛑 [SYSTEM]: Sniper deactivated. Vault sealed.")