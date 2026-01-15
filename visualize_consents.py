#!/usr/bin/env python3
"""
Visualization of Building Consents Data from Victoria, Australia
Data source: Table 02 - Number of dwelling units approved by sector
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re

# Set style
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (16, 12)

# Read the Excel file
df = pd.read_excel('8731002.xlsx', header=None)

# Extract metadata (rows 11-26 contain the actual data series information)
metadata_rows = df.iloc[10:27].copy()
metadata_rows.columns = df.iloc[9].values

# Clean up the metadata
metadata = metadata_rows[metadata_rows['Data Item Description'].notna()].copy()
metadata = metadata[['Data Item Description', 'Series Type', 'Series ID', 'Series Start', 'Series End', 'No. Obs.']]

# Parse the description to extract building type and sector
def parse_description(desc):
    """Extract building type and sector from description"""
    if pd.isna(desc):
        return None, None

    parts = desc.split(';')
    if len(parts) >= 4:
        building_type = parts[2].strip()
        sector = parts[3].strip()
        return building_type, sector
    return None, None

metadata[['Building Type', 'Sector']] = metadata['Data Item Description'].apply(
    lambda x: pd.Series(parse_description(x))
)

# Create visualizations
fig = plt.figure(figsize=(16, 12))
fig.suptitle('Building Consents Analysis - Victoria, Australia\nNumber of Dwelling Units Approved (1983-2025)',
             fontsize=16, fontweight='bold', y=0.98)

# 1. Count by Series Type
ax1 = plt.subplot(2, 3, 1)
series_counts = metadata['Series Type'].value_counts()
colors = sns.color_palette("Set2", len(series_counts))
series_counts.plot(kind='bar', ax=ax1, color=colors)
ax1.set_title('Time Series by Type', fontsize=12, fontweight='bold')
ax1.set_xlabel('Series Type', fontsize=10)
ax1.set_ylabel('Count', fontsize=10)
ax1.tick_params(axis='x', rotation=45)
for i, v in enumerate(series_counts.values):
    ax1.text(i, v + 0.1, str(v), ha='center', va='bottom', fontweight='bold')

# 2. Count by Building Type
ax2 = plt.subplot(2, 3, 2)
building_counts = metadata['Building Type'].value_counts()
colors = sns.color_palette("Set3", len(building_counts))
building_counts.plot(kind='bar', ax=ax2, color=colors)
ax2.set_title('Series by Building Type', fontsize=12, fontweight='bold')
ax2.set_xlabel('Building Type', fontsize=10)
ax2.set_ylabel('Count', fontsize=10)
ax2.tick_params(axis='x', rotation=45)
for i, v in enumerate(building_counts.values):
    ax2.text(i, v + 0.1, str(v), ha='center', va='bottom', fontweight='bold')

# 3. Count by Sector
ax3 = plt.subplot(2, 3, 3)
sector_counts = metadata['Sector'].value_counts()
colors = sns.color_palette("Pastel1", len(sector_counts))
sector_counts.plot(kind='bar', ax=ax3, color=colors)
ax3.set_title('Series by Sector', fontsize=12, fontweight='bold')
ax3.set_xlabel('Sector', fontsize=10)
ax3.set_ylabel('Count', fontsize=10)
ax3.tick_params(axis='x', rotation=45)
for i, v in enumerate(sector_counts.values):
    ax3.text(i, v + 0.1, str(v), ha='center', va='bottom', fontweight='bold')

# 4. Heatmap of Series Type vs Building Type
ax4 = plt.subplot(2, 3, 4)
heatmap_data = pd.crosstab(metadata['Series Type'], metadata['Building Type'])
sns.heatmap(heatmap_data, annot=True, fmt='d', cmap='YlOrRd', ax=ax4, cbar_kws={'label': 'Count'})
ax4.set_title('Series Type vs Building Type', fontsize=12, fontweight='bold')
ax4.set_xlabel('Building Type', fontsize=10)
ax4.set_ylabel('Series Type', fontsize=10)

# 5. Heatmap of Building Type vs Sector
ax5 = plt.subplot(2, 3, 5)
heatmap_data2 = pd.crosstab(metadata['Building Type'], metadata['Sector'])
sns.heatmap(heatmap_data2, annot=True, fmt='d', cmap='Blues', ax=ax5, cbar_kws={'label': 'Count'})
ax5.set_title('Building Type vs Sector', fontsize=12, fontweight='bold')
ax5.set_xlabel('Sector', fontsize=10)
ax5.set_ylabel('Building Type', fontsize=10)

# 6. Summary statistics table
ax6 = plt.subplot(2, 3, 6)
ax6.axis('off')

# Create summary text
summary_text = f"""
SUMMARY STATISTICS
{'='*50}

Total Series: {len(metadata)}
Time Period: July 1983 - November 2025
Observations per series: 509 months
Location: Victoria, Australia

Series Types:
  • Original: {len(metadata[metadata['Series Type'] == 'Original'])}
  • Seasonally Adjusted: {len(metadata[metadata['Series Type'] == 'Seasonally Adjusted'])}
  • Trend: {len(metadata[metadata['Series Type'] == 'Trend'])}

Building Types:
  • Houses: {len(metadata[metadata['Building Type'] == 'Houses'])}
  • Dwellings excluding houses: {len(metadata[metadata['Building Type'] == 'Dwellings excluding houses'])}
  • Total (all types): {len(metadata[metadata['Building Type'] == 'Total (Type of Building)'])}

Sectors:
  • Private Sector: {len(metadata[metadata['Sector'] == 'Private Sector'])}
  • Total Sectors: {len(metadata[metadata['Sector'] == 'Total Sectors'])}
"""

ax6.text(0.1, 0.5, summary_text, fontsize=10, verticalalignment='center',
         family='monospace', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))

plt.tight_layout(rect=[0, 0.03, 1, 0.96])
plt.savefig('building_consents_visualization.png', dpi=300, bbox_inches='tight')
print("Visualization saved as 'building_consents_visualization.png'")

# Create a detailed breakdown chart
fig2, axes = plt.subplots(2, 2, figsize=(16, 10))
fig2.suptitle('Building Consents - Detailed Breakdown by Category', fontsize=16, fontweight='bold')

# Filter for each series type
for idx, series_type in enumerate(['Original', 'Seasonally Adjusted', 'Trend']):
    if idx < 3:
        row = idx // 2
        col = idx % 2
        ax = axes[row, col]

        subset = metadata[metadata['Series Type'] == series_type]

        # Create grouped bar chart
        building_sector_data = subset.groupby(['Building Type', 'Sector']).size().unstack(fill_value=0)
        building_sector_data.plot(kind='bar', ax=ax, color=['#FF6B6B', '#4ECDC4'])
        ax.set_title(f'{series_type} Data Series', fontsize=12, fontweight='bold')
        ax.set_xlabel('Building Type', fontsize=10)
        ax.set_ylabel('Number of Series', fontsize=10)
        ax.legend(title='Sector', fontsize=9)
        ax.tick_params(axis='x', rotation=45)

        # Add value labels
        for container in ax.containers:
            ax.bar_label(container, fontweight='bold', fontsize=9)

# Use the last subplot for a pie chart
ax = axes[1, 1]
all_categories = metadata['Building Type'] + ' - ' + metadata['Sector']
category_counts = all_categories.value_counts()
colors = sns.color_palette("husl", len(category_counts))
wedges, texts, autotexts = ax.pie(category_counts.values, labels=category_counts.index,
                                    autopct='%1.1f%%', startangle=90, colors=colors)
ax.set_title('Distribution of All Categories', fontsize=12, fontweight='bold')
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')
    autotext.set_fontsize(8)
for text in texts:
    text.set_fontsize(8)

plt.tight_layout(rect=[0, 0.03, 1, 0.96])
plt.savefig('building_consents_detailed.png', dpi=300, bbox_inches='tight')
print("Detailed visualization saved as 'building_consents_detailed.png'")

# Export metadata to CSV for reference
metadata.to_csv('building_consents_metadata.csv', index=False)
print("Metadata exported to 'building_consents_metadata.csv'")

print("\nVisualization complete!")
print(f"Total series analyzed: {len(metadata)}")
print(f"Time period covered: July 1983 - November 2025 (509 months)")
