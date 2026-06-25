# =============================================================================
#  HiGen Labs Data Analytics Assessment — EDA + Chart Generator
#  Author  : Samaksh Kori
#  Email   : Samakshkori.2007@gmail.com
#  College : Hansraj College, University of Delhi
#  Date    : June 2026
#
#  HOW TO RUN:
#    python higen_labs_eda.py
#    A file dialogue box will open — select your cleaned CSV or Excel file.
#    All charts + EDA dashboard will be saved in the same folder.
# =============================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("TkAgg")   # needed for tkinter to work alongside matplotlib
import seaborn as sns
import os
import warnings
warnings.filterwarnings("ignore")

from tkinter import Tk, filedialog, messagebox

# ─────────────────────────────────────────────────────────────────────────────
# STEP 1 — FILE SELECTION VIA DIALOGUE BOX
# ─────────────────────────────────────────────────────────────────────────────
def select_file():
    root = Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    file_path = filedialog.askopenfilename(
        title="Select Cleaned Student Dataset",
        filetypes=[
            ("CSV files",   "*.csv"),
            ("Excel files", "*.xlsx *.xls"),
            ("All files",   "*.*")
        ]
    )
    root.destroy()
    return file_path

print("=" * 65)
print("  HiGen Labs — BBA/MBA Student EDA + Chart Generator")
print("  Author : Samaksh Kori | Hansraj College, Delhi")
print("=" * 65)
print("\n📁 Opening file dialogue... please select your dataset.")

file_path = select_file()

if not file_path:
    print("❌ No file selected. Exiting.")
    exit()

print(f"✅ File selected: {file_path}")
output_dir = os.path.dirname(file_path)

# ─────────────────────────────────────────────────────────────────────────────
# STEP 2 — LOAD DATA
# ─────────────────────────────────────────────────────────────────────────────
if file_path.endswith(".xlsx") or file_path.endswith(".xls"):
    df = pd.read_excel(file_path)
else:
    df = pd.read_csv(file_path)

print(f"\n[✓] Dataset loaded: {df.shape[0]} rows × {df.shape[1]} columns")

# ─────────────────────────────────────────────────────────────────────────────
# STEP 3 — BASIC OVERVIEW
# ─────────────────────────────────────────────────────────────────────────────
print("\n── COLUMN OVERVIEW ─────────────────────────────────────────")
info_df = pd.DataFrame({
    "Column"   : df.columns,
    "Dtype"    : df.dtypes.values,
    "Non-Null" : df.notnull().sum().values,
    "Nulls"    : df.isnull().sum().values,
})
print(info_df.to_string(index=False))

print("\n── SAMPLE ROWS (first 3) ────────────────────────────────────")
print(df.head(3).to_string(index=False))

# ─────────────────────────────────────────────────────────────────────────────
# STEP 4 — EDA: DEGREE, SKILLS, SPECS, CITIES, YEARS
# ─────────────────────────────────────────────────────────────────────────────
print("\n── DEGREE DISTRIBUTION ─────────────────────────────────────")
deg = df["Degree"].value_counts()
for d, c in deg.items():
    print(f"    {d}: {c}  ({c/len(df)*100:.1f}%)")

print("\n── TOP 10 MOST COMMON SKILLS ───────────────────────────────")
all_skills = df["Skills"].dropna().str.split(", ").explode().str.strip()
top_skills = all_skills.value_counts().head(10)
print(top_skills.to_string())

print("\n── TOP 8 SPECIALIZATIONS ───────────────────────────────────")
spec = df["Specialization"].value_counts().head(8)
print(spec.to_string())

print("\n── TOP 10 CITIES ───────────────────────────────────────────")
city = df["Location"].value_counts().head(10)
print(city.to_string())

print("\n── GRADUATION YEAR DISTRIBUTION ────────────────────────────")
grad = df["Graduation Year"].astype(str).value_counts().sort_index()
print(grad.to_string())

# ─────────────────────────────────────────────────────────────────────────────
# STEP 5 — INTERNSHIP & CERTIFICATION FLAGS
# ─────────────────────────────────────────────────────────────────────────────
df["Has_Internship"] = df["Internship Experience"].apply(
    lambda x: "No" if str(x).strip().lower() == "none" else "Yes"
)
df["Has_Cert"] = df["Certifications"].apply(
    lambda x: "No" if str(x).strip().lower() == "none" else "Yes"
)

print("\n── INTERNSHIP PARTICIPATION ─────────────────────────────────")
print(df["Has_Internship"].value_counts().to_string())

print("\n── TOP 8 CERTIFICATIONS ─────────────────────────────────────")
top_certs = df[df["Has_Cert"] == "Yes"]["Certifications"].value_counts().head(8)
print(top_certs.to_string())

print("\n── TOP INTERNSHIP COMPANIES ─────────────────────────────────")
companies = (
    df[df["Has_Internship"] == "Yes"]["Internship Experience"]
    .str.extract(r"at (.+?) \(")[0]
    .value_counts().head(10)
)
print(companies.to_string())

print("\n── TOP 5 SKILLS BY DEGREE ───────────────────────────────────")
for deg_name in ["MBA", "BBA"]:
    subset = df[df["Degree"] == deg_name]["Skills"].dropna()
    top = subset.str.split(", ").explode().str.strip().value_counts().head(5)
    print(f"\n  {deg_name}:")
    print(top.to_string())

print("\n── CITY × DEGREE BREAKDOWN (Top 5 Cities) ──────────────────")
top5 = df["Location"].value_counts().head(5).index
city_deg = df[df["Location"].isin(top5)].groupby(
    ["Location", "Degree"]).size().unstack(fill_value=0)
print(city_deg.to_string())

df["Skills_Count"] = df["Skills"].apply(
    lambda x: len(str(x).split(",")) if pd.notnull(x) else 0
)
print("\n── SKILLS COUNT PER STUDENT (stats) ─────────────────────────")
print(df["Skills_Count"].describe().round(2).to_string())

# ─────────────────────────────────────────────────────────────────────────────
# COLOUR PALETTE
# ─────────────────────────────────────────────────────────────────────────────
NAVY  = "#1A3C6E"
TEAL  = "#2E86AB"
RED   = "#E84855"
sns.set_theme(style="whitegrid", palette="muted")

# ─────────────────────────────────────────────────────────────────────────────
# CHART 1 — Top 10 Skills (Horizontal Bar)
# ─────────────────────────────────────────────────────────────────────────────
plt.figure(figsize=(10, 6))
sns.barplot(x=top_skills.values, y=top_skills.index, color=TEAL)
plt.title("Top 10 Student Skills", fontsize=13, fontweight="bold")
plt.xlabel("Number of Students")
for i, v in enumerate(top_skills.values):
    plt.text(v + 1.5, i, str(v), va="center", fontsize=9, fontweight="bold")
plt.tight_layout()
p1 = os.path.join(output_dir, "chart1_skills.png")
plt.savefig(p1, dpi=150)
plt.close()
print("\n[✓] chart1_skills.png saved")

# ─────────────────────────────────────────────────────────────────────────────
# CHART 2 — Specialization by Degree (Grouped Bar)
# ─────────────────────────────────────────────────────────────────────────────
plt.figure(figsize=(10, 6))
top_specs   = df["Specialization"].value_counts().head(5).index
filtered_df = df[df["Specialization"].isin(top_specs)]
ax2 = sns.countplot(data=filtered_df, x="Specialization", hue="Degree",
                    palette=[NAVY, TEAL])
plt.title("Specialization Distribution by Degree", fontsize=13, fontweight="bold")
plt.xlabel("Specialization")
plt.ylabel("Count")
for p in ax2.patches:
    if p.get_height() > 0:
        ax2.annotate(f"{int(p.get_height())}",
                     (p.get_x() + p.get_width() / 2., p.get_height()),
                     ha="center", va="bottom", xytext=(0, 4),
                     textcoords="offset points", fontsize=9, fontweight="bold")
plt.tight_layout()
p2 = os.path.join(output_dir, "chart2_specialization.png")
plt.savefig(p2, dpi=150)
plt.close()
print("[✓] chart2_specialization.png saved")

# ─────────────────────────────────────────────────────────────────────────────
# CHART 3 — Top 5 Cities (Pie)
# ─────────────────────────────────────────────────────────────────────────────
plt.figure(figsize=(7, 7))
top_cities  = df["Location"].value_counts().head(5)
colors_pie  = [NAVY, TEAL, "#4ECDC4", "#A8DADC", "#457B9D"]
plt.pie(top_cities.values, labels=top_cities.index,
        autopct="%1.1f%%", colors=colors_pie, startangle=140)
plt.title("Top 5 Student Locations", fontsize=13, fontweight="bold")
plt.tight_layout()
p3 = os.path.join(output_dir, "chart3_cities.png")
plt.savefig(p3, dpi=150)
plt.close()
print("[✓] chart3_cities.png saved")

# ─────────────────────────────────────────────────────────────────────────────
# CHART 4 — Graduation Year Trend (Line)
# ─────────────────────────────────────────────────────────────────────────────
plt.figure(figsize=(9, 5))
grad_plot = df["Graduation Year"].astype(str).value_counts().sort_index()
plt.plot(grad_plot.index, grad_plot.values, marker="o",
         color=RED, linewidth=2.5)
plt.fill_between(grad_plot.index, grad_plot.values, alpha=0.12, color=RED)
plt.title("Graduation Year Trend (2024–2027)", fontsize=13, fontweight="bold")
plt.xlabel("Graduation Year")
plt.ylabel("Student Count")
for i, (x, y) in enumerate(zip(grad_plot.index, grad_plot.values)):
    plt.text(i, y + 3, str(y), ha="center", fontsize=9, fontweight="bold")
plt.grid(True, linestyle=":")
plt.tight_layout()
p4 = os.path.join(output_dir, "chart4_gradyear.png")
plt.savefig(p4, dpi=150)
plt.close()
print("[✓] chart4_gradyear.png saved")

# ─────────────────────────────────────────────────────────────────────────────
# CHART 5 — Internship vs Certification (Grouped Bar)
# ─────────────────────────────────────────────────────────────────────────────
plt.figure(figsize=(8, 5))
has_intern = df["Has_Internship"].value_counts()
has_cert   = df["Has_Cert"].value_counts()
summary_df = pd.DataFrame({
    "Status" : ["Yes", "No", "Yes", "No"],
    "Metric" : ["Internship", "Internship", "Certification", "Certification"],
    "Count"  : [
        has_intern.get("Yes", 0), has_intern.get("No", 0),
        has_cert.get("Yes", 0),   has_cert.get("No", 0)
    ]
})
ax5 = sns.barplot(data=summary_df, x="Metric", y="Count", hue="Status",
                  palette=[TEAL, "#E0E0E0"])
plt.title("Students with Internships vs Certifications",
          fontsize=13, fontweight="bold")
plt.xlabel("")
plt.ylabel("Number of Students")
for p in ax5.patches:
    if p.get_height() > 0:
        ax5.annotate(f"{int(p.get_height())}",
                     (p.get_x() + p.get_width() / 2., p.get_height()),
                     ha="center", va="bottom", xytext=(0, 4),
                     textcoords="offset points", fontsize=9, fontweight="bold")
plt.tight_layout()
p5 = os.path.join(output_dir, "chart5_intern_cert.png")
plt.savefig(p5, dpi=150)
plt.close()
print("[✓] chart5_intern_cert.png saved")

# ─────────────────────────────────────────────────────────────────────────────
# EDA DASHBOARD — 6-panel summary
# ─────────────────────────────────────────────────────────────────────────────
fig, axes = plt.subplots(2, 3, figsize=(18, 11))
fig.suptitle(
    "HiGen Labs — BBA/MBA Student EDA Dashboard\n"
    "Samaksh Kori | Hansraj College, University of Delhi",
    fontsize=14, fontweight="bold", y=1.01
)

# Panel 1: Degree pie
deg_c = df["Degree"].value_counts()
axes[0, 0].pie(deg_c.values, labels=deg_c.index, autopct="%1.1f%%",
               colors=[NAVY, TEAL], startangle=90)
axes[0, 0].set_title("MBA vs BBA Split")

# Panel 2: Top skills
axes[0, 1].barh(top_skills.index[::-1], top_skills.values[::-1], color=TEAL)
axes[0, 1].set_title("Top 10 Skills")
axes[0, 1].set_xlabel("Count")
for i, v in enumerate(top_skills.values[::-1]):
    axes[0, 1].text(v + 1, i, str(v), va="center", fontsize=8)

# Panel 3: Top specializations
top_spec = df["Specialization"].value_counts().head(6)
axes[0, 2].barh(top_spec.index[::-1], top_spec.values[::-1], color=NAVY)
axes[0, 2].set_title("Top 6 Specializations")
axes[0, 2].set_xlabel("Count")

# Panel 4: Grad year line
axes[1, 0].plot(grad_plot.index, grad_plot.values,
                marker="o", color=RED, linewidth=2.5)
axes[1, 0].fill_between(grad_plot.index, grad_plot.values,
                         alpha=0.15, color=RED)
axes[1, 0].set_title("Graduation Year Trend")
axes[1, 0].set_xlabel("Year")
axes[1, 0].set_ylabel("Count")
for i, (x, y) in enumerate(zip(grad_plot.index, grad_plot.values)):
    axes[1, 0].text(i, y + 3, str(y), ha="center",
                    fontsize=9, fontweight="bold")

# Panel 5: Top cities bar
top_c = df["Location"].value_counts().head(8)
sns.barplot(ax=axes[1, 1], x=top_c.values, y=top_c.index, palette="Blues_r")
axes[1, 1].set_title("Top 8 Cities")
axes[1, 1].set_xlabel("Students")

# Panel 6: Specialization × Degree grouped bar
spec_deg = df[df["Specialization"].isin(spec.head(5).index)].groupby(
    ["Specialization", "Degree"]).size().unstack(fill_value=0)
spec_deg.plot(kind="bar", ax=axes[1, 2],
              color=[NAVY, TEAL], edgecolor="white")
axes[1, 2].set_title("Specialization by Degree")
axes[1, 2].set_xlabel("")
axes[1, 2].tick_params(axis="x", rotation=25)
axes[1, 2].legend(title="Degree")

plt.tight_layout()
dash = os.path.join(output_dir, "eda_dashboard.png")
plt.savefig(dash, dpi=150, bbox_inches="tight")
plt.close()
print("[✓] eda_dashboard.png saved")

# ─────────────────────────────────────────────────────────────────────────────
# DONE — show popup confirmation
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 65)
print("  All charts and EDA complete!")
print(f"  Files saved in: {output_dir}")
print("    chart1_skills.png")
print("    chart2_specialization.png")
print("    chart3_cities.png")
print("    chart4_gradyear.png")
print("    chart5_intern_cert.png")
print("    eda_dashboard.png")
print("=" * 65)

root = Tk()
root.withdraw()
messagebox.showinfo(
    "Done!",
    f"All 6 charts saved successfully in:\n{output_dir}\n\n"
    "chart1_skills.png\n"
    "chart2_specialization.png\n"
    "chart3_cities.png\n"
    "chart4_gradyear.png\n"
    "chart5_intern_cert.png\n"
    "eda_dashboard.png"
)
root.destroy()