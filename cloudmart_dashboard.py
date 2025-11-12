import io

import pandas as pd
import plotly.express as px
import streamlit as st

# Page configuration
st.set_page_config(page_title="CloudMart Resource Tagging Dashboard", layout="wide")

st.title("CloudMart Resource Tagging & Cost Governance Dashboard")
st.markdown("### Week 10 Activity - Data Exploration")
st.markdown("---")


# Load dataset function
@st.cache_data
def load_data():
    # Read file and handle the quoted CSV format
    # Use relative path so it works on any system
    try:
        with open("cloudmart_multi_account.csv", "r") as f:
            content = f.read()
            lines = content.strip().split("\n")
            cleaned_lines = [line.strip('"') for line in lines]
            cleaned_content = "\n".join(cleaned_lines)

        df = pd.read_csv(io.StringIO(cleaned_content))
        df = df.replace("", pd.NA)
        return df
    except FileNotFoundError:
        st.error(
            "❌ Error: 'cloudmart_multi_account.csv' file not found. Please ensure the CSV file is in the same directory as this script."
        )
        st.stop()


df = load_data()

# ============================================================================
# TASK SET 1 - DATA EXPLORATION
# ============================================================================

st.header("Task Set 1 - Data Exploration")

# Task 1.1: Load the dataset and display the first 5 rows
st.subheader("Task 1.1: Load the dataset and display the first 5 rows")
st.write("**Hint:** Use pd.read_csv() or upload via Streamlit")
st.dataframe(df.head())
st.success(
    f"✓ Dataset loaded successfully with {len(df)} rows and {len(df.columns)} columns"
)

st.markdown("---")

# Task 1.2: Check for missing values in the dataset
st.subheader("Task 1.2: Check for missing values in the dataset")
st.write("**Hint:** df.isnull().sum()")
missing_values = df.isnull().sum()
st.write("Missing values per column:")
st.dataframe(missing_values)

st.markdown("---")

# Task 1.3: Identify which columns have the most missing values
st.subheader("Task 1.3: Identify which columns have the most missing values")
st.write("**Hint:** Look for Department, Project, or Owner")
missing_sorted = missing_values[missing_values > 0].sort_values(ascending=False)
st.write("Columns with missing values (sorted by count):")
st.dataframe(missing_sorted)
st.info(f"Columns with most missing values: {', '.join(missing_sorted.index.tolist())}")

st.markdown("---")

# Task 1.4: Count total resources and how many are tagged vs untagged
st.subheader("Task 1.4: Count total resources and how many are tagged vs untagged")
st.write("**Hint:** Use df['Tagged'].value_counts()")
tagged_counts = df["Tagged"].value_counts()
st.write("Tagged vs Untagged count:")
st.dataframe(tagged_counts)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Resources", len(df))
with col2:
    st.metric("Tagged (Yes)", tagged_counts.get("Yes", 0))
with col3:
    st.metric("Untagged (No)", tagged_counts.get("No", 0))

st.markdown("---")

# Task 1.5: What percentage of resources are untagged?
st.subheader("Task 1.5: What percentage of resources are untagged?")
st.write("**Hint:** Compute (untagged / total) * 100")

total = len(df)
untagged = tagged_counts.get("No", 0)
percentage_untagged = (untagged / total) * 100

st.write(f"**Calculation:** ({untagged} / {total}) * 100 = {percentage_untagged:.2f}%")
st.metric("Percentage of Untagged Resources", f"{percentage_untagged:.2f}%")

st.markdown("---")

# ============================================================================
# TASK SET 2 - COST VISIBILITY
# ============================================================================

st.header("Task Set 2 - Cost Visibility")

# Task 2.1: Calculate total cost of tagged vs untagged resources
st.subheader("Task 2.1: Calculate total cost of tagged vs untagged resources")
st.write("**Hint:** Group by Tagged and sum MonthlyCostUSD")

cost_by_tagged = df.groupby("Tagged")["MonthlyCostUSD"].sum().reset_index()
st.write("Total cost by tagging status:")
st.dataframe(cost_by_tagged)

col1, col2 = st.columns(2)
with col1:
    tagged_cost = cost_by_tagged[cost_by_tagged["Tagged"] == "Yes"][
        "MonthlyCostUSD"
    ].values
    st.metric(
        "Tagged Resources Cost",
        f"${tagged_cost[0]:,.2f}" if len(tagged_cost) > 0 else "$0.00",
    )
with col2:
    untagged_cost = cost_by_tagged[cost_by_tagged["Tagged"] == "No"][
        "MonthlyCostUSD"
    ].values
    st.metric(
        "Untagged Resources Cost",
        f"${untagged_cost[0]:,.2f}" if len(untagged_cost) > 0 else "$0.00",
    )

st.markdown("---")

# Task 2.2: Compute the percentage of total cost that is untagged
st.subheader("Task 2.2: Compute the percentage of total cost that is untagged")
st.write("**Hint:** (untagged_cost / total_cost) * 100")

total_cost = df["MonthlyCostUSD"].sum()
untagged_cost_value = untagged_cost[0] if len(untagged_cost) > 0 else 0
percentage_untagged_cost = (untagged_cost_value / total_cost) * 100

st.write(
    f"**Calculation:** (${untagged_cost_value:,.2f} / ${total_cost:,.2f}) * 100 = {percentage_untagged_cost:.2f}%"
)
st.metric("Percentage of Untagged Cost", f"{percentage_untagged_cost:.2f}%")

st.markdown("---")

# Task 2.3: Identify which department has the most untagged cost
st.subheader("Task 2.3: Identify which department has the most untagged cost")
st.write("**Hint:** Group by Department and Tagged")

cost_by_dept_tagged = (
    df.groupby(["Department", "Tagged"])["MonthlyCostUSD"].sum().reset_index()
)
untagged_by_dept = cost_by_dept_tagged[
    cost_by_dept_tagged["Tagged"] == "No"
].sort_values("MonthlyCostUSD", ascending=False)

st.write("Untagged cost by department:")
st.dataframe(untagged_by_dept)

if len(untagged_by_dept) > 0:
    top_dept = untagged_by_dept.iloc[0]
    st.info(
        f"Department with most untagged cost: **{top_dept['Department']}** with ${top_dept['MonthlyCostUSD']:,.2f}"
    )

st.markdown("---")

# Task 2.4: Which project consumes the most cost overall?
st.subheader("Task 2.4: Which project consumes the most cost overall?")
st.write("**Hint:** Use .groupby('Project')['MonthlyCostUSD'].sum()")

cost_by_project = (
    df.groupby("Project")["MonthlyCostUSD"]
    .sum()
    .reset_index()
    .sort_values("MonthlyCostUSD", ascending=False)
)

st.write("Total cost by project (top 10):")
st.dataframe(cost_by_project.head(10))

if len(cost_by_project) > 0:
    top_project = cost_by_project.iloc[0]
    st.metric(
        f"Highest Cost Project: {top_project['Project']}",
        f"${top_project['MonthlyCostUSD']:,.2f}",
    )

st.markdown("---")

# Task 2.5: Compare Prod vs Dev environments in terms of cost and tagging quality
st.subheader(
    "Task 2.5: Compare Prod vs Dev environments in terms of cost and tagging quality"
)
st.write("**Hint:** Group by Environment and Tagged")

cost_by_env_tagged = (
    df.groupby(["Environment", "Tagged"])["MonthlyCostUSD"].sum().reset_index()
)
st.write("Cost by environment and tagging status:")
st.dataframe(cost_by_env_tagged)

# Create a pivot table for better visualization
pivot_env = cost_by_env_tagged.pivot(
    index="Environment", columns="Tagged", values="MonthlyCostUSD"
).fillna(0)
st.write("Cost comparison (Pivot view):")
st.dataframe(pivot_env)

# Calculate tagging percentage per environment
env_summary = (
    df.groupby("Environment")
    .agg({"ResourceID": "count", "MonthlyCostUSD": "sum"})
    .reset_index()
)
env_summary.columns = ["Environment", "Total Resources", "Total Cost"]

tagged_counts_env = (
    df[df["Tagged"] == "Yes"].groupby("Environment")["ResourceID"].count().reset_index()
)
tagged_counts_env.columns = ["Environment", "Tagged Resources"]

env_summary = env_summary.merge(tagged_counts_env, on="Environment", how="left").fillna(
    0
)
env_summary["Tagging %"] = (
    env_summary["Tagged Resources"] / env_summary["Total Resources"] * 100
).round(2)

st.write("Environment summary with tagging percentage:")
st.dataframe(env_summary)

st.markdown("---")

# ============================================================================
# TASK SET 3 - TAGGING COMPLIANCE
# ============================================================================

st.header("Task Set 3 - Tagging Compliance")

# Task 3.1: Create a "Tag Completeness Score" per resource
st.subheader("Task 3.1: Create a 'Tag Completeness Score' per resource")
st.write("**Hint:** Count how many of the tag fields are non-empty")

# Define tag fields to check
tag_fields = ["Department", "Project", "Environment", "Owner", "CostCenter"]

# Create a copy of the dataframe with completeness score
df_with_score = df.copy()

# Count non-null values for each resource across tag fields
df_with_score["Tag_Completeness_Score"] = df_with_score[tag_fields].notna().sum(axis=1)
df_with_score["Tag_Completeness_Percentage"] = (
    df_with_score["Tag_Completeness_Score"] / len(tag_fields) * 100
).round(2)

st.write("Resources with completeness scores (first 10):")
st.dataframe(
    df_with_score[
        ["ResourceID", "Service", "Tagged"]
        + tag_fields
        + ["Tag_Completeness_Score", "Tag_Completeness_Percentage"]
    ].head(10)
)

avg_completeness = df_with_score["Tag_Completeness_Percentage"].mean()
st.metric("Average Tag Completeness", f"{avg_completeness:.2f}%")

st.markdown("---")

# Task 3.2: Find top 5 resources with lowest completeness scores
st.subheader("Task 3.2: Find top 5 resources with lowest completeness scores")
st.write("**Hint:** Sort by the new score column")

lowest_completeness = df_with_score.sort_values("Tag_Completeness_Score").head(5)
st.write("Top 5 resources with lowest completeness scores:")
st.dataframe(
    lowest_completeness[
        [
            "ResourceID",
            "Service",
            "Department",
            "Project",
            "Owner",
            "Tag_Completeness_Score",
            "Tag_Completeness_Percentage",
            "MonthlyCostUSD",
        ]
    ]
)

st.warning(
    f"These 5 resources have the poorest tagging quality with completeness scores ranging from {lowest_completeness['Tag_Completeness_Score'].min()} to {lowest_completeness['Tag_Completeness_Score'].max()} out of {len(tag_fields)}"
)

st.markdown("---")

# Task 3.3: Identify the most frequently missing tag fields
st.subheader("Task 3.3: Identify the most frequently missing tag fields")
st.write("**Hint:** Count missing entries per column")

missing_counts = df[tag_fields].isnull().sum().sort_values(ascending=False)
st.write("Missing tag field counts:")
st.dataframe(missing_counts)

# Create a bar chart for missing fields
fig_missing = px.bar(
    x=missing_counts.index,
    y=missing_counts.values,
    labels={"x": "Tag Field", "y": "Number of Missing Values"},
    title="Missing Tag Fields Frequency",
)
st.plotly_chart(fig_missing, use_container_width=True)

if len(missing_counts) > 0:
    st.info(
        f"Most frequently missing tag field: **{missing_counts.index[0]}** with {missing_counts.values[0]} missing entries"
    )

st.markdown("---")

# Task 3.4: List all untagged resources and their costs
st.subheader("Task 3.4: List all untagged resources and their costs")
st.write("**Hint:** Filter where Tagged == 'No'")

untagged_resources = df[df["Tagged"] == "No"].sort_values(
    "MonthlyCostUSD", ascending=False
)
st.write(f"Total untagged resources: {len(untagged_resources)}")
st.write("Untagged resources (sorted by cost):")
st.dataframe(
    untagged_resources[
        [
            "ResourceID",
            "Service",
            "Region",
            "Department",
            "Project",
            "Environment",
            "MonthlyCostUSD",
        ]
    ]
)

total_untagged_cost = untagged_resources["MonthlyCostUSD"].sum()
st.metric("Total Cost of Untagged Resources", f"${total_untagged_cost:,.2f}")

st.markdown("---")

# Task 3.5: Export untagged resources to a new CSV file
st.subheader("Task 3.5: Export untagged resources to a new CSV file")
st.write("**Hint:** Use df[df['Tagged']=='No'].to_csv('untagged.csv')")

# Save to file
untagged_csv_path = "/Users/winsometang/Downloads/untagged.csv"
untagged_resources.to_csv(untagged_csv_path, index=False)
st.success(f"✓ Untagged resources exported to: {untagged_csv_path}")

# Also provide download button in Streamlit
csv_data = untagged_resources.to_csv(index=False)
st.download_button(
    label="📥 Download Untagged Resources CSV",
    data=csv_data,
    file_name="untagged_resources.csv",
    mime="text/csv",
)

st.info(
    f"Exported {len(untagged_resources)} untagged resources with a total cost of ${total_untagged_cost:,.2f}"
)

st.markdown("---")

# ============================================================================
# TASK SET 4 - VISUALIZATION DASHBOARD
# ============================================================================

st.header("Task Set 4 - Visualization Dashboard")

# Task 4.1: Create a pie chart of tagged vs untagged resources
st.subheader("Task 4.1: Create a pie chart of tagged vs untagged resources")
st.write("**Hint:** Use plotly.express.pie()")

tagged_counts_viz = df["Tagged"].value_counts().reset_index()
tagged_counts_viz.columns = ["Tagged", "Count"]

fig_pie_tagged = px.pie(
    tagged_counts_viz,
    values="Count",
    names="Tagged",
    title="Tagged vs Untagged Resources",
    color="Tagged",
    color_discrete_map={"Yes": "#28a745", "No": "#dc3545"},
)
st.plotly_chart(fig_pie_tagged, use_container_width=True)

st.markdown("---")

# Task 4.2: Plot a bar chart showing cost per department by tagging status
st.subheader("Task 4.2: Plot a bar chart showing cost per department by tagging status")
st.write("**Hint:** Use barmode='group'")

cost_dept_tagged_viz = (
    df.groupby(["Department", "Tagged"])["MonthlyCostUSD"].sum().reset_index()
)

fig_bar_dept = px.bar(
    cost_dept_tagged_viz,
    x="Department",
    y="MonthlyCostUSD",
    color="Tagged",
    title="Cost per Department by Tagging Status",
    barmode="group",
    labels={"MonthlyCostUSD": "Monthly Cost (USD)", "Department": "Department"},
    color_discrete_map={"Yes": "#28a745", "No": "#dc3545"},
)
st.plotly_chart(fig_bar_dept, use_container_width=True)

st.markdown("---")

# Task 4.3: Show a horizontal bar chart of total cost per service
st.subheader("Task 4.3: Show a horizontal bar chart of total cost per service")
st.write("**Hint:** Group by Service")

cost_by_service = (
    df.groupby("Service")["MonthlyCostUSD"]
    .sum()
    .reset_index()
    .sort_values("MonthlyCostUSD", ascending=True)
)

fig_hbar_service = px.bar(
    cost_by_service,
    x="MonthlyCostUSD",
    y="Service",
    orientation="h",
    title="Total Cost per Service",
    labels={"MonthlyCostUSD": "Monthly Cost (USD)", "Service": "Service"},
    color="MonthlyCostUSD",
    color_continuous_scale="Blues",
)
st.plotly_chart(fig_hbar_service, use_container_width=True)

st.markdown("---")

# Task 4.4: Visualize cost by environment (Prod, Dev, Test)
st.subheader("Task 4.4: Visualize cost by environment (Prod, Dev, Test)")
st.write("**Hint:** Pie or bar chart works")

cost_by_env = df.groupby("Environment")["MonthlyCostUSD"].sum().reset_index()

col1, col2 = st.columns(2)

with col1:
    fig_pie_env = px.pie(
        cost_by_env,
        values="MonthlyCostUSD",
        names="Environment",
        title="Cost by Environment (Pie Chart)",
    )
    st.plotly_chart(fig_pie_env, use_container_width=True)

with col2:
    fig_bar_env = px.bar(
        cost_by_env,
        x="Environment",
        y="MonthlyCostUSD",
        title="Cost by Environment (Bar Chart)",
        labels={"MonthlyCostUSD": "Monthly Cost (USD)", "Environment": "Environment"},
        color="Environment",
    )
    st.plotly_chart(fig_bar_env, use_container_width=True)

st.markdown("---")

# Task 4.5: Add interactive filters in Streamlit (Service, Region, Department)
st.subheader(
    "Task 4.5: Add interactive filters in Streamlit (Service, Region, Department)"
)
st.write("**Hint:** Use st.selectbox() or st.multiselect()")

st.write("### Interactive Filtering Dashboard")

# Create filters
col1, col2, col3 = st.columns(3)

with col1:
    service_filter = st.multiselect(
        "Select Service(s)",
        options=["All"] + sorted(df["Service"].dropna().unique().tolist()),
        default=["All"],
    )

with col2:
    region_filter = st.multiselect(
        "Select Region(s)",
        options=["All"] + sorted(df["Region"].dropna().unique().tolist()),
        default=["All"],
    )

with col3:
    department_filter = st.multiselect(
        "Select Department(s)",
        options=["All"] + sorted(df["Department"].dropna().unique().tolist()),
        default=["All"],
    )

# Apply filters
filtered_df = df.copy()

if "All" not in service_filter and len(service_filter) > 0:
    filtered_df = filtered_df[filtered_df["Service"].isin(service_filter)]

if "All" not in region_filter and len(region_filter) > 0:
    filtered_df = filtered_df[filtered_df["Region"].isin(region_filter)]

if "All" not in department_filter and len(department_filter) > 0:
    filtered_df = filtered_df[filtered_df["Department"].isin(department_filter)]

# Display filtered results
st.write(f"**Filtered Results:** {len(filtered_df)} resources out of {len(df)} total")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Cost (Filtered)", f"${filtered_df['MonthlyCostUSD'].sum():,.2f}")
with col2:
    tagged_filtered = len(filtered_df[filtered_df["Tagged"] == "Yes"])
    st.metric("Tagged Resources", tagged_filtered)
with col3:
    untagged_filtered = len(filtered_df[filtered_df["Tagged"] == "No"])
    st.metric("Untagged Resources", untagged_filtered)

# Show filtered data
st.write("### Filtered Data Preview")
st.dataframe(
    filtered_df[
        [
            "ResourceID",
            "Service",
            "Region",
            "Department",
            "Project",
            "Environment",
            "Tagged",
            "MonthlyCostUSD",
        ]
    ].head(20)
)

# Filtered visualizations
st.write("### Filtered Visualizations")

col1, col2 = st.columns(2)

with col1:
    # Filtered tagged vs untagged pie chart
    filtered_tagged_counts = filtered_df["Tagged"].value_counts().reset_index()
    filtered_tagged_counts.columns = ["Tagged", "Count"]

    fig_filtered_pie = px.pie(
        filtered_tagged_counts,
        values="Count",
        names="Tagged",
        title="Filtered: Tagged vs Untagged",
        color="Tagged",
        color_discrete_map={"Yes": "#28a745", "No": "#dc3545"},
    )
    st.plotly_chart(fig_filtered_pie, use_container_width=True)

with col2:
    # Filtered cost by service
    filtered_service_cost = (
        filtered_df.groupby("Service")["MonthlyCostUSD"]
        .sum()
        .reset_index()
        .sort_values("MonthlyCostUSD", ascending=False)
        .head(10)
    )

    fig_filtered_service = px.bar(
        filtered_service_cost,
        x="Service",
        y="MonthlyCostUSD",
        title="Filtered: Top 10 Services by Cost",
        labels={"MonthlyCostUSD": "Monthly Cost (USD)"},
        color="MonthlyCostUSD",
        color_continuous_scale="Viridis",
    )
    st.plotly_chart(fig_filtered_service, use_container_width=True)

st.markdown("---")
# ============================================================================
# TASK SET 5 - TAG REMEDIATION WORKFLOW
# ============================================================================

st.header("Task Set 5 - Tag Remediation Workflow")

# Task 5.1: In Streamlit, create a table where untagged resources can be edited
st.subheader("Task 5.1: Create a table where untagged resources can be edited")
st.write("**Hint:** Use st.data_editor()")

# Get untagged resources for editing
untagged_for_edit = df[df["Tagged"] == "No"].copy().reset_index(drop=True)

st.write(f"**Total Untagged Resources to Edit:** {len(untagged_for_edit)}")
st.info(
    "You can edit the Department, Project, Environment, Owner, and CostCenter fields below. Other fields are read-only."
)

# Task 5.2: Fill missing tags (Department, Project, Owner) manually
st.subheader("Task 5.2: Fill missing tags (Department, Project, Owner) manually")
st.write("**Hint:** Simulate remediation")

st.write("Edit the table below to fill in missing tag information:")

# Use data_editor to allow editing - all columns included as per user's request
edited_df = st.data_editor(
    untagged_for_edit,
    num_rows="fixed",
    disabled=[
        "AccountID",
        "ResourceID",
        "Service",
        "Region",
        "CreatedBy",
        "MonthlyCostUSD",
        "Tagged",
    ],
    use_container_width=True,
    key="untagged_editor",
)

st.markdown("---")

# Task 5.3: Download the updated dataset
st.subheader("Task 5.3: Download the updated dataset")
st.write("**Hint:** Use st.download_button()")

# Mark edited resources as tagged if key fields are filled
edited_df_copy = edited_df.copy()

# Check if key tag fields are filled
edited_df_copy["Tags_Filled"] = (
    edited_df_copy["Department"].notna()
    & edited_df_copy["Project"].notna()
    & edited_df_copy["Owner"].notna()
    & edited_df_copy["CostCenter"].notna()
    & edited_df_copy["Environment"].notna()
)

# Update Tagged status for remediated resources
edited_df_copy.loc[edited_df_copy["Tags_Filled"], "Tagged"] = "Yes"
edited_df_copy = edited_df_copy.drop(columns=["Tags_Filled"])

# Create remediated dataset by combining edited untagged with original tagged resources
originally_tagged = df[df["Tagged"] == "Yes"].copy()
remediated_full_dataset = pd.concat(
    [originally_tagged, edited_df_copy], ignore_index=True
)

st.write("**Remediated Dataset Preview:**")
st.dataframe(remediated_full_dataset.head(10))

# Download buttons for both original and remediated datasets
col1, col2 = st.columns(2)

with col1:
    original_csv = df.to_csv(index=False)
    st.download_button(
        label="📥 Download Original Dataset",
        data=original_csv,
        file_name="original.csv",
        mime="text/csv",
        key="download_original",
    )

with col2:
    remediated_csv = remediated_full_dataset.to_csv(index=False)
    st.download_button(
        label="📥 Download Remediated Dataset",
        data=remediated_csv,
        file_name="remediated.csv",
        mime="text/csv",
        key="download_remediated",
    )

st.success("✓ You can now download both the original and remediated datasets!")

st.markdown("---")

# Task 5.4: Compare cost visibility before and after remediation
st.subheader("Task 5.4: Compare cost visibility before and after remediation")
st.write("**Hint:** Recalculate tagging metrics after updates")

st.write("### Before and After Comparison")

# Before metrics (original dataset)
before_total_resources = len(df)
before_untagged = len(df[df["Tagged"] == "No"])
before_tagged = len(df[df["Tagged"] == "Yes"])
before_untagged_pct = before_untagged / before_total_resources * 100
before_untagged_cost = df[df["Tagged"] == "No"]["MonthlyCostUSD"].sum()
before_total_cost = df["MonthlyCostUSD"].sum()
before_untagged_cost_pct = before_untagged_cost / before_total_cost * 100

# After metrics (remediated dataset)
after_total_resources = len(remediated_full_dataset)
after_untagged = len(remediated_full_dataset[remediated_full_dataset["Tagged"] == "No"])
after_tagged = len(remediated_full_dataset[remediated_full_dataset["Tagged"] == "Yes"])
after_untagged_pct = (
    (after_untagged / after_total_resources * 100) if after_total_resources > 0 else 0
)
after_untagged_cost = remediated_full_dataset[
    remediated_full_dataset["Tagged"] == "No"
]["MonthlyCostUSD"].sum()
after_total_cost = remediated_full_dataset["MonthlyCostUSD"].sum()
after_untagged_cost_pct = (
    (after_untagged_cost / after_total_cost * 100) if after_total_cost > 0 else 0
)

# Display comparison
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Untagged Resources",
        f"{after_untagged}",
        delta=f"{after_untagged - before_untagged}",
        delta_color="inverse",
    )
    st.caption(f"Before: {before_untagged} | After: {after_untagged}")

with col2:
    st.metric(
        "Tagged Resources",
        f"{after_tagged}",
        delta=f"{after_tagged - before_tagged}",
        delta_color="normal",
    )
    st.caption(f"Before: {before_tagged} | After: {after_tagged}")

with col3:
    st.metric(
        "Untagged %",
        f"{after_untagged_pct:.2f}%",
        delta=f"{after_untagged_pct - before_untagged_pct:.2f}%",
        delta_color="inverse",
    )
    st.caption(f"Before: {before_untagged_pct:.2f}% | After: {after_untagged_pct:.2f}%")

st.write("### Cost Visibility Comparison")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Untagged Cost",
        f"${after_untagged_cost:,.2f}",
        delta=f"${after_untagged_cost - before_untagged_cost:,.2f}",
        delta_color="inverse",
    )
    st.caption(f"Before: ${before_untagged_cost:,.2f}")

with col2:
    st.metric(
        "Untagged Cost %",
        f"{after_untagged_cost_pct:.2f}%",
        delta=f"{after_untagged_cost_pct - before_untagged_cost_pct:.2f}%",
        delta_color="inverse",
    )
    st.caption(f"Before: {before_untagged_cost_pct:.2f}%")

with col3:
    improvement = before_untagged_pct - after_untagged_pct
    st.metric(
        "Improvement",
        f"{improvement:.2f}%",
        delta=f"{improvement:.2f}%",
        delta_color="normal",
    )
    st.caption("Reduction in untagged resources")

# Visualization comparison
st.write("### Visual Comparison")

comparison_data = pd.DataFrame(
    {
        "Status": ["Before", "After"],
        "Tagged": [before_tagged, after_tagged],
        "Untagged": [before_untagged, after_untagged],
    }
)

fig_comparison = px.bar(
    comparison_data,
    x="Status",
    y=["Tagged", "Untagged"],
    title="Before vs After Remediation",
    barmode="group",
    labels={"value": "Number of Resources", "variable": "Tagging Status"},
    color_discrete_map={"Tagged": "#28a745", "Untagged": "#dc3545"},
)
st.plotly_chart(fig_comparison, use_container_width=True)

st.markdown("---")

# Task 5.5: Discuss how improved tagging affects accountability and reports
st.subheader(
    "Task 5.5: Discuss how improved tagging affects accountability and reports"
)
st.write("**Hint:** Write a short reflection")

st.write("### Impact of Improved Tagging on Accountability and Reports")

st.markdown(
    """
#### Key Benefits of Tag Remediation:

**1. Enhanced Cost Accountability**
- Improved tagging enables accurate cost allocation to specific departments, projects, and teams
- Finance teams can track spending more precisely and hold departments accountable for their cloud usage
- Budget owners can see exactly where their money is going

**2. Better Financial Reporting**
- Complete tags allow for detailed cost breakdowns in reports
- Executives can make informed decisions based on accurate cost visibility
- Trend analysis becomes more reliable when resources are properly categorized

**3. Improved Governance and Compliance**
- Tag compliance ensures organizational policies are followed
- Easier to identify resource owners for security and compliance audits
- Reduces "orphaned" resources that nobody claims ownership of

**4. Optimized Resource Management**
- Teams can identify underutilized resources within their projects
- Easier to implement cost optimization strategies when resources are properly tagged
- Facilitates cleanup of unused or unnecessary resources

**5. Better Operational Efficiency**
- Automated policies can be applied based on tags (e.g., auto-shutdown for Dev resources)
- Faster incident response when resource owners are clearly identified
- Simplified resource lifecycle management

#### Recommendations for Maintaining Tag Compliance:

1. **Implement automated tagging** at resource creation time using Infrastructure as Code (Terraform, CloudFormation)
2. **Set up tag policies** that require specific tags before resources can be created
3. **Regular audits** using dashboards like this one to identify and remediate untagged resources
4. **Training and documentation** to ensure all teams understand tagging requirements
5. **Cost allocation reports** that highlight departments with poor tagging compliance
6. **Gamification** - reward teams with high tag compliance rates

#### Conclusion:

The remediation process demonstrated in this dashboard shows tangible improvements in cost visibility and accountability.
By reducing untagged resources from **{:.2f}%** to **{:.2f}%**, the organization gains better control over its cloud spending
and can make more informed financial decisions. Maintaining this level of tag compliance should be an ongoing priority.
""".format(before_untagged_pct, after_untagged_pct)
)

st.markdown("---")
