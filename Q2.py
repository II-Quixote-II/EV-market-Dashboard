# Question 2

# Oil SHock Charts

# Check over - elasticity

#Sales By Year + Segment

segment_sales = (
df.groupby(['year', 'market_segment'])['annual_sales_units']
    .sum()
    .reset_index()
)

segment_pivot = segment_sales.pivot(
    index='year', columns='market_segment', values='annual_sales_units').fillna(0)

# YoY growth per segment

segment_growth = segment_pivot.pct_change() * 100

print("Yearly Segment Sales \n")
print(segment_pivot.to_string())
print("\n yoy growth by segment \n")
print(segment_growth.round(2).to_string())

# Merging oil price into df
segment_pivot_oil = segment_pivot.reset_index().merge(oil_prices, on='year', how='left')
segment_growth_oil = segment_growth.reset_index().merge(oil_prices, on='year', how='left')

# ------------------------------------------------------------------------------------------------------------------------------------

# Elasticity 

#  removes 2020 
growth_reset = segment_growth.dropna().reset_index()


oil_pct_change = oil_prices.set_index('year')['oil_price'].pct_change() * 100
oil_change_df  = oil_pct_change.dropna().reset_index()
oil_change_df.columns = ['year', 'oil_pct_change']


merged_growth = growth_reset.merge(oil_change_df, on='year', how='inner')
print(merged_growth)


# calculate elasticity per segment
elasticity_data = merged_growth[merged_growth['year'] <= 2025].copy()
 
elasticity_fixed = {}
for segment in ['Budget', 'Mid-range', 'Premium', 'Luxury']:
    slope, intercept, r_value, p_value, std_err = stats.linregress(
        elasticity_data['oil_pct_change'], elasticity_data[segment]
    )
    elasticity_fixed[segment] = {
        'Elasticity': round(slope, 2),
        'R_squared': round(r_value ** 2, 3),
        'P_value': round(p_value, 3),
    }
 
elasticity_df = (
    pd.DataFrame.from_dict(elasticity_fixed, orient='index')
    .sort_values('Elasticity', ascending=False)
)
 
print(" Demand elasticity by segment")
print("Elasticity = % change in sales growth per 1% change in oil price")
print("Positive = sales grew faster when oil rose | Negative = sales grew slower/fell when oil rose\n")
print(elasticity_df.to_string())
print(f"\n(n = {len(elasticity_data)} years — small sample, treat p-values as indicative, not conclusive)")
 

# ---------------------------------------------------------------------------------------------------------------------------------------------

# Charts

fig, axes = plt.subplots(1,3,figsize=(18,6))
fig.suptitle('Oil SHock demand signal 2020-2026)', fontsize=14, fontweight='bold')

segment_colors = {
    'Budget': '#27AE60', 
    'Mid-range': '#2980B9',
    'Premium': '#E67E22',
    'Luxury': '#8E44AD',
}

# Chart 1: Segment Sales + Oil Prices

ax1 = axes[0]
ax2 = ax1.twinx()

for segment, color in segment_colors.items():
    ax1.plot(segment_pivot_oil['year'], segment_pivot_oil[segment],
             'o-', color=color, linewidth=2, label=segment)

ax2.plot(oil_prices['year'], oil_prices['oil_price'],
         's--', color= 'black', linewidth=1.5, alpha=0.6, label='Oil Price $/barrel')

ax1.axvline(x=2022, color='red', linestyle=':', alpha=0.7)
ax1.text(2022.05, ax1.get_ylim()[1] * 0.95, '2022 Oil Spike', fontsize= 7, color='red')

ax1.set_ylabel('Annual Sales Units')
ax2.set_ylabel('Oil Price $/Barrel')

ax1.set_xlabel('Year')
ax1.set_title('Segment Sales vs Oil Price')
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x/1e6:.0f}M'))

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()

ax1.legend(lines1 + lines2, labels1 + labels2, fontsize=7)
ax1.grid(alpha=0.3)

# Chart 2: Grouped Bar - YoY Growth by Segment 
ax = axes[1]
growth_clean = segment_growth.dropna()   # Remove 2020 NaN row
years  = growth_clean.index.tolist()
x      = np.arange(len(years))
width  = 0.2
segs   = ['Budget', 'Mid-range', 'Premium', 'Luxury']

for i, segment in enumerate(segs):
    bars = ax.bar(x + i * width, growth_clean[segment],
                  width, label=segment, color=segment_colors[segment], alpha=0.85)

ax.axhline(y=0, color='black', linewidth=0.8)
ax.set_xticks(x + width * 1.5)
ax.set_xticklabels(years)
ax.set_ylabel('YoY Growth (%)')
ax.set_title('Year-on-Year Sales Growth by Segment')
ax.set_xlabel('Year')
ax.legend(fontsize=8)
ax.grid(alpha=0.3, axis='y')

# Highlight 2022 bars
ax.axvspan(0.9, 1.7, alpha=0.08, color='red')
ax.text(2.0, ax.get_ylim()[1] * 0.9, '2022\nOil Shock', fontsize=7, color='red')

# Chart 3: Elasticity Bar Chart
ax = axes[2]
colors_list = [segment_colors[s] for s in elasticity_df.index]
bars = ax.barh(elasticity_df.index, elasticity_df['Elasticity'],
               color=colors_list, alpha=0.85, edgecolor='white')
 
ax.axvline(x=0, color='black', linewidth=1)
ax.set_xlabel('Elasticity (Sales % change per 1% oil price change)')
ax.set_title('Demand Elasticity to Oil Price)', fontsize=10)
ax.grid(alpha=0.3, axis='x')
 
# Labeling each bar with its number and R2 / R Squared
for bar, val, r2 in zip(bars, elasticity_df['Elasticity'], elasticity_df['R_squared']):
    offset = 0.05 if val >= 0 else -0.05
    ha = 'left' if val >= 0 else 'right'
    ax.text(val + offset, bar.get_y() + bar.get_height()/2,
            f'{val:.2f}  (R\u00b2={r2:.2f})', va='center', ha=ha, fontsize=8)
 
plt.tight_layout()
plt.show()

