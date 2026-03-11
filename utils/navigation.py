import streamlit as st

def navigation_header():
    st.markdown(
        """
        <style>
            .nav-container {
                background-color: #f0f4f8;
                padding: 12px 20px;
                border-radius: 8px;
                margin-bottom: 20px;
                display: flex;
                gap: 20px;
                font-size: 18px;
                font-weight: 600;
            }
            .nav-item {
                text-decoration: none;
                color: #333;
                padding: 6px 12px;
                border-radius: 6px;
            }
            .nav-item:hover {
                background-color: #dce7f3;
            }
        </style>

        <div class="nav-container">
            <a class="nav-item" href="/">🏠 Home</a>
            <a class="nav-item" href="/1_Pose_Explorer">🧘 Pose Explorer</a>
            <a class="nav-item" href="/2_Analytics_Dashboard">📊 Analytics</a>
            <a class="nav-item" href="/3_Props_Explorer">🧰 Props Explorer</a>
            <a class="nav-item" href="/4_Therapy_Conditions">❤️ Therapy Conditions</a>
        </div>
        """,
        unsafe_allow_html=True
    )
