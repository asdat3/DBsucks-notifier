from app.main import main
import scheduler
import datetime as dt
import time

def run_main():
    """Wrapper function to run the main function"""
    try:
        main()
        print(f"Main function executed successfully at {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    except Exception as e:
        print(f"Error running main function at {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {e}")

if __name__ == "__main__":
    # Create scheduler instance
    schedule = scheduler.Scheduler()
    
    # Schedule the main function to run twice daily
    schedule.daily(dt.time(hour=5, minute=0), run_main)   # 5 AM
    schedule.daily(dt.time(hour=21, minute=0), run_main)  # 9 PM
    
    print("Scheduler started. Main function will run at 5 AM and 9 PM daily.")
    print("Press Ctrl+C to stop the scheduler.")
    
    try:
        # Run the scheduler in a loop
        while True:
            schedule.exec_jobs()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        print("\nScheduler stopped by user.")
