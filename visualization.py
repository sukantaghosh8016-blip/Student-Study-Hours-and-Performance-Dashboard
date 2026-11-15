"""visualization.py - Matplotlib graphs saved as PNG images."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # save to files; works without a display window
import matplotlib.pyplot as plt
import numpy as np


def _prepare(graphs_dir):
    graphs_dir = Path(graphs_dir)
    graphs_dir.mkdir(exist_ok=True)
    return graphs_dir


def scatter_study_vs_marks(df, graphs_dir):
    """Scatter plot of study hours vs marks, with a trend line."""
    path = _prepare(graphs_dir) / "scatter_hours_vs_marks.png"
    x, y = df["study_hours"].to_numpy(), df["marks"].to_numpy()

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(x, y, alpha=0.75, edgecolors="black")
    if len(x) > 1 and x.std() > 0:
        slope, intercept = np.polyfit(x, y, 1)
        xs = np.linspace(x.min(), x.max(), 100)
        ax.plot(xs, slope * xs + intercept, color="red",
                label=f"Trend line (slope = {slope:.2f})")
        ax.legend()
    ax.set_title("Daily Study Hours vs Examination Marks")
    ax.set_xlabel("Daily study hours")
    ax.set_ylabel("Examination marks")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


def histogram_marks(df, graphs_dir):
    """Histogram of the distribution of marks."""
    path = _prepare(graphs_dir) / "histogram_marks.png"
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(df["marks"], bins=10, edgecolor="black")
    ax.axvline(df["marks"].mean(), color="red", linestyle="--",
               label=f"Mean = {df['marks'].mean():.1f}")
    ax.set_title("Distribution of Examination Marks")
    ax.set_xlabel("Marks")
    ax.set_ylabel("Number of students")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


def bar_course_average(df, graphs_dir):
    """Bar chart comparing average marks of each course."""
    path = _prepare(graphs_dir) / "bar_course_average_marks.png"
    avg = df.groupby("course")["marks"].mean().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(avg.index, avg.values, edgecolor="black")
    for bar, val in zip(bars, avg.values):
        ax.text(bar.get_x() + bar.get_width() / 2, val + 0.5, f"{val:.1f}",
                ha="center")
    ax.set_title("Average Examination Marks by Course")
    ax.set_xlabel("Course")
    ax.set_ylabel("Average marks")
    ax.set_ylim(0, 100)
    plt.setp(ax.get_xticklabels(), rotation=20, ha="right")
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


def generate_all_graphs(df, graphs_dir):
    return [scatter_study_vs_marks(df, graphs_dir),
            histogram_marks(df, graphs_dir),
            bar_course_average(df, graphs_dir)]
