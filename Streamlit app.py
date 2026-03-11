import streamlit as st
import pandas as pd
import os

# Set Page Config 
st.set_page_config(page_title="Yoga with Sindhu", page_icon="🧘", layout="wide")

# Custom CSS for ui
st.markdown("""
    <style>
    .main { border-radius: 10px; }
    .stMetric { background-color: #f0f2f6; padding: 10px; border-radius: 10px; }
    .st-expander { border: none !important; box-shadow: none !important; }
    /* Custom Card Style */
    .pose-card {
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #6D8299;
        background-color: #ffffff;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🧘 Yoga with Sindhu")
with st.sidebar:
    # Custom CSS for a clean profile card
    st.markdown("""
        <div style="text-align: center; padding: 10px; border: 1px solid #ddd; border-radius: 10px; margin-bottom: 20px;">
            <img src="https://www.yogaalliance.org/Portals/0/Images/Logos/YA_MainLogo_Color.png" width="100">
            <h3 style="margin: 10px 0 5px 0;">Sindhu</h3>
            <p style="color: gray; font-size: 0.9em;">Registered Yoga Teacher (RYT®)</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.header("✨ Refine Practice")
    # ... rest of your filters ...

# --- Navigation ---
# (Assuming utils.navigation exists)
# from utils.navigation import navigation_header
# navigation_header()

# --- Data Loading (Kept your logic) ---
@st.cache_data
def load_data():
    # Placeholder for your CSV loading logic
    # poses, variations, therapy, contra, props, bio, seq = ...
    return poses, variations, therapy, contra, props, bio, seq

# --- Sidebar Filters (Grouping with Expanders) ---
with st.sidebar:
    st.header("✨ Refine Practice")
    
    with st.expander("🎯 Primary Filters", expanded=True):
        category_filter = st.selectbox("Category", ["All"] + sorted(poses["category"].unique()))
        level_filter = st.selectbox("Difficulty Level", ["All"] + sorted(poses["level"].unique()))
        therapy_filter = st.selectbox("Therapeutic Need", ["None"] + sorted(therapy["therapy_condition"].unique()))

    with st.expander("🛠️ Anatomy & Equipment"):
        props_filter = st.multiselect("Props Needed", sorted(props["prop"].dropna().unique()))
        muscle_filter = st.multiselect("Muscles Activated", sorted(bio["muscles_activated"].dropna().unique()))
    
    # Theme Selection
    theme = st.selectbox("🎨 App Theme", ["Light", "Calm Blue", "Earth Brown", "Forest Green"])

# (Insert your Filter Logic here - same as your original code)

# --- Main Interface ---
st.subheader("Explore Poses")

if len(filtered) == 0:
    st.warning("No poses match your filters. Try broadening your search!")
else:
    # Use a cleaner selection box
    selected_pose_name = st.selectbox("Select a Pose to deepen your practice:", filtered["english_name"].tolist())
    pose = poses[poses["english_name"] == selected_pose_name].iloc[0]

    # --- Pose Detail Layout ---
    col1, col2 = st.columns([1, 1.5], gap="large")

    with col1:
        image_path = os.path.join("images", pose["image_path"])
        if os.path.exists(image_path):
            st.image(image_path, use_container_width=True, caption=pose['sanskrit_name'])
        else:
            st.info("📷 Image preview coming soon.")
            
        # Quick Stats under image
        c1, c2 = st.columns(2)
        c1.metric("Level", pose['level'])
        c2.metric("Category", pose['category'])

    with col2:
        st.header(f"{pose['english_name']}")
        st.subheader(f"*{pose['sanskrit_name']}*")
        st.write(pose["description"])
        
        # Using Tabs to organize dense information
        tab1, tab2, tab3, tab4 = st.tabs(["💡 Benefits & Anatomy", "🛠️ Practice & Props", "⚠️ Safety", "🔄 Flow"])

        with tab1:
            st.markdown("#### Biomechanics")
            bio_row = bio[bio["pose_id"] == pose["id"]].iloc[0] if not bio[bio["pose_id"] == pose["id"]].empty else None
            if bio_row is not None:
                st.write(f"**Muscles:** {bio_row['muscles_activated']}")
                st.write(f"**Focus:** {bio_row['joint_actions']}")
            
            st.markdown("#### Therapeutic Uses")
            pose_therapy = therapy[therapy["pose_id"] == pose["id"]]
            st.write(", ".join(pose_therapy["therapy_condition"].tolist()) if not pose_therapy.empty else "General wellness")

        with tab2:
            st.markdown("#### Props & Modifications")
            pose_props = props[props["pose_id"] == pose["id"]]
            if not pose_props.empty:
                st.dataframe(pose_props[["prop", "usage"]], use_container_width=True, hide_index=True)
            
            st.markdown("#### Variations")
            pose_vars = variations[variations["pose_id"] == pose["id"]]
            if not pose_vars.empty:
                st.table(pose_vars[["variation_type", "description"]])

        with tab3:
            st.markdown("#### Contraindications")
            pose_contra = contra[contra["pose_id"] == pose["id"]]
            if not pose_contra.empty:
                for item in pose_contra["contraindication"]:
                    st.error(f"**Be careful if:** {item}")
            else:
                st.success("No specific contraindications listed. Always listen to your body.")

        with tab4:
            st.markdown("#### Sequencing")
            pose_seq = seq[seq["pose_id"] == pose["id"]]
            if not pose_seq.empty:
                seq_row = pose_seq.iloc[0]
                st.write(f"🟢 **Prep with:** {seq_row['prep_pose']}")
                st.write(f"🔵 **Counter with:** {seq_row['counter_pose']}")

# --- Visualizations Section ---
st.divider()
with st.expander("📊 Practice Insights & Data"):
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        st.write("**Pose Categories**")
        st.bar_chart(poses["category"].value_counts())
    with col_v2:
        st.write("**Difficulty Distribution**")
        st.bar_chart(poses["level"].value_counts())
