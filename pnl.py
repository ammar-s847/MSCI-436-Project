#TODO store trades
# tuple of buy or sell
# output the array
# from scheduler print out list each time

from scheduler import scheduled_job, ticker, decision_queue, data_queue

trades = []

def modified_scheduled_job():
    global trades
    scheduled_job(ticker)
    last_decision = decision_queue[-1] if decision_queue else 'hold'
    if last_decision in ['buy', 'sell']:
        trades.append((last_decision, data_queue[-1]))
    print(f"Trades: {trades}")

if __name__ == "__main__":
    modified_scheduled_job()
    