from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from modules.analytics import (
    donations_by_cause, donations_by_source, donations_by_month
)


def _new_figure(title):
    fig, ax = plt.subplots(figsize=(8.6, 4.4))
    ax.set_title(title, fontsize=13, fontweight="bold")
    ax.grid(axis="y", alpha=0.25)
    return fig, ax


def create_cause_chart(data):
    fig, ax = _new_figure("Donation Distribution by Cause")
    if hasattr(data, "empty") and not data.empty:
        data.plot(kind="bar", ax=ax, color="#2f75b5")
        ax.set_xlabel("Cause")
        ax.set_ylabel("Donation Amount (₹)")
        ax.tick_params(axis="x", rotation=35)
    else:
        ax.text(0.5, 0.5, "No donation data available.",
                ha="center", va="center", transform=ax.transAxes)
    fig.tight_layout()
    return fig


def create_source_chart(data):
    fig, ax = _new_figure("Donation Distribution by Source")
    if hasattr(data, "empty") and not data.empty:
        wedges, _ = ax.pie(data.values, startangle=90,
                           wedgeprops={"width": 0.45})
        ax.legend(
            wedges,
            [f"{label}: ₹{value:,.0f}" for label, value in data.items()],
            loc="center left", bbox_to_anchor=(1, 0.5), fontsize=8
        )
        ax.set_title("Donation Distribution by Source", fontsize=13,
                     fontweight="bold")
    else:
        ax.text(0.5, 0.5, "No donation data available.",
                ha="center", va="center", transform=ax.transAxes)
    fig.tight_layout()
    return fig


def create_month_chart(data):
    fig, ax = _new_figure("Monthly Donation Trend")
    if hasattr(data, "empty") and not data.empty:
        data.plot(kind="line", marker="o", ax=ax, color="#1f9d55",
                  linewidth=2)
        ax.set_xlabel("Month")
        ax.set_ylabel("Donation Amount (₹)")
        ax.tick_params(axis="x", rotation=35)
    else:
        ax.text(0.5, 0.5, "No donation data available.",
                ha="center", va="center", transform=ax.transAxes)
    fig.tight_layout()
    return fig


def show_chart_in_frame(parent, fig):
    for child in parent.winfo_children():
        child.destroy()

    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    widget = canvas.get_tk_widget()
    widget.pack(fill="both", expand=True, padx=8, pady=8)
    parent._canvas = canvas


def save_all_reports(base_dir, donations):
    reports_dir = Path(base_dir) / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    outputs = []

    cause_fig = create_cause_chart(donations_by_cause(donations))
    cause_path = reports_dir / "donation_by_cause.png"
    cause_fig.savefig(cause_path, dpi=160, bbox_inches="tight")
    plt.close(cause_fig)
    outputs.append(cause_path)

    source_fig = create_source_chart(donations_by_source(donations))
    source_path = reports_dir / "donation_by_source.png"
    source_fig.savefig(source_path, dpi=160, bbox_inches="tight")
    plt.close(source_fig)
    outputs.append(source_path)

    month_fig = create_month_chart(donations_by_month(donations))
    month_path = reports_dir / "donation_trend_by_month.png"
    month_fig.savefig(month_path, dpi=160, bbox_inches="tight")
    plt.close(month_fig)
    outputs.append(month_path)

    from modules.analytics import donations_dataframe
    df = donations_dataframe(donations)
    csv_path = reports_dir / "donation_analysis.csv"
    df.to_csv(csv_path, index=False)
    outputs.append(csv_path)

    return outputs
