#!/usr/bin/env python3
"""
Time Series Visualization of Building Consents Data from Victoria, Australia
Shows actual dwelling units approved over time (1983-2025)
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set style
sns.set_theme(style="whitegrid")

# Read the time series data
df = pd.read_excel('8731002.xlsx', sheet_name='Data1', header=None)

# Extract dates (starting from row 10)
dates = pd.to_datetime(df.iloc[10:, 0])

# Extract data (starting from row 10, columns 1 onwards)
data_df = df.iloc[10:, 1:].copy()
data_df.index = dates

# Convert all columns to numeric
for col in data_df.columns:
    data_df[col] = pd.to_numeric(data_df[col], errors='coerce')

# Get metadata for column naming
descriptions = df.iloc[0, 1:].values  # Row 0: descriptions
series_types = df.iloc[2, 1:].values  # Row 2: series types (Original, SA, Trend)

# Create readable column names by combining description and series type
column_names = []
for i, (desc, stype) in enumerate(zip(descriptions, series_types)):
    if pd.notna(desc):
        # Extract key parts
        parts = str(desc).split(';')
        if len(parts) >= 4:
            building = parts[2].strip()
            sector = parts[3].strip()

            # Simplify names
            if 'excluding houses' in building:
                building = 'Other Dwellings'
            elif 'Total (Type of Building)' in building:
                building = 'All Dwellings'

            # Simplify series type
            stype_short = str(stype)
            if stype_short == 'Seasonally Adjusted':
                stype_short = 'SA'

            col_name = f"{building} - {sector} ({stype_short})"
            column_names.append(col_name)
        else:
            column_names.append(f"Series_{i}")
    else:
        column_names.append(f"Series_{i}")

# Assign new column names
data_df.columns = column_names

print(f"Loaded data: {len(data_df)} time periods")
print(f"Date range: {data_df.index[0].strftime('%Y-%m')} to {data_df.index[-1].strftime('%Y-%m')}")
print(f"Columns: {data_df.columns.tolist()}")

# Create comprehensive time series visualization
fig = plt.figure(figsize=(20, 14))
fig.suptitle('Building Consents Time Series - Victoria, Australia (1983-2025)\nNumber of Dwelling Units Approved',
             fontsize=18, fontweight='bold', y=0.995)

# 1. Total Dwelling Units - All Series Types
ax1 = plt.subplot(3, 2, 1)
colors = ['#2E86AB', '#A23B72', '#F18F01']
for col in data_df.columns:
    if 'All Dwellings - Total Sectors' in col:
        if '(Original)' in col:
            ax1.plot(data_df.index, data_df[col], label='Original', alpha=0.6, linewidth=1, color=colors[0])
        elif '(SA)' in col:
            ax1.plot(data_df.index, data_df[col], label='Seasonally Adjusted', alpha=0.7, linewidth=1.5, color=colors[1])
        elif '(Trend)' in col:
            ax1.plot(data_df.index, data_df[col], label='Trend', linewidth=2.5, color=colors[2])
ax1.set_title('Total Dwelling Units - All Sectors', fontsize=12, fontweight='bold')
ax1.set_xlabel('Year', fontsize=10)
ax1.set_ylabel('Number of Units', fontsize=10)
ax1.legend(loc='best', fontsize=9)
ax1.grid(True, alpha=0.3)

# 2. Houses vs Other Dwellings (Trend)
ax2 = plt.subplot(3, 2, 2)
for col in data_df.columns:
    if 'Trend' in col and 'Total Sectors' in col:
        if 'Houses' in col and 'Other' not in col and 'All' not in col:
            ax2.plot(data_df.index, data_df[col], label='Houses', linewidth=2.5, color='#06A77D')
        elif 'Other Dwellings' in col:
            ax2.plot(data_df.index, data_df[col], label='Other Dwellings', linewidth=2.5, color='#D62246')
ax2.set_title('Building Type Comparison (Trend)', fontsize=12, fontweight='bold')
ax2.set_xlabel('Year', fontsize=10)
ax2.set_ylabel('Number of Units', fontsize=10)
ax2.legend(loc='best', fontsize=9)
ax2.grid(True, alpha=0.3)

# 3. Private Sector - Houses (Original vs Trend)
ax3 = plt.subplot(3, 2, 3)
for col in data_df.columns:
    if 'Houses - Private Sector' in col:
        if '(Original)' in col:
            ax3.plot(data_df.index, data_df[col], label='Original', alpha=0.5, linewidth=1, color='#758BFD')
        elif '(Trend)' in col:
            ax3.plot(data_df.index, data_df[col], label='Trend', linewidth=2.5, color='#F25C54')
ax3.set_title('Houses - Private Sector', fontsize=12, fontweight='bold')
ax3.set_xlabel('Year', fontsize=10)
ax3.set_ylabel('Number of Units', fontsize=10)
ax3.legend(loc='best', fontsize=9)
ax3.grid(True, alpha=0.3)

# 4. All Dwellings - Private vs Total Sectors (Trend)
ax4 = plt.subplot(3, 2, 4)
for col in data_df.columns:
    if 'All Dwellings' in col and 'Trend' in col:
        if 'Private Sector' in col:
            ax4.plot(data_df.index, data_df[col], label='Private Sector', linewidth=2.5, color='#4A4E69')
        elif 'Total Sectors' in col:
            ax4.plot(data_df.index, data_df[col], label='All Sectors', linewidth=2.5, color='#9A8C98')
ax4.set_title('All Dwellings - Sector Comparison (Trend)', fontsize=12, fontweight='bold')
ax4.set_xlabel('Year', fontsize=10)
ax4.set_ylabel('Number of Units', fontsize=10)
ax4.legend(loc='best', fontsize=9)
ax4.grid(True, alpha=0.3)

# 5. Recent Trends (Last 10 years) - All Building Types
ax5 = plt.subplot(3, 2, 5)
recent_data = data_df[data_df.index >= '2015-01-01']
for col in recent_data.columns:
    if 'Trend' in col and 'Total Sectors' in col:
        if 'Houses - Total Sectors' in col:
            ax5.plot(recent_data.index, recent_data[col], label='Houses', linewidth=2.5, color='#06A77D', marker='o', markersize=2)
        elif 'Other Dwellings - Total Sectors' in col:
            ax5.plot(recent_data.index, recent_data[col], label='Other Dwellings', linewidth=2.5, color='#D62246', marker='s', markersize=2)
        elif 'All Dwellings - Total Sectors' in col:
            ax5.plot(recent_data.index, recent_data[col], label='All Dwellings', linewidth=2.5, color='#F18F01', marker='^', markersize=2)
ax5.set_title('Recent Trends (2015-2025)', fontsize=12, fontweight='bold')
ax5.set_xlabel('Year', fontsize=10)
ax5.set_ylabel('Number of Units', fontsize=10)
ax5.legend(loc='best', fontsize=9)
ax5.grid(True, alpha=0.3)

# 6. Year-over-Year Change (All Dwellings Total)
ax6 = plt.subplot(3, 2, 6)
for col in data_df.columns:
    if 'All Dwellings - Total Sectors (Trend)' in col:
        yoy_change = data_df[col].pct_change(periods=12) * 100
        ax6.fill_between(data_df.index, 0, yoy_change, alpha=0.3, color='gray')
        ax6.plot(data_df.index, yoy_change, linewidth=2, color='#2E86AB')
        ax6.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
        break
ax6.set_title('Year-over-Year % Change (All Dwellings Total)', fontsize=12, fontweight='bold')
ax6.set_xlabel('Year', fontsize=10)
ax6.set_ylabel('% Change', fontsize=10)
ax6.grid(True, alpha=0.3)

plt.tight_layout(rect=[0, 0.03, 1, 0.99])
plt.savefig('building_consents_timeseries.png', dpi=300, bbox_inches='tight')
print("\nTime series visualization saved as 'building_consents_timeseries.png'")

# Create a second figure with stacked area chart
fig2, axes = plt.subplots(2, 1, figsize=(20, 10))
fig2.suptitle('Building Consents - Stacked Area Charts & Moving Averages', fontsize=16, fontweight='bold')

# Stacked area chart - Building Types
ax = axes[0]
houses_col = None
other_col = None
for col in data_df.columns:
    if 'Houses - Total Sectors (Trend)' in col:
        houses_col = col
    elif 'Other Dwellings - Total Sectors (Trend)' in col:
        other_col = col

if houses_col and other_col:
    ax.fill_between(data_df.index, 0, data_df[houses_col],
                     label='Houses', alpha=0.7, color='#06A77D')
    ax.fill_between(data_df.index, data_df[houses_col],
                     data_df[houses_col] + data_df[other_col],
                     label='Other Dwellings', alpha=0.7, color='#D62246')
ax.set_title('Building Types Over Time (Stacked)', fontsize=12, fontweight='bold')
ax.set_xlabel('Year', fontsize=10)
ax.set_ylabel('Number of Units', fontsize=10)
ax.legend(loc='best', fontsize=10)
ax.grid(True, alpha=0.3)

# Rolling average comparison
ax = axes[1]
original_col = None
for col in data_df.columns:
    if 'All Dwellings - Total Sectors (Original)' in col:
        original_col = col
        break

if original_col:
    rolling_12m = data_df[original_col].rolling(window=12).mean()
    rolling_24m = data_df[original_col].rolling(window=24).mean()

    ax.plot(data_df.index, data_df[original_col],
            label='Monthly (Original)', alpha=0.3, linewidth=0.5, color='gray')
    ax.plot(data_df.index, rolling_12m, label='12-Month Average',
            linewidth=2.5, color='#2E86AB')
    ax.plot(data_df.index, rolling_24m, label='24-Month Average',
            linewidth=2.5, color='#F18F01')
ax.set_title('All Dwellings - Total (Moving Averages)', fontsize=12, fontweight='bold')
ax.set_xlabel('Year', fontsize=10)
ax.set_ylabel('Number of Units', fontsize=10)
ax.legend(loc='best', fontsize=10)
ax.grid(True, alpha=0.3)

plt.tight_layout(rect=[0, 0.03, 1, 0.97])
plt.savefig('building_consents_timeseries_stacked.png', dpi=300, bbox_inches='tight')
print("Stacked time series visualization saved as 'building_consents_timeseries_stacked.png'")

# Print summary statistics
print("\n" + "="*70)
print("TIME SERIES SUMMARY STATISTICS")
print("="*70)

for col in data_df.columns:
    if 'All Dwellings - Total Sectors (Trend)' in col:
        series = data_df[col].dropna()
        print(f"\nAll Dwellings - Total Sectors (Trend):")
        print(f"  Period: {series.index[0].strftime('%Y-%m')} to {series.index[-1].strftime('%Y-%m')}")
        print(f"  Mean: {series.mean():.0f} units/month")
        print(f"  Median: {series.median():.0f} units/month")
        print(f"  Min: {series.min():.0f} units ({series.idxmin().strftime('%Y-%m')})")
        print(f"  Max: {series.max():.0f} units ({series.idxmax().strftime('%Y-%m')})")
        print(f"  Latest: {series.iloc[-1]:.0f} units ({series.index[-1].strftime('%Y-%m')})")

        # Recent trend
        recent_6m = series.iloc[-6:].mean()
        prev_6m = series.iloc[-12:-6].mean()
        change = ((recent_6m - prev_6m) / prev_6m) * 100
        print(f"\n  Recent trend (last 6 months vs previous 6):")
        print(f"    Last 6 months average: {recent_6m:.0f} units")
        print(f"    Previous 6 months average: {prev_6m:.0f} units")
        print(f"    Change: {change:+.1f}%")
        break

for col in data_df.columns:
    if 'Houses - Total Sectors (Trend)' in col:
        series = data_df[col].dropna()
        print(f"\nHouses - Total Sectors (Trend):")
        print(f"  Mean: {series.mean():.0f} units/month")
        print(f"  Latest: {series.iloc[-1]:.0f} units ({series.index[-1].strftime('%Y-%m')})")
        break

for col in data_df.columns:
    if 'Other Dwellings - Total Sectors (Trend)' in col:
        series = data_df[col].dropna()
        print(f"\nOther Dwellings - Total Sectors (Trend):")
        print(f"  Mean: {series.mean():.0f} units/month")
        print(f"  Latest: {series.iloc[-1]:.0f} units ({series.index[-1].strftime('%Y-%m')})")
        break

print("\n" + "="*70)
print("Visualization complete!")
print("="*70)
