import streamlit as st
import pandas as pd
import os

#  Page Config 
st.set_page_config(page_title="Yoga Everyday", page_icon="🧘", layout="wide")

# css 
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

st.title("🧘 Yoga Everyday")


#----------------------Navigation
from utils.navigation import navigation_header

navigation_header()



# ---------------------------------------------------------
# Load CSV files
# ---------------------------------------------------------
@st.cache_data
def load_data():
    poses = pd.read_csv("data/poses.csv")
    variations = pd.read_csv("data/variations.csv")
    therapy = pd.read_csv("data/therapy_map.csv")
    contra = pd.read_csv("data/contraindications.csv")
    props = pd.read_csv("data/props.csv")
    bio = pd.read_csv("data/biomechanics.csv")
    seq = pd.read_csv("data/sequencing.csv")
    return poses, variations, therapy, contra, props, bio, seq
    
poses, variations, therapy, contra, props, bio, seq = load_data()



# ------------------------------
# Sidebar Filters
# ------------------------------
with st.sidebar:
     st.header("✨ Refine Practice")
with st.expander("🎯 Primary Filters", expanded=True):

    st.header("✨ Refine Practice")
    category_filter = st.sidebar.selectbox(
        "Category",
        ["All"] + sorted(poses["category"].unique())
    )
    
    level_filter = st.sidebar.selectbox(
        "Difficulty Level",
        ["All"] + sorted(poses["level"].unique())
    )
    
    props_filter = st.sidebar.multiselect(
        "Props Needed",
        sorted(props["prop"].dropna().unique())
    )
#therapy
#---------------------------------------------------------------
with st.expander("🛠️ Anatomy & Therapy"):

    therapy_filter = st.sidebar.selectbox(
    "Therapeutic Need",
    ["None"] + sorted(therapy["therapy_condition"].unique())
    )
    joint_filter = st.sidebar.multiselect(
        "Joint Actions",
        sorted(bio["joint_actions"].dropna().unique())
    )

    muscle_filter = st.sidebar.multiselect(
        "Muscles Activated",
        sorted(bio["muscles_activated"].dropna().unique())
    )

    plane_filter = st.sidebar.multiselect(
        "Planes of Movement",
        sorted(bio["planes_of_movement"].dropna().unique())
    )

#theme---
    theme = st.selectbox("🎨 App Theme", ["Light", "Calm Blue", "Earth Brown", "Forest Green"])
# ---------------------------------------------------------
# Filter Logic
# ---------------------------------------------------------
filtered = poses.copy()

if category_filter != "All":
    filtered = filtered[filtered["category"] == category_filter]

if level_filter != "All":
    filtered = filtered[filtered["level"] == level_filter]


#---------------------------------------------------------------------------------
# Props filter
if props_filter:
    pose_ids = props[props["prop"].isin(props_filter)]["pose_id"]
    filtered = filtered[filtered["id"].isin(pose_ids)]

if therapy_filter != "None":
    pose_ids = therapy[therapy["therapy_condition"] == therapy_filter]["pose_id"]
    filtered = filtered[filtered["id"].isin(pose_ids)]
    
# Joint actions filter
if joint_filter:
    pose_ids = bio[bio["joint_actions"].isin(joint_filter)]["pose_id"]
    filtered = filtered[filtered["id"].isin(pose_ids)]

# Muscles activated filter
if muscle_filter:
    pose_ids = bio[bio["muscles_activated"].isin(muscle_filter)]["pose_id"]
    filtered = filtered[filtered["id"].isin(pose_ids)]

# Planes of movement filter
if plane_filter:
    pose_ids = bio[bio["planes_of_movement"].isin(plane_filter)]["pose_id"]
    filtered = filtered[filtered["id"].isin(pose_ids)]


    
# ---------------------------------------------------------
# Pose Selection
# ---------------------------------------------------------
st.subheader("🧘 Explore Poses")

if len(pose_names) == 0:
    st.warning("No poses match your filters.Try broadening your search!")
else:
    selected_pose = st.selectbox("Select a Pose to deepen your practice:", pose_names)

    pose = poses[poses["english_name"] == selected_pose].iloc[0]

    # ---------------------------------------------------------
    # Display Pose Information
    # ---------------------------------------------------------

    # Create columns with gap and ratio 1:1.5

    col1, col2 = st.columns([1, 1.5], gap="large")
# Handle the image path
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
        st.title(f"{pose['english_name']} | {pose['sanskrit_name']}")
        st.write(pose["description"])
        # Using an 'info' box for metadata keeps it visually separated from the description
        st.info(f"**Level:** {pose['level']}  |  **Category:** {pose['category']}")
        
        # Using Tabs to organize dense information
        tab1, tab2, tab3, tab4 = st.tabs(["🛠️ Practice & Props", "⚠️ Safety", "🔄 Flow","💡 Benefits & Anatomy"])

    with tab1:
            st.markdown("#### Props & Modifications")
            pose_props = props[props["pose_id"] == pose["id"]]
            if not pose_props.empty:
                st.dataframe(pose_props[["prop", "usage"]], use_container_width=True, hide_index=True)
            
            st.markdown("#### Variations")
            pose_vars = variations[variations["pose_id"] == pose["id"]]
            if not pose_vars.empty:
                st.table(pose_vars[["variation_type", "description"]])
                
            

    with tab2:
            st.markdown("#### Contraindications")
            pose_contra = contra[contra["pose_id"] == pose["id"]]
            if not pose_contra.empty:
                for item in pose_contra["contraindication"]:
                    st.error(f"**Be careful if:** {item}")
            else:
                st.success("No specific contraindications listed. Always listen to your body.")


    with tab3:
            st.markdown("#### Sequencing")
            pose_seq = seq[seq["pose_id"] == pose["id"]]
            if not pose_seq.empty:
                seq_row = pose_seq.iloc[0]
                st.write(f"🟢 **Prep with:** {seq_row['prep_pose']}")
                st.write(f"🔵 **Counter with:** {seq_row['counter_pose']}")
                
    with tab4:

            st.markdown("#### Biomechanics")
            bio_row = bio[bio["pose_id"] == pose["id"]].iloc[0] if not bio[bio["pose_id"] == pose["id"]].empty else None
            if bio_row is not None:
                st.write(f"**Muscles:** {bio_row['muscles_activated']}")
                st.write(f"**Focus:** {bio_row['joint_actions']}")
            
            st.markdown("#### Therapeutic Uses")
            pose_therapy = therapy[therapy["pose_id"] == pose["id"]]
            st.write(", ".join(pose_therapy["therapy_condition"].tolist()) if not pose_therapy.empty else "General wellness")

#visualization
st.divider()
with st.expander("📊 Practice Insights & Data"):
     col_v1, col_v2 = st.columns(2)
with col_v1:
        st.write("🧘‍♀️Pose Distribution by Category")
        st.bar_chart(poses["category"].value_counts())
with col_v2:
        st.write("**Difficulty Distribution**")
        st.bar_chart(poses["level"].value_counts())



#visualization
#--------------------------------------------------------------------
st.sidebar.write("### Visualizations")

if st.sidebar.checkbox("Show Pose Statistics"):
    st.subheader("📊 Pose Distribution by Category")
    st.bar_chart(poses["category"].value_counts())

    st.subheader("📈 Difficulty Level Distribution")
    st.bar_chart(poses["level"].value_counts())

    st.subheader("🧰 Props Usage Frequency")
    st.bar_chart(props["prop"].value_counts())

    st.subheader("❤️ Therapy Conditions Count")
    st.bar_chart(therapy["therapy_condition"].value_counts())
