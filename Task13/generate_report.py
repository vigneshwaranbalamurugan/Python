import argparse
from db import fetch_sales
from charts import revenue_by_region_chart, daily_sales_chart
from template_render import render_template
from pdf_generate import generate_pdf
from send_email import send_email

def main(month):
    print("Fetching data...")
    data = fetch_sales(month)

    print("Generating charts...")
    region_chart = revenue_by_region_chart(data)
    daily_chart = daily_sales_chart(data)

    revenue = sum(row[1] for row in data)
    units = sum(row[2] for row in data)

    warning = revenue < 200000

    print("Rendering template...")

    context = {
        "month": month,
        "revenue": revenue,
        "units": units,
        "region_chart": region_chart,
        "daily_chart": daily_chart,
        "warning": warning
    }

    html_path = render_template(
        "monthly_sales.html",
        context
    )

    print("Generating PDF...")
    pdf = generate_pdf(context, f"sales_report_{month}.pdf")
    print("ending Email...")
    send_email(pdf)

    print("Report completed ")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--month")
    args = parser.parse_args()
    main(args.month)