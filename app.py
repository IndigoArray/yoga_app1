import streamlit as st
import pandas as pd

st.title("🧘 Yoga Therapy Pose Explorer")

# Sidebar filters
st.sidebar.header("Filters")

categories = ["All"] + sorted(poses["category"].unique().tolist())
levels = ["All"] + sorted(poses["level"].unique().tolist())
therapy_conditions = ["All"] + sorted(therapy["therapy_condition"].unique().tolist())

selected_category = st.sidebar.selectbox("Category", categories)
selected_level = st.sidebar.selectbox("Level", levels)
selected_therapy = st.sidebar.selectbox("Therapy Condition", therapy_conditions)

filtered = poses.copy()

if selected_category != "All":
    filtered = filtered[filtered["category"] == selected_category]

if selected_level != "All":
    filtered = filtered[filtered["level"] == selected_level]

if selected_therapy != "All":
    pose_ids_for_therapy = therapy[therapy["therapy_condition"] == selected_therapy]["pose_id"].unique()
    filtered = filtered[filtered["id"].isin(pose_ids_for_therapy)]

st.subheader("Filtered Poses")
st.dataframe(filtered[["id", "english_name", "sanskrit_name", "category", "level"]])

# Pose viewer
st.subheader("Pose Details")

pose_options = filtered["english_name"].tolist()
if pose_options:
    selected_pose_name = st.selectbox("Select a pose", pose_options)
    pose = poses[poses["english_name"] == selected_pose_name].iloc[0]
    
    st.markdown(f"### {pose['english_name']} ({pose['sanskrit_name']})")
    st.write(f"**Category:** {pose['category']}")
    st.write(f"**Level:** {pose['level']}")
    st.write(f"**Description:** {pose['description']}")

    # Biomechanics
    bm = biomechanics[biomechanics["pose_id"] == pose["id"]]
    if not bm.empty:
        bm = bm.iloc[0]
        st.markdown("#### Biomechanics")
        st.write(f"**Joint actions:** {bm['joint_actions']}")
        st.write(f"**Muscles activated:** {bm['muscles_activated']}")
        st.write(f"**Muscles stretched:** {bm['muscles_stretched']}")
        st.write(f"**Planes of movement:** {bm['planes_of_movement']}")

    # Therapy uses
    st.markdown("#### Therapy Uses")
    pose_therapy = therapy[therapy["pose_id"] == pose["id"]]["therapy_condition"].tolist()
    if pose_therapy:
        st.write(", ".join(pose_therapy))
    else:
        st.write("No therapy mappings yet.")

    # Contraindications
    st.markdown("#### Contraindications")
    pose_contras = contraindications[contraindications["pose_id"] == pose["id"]]["contraindication"].tolist()
    if pose_contras:
        st.write(", ".join(pose_contras))
    else:
        st.write("None listed.")

    # Variations
    st.markdown("#### Variations")
    pose_vars = variations[variations["pose_id"] == pose["id"]]
    if not pose_vars.empty:
        for _, row in pose_vars.iterrows():
            st.write(f"- **{row['variation_type']}:** {row['description']}")
    else:
        st.write("No variations listed.")

    # Props
    st.markdown("#### Props")
    pose_props = props[props["pose_id"] == pose["id"]]
    if not pose_props.empty:
        for _, row in pose_props.iterrows():
            st.write(f"- **{row['prop']}:** {row['usage']}")
    else:
        st.write("No props listed.")

    # Sequencing
    st.markdown("#### Sequencing")
    pose_seq = sequencing[sequencing["pose_id"] == pose["id"]]
    if not pose_seq.empty:
        for _, row in pose_seq.iterrows():
            st.write(f"- **Prep pose:** {row['prep_pose']} | **Counter pose:** {row['counter_pose']}")
    else:
        st.write("No sequencing info yet.")
else:
    st.info("No poses match the current filters.")
