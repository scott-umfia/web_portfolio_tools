import pandas as pd
import numpy as np
from datetime import datetime

def generate_monthly_returns_report(df, strategy_name="Investment Strategy", output_file="monthly_returns_report.html"):
    """
    Generate a web report of monthly return data in matrix format.
    
    Parameters:
    df (pd.DataFrame): DataFrame with columns 'YYYY_MM' and 'monthly_return'
    strategy_name (str): Name of the investment strategy for the report title
    output_file (str): Output HTML file name
    
    Returns:
    str: Path to the generated HTML file
    """
    
    # Create a copy of the dataframe to avoid modifying the original
    data = df.copy()
    
    # Parse the YYYY_MM column to extract year and month
    data['year'] = data['YYYY_MM'].astype(str).str[:4].astype(int)
    data['month'] = data['YYYY_MM'].astype(str).str[5:].astype(int)
    
    # Create pivot table with years as index and months as columns
    pivot_table = data.pivot(index='year', columns='month', values='monthly_return')
    
    # Reorder columns to show months 1-12
    month_cols = [i for i in range(1, 13) if i in pivot_table.columns]
    pivot_table = pivot_table[month_cols]
    
    # Calculate annual returns (sum of monthly returns for each year)
    pivot_table['Annual Total'] = pivot_table.sum(axis=1)
    
    # Generate HTML content
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{strategy_name} - Monthly Returns Report</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 20px;
                background-color: #f5f5f5;
            }}
            
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                background-color: white;
                padding: 30px;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}
            
            h1 {{
                color: #2c3e50;
                text-align: center;
                margin-bottom: 10px;
                font-size: 2.2em;
            }}
            
            .subtitle {{
                text-align: center;
                color: #7f8c8d;
                margin-bottom: 30px;
                font-size: 1.1em;
            }}
            
            .report-table {{
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
                font-size: 0.9em;
            }}
            
            .report-table th {{
                background-color: #34495e;
                color: white;
                padding: 12px 8px;
                text-align: center;
                font-weight: bold;
                border: 1px solid #2c3e50;
            }}
            
            .report-table td {{
                padding: 8px;
                text-align: center;
                border: 1px solid #bdc3c7;
            }}
            
            .year-header {{
                background-color: #ecf0f1;
                font-weight: bold;
                color: #2c3e50;
            }}
            
            .positive {{
                background-color: #d5f4e6;
                color: #27ae60;
            }}
            
            .negative {{
                background-color: #fadbd8;
                color: #e74c3c;
            }}
            
            .annual-total {{
                background-color: #f8f9fa;
                font-weight: bold;
                border-left: 3px solid #3498db;
            }}
            
            .summary {{
                margin-top: 30px;
                padding: 20px;
                background-color: #f8f9fa;
                border-radius: 5px;
                border-left: 4px solid #3498db;
            }}
            
            .summary h3 {{
                color: #2c3e50;
                margin-top: 0;
            }}
            
            .summary-stats {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px;
                margin-top: 15px;
            }}
            
            .stat-item {{
                text-align: center;
                padding: 10px;
                background-color: white;
                border-radius: 5px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            }}
            
            .stat-value {{
                font-size: 1.5em;
                font-weight: bold;
                color: #2c3e50;
            }}
            
            .stat-label {{
                color: #7f8c8d;
                font-size: 0.9em;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>{strategy_name}</h1>
            <div class="subtitle">Monthly Returns Report - Generated on {datetime.now().strftime('%B %d, %Y')}</div>
            
            <table class="report-table">
                <thead>
                    <tr>
                        <th>Year</th>
                        <th>Jan</th>
                        <th>Feb</th>
                        <th>Mar</th>
                        <th>Apr</th>
                        <th>May</th>
                        <th>Jun</th>
                        <th>Jul</th>
                        <th>Aug</th>
                        <th>Sep</th>
                        <th>Oct</th>
                        <th>Nov</th>
                        <th>Dec</th>
                        <th>Annual Total</th>
                    </tr>
                </thead>
                <tbody>
    """
    
    # Add table rows for each year
    for year in sorted(pivot_table.index):
        html_content += f'                    <tr>\n                        <td class="year-header">{year}</td>\n'
        
        # Add monthly returns
        for month in range(1, 13):
            value = pivot_table.loc[year, month] if month in pivot_table.columns and not pd.isna(pivot_table.loc[year, month]) else None
            
            if value is not None:
                # Format the value as percentage
                formatted_value = f"{value:.2f}%"
                css_class = "positive" if value >= 0 else "negative"
                html_content += f'                        <td class="{css_class}">{formatted_value}</td>\n'
            else:
                html_content += '                        <td>-</td>\n'
        
        # Add annual total
        annual_total = pivot_table.loc[year, 'Annual Total']
        annual_formatted = f"{annual_total:.2f}%"
        annual_class = "annual-total positive" if annual_total >= 0 else "annual-total negative"
        html_content += f'                        <td class="{annual_class}">{annual_formatted}</td>\n'
        html_content += '                    </tr>\n'
    
    # Calculate summary statistics
    annual_returns = pivot_table['Annual Total']
    monthly_returns = data['monthly_return']
    
    best_year = annual_returns.idxmax()
    worst_year = annual_returns.idxmin()
    avg_annual_return = annual_returns.mean()
    total_return = annual_returns.sum()
    
    html_content += f"""
                </tbody>
            </table>
            
            <div class="summary">
                <h3>Summary Statistics</h3>
                <div class="summary-stats">
                    <div class="stat-item">
                        <div class="stat-value">{best_year}</div>
                        <div class="stat-label">Best Year</div>
                        <div class="stat-label">({annual_returns.loc[best_year]:.2f}%)</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">{worst_year}</div>
                        <div class="stat-label">Worst Year</div>
                        <div class="stat-label">({annual_returns.loc[worst_year]:.2f}%)</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">{avg_annual_return:.2f}%</div>
                        <div class="stat-label">Average Annual Return</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">{total_return:.2f}%</div>
                        <div class="stat-label">Total Cumulative Return</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">{len(annual_returns)}</div>
                        <div class="stat-label">Years of Data</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">{len(monthly_returns)}</div>
                        <div class="stat-label">Months of Data</div>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Write HTML to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Report generated successfully: {output_file}")
    return output_file


# Example usage and test data generation
def create_sample_data():
    """Create sample data for testing the report generator"""
    
    # Generate sample data for 3 years (2021-2023) with monthly returns
    dates = []
    returns = []
    
    # Generate realistic-looking monthly returns (random but somewhat realistic)
    np.random.seed(42)  # For reproducible results
    
    for year in range(2021, 2024):
        for month in range(1, 13):
            # Skip future months in current year
            if year == 2023 and month > 8:  # Simulate data up to August 2023
                continue
                
            date_str = f"{year}_{month:02d}"
            dates.append(date_str)
            
            # Generate somewhat realistic monthly returns (-10% to +15%)
            monthly_return = np.random.normal(0.8, 3.5)  # Mean 0.8%, std 3.5%
            monthly_return = max(-10, min(15, monthly_return))  # Cap between -10% and 15%
            returns.append(round(monthly_return, 2))
    
    return pd.DataFrame({
        'YYYY_MM': dates,
        'monthly_return': returns
    })


if __name__ == "__main__":
    # Create sample data
    sample_df = create_sample_data()
    
    # Display sample data
    print("Sample Data:")
    print(sample_df.head(10))
    print(f"\nTotal records: {len(sample_df)}")
    
    # Generate the report
    report_file = generate_monthly_returns_report(
        sample_df, 
        strategy_name="Sample Investment Strategy",
        output_file="sample_monthly_returns_report.html"
    )
    
    print(f"\nReport saved as: {report_file}")
    print("Open the HTML file in your web browser to view the report.")