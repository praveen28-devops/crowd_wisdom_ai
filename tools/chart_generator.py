# tools/chart_generator.py
import matplotlib
# ESSENTIAL: Use a non-GUI backend to prevent threading errors
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
from crewai.tools import tool
import json
import os
from datetime import datetime
import seaborn as sns

# Set style for better looking charts
sns.set_style("whitegrid")
plt.style.use('seaborn-v0_8')

def create_comparison_chart_simple(data_24hr, data_weekly):
    """
    Simple chart generator function for demo purposes
    """
    try:
        os.makedirs('reports', exist_ok=True)
        
        # Parse input data
        if isinstance(data_24hr, str):
            data_24 = json.loads(data_24hr)
        else:
            data_24 = data_24hr
            
        if isinstance(data_weekly, str):
            data_week = json.loads(data_weekly)
        else:
            data_week = data_weekly
        
        # Create simple volume comparison chart
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Extract volume data
        filings_24hr = data_24.get('recent_filings', [])
        filings_week = data_week.get('recent_filings', [])
        
        companies_24hr = [filing.get('company', 'Unknown') for filing in filings_24hr]
        volumes_24hr = [filing.get('shares', 0) for filing in filings_24hr]
        
        companies_week = [filing.get('company', 'Unknown') for filing in filings_week]
        volumes_week = [filing.get('shares', 0) for filing in filings_week]
        
        # Simple comparison
        all_companies = list(set(companies_24hr + companies_week))[:10]  # Top 10
        
        vol_24hr_by_company = {}
        for comp, vol in zip(companies_24hr, volumes_24hr):
            vol_24hr_by_company[comp] = vol_24hr_by_company.get(comp, 0) + vol
        
        vol_week_by_company = {}
        for comp, vol in zip(companies_week, volumes_week):
            vol_week_by_company[comp] = vol_week_by_company.get(comp, 0) + vol
        
        # Create bar chart
        x_pos = range(len(all_companies))
        vals_24hr = [vol_24hr_by_company.get(c, 0) for c in all_companies]
        vals_week = [vol_week_by_company.get(c, 0) for c in all_companies]
        
        width = 0.35
        ax.bar([x - width/2 for x in x_pos], vals_24hr, width, label='24 Hours', color='red', alpha=0.7)
        ax.bar([x + width/2 for x in x_pos], vals_week, width, label='Weekly Avg', color='blue', alpha=0.7)
        
        ax.set_xlabel('Companies')
        ax.set_ylabel('Trading Volume (shares)')
        ax.set_title('Insider Trading Volume Comparison', fontsize=14, fontweight='bold')
        ax.set_xticks(x_pos)
        ax.set_xticklabels(all_companies, rotation=45)
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        chart_path = 'reports/simple_comparison_chart.png'
        plt.tight_layout()
        plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return f"Chart created successfully: {chart_path}"
        
    except Exception as e:
        return f"Chart creation error: {str(e)}"

@tool("Comparative Chart Generator")
def create_comparison_chart(data_24hr: str, data_weekly: str) -> str:
    """
    Creates comparative charts showing 24hr vs prior week insider trading activity.
    Highlights trends, spikes, and notable trades.
    """
    try:
        os.makedirs('reports', exist_ok=True)
        
        # Parse input data
        data_24 = json.loads(data_24hr) if isinstance(data_24hr, str) else data_24hr
        data_week = json.loads(data_weekly) if isinstance(data_weekly, str) else data_weekly
        
        # Create multiple chart types
        chart_paths = []
        
        # 1. Volume Comparison Bar Chart
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
        
        # Extract volume data
        companies_24hr = [item.get('company', 'Unknown') for item in data_24.get('recent_filings', [])]
        volumes_24hr = [item.get('shares', 0) for item in data_24.get('recent_filings', [])]
        
        companies_week = [item.get('company', 'Unknown') for item in data_week.get('recent_filings', [])]
        volumes_week = [item.get('shares', 0) for item in data_week.get('recent_filings', [])]
        
        # Aggregate by company
        company_vol_24hr = {}
        for comp, vol in zip(companies_24hr, volumes_24hr):
            company_vol_24hr[comp] = company_vol_24hr.get(comp, 0) + vol
            
        company_vol_week = {}
        for comp, vol in zip(companies_week, volumes_week):
            company_vol_week[comp] = company_vol_week.get(comp, 0) + vol
        
        # Plot 24hr data
        if company_vol_24hr:
            companies = list(company_vol_24hr.keys())[:10]  # Top 10
            volumes = [company_vol_24hr[c] for c in companies]
            bars1 = ax1.bar(companies, volumes, color='darkred', alpha=0.7)
            ax1.set_title('Last 24 Hours - Insider Trading Volume', fontsize=14, fontweight='bold')
            ax1.set_ylabel('Shares Traded')
            ax1.tick_params(axis='x', rotation=45)
            
            # Add value labels
            for bar, vol in zip(bars1, volumes):
                height = bar.get_height()
                ax1.text(bar.get_x() + bar.get_width()/2., height,
                        f'{vol:,}', ha='center', va='bottom', fontsize=9)
        
        # Plot weekly data
        if company_vol_week:
            companies_w = list(company_vol_week.keys())[:10]  # Top 10
            volumes_w = [company_vol_week[c] for c in companies_w]
            bars2 = ax2.bar(companies_w, volumes_w, color='darkblue', alpha=0.7)
            ax2.set_title('Prior Week - Insider Trading Volume', fontsize=14, fontweight='bold')
            ax2.set_ylabel('Shares Traded')
            ax2.tick_params(axis='x', rotation=45)
            
            # Add value labels
            for bar, vol in zip(bars2, volumes_w):
                height = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width()/2., height,
                        f'{vol:,}', ha='center', va='bottom', fontsize=9)
        
        plt.tight_layout()
        chart_path1 = 'reports/volume_comparison_chart.png'
        plt.savefig(chart_path1, dpi=300, bbox_inches='tight')
        plt.close()
        chart_paths.append(chart_path1)
        
        # 2. Transaction Type Analysis
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Count transaction types
        transactions_24hr = [item.get('transaction', 'Unknown') for item in data_24.get('recent_filings', [])]
        transactions_week = [item.get('transaction', 'Unknown') for item in data_week.get('recent_filings', [])]
        
        from collections import Counter
        trans_count_24hr = Counter(transactions_24hr)
        trans_count_week = Counter(transactions_week)
        
        # Create comparison data
        all_transaction_types = set(trans_count_24hr.keys()) | set(trans_count_week.keys())
        x_labels = list(all_transaction_types)
        
        counts_24hr = [trans_count_24hr.get(t, 0) for t in x_labels]
        counts_week = [trans_count_week.get(t, 0) for t in x_labels]
        
        x = range(len(x_labels))
        width = 0.35
        
        bars1 = ax.bar([i - width/2 for i in x], counts_24hr, width, label='Last 24 Hours', color='red', alpha=0.7)
        bars2 = ax.bar([i + width/2 for i in x], counts_week, width, label='Prior Week', color='blue', alpha=0.7)
        
        ax.set_xlabel('Transaction Type')
        ax.set_ylabel('Number of Transactions')
        ax.set_title('Insider Trading Activity: Buy vs Sell Comparison', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(x_labels)
        ax.legend()
        
        # Add value labels on bars
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{int(height)}', ha='center', va='bottom', fontsize=10)
        
        plt.tight_layout()
        chart_path2 = 'reports/transaction_type_comparison.png'
        plt.savefig(chart_path2, dpi=300, bbox_inches='tight')
        plt.close()
        chart_paths.append(chart_path2)
        
        # 3. Create Interactive Plotly Chart
        create_interactive_comparison_chart(data_24, data_week)
        chart_paths.append('reports/interactive_comparison.html')
        
        return f"Successfully created comparison charts: {', '.join(chart_paths)}"
        
    except Exception as e:
        return f"Error creating comparison charts: {str(e)}"

def create_interactive_comparison_chart(data_24hr, data_weekly):
    """Create interactive Plotly chart for web viewing"""
    try:
        # Prepare data
        filings_24hr = data_24hr.get('recent_filings', [])
        filings_week = data_weekly.get('recent_filings', [])
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Trading Volume Comparison', 'Transaction Types', 
                          'Top Companies (24hr)', 'Top Companies (Weekly)'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"type": "scatter"}, {"type": "scatter"}]]
        )
        
        # Volume comparison
        companies_24hr = {}
        for filing in filings_24hr:
            comp = filing.get('company', 'Unknown')
            shares = filing.get('shares', 0)
            companies_24hr[comp] = companies_24hr.get(comp, 0) + shares
        
        companies_week = {}
        for filing in filings_week:
            comp = filing.get('company', 'Unknown')
            shares = filing.get('shares', 0)
            companies_week[comp] = companies_week.get(comp, 0) + shares
        
        # Top companies bar chart
        top_companies_24hr = sorted(companies_24hr.items(), key=lambda x: x[1], reverse=True)[:10]
        top_companies_week = sorted(companies_week.items(), key=lambda x: x[1], reverse=True)[:10]
        
        if top_companies_24hr:
            fig.add_trace(
                go.Bar(x=[c[0] for c in top_companies_24hr], 
                      y=[c[1] for c in top_companies_24hr],
                      name='24 Hours',
                      marker_color='red'),
                row=1, col=1
            )
        
        if top_companies_week:
            fig.add_trace(
                go.Bar(x=[c[0] for c in top_companies_week], 
                      y=[c[1] for c in top_companies_week],
                      name='Prior Week',
                      marker_color='blue'),
                row=1, col=1
            )
        
        fig.update_layout(
            title="Insider Trading Analysis Dashboard",
            height=800,
            showlegend=True
        )
        
        # Save interactive chart
        fig.write_html('reports/interactive_comparison.html')
        
    except Exception as e:
        print(f"Error creating interactive chart: {e}")

@tool("Interactive Chart Generator")
def create_interactive_chart(insider_data: str) -> str:
    """
    Creates interactive Plotly charts for insider trading data analysis.
    """
    try:
        os.makedirs('reports', exist_ok=True)
        
        data = json.loads(insider_data) if isinstance(insider_data, str) else insider_data
        filings = data.get('recent_filings', [])
        
        if not filings:
            return "No data available for interactive chart"
        
        # Create DataFrame
        df = pd.DataFrame(filings)
        
        # 1. Interactive scatter plot
        fig = px.scatter(df, x='shares', y='price', color='company', size='shares',
                        hover_data=['insider', 'transaction', 'date'],
                        title='Insider Trading Activity - Volume vs Price')
        
        fig.update_layout(
            xaxis_title="Shares Traded",
            yaxis_title="Price per Share ($)",
            font=dict(size=12)
        )
        
        chart_path = 'reports/interactive_insider_chart.html'
        fig.write_html(chart_path)
        
        return f"Interactive chart created: {chart_path}"
        
    except Exception as e:
        return f"Error creating interactive chart: {str(e)}"

# Legacy function for backward compatibility
@tool("Chart Generator")
def chart_generator(comparison_data_json: str) -> str:
    """
    Creates a comparison chart for insider trading activity based on a JSON input
    and saves it to a file. The JSON should have 'today' and 'prior_week_avg' keys.
    """
    try:
        os.makedirs('reports', exist_ok=True)
        data = json.loads(comparison_data_json)
        
        labels = ['Prior 7-Day Average', 'Last 24 Hours']
        trading_volume = [data.get('prior_week_avg', 0), data.get('today', 0)]
        
        plt.figure(figsize=(10, 6))
        bars = plt.bar(labels, trading_volume, color=['royalblue', 'skyblue'])
        plt.title('Insider Trading Activity Comparison', fontsize=16)
        plt.ylabel('Number of Transactions')
        
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2.0, yval, int(yval), va='bottom', ha='center')

        chart_path = 'reports/insider_trading_comparison.png'
        plt.savefig(chart_path)
        plt.close()
        
        return f"Chart saved successfully to {chart_path}"
    
    except Exception as e:
        return f"Error creating chart: {str(e)}"