import streamlit as st
import requests
from datetime import date, time
from PIL import Image
import base64

# ---------------- Background Setup ----------------
def set_background(image_path):
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
    st.markdown(f"""
        <style>
            .stApp {{
                background-image: url("data:image/png;base64,{encoded}");
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
            }}
            .glass {{
                background: rgba(0, 0, 0, 0.6);
                backdrop-filter: blur(8px);
                -webkit-backdrop-filter: blur(8px);
                padding: 2rem;
                border-radius: 15px;
                margin: auto;
                box-shadow: 0 8px 32px 0 rgba(0,0,0,0.5);
                color: white;
            }}
            h1, h3, label, p {{
                color: #ffe9c5 !important;
            }}
            .stButton > button {{
                background: linear-gradient(to right, #ff7e5f, #feb47b);
                color: white;
                border-radius: 10px;
                font-weight: bold;
                margin-top: 10px;
            }}
            textarea {{
                background-color: #1c1c1c !important;
                color: white !important;
            }}
        </style>
    """, unsafe_allow_html=True)

# ---------------- Page Config ----------------
st.set_page_config(page_title="Astrology Chatbot", page_icon="🔮", layout="centered")
set_background("D:/Self Project/astro_image.jpg")  # update path if needed

# ---------------- Session State Setup ----------------
if "horoscope_shown" not in st.session_state:
    st.session_state.horoscope_shown = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "kundli_summary" not in st.session_state:
    st.session_state.kundli_summary = {}

# ---------------- Kundli Input Form ----------------
with st.container():
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.markdown("<h1 style='text-align:center;'>🔮 Astrology Chatbot</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Enter your birth details to generate your Kundli.</p>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        dob = st.date_input("📅 Date of Birth", min_value=date(1950, 1, 1), max_value=date.today(), value=date(2000, 1, 1))
    with col2:
        tob = st.time_input("⏰ Time of Birth", value=time(12, 0), step=60)

    place = st.text_input("📍 Place of Birth", "Kolkata")
    submit = st.button("🔍 Generate Kundli")
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- Kundli Summary ----------------
if submit:
    st.session_state.horoscope_shown = False
    with st.spinner("Fetching your horoscope..."):
        try:
            response = requests.post(
                "http://localhost:8000/daily-horoscope",
                json={"dob": str(dob), "tob": tob.strftime("%H:%M"), "place": place}
            )
            if response.status_code == 200:
                data = response.json()
                summary = data.get("kundli_summary", {})

                st.session_state.horoscope_shown = True
                st.session_state.kundli_summary = summary

                st.success("✅ Horoscope Generated Successfully!")

                st.markdown('<div class="glass">', unsafe_allow_html=True)
                st.markdown("### 🧾 Kundli Summary", unsafe_allow_html=True)

                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**🌞 Ayanamsha:** {summary.get('ayanamsha')}")
                    st.markdown(f"**🌗 Tithi:** {summary.get('tithi')}")
                    st.markdown(f"**📅 Vaar:** {summary.get('vaar')}")
                    st.markdown(f"**🌌 Nakshatra #:** {summary.get('nakshatra_number')}")
                    st.markdown(f"**🧭 Pada:** {summary.get('nakshatra_pada')}")
                    st.markdown(f"**🌙 Paksha:** {summary.get('paksha')}")

                with col2:
                    st.markdown(f"**📘 Maah (Solar):** {summary.get('maah_solar')}")
                    st.markdown(f"**📗 Maah (Lunar):** {summary.get('maah_lunar_amant')}")
                    st.markdown(f"**❄️ Ritu:** {summary.get('ritu')}")
                    st.markdown(f"**📈 Ayan:** {summary.get('ayan')}")
                    st.markdown(f"**🌍 Gol:** {summary.get('gol')}")
                    st.markdown(f"**🌅 Sunrise:** {summary.get('sunrise')}")
                    st.markdown(f"**🌇 Sunset:** {summary.get('sunset')}")
                    st.markdown(f"**🌙 Moonrise:** {summary.get('moonrise')}")
                    st.markdown(f"**🌘 Moonset:** {summary.get('moonset')}")

                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.error(f"API Error {response.status_code}: {response.text}")
        except Exception as e:
            st.error(f"Something went wrong: {e}")

# ---------------- Chatbot UI ----------------
if st.session_state.horoscope_shown:
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.markdown("### 💬 Talk to Your Astrologer", unsafe_allow_html=True)

    # Display chat history using Streamlit's chat-like message UI
    for chat in st.session_state.chat_history:
        with st.chat_message("user"):
            st.markdown(chat["user"])
        with st.chat_message("assistant"):
            st.markdown(chat["bot"])

    user_question = st.chat_input("Ask your astrology question here...")

    if user_question:
        with st.chat_message("user"):
            st.markdown(user_question)

        from backend.services.llm_service import interpret_horoscope
        kundli = st.session_state.kundli_summary

        with st.spinner("Astrologer is thinking..."):
            try:
                bot_reply = interpret_horoscope(kundli, user_question)
            except Exception as e:
                bot_reply = "Sorry, I couldn't interpret your question due to an internal error."

        with st.chat_message("assistant"):
            st.markdown(bot_reply)

        st.session_state.chat_history.append({
            "user": user_question,
            "bot": bot_reply
        })

    st.markdown('</div>', unsafe_allow_html=True)
