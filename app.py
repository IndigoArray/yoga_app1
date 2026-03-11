import streamlit as st
import pandas as pd
import os

st.title("🧘 Yoga Therapy App")

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

# ---------------------------------------------------------
# Sidebar Filters
# ---------------------------------------------------------
st.sidebar.header("Filters")

category_filter = st.sidebar.selectbox(
    "Category",
    ["All"] + sorted(poses["category"].unique())
)

therapy_filter = st.sidebar.selectbox(
    "Therapeutic Need",
    ["None"] + sorted(therapy["therapy_condition"].unique())
)

level_filter = st.sidebar.selectbox(
    "Difficulty Level",
    ["All"] + sorted(poses["level"].unique())
)
#---------------------------------------------------------------

props_filter = st.sidebar.multiselect(
    "Props Needed",
    sorted(props["prop"].dropna().unique())
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

# ---------------------------------------------------------
# Filter Logic
# ---------------------------------------------------------
filtered = poses.copy()

if category_filter != "All":
    filtered = filtered[filtered["category"] == category_filter]

if level_filter != "All":
    filtered = filtered[filtered["level"] == level_filter]

if therapy_filter != "None":
    pose_ids = therapy[therapy["therapy_condition"] == therapy_filter]["pose_id"]
    filtered = filtered[filtered["id"].isin(pose_ids)]
#---------------------------------------------------------------------------------
# Props filter
if props_filter:
    pose_ids = props[props["prop"].isin(props_filter)]["pose_id"]
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
st.title("🧘 Yoga Therapy Pose Explorer")


pose_names = filtered["english_name"].tolist()


if len(pose_names) == 0:
    st.warning("No poses match your filters.")
else:
    selected_pose = st.selectbox("Choose a pose", pose_names)

    pose = poses[poses["english_name"] == selected_pose].iloc[0]

    # ---------------------------------------------------------
    # Display Pose Information
    # ---------------------------------------------------------
    st.header(pose["english_name"])
    st.subheader(pose["sanskrit_name"])

    image_path = os.path.join("images", pose["image_path"])
    if os.path.exists(image_path):
        st.image(image_path, use_column_width=True)
    else:
        st.info("Image not found. Add it to the images folder.")

    st.write("### Description")
    st.write(pose["description"])

    # ---------------------------------------------------------
    # Variations
    # ---------------------------------------------------------
    st.write("### Variations")
    pose_variations = variations[variations["pose_id"] == pose["id"]]
    if len(pose_variations) > 0:
        st.table(pose_variations[["variation_type", "description"]])
    else:
        st.write("No variations available.")

    # ---------------------------------------------------------
    # Therapeutic Uses
    # ---------------------------------------------------------
    st.write("### Therapeutic Uses")
    pose_therapy = therapy[therapy["pose_id"] == pose["id"]]
    if len(pose_therapy) > 0:
        st.write(", ".join(pose_therapy["therapy_condition"].tolist()))
    else:
        st.write("No therapeutic uses listed.")

    # ---------------------------------------------------------
    # Contraindications
    # ---------------------------------------------------------
    st.write("### Contraindications")
    pose_contra = contra[contra["pose_id"] == pose["id"]]
    if len(pose_contra) > 0:
        st.write(", ".join(pose_contra["contraindication"].tolist()))
    else:
        st.write("No contraindications listed.")

    # ---------------------------------------------------------
    # Props
    # ---------------------------------------------------------
    st.write("### Props")
    pose_props = props[props["pose_id"] == pose["id"]]
    if len(pose_props) > 0:
        st.table(pose_props[["prop", "usage"]])
    else:
        st.write("No props listed.")

    # ---------------------------------------------------------
    # Biomechanics
    # ---------------------------------------------------------
    st.write("### Biomechanics")
    pose_bio = bio[bio["pose_id"] == pose["id"]]
    if len(pose_bio) > 0:
        bio_row = pose_bio.iloc[0]
        st.write("**Joint Actions:**", bio_row["joint_actions"])
        st.write("**Muscles Activated:**", bio_row["muscles_activated"])
        st.write("**Muscles Stretched:**", bio_row["muscles_stretched"])
        st.write("**Planes of Movement:**", bio_row["planes_of_movement"])
    else:
        st.write("No biomechanics data available.")

    # ---------------------------------------------------------
    # Sequencing
    # ---------------------------------------------------------
    st.write("### Sequencing")
    pose_seq = seq[seq["pose_id"] == pose["id"]]
    if len(pose_seq) > 0:
        seq_row = pose_seq.iloc[0]
        st.write("**Prep Pose:**", seq_row["prep_pose"])
        st.write("**Counter Pose:**", seq_row["counter_pose"])
    else:
        st.write("No sequencing data available.")

#theme

theme = st.sidebar.selectbox(
    "Theme",
    ["Light", "Calm Blue", "Earth Brown", "Forest Green"]
)

theme_colors = {
    "Light": "#FFFFFF",
    "Calm Blue": "#E3F2FD",
    "Earth Brown": "#EFEBE9",
    "Forest Green": "#E8F5E9"
}

st.markdown(
    f"""
    <style>
        .main {{
            background-color: {theme_colors[theme]};
        }}
    </style>
    """,
    unsafe_allow_html=True
)



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
