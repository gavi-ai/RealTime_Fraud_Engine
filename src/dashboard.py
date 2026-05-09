import streamlit as st
import pandas as pd
import time
import redis
import os

st.set_page_config(page_title="Vault of Millions", layout='wide')
st.title(" Vault of Millions")
st.subheader("Live Real-Time Fraud Detection Radar 📡")
st.markdown("Monitoring high-velocity Redis data streams in milliseconds.")

@st.cache_resource
def get_redis_connection():
    return redis.Redis(host='redis', port=6379, decode_responses=True)

r= get_redis_connection()
placeholder = st.empty()

while True:
    try:
        stream_data=r.xrange('live_transactions', '-', '+')
        if stream_data:
            latest_txn = stream_data[-12:]
            table_data=[]
            rolling_volume = 0 
            for tx_id, data in latest_txn:  
                amount = float(data['amount'])
                rolling_volume += amount
                table_data.append({
                    'timestamp': data['timestamp'][11:19],
                    'user_id': data['user_id'],
                    'merchant': data['merchant'],
                    'amount': f"₹{amount:.2f}"
                })
            df = pd.DataFrame(table_data)
            with placeholder.container():
                col1,col2,col3 = st.columns(3)
                col1.metric(label="Total Transactions Analyzed", value=len(stream_data))
                col2.metric(label="Rolling Volume (Last 12)", value=f"₹ {rolling_volume:,.2f}")
                col3.metric(label="System Status", value="🟢 Active Listening")
                st.divider()
                st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            with placeholder.container():
                st.info("No transactions detected yet. Waiting for live data...")
        time.sleep(1)  # Sleep for a second before checking for new transactions
    except Exception as e:
        with placeholder.container():
            st.error(f"Error connecting to Redis: {e}")
        time.sleep(5)  # Wait before retrying connection