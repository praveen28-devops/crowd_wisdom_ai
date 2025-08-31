# tools/chart_generator.py
import matplotlib
# ESSENTIAL: Use a non-GUI backend to prevent threading errors
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
from crewai.tools import tool
import json
import os

@tool("Chart Generator")
def chart_generator(comparison_data_json: str) -> str:
    """
    Creates a comparison chart for insider trading activity based on a JSON input
    and saves it to a file. The JSON should have 'today' and 'prior_week_avg' keys.
    """
    try:
        # Create the 'reports' directory if it doesn't exist
        if not os.path.exists('reports'):
            os.makedirs('reports')

        # Parse the JSON string from the analyst agent
        data = json.loads(comparison_data_json)
        
        # Use the actual data from the input
        labels = ['Prior 7-Day Average', 'Last 24 Hours']
        trading_volume = [data.get('prior_week_avg', 0), data.get('today', 0)]
        
        plt.figure(figsize=(10, 6))
        bars = plt.bar(labels, trading_volume, color=['royalblue', 'skyblue'])
        plt.title('Insider Trading Activity Comparison', fontsize=16)
        plt.ylabel('Number of Transactions')
        
        # Add data labels on top of the bars
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2.0, yval, int(yval), va='bottom', ha='center')

        chart_path = 'reports/insider_trading_comparison.png'
        plt.savefig(chart_path)
        plt.close()
        
        return f"Chart saved successfully to {chart_path}"
    
    except Exception as e:
        return f"Error creating chart: {str(e)}"