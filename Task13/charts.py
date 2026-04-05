import matplotlib.pyplot as plt
from pathlib import Path
from collections import defaultdict

OUTPUT = Path("charts_output")

def revenue_by_region_chart(data):
    region_map = defaultdict(int)
    for region, revenue, units, date in data:
        region_map[region] += revenue
    regions = list(region_map.keys())
    revenue = list(region_map.values())

    OUTPUT.mkdir(exist_ok=True)

    chart_path = OUTPUT / "region_chart.png"

    plt.bar(regions, revenue)
    plt.title("Revenue by Region")
    plt.savefig(chart_path)
    plt.close()
    return chart_path


def daily_sales_chart(data):
    daily_map = defaultdict(int)
    for region, revenue, units, date in data:
        daily_map[date] += revenue
    dates = list(daily_map.keys())
    revenue = list(daily_map.values())
    chart_path = OUTPUT / "daily_chart.png"

    plt.plot(dates, revenue)
    plt.title("Daily Sales Trend")
    plt.xticks(rotation=45)

    plt.savefig(chart_path)
    plt.close()

    return chart_path