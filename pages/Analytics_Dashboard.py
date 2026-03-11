import streamlit as st
import pandas as pd
import altair as alt

# Load Data
# ---------------------------------------------------------
@st.cache_data
def load_data():
    poses = pd.read_csv("data/poses.csv")
    therapy = pd.read_csv("data/therapy_map.csv")
    props = pd.read_csv("data/props.csv")
    return poses, therapy, props

poses, therapy, props = load_data()

st.title("📊 Yoga Therapy Analytics Dashboard")

st.write(
    "This dashboard gives an overview of pose distribution, difficulty levels, "
    "props usage, and therapeutic condition frequency."
)


# Pose Distribution by Category
# -------------------------------------
st.subheader("🧘 Pose Distribution by Category")

category_chart = (
    alt.Chart(poses)
    .mark_bar(color="#6C63FF")
    .encode(
        x=alt.X("category:N", title="Category"),
        y=alt.Y("count():Q", title="Number of Poses"),
        tooltip=["category", "count()"]
    )
)

st.altair_chart(category_chart, use_container_width=True)


# Difficulty Level Distribution
# ----------------------------------
st.subheader("📈 Difficulty Level Distribution")

level_chart = (
    alt.Chart(poses)
    .mark_bar(color="#00A676")
    .encode(
        x=alt.X("level:N", title="Difficulty Level"),
        y=alt.Y("count():Q", title="Number of Poses"),
        tooltip=["level", "count()"]
    )
)

st.altair_chart(level_chart, use_container_width=True)


# Props Usage Frequency
# ----------------------------------
st.subheader("🧰 Props Usage Frequency")

if "prop" in props.columns:
    props_chart = (
        alt.Chart(props)
        .mark_bar(color="#FF6F61")
        .encode(
            x=alt.X("prop:N", title="Prop"),
            y=alt.Y("count():Q", title="Usage Count"),
            tooltip=["prop", "count()"]
        )
    )
    st.altair_chart(props_chart, use_container_width=True)
else:
    st.info("Props file does not contain a 'prop' column.")

# ---------------------------------------------------------
# Therapy Condition Frequency
# ---------------------------------------------------------
st.subheader("❤️ Therapy Condition Frequency")

therapy_chart = (
    alt.Chart(therapy)
    .mark_bar(color="#F4A261")
    .encode(
        x=alt.X("therapy_condition:N", title="Therapy Condition"),
        y=alt.Y("count():Q", title="Number of Poses"),
        tooltip=["therapy_condition", "count()"]
    )
)

st.altair_chart(therapy_chart, use_container_width=True)

# ---------------------------------------------------------
# Heatmap: Therapy Condition vs Category
# ---------------------------------------------------------
st.subheader("🔥 Therapy Condition × Category Heatmap")

merged = therapy.merge(poses, left_on="pose_id", right_on="id")

heatmap = (
    alt.Chart(merged)
    .mark_rect()
    .encode(
        x=alt.X("category:N", title="Category"),
        y=alt.Y("therapy_condition:N", title="Therapy Condition"),
        color=alt.Color("count():Q", scale=alt.Scale(scheme="viridis")),
        tooltip=["category", "therapy_condition", "count()"]
    )
)

st.altair_chart(heatmap, use_container_width=True)
