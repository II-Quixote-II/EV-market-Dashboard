Question 1
# competitive pressure

# ====================================

# Total MKT Sales by Year

total_by_year = (
    df.groupby('year')['annual_sales_units'].sum())

# Teslas Sales, shares and ratings by year

tesla = df[df['brand'] == 'Tesla']
tesla_by_year = tesla.groupby('year').agg(
    Tesla_Sales = ('annual_sales_units', 'sum'),
    Avg_rating = ('customer_rating', 'mean'), 
    Model_count = ('model', 'nunique')).round(2)

tesla_by_year['Market_Share_Pct'] = (
    tesla_by_year['Tesla_Sales'] / total_by_year * 100).round(2)

print("--Tesla YoY--")
print(tesla_by_year.to_string())

# Prints Tesla YoY 

-------------------------------------------

# brand Stacked Chart

brand_sales = (
    df.groupby(['year', 'brand'])['annual_sales_units']
        .sum()
        .unstack(fill_value=0))

brand_share_pct = brand_sales.div(brand_sales.sum(axis=1), axis=0) * 100

print("Mkt share top 6")

top_brands = brand_share_pct.sum().sort_values(ascending=False).head(6).index
print(brand_share_pct[top_brands].round(1).to_string())

# prints Top 6 companies and sales

--------------------------------------------------
# Rival comparison - Competitive Landscape

rivals = ['Tesla', 'BYD', 'Hyundai', 'Kia', 'BMW']

rival_specs = (
    df[df['brand'].isin(rivals)]
    .groupby('brand').agg(
        Range = ('range_miles', 'mean'),
        Charging_Speed = ('charging_speed_kw', 'mean'),
        Autopilot = ('autopilot_level', 'mean'),
        Customer_Ratings = ('customer_rating', 'mean'),
        Range_per_dollar = ('range_per_dollar', 'mean')).round(2))

print("rival specifications")
print(rival_specs.to_string())

# prints top 6 rival specs

-------------------------------------------------------------

# Charts

fig, axes = plt.subplots(1, 3, figsize=(18, 6))
fig.suptitle('Tesla Dominance and Erosure)', fontsize=14, fontweight='bold')

## Chart 1 - Dual axis - Mkt Share+ Customer Ratings

ax1= axes[0]
ax2 = ax1.twinx()

ax1.plot(tesla_by_year.index, tesla_by_year['Market_Share_Pct'],
'o-', color='#E50914', linewidth=2.5, label= 'Market Share %')

ax2.plot(tesla_by_year.index, tesla_by_year['Avg_rating'],
         's-', color= '#2c3e50', linewidth=2, label ='Avg Customer Rating')

ax1.set_ylabel('Market Share (%)', color= '#E50914')
ax2.set_ylabel('Customer Rating', color='#2C3E50')
ax1.set_title('Tesla- Market Share Versus Ratings Over Time')
ax1.set_label('Year')

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=8)
ax1.grid(alpha=0.3)

# Chart 2 - Stacked Area Chart - Brand Market Share

ax = axes[1]

# Top 5 Brands - Rest are listed as Other

top5 = brand_share_pct.sum().sort_values(ascending=False).head(5).index
plot_share = brand_share_pct[top5].copy()
plot_share['Other'] = 100 - plot_share.sum(axis=1)

colors = ['#E50914', '#e67e22', '#2980b9', '#27ae60', '#8e44ad', '#95a5a6']
ax.stackplot(plot_share.index, plot_share.T, labels=plot_share.columns, colors=colors, alpha=0.60)

ax.set_title('EV Market Share by Brand')
ax.set_ylabel('Market Share (%)')
ax.set_xlabel('year')
ax.legend(loc='upper left', fontsize=7)
ax.set_ylim(0, 100)
ax.grid(alpha=0.3)

# Chart 3 - Radar - Tesla versus Rivals

ax = axes[2]
ax.set_title('spec comparison - Tesla vs Rivals (Normalised 0-1)', pad=20)

# Normalise

radar_df = rival_specs.copy()
for col in radar_df.columns:
    radar_df[col] = (radar_df[col] - radar_df[col].min()) / (radar_df[col].max() - radar_df[col].min())

categories = list(radar_df.columns)
N = len(categories)
angles = [n / float(N) * 2 * np.pi for n in range(N)]
angles += angles[:1] #close polygon

ax = plt.subplot(1, 3, 3, polar = True)


radar_colors = ['#E50914', '#e67e22', '#2980b9', '#27ae60', '#8e44ad']
for i, brand in enumerate(radar_df.index):
    values = radar_df.loc[brand].tolist()
    values += values[:1]
    ax.plot(angles, values, linewidth=2, label=brand, color=radar_colors[i])
    ax.fill(angles, values, alpha=0.1, color=radar_colors[i])

ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories, fontsize=8)
ax.legend(loc='upper right', bbox_to_anchor= (1.35, 1.1), fontsize=8)

plt.tight_layout()
plt.show()



