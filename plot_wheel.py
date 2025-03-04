#!/usr/bin/env python3
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.lines as mlines

import argparse
import os
from questions import questions_list


def plot_wheel_of_life(json_file, output_file):
    json_file = "user_responses.json"
    with open(json_file, "r") as f:
        data = json.load(f)

    categories = list(data.keys())
    num_categories = len(categories)
    num_questions = len(next(iter(data.values())))

    cmap = plt.get_cmap("tab10")  # Color map for categories
    all_questions = []
    values = []
    colors = []
    thetas = []
    widths = []
    category_colors = {}

    for i, (category, scores) in enumerate(data.items()):
        base_color = cmap(i % num_categories)
        category_colors[category] = base_color
        shades = list(
            mcolors.LinearSegmentedColormap.from_list("shade", ["white", base_color])(
                np.linspace(0.3, 1, num_questions)
            )
        )

        for j, (question, value) in enumerate(scores.items()):
            question_string = [
                d["question"] for d in questions_list[category] if d["key"] == question
            ][0]
            all_questions.append(question_string)
            values.append(value)
            colors.append(shades[j])
            thetas.append(
                (i * num_questions + j) * (2 * np.pi / (num_categories * num_questions))
            )
            widths.append(2 * np.pi / (num_categories * num_questions))
    # set figure size
    # plt.figure(figsize=(10,10))

    ax = plt.subplot(projection="polar")
    plt.axis("off")
    radii = values
    # Set the coordinates limits
    upperLimit = 50
    lowerLimit = 2
    bars = ax.bar(
        thetas,
        radii,
        width=widths,
        bottom=0.0,
        color=colors,
        alpha=0.5,
        edgecolor="white",
    )

    # little space between the bar and the label
    labelPadding = 2

    # Add labels
    for bar, angle, height, label in zip(bars, thetas, values, all_questions):
        # Labels are rotated. Rotation must be specified in degrees :(
        rotation = np.rad2deg(angle)

        # Flip some labels upside down
        alignment = ""
        if angle >= np.pi / 2 and angle < 3 * np.pi / 2:
            alignment = "right"
            rotation = rotation + 180
        else:
            alignment = "left"

        # Finally add the labels
        ax.text(
            x=angle,
            y=lowerLimit + bar.get_height() + labelPadding,
            s=label[0:70],
            ha=alignment,
            va="center",
            size=9,
            rotation=rotation,
            rotation_mode="anchor",
        )

    # Create legend with category colors
    legend_handles = [
        mlines.Line2D(
            [],
            [],
            color=color,
            marker="o",
            linestyle="None",
            markersize=8,
            label=category,
        )
        for category, color in category_colors.items()
    ]
    ax.legend(handles=legend_handles, loc="upper right", bbox_to_anchor=(3.0, 1.1))
    # plt.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1))

    # plt.title("Wheel of Life", fontsize=14, fontweight="bold")
    plt.savefig(output_file, dpi=300, bbox_inches="tight")
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate a Wheel of Life chart from a JSON file."
    )
    parser.add_argument(
        "--input-file", "-i", required=True, help="Path to the input JSON file."
    )
    parser.add_argument(
        "--output-folder",
        "-o",
        default=".",
        help="Path to the output folder. Defaults to the current directory.",
    )

    args = parser.parse_args()
    if not os.path.exists(args.input_file):
        raise FileNotFoundError(f"Input file '{args.input_file}' not found.")
    if not os.path.exists(args.output_folder):
        os.makedirs(args.output_folder)

    output_file = os.path.join(args.output_folder, "wheel_of_life.png")
    plot_wheel_of_life(args.input_file, output_file)

