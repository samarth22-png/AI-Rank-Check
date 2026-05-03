import streamlit as st
import time
from prompts import get_prompt
from llm_calls import get_gemini_response
from analysis import extract_products, calculate_visibility, generate_report_card

st.set_page_config(page_title="AEO Tool", layout="wide", initial_sidebar_state="expanded")

# --- Custom CSS ---
st.markdown("""
<style>
/* Premium styling for buttons */
.stButton>button {
    background: linear-gradient(135deg, #ff4b4b, #ff7676);
    color: white;
    font-size: 18px;
    border-radius: 10px;
    border: none;
    transition: all 0.3s ease;
    width: 100%;
}
.stButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(255, 75, 75, 0.4);
    color: white;
}
/* Styling for metric cards */
div[data-testid="stMetricValue"] {
    font-size: 2.5rem;
    font-weight: 800;
}
div[data-testid="stMetricLabel"] {
    font-size: 1.1rem;
    color: #555;
}
</style>
""", unsafe_allow_html=True)

# --- Initialize Session State ---
if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Sidebar Controls ---
with st.sidebar:
    st.title("⚙️ Control Panel")
    st.markdown("Enter your details below to run the AEO diagnostic.")
    
    product = st.text_input("Your Product Name", placeholder="e.g. Acme Protein")
    query = st.text_input("Search Query", placeholder="e.g. best protein powder")
    
    st.markdown("<br>", unsafe_allow_html=True)
    analyze_btn = st.button("🚀 Run Analysis")

# --- Main App Logic ---
if analyze_btn:
    if not product or not query:
        st.sidebar.warning("⚠️ Please fill out both fields!")
        st.stop()

    try:
        st.toast("Starting AEO Analysis...", icon="⏳")
        prompt = get_prompt(query)

        with st.spinner("🔍 Fetching AI recommendations..."):
            time.sleep(0.5) # Slight delay for smooth UI feedback
            response_text = get_gemini_response(prompt)
            
            if "Error connecting" in response_text:
                st.error(response_text)
                st.stop()

            product_list = extract_products(response_text)
            all_results = [product_list]
            score = calculate_visibility(product, all_results)
            report_card = generate_report_card(product, product_list, score)

        # Store results
        st.session_state.score = score
        st.session_state.response_text = response_text
        st.session_state.report_card = report_card
        
        suggest_prompt = f"""
A product is not ranking well in AI recommendations for this query:
{query}

Give 3 short actionable suggestions to improve:
- product naming
- description
- positioning
"""
        with st.spinner("💡 Generating actionable suggestions..."):
            suggestions = get_gemini_response(suggest_prompt)
            st.session_state.suggestions = suggestions
            st.session_state.analysis_done = True
            
            # Reset chat history
            st.session_state.chat_history = [
                {"role": "assistant", "content": f"I've analyzed **{product}**. Ask me how to implement these suggestions!"}
            ]
        
        st.toast("Analysis Complete! 🎉", icon="✅")
        if score >= 80:
            st.balloons()

    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

# --- Main Dashboard ---
st.title("🚀 AEO Diagnostic Dashboard")

if not st.session_state.analysis_done:
    st.info("👈 Please enter your product details in the sidebar and click **Run Analysis** to begin.")
else:
    score = st.session_state.score
    report_card = st.session_state.report_card
    
    # 3-Column Top Metric Dashboard
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Visibility Score", f"{score}%")
    with col2:
        st.metric("Report Card Grade", report_card["grade"])
    with col3:
        st.metric("AI Search Rank", report_card["rank"])

    if score == 0:
        st.error("❌ Your product is **NOT visible** in AI recommendations.")
    elif score < 50:
        st.warning("⚠️ Your product has **LOW visibility**.")
    else:
        st.success("✅ Your product is **performing well** in AI search!")

    st.markdown("---")
    
    # --- Interactive Tabs ---
    tab1, tab2, tab3, tab4 = st.tabs(["🏆 Top Competitors", "💡 AI Suggestions", "💬 Implementation Chat", "🧠 Raw AI Data"])
    
    with tab1:
        st.subheader("🚨 Competitors Stealing Your Visibility")
        if report_card["competitors"]:
            for comp in report_card["competitors"]:
                st.markdown(f"- **{comp}**")
        else:
            st.success("No competitors found! You completely own this search query.")
            
    with tab2:
        st.subheader("Actionable Steps to Improve")
        st.write(st.session_state.suggestions)
        
    with tab3:
        st.subheader("Ask for Implementation Guidance")
        
        # Display Chat History
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
                
        # Chat Input
        if follow_up := st.chat_input("Ask a follow-up question here...", key="chat_input"):
            # Display user message
            st.session_state.chat_history.append({"role": "user", "content": follow_up})
            with st.chat_message("user"):
                st.write(follow_up)
                
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    context_prompt = f"""
Context of our analysis:
User's Product: {product}
Search Query: {query}
Initial Suggestions given to the user:
{st.session_state.suggestions}

User Follow-up Question: {follow_up}

Provide a detailed, step-by-step actionable guide or answer based on the context above.
"""
                    answer = get_gemini_response(context_prompt)
                    st.write(answer)
                    
            # Save assistant message
            st.session_state.chat_history.append({"role": "assistant", "content": answer})

    with tab4:
        st.subheader("Raw Recommendations from Gemini")
        st.info(st.session_state.response_text)

st.markdown("<br><br><br>", unsafe_allow_html=True)
st.caption("Built by Samarth Agarwal 🚀 | Powered by Gemini AI ✅")