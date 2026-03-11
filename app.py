import streamlit as st
import pandas as pd
import os

# --- Page Config ---
st.set_page_config(page_title="Yoga Everyday", page_icon="🧘", layout="wide")

# --- Custom Styling ---
st.markdown("""
    <style>
    .stApp { background-color: #fcfaf8; }
    .main { border-radius: 10px; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 12px; border: 1px solid #e6e9ef; }
    .pose-header { color: #2c3e50; font-family: 'Helvetica Neue', sans-serif; }
    </style>
""", unsafe_allow_html=True)

# --- Data Loading (Cached) ---
@st.cache_data
def load_data():
    # Helper to load CSV or return empty DF if missing
    def read_df(name):
        path = f"data/{name}.csv"
        return pd.read_csv(path) if os.path.exists(path) else pd.DataFrame()

    return (
        read_df("poses"), read_df("variations"), read_df("therapy_map"),
        read_df("contraindications"), read_df("props"), read_df("biomechanics"),
        read_df("sequencing")
    )

poses, variations, therapy, contra, props, bio, seq = load_data()

# --- Sidebar & Navigation ---
from utils.navigation import navigation_header
navigation_header()

st.sidebar.header("✨ Refine Practice")

# --- Filter Sidebar Logic ---
with st.sidebar:
    category_filter = st.selectbox("Category", ["All"] + sorted(poses["category"].unique().tolist()))
    level_filter = st.selectbox("Difficulty Level", ["All"] + sorted(poses["level"].unique().tolist()))
    
    with st.expander("🛠️ Anatomy & Therapy"):
        therapy_filter = st.selectbox("Therapeutic Need", ["None"] + sorted(therapy["therapy_condition"].unique().tolist()))
        
        # Check if bio data exists before filtering
        joint_list = sorted(bio["joint_actions"].dropna().unique().tolist()) if not bio.empty else []
        muscle_list = sorted(bio["muscles_activated"].dropna().unique().tolist()) if not bio.empty else []
        
        joint_filter = st.multiselect("Joint Actions", joint_list)
        muscle_filter = st.multiselect("Muscles Activated", muscle_list)

    show_stats = st.checkbox("📊 Show Practice Insights")

# --- Filter Logic ---
filtered = poses.copy()

if category_filter != "All":
    filtered = filtered[filtered["category"] == category_filter]

if level_filter != "All":
    filtered = filtered[filtered["level"] == level_filter]

if therapy_filter != "None":
    valid_ids = therapy[therapy["therapy_condition"] == therapy_filter]["pose_id"]
    filtered = filtered[filtered["id"].isin(valid_ids)]

if joint_filter:
    valid_ids = bio[bio["joint_actions"].isin(joint_filter)]["pose_id"]
    filtered = filtered[filtered["id"].isin(valid_ids)]

if muscle_filter:
    valid_ids = bio[bio["muscles_activated"].isin(muscle_filter)]["pose_id"]
    filtered = filtered[filtered["id"].isin(valid_ids)]

# --- Main UI ---
st.title("🧘 Yoga Everyday")

if filtered.empty:
    st.warning("No poses match your current filters. Try broadening your search!")
else:
    # Pose Selection
    pose_names = sorted(filtered["english_name"].tolist())
    selected_pose_name = st.selectbox("Select a Pose to deepen your practice:", pose_names)
    
    # Get details for the selected pose
    pose = filtered[filtered["english_name"] == selected_pose_name].iloc[0]
    pose_id = pose["id"]

    # Layout: Image and Quick Info
    col1, col2 = st.columns([1, 1.5], gap="large")

    with col1:
        img_filename = pose.get("image_path", f"{pose_id}.jpg")
        image_path = os.path.join("images", img_filename)
        
        if os.path.exists(image_path):
            st.image(image_path, use_container_width=True)
        else:
            st.info("📷 Image preview coming soon.")
        
        # Key Metrics
        m1, m2 = st.columns(2)
        m1.metric("Level", pose['level'])
        m2.metric("Category", pose['category'])

    with col2:
        st.markdown(f"<h1 class='pose-header'>{pose['english_name']}</h1>", unsafe_allow_html=True)
        st.markdown(f"*{pose['sanskrit_name']}*")
        st.write(pose["description"])
        
        # Tabs for deep-dive info
        tab1, tab2, tab3, tab4 = st.tabs(["🛠️ Practice", "⚠️ Safety", "🔄 Flow", "💡 Anatomy"])

        with tab1:
            st.subheader("Props & Modifications")
            pose_props = props[props["pose_id"] == pose_id]
            if not pose_props.empty:
                st.table(pose_props[["prop", "usage"]])
            
            st.subheader("Variations")
            pose_vars = variations[variations["pose_id"] == pose_id]
            if not pose_vars.empty:
                for _, row in pose_vars.iterrows():
                    st.markdown(f"**{row['variation_type']}**: {row['description']}")

        with tab2:
            st.subheader("Contraindications")
            pose_contra = contra[contra["pose_id"] == pose_id]
            if not pose_contra.empty:
                for item in pose_contra["contraindication"]:
                    st.error(item)
            else:
                st.success("No specific contraindications listed. Listen to your body!")

        with tab3:
            st.subheader("Smart Sequencing")
            pose_seq = seq[seq["pose_id"] == pose_id]
            if not pose_seq.empty:
                s = pose_seq.iloc[0]
                st.info(f"🟢 **Prep Poses:** {s['prep_pose']}")
                st.warning(f"🔵 **Counter Poses:** {s['counter_pose']}")

        with tab4:
            st.subheader("Biomechanics")
            pose_bio = bio[bio["pose_id"] == pose_id]
            if not pose_bio.empty:
                b = pose_bio.iloc[0]
                st.write(f"**Muscles Activated:** {b['muscles_activated']}")
                st.write(f"**Primary Action:** {b['joint_actions']}")
            
            st.subheader("Therapeutic Focus")
            pose_ther = therapy[therapy["pose_id"] == pose_id]
            if not pose_ther.empty:
                st.write(", ".join(pose_ther["therapy_condition"].unique()))

# --- Global Visualizations ---
if show_stats:
    st.divider()
    st.header("📊 Practice Insights")
    v_col1, v_col2 = st.columns(2)
    
    with v_col1:
        st.write("**Pose Categories**")
        st.bar_chart(poses["category"].value_counts())
    
    with v_col2:
        st.write("**Difficulty Levels**")
        st.bar_chart(poses["level"].value_counts())
