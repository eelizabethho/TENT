import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the clean data
df_2019 = pd.read_csv("broadband_data_2019_clean.csv")
df_2020 = pd.read_csv("broadband_data_2020_clean.csv")

# Clean the numeric columns (remove spaces and convert to float, handling non-numeric values)
df_2019['BROADBAND AVAILABILITY PER FCC'] = pd.to_numeric(df_2019['BROADBAND AVAILABILITY PER FCC'].str.strip(), errors='coerce')
df_2019['BROADBAND USAGE'] = pd.to_numeric(df_2019['BROADBAND USAGE'].str.strip(), errors='coerce')
df_2020['BROADBAND AVAILABILITY PER FCC'] = pd.to_numeric(df_2020['BROADBAND AVAILABILITY PER FCC'], errors='coerce')
df_2020['BROADBAND USAGE'] = pd.to_numeric(df_2020['BROADBAND USAGE'], errors='coerce')

# Drop rows with NaN values in key columns
df_2019 = df_2019.dropna(subset=['BROADBAND AVAILABILITY PER FCC', 'BROADBAND USAGE'])
df_2020 = df_2020.dropna(subset=['BROADBAND AVAILABILITY PER FCC', 'BROADBAND USAGE'])

# Merge on COUNTY ID to compare same counties
merged = pd.merge(df_2019[['COUNTY ID', 'COUNTY NAME', 'BROADBAND AVAILABILITY PER FCC', 'BROADBAND USAGE']], 
                  df_2020[['COUNTY ID', 'COUNTY NAME', 'BROADBAND AVAILABILITY PER FCC', 'BROADBAND USAGE']], 
                  on='COUNTY ID', 
                  suffixes=('_2019', '_2020'))

# Create figure with subplots (1 row, 2 columns for the two bottom graphs)
fig, axes = plt.subplots(1, 2, figsize=(16, 8))
fig.suptitle('Broadband Data Comparison: 2019 vs 2020', fontsize=16, fontweight='bold')

# Top 10 Counties by Usage - Comparison
ax3 = axes[0]
top_10_usage = merged.nlargest(10, 'BROADBAND USAGE_2020')
counties_usage = top_10_usage['COUNTY NAME_2019'].values
x_pos_usage = np.arange(len(counties_usage))
width = 0.35

ax3.barh(x_pos_usage - width/2, top_10_usage['BROADBAND USAGE_2019'], width, 
         label='2019', color='#3498db', alpha=0.8)
ax3.barh(x_pos_usage + width/2, top_10_usage['BROADBAND USAGE_2020'], width, 
         label='2020', color='#e74c3c', alpha=0.8)
ax3.set_yticks(x_pos_usage)
ax3.set_yticklabels(counties_usage, fontsize=8)
ax3.set_xlabel('Broadband Usage', fontsize=11)
ax3.set_title('Top 10 Counties by Usage (2020)', fontsize=12, fontweight='bold')
ax3.legend()
ax3.grid(axis='x', alpha=0.3)
ax3.set_xlim([0, 1.1])

# Change in Availability (2020 - 2019)
ax4 = axes[1]
merged['Change_Availability'] = merged['BROADBAND AVAILABILITY PER FCC_2020'] - merged['BROADBAND AVAILABILITY PER FCC_2019']
merged_sorted = merged.sort_values('Change_Availability', ascending=False)
top_changes = merged_sorted.head(10)
bottom_changes = merged_sorted.tail(10)
combined_changes = pd.concat([top_changes, bottom_changes]).sort_values('Change_Availability')

counties_change = combined_changes['COUNTY NAME_2019'].values
x_pos_change = np.arange(len(counties_change))
colors_change = ['#27ae60' if x > 0 else '#c0392b' for x in combined_changes['Change_Availability']]

ax4.barh(x_pos_change, combined_changes['Change_Availability'], color=colors_change, alpha=0.8)
ax4.set_yticks(x_pos_change)
ax4.set_yticklabels(counties_change, fontsize=8)
ax4.set_xlabel('Change in Availability (2020 - 2019)', fontsize=11)
ax4.set_title('Top 10 Increases & Decreases in Availability', fontsize=12, fontweight='bold')
ax4.axvline(x=0, color='black', linestyle='--', linewidth=0.8)
ax4.grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.savefig('broadband_comparison_2019_2020.png', dpi=300, bbox_inches='tight')
print("Bar graph saved as 'broadband_comparison_2019_2020.png'")
plt.show()

