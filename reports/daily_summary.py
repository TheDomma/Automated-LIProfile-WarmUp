import csv
import logging
from datetime import date
from db.database import get_connection

logger = logging.getLogger(__name__)

def generate_report():
    """
    Generates a daily summary report of all sessions.
    """
    today_date = date.today().isoformat()
    logger.info(f"Generating daily report for {today_date}...")
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT profile_id, status, reason, created_at FROM sessions WHERE date = ?",
            (today_date,)
        )
        sessions = cursor.fetchall()
        conn.close()
        
        report_filename = f"report_{today_date}.csv"
        
        with open(report_filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Profile ID", "Status", "Reason", "Timestamp"])
            writer.writerows(sessions)
            
        logger.info(f"Report generated successfully: {report_filename}")
        
    except Exception as e:
        logger.error(f"Failed to generate report: {e}")
