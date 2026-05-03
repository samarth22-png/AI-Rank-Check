import streamlit as st
from prompts import get_prompt
from llm_calls import get_gemini_response
from analysis import extract_products, calculate_visibility

st.set_page_config(page_title="AEO Tool", layout="wide")

st.title("🚀 AEO Diagnostic Tool")
st.caption("Check how AI recommends your product")

st.markdown("""
<style>
.stButton>button {
    background-color: #ff4b4b;
    color: white;
    font-size: 18px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

product = st.text_input("Enter your product name")
query = st.text_input("Enter search query (e.g. best protein powder)")

if st.button("Analyze"):
    if not product or not query:
        st.warning("Please fill both fields")
        st.stop()

    try:
        prompt = get_prompt(query)

        with st.spinner("Analyzing AI responses..."):
            response_text = get_gemini_response(prompt)
            
            if "Error connecting" in response_text:
                st.error(response_text)
                st.stop()

            product_list = extract_products(response_text)
            all_results = [product_list]
            score = calculate_visibility(product, all_results)

        # Store results in session state
        st.session_state.score = score
        st.session_state.response_text = response_text
        
        suggest_prompt = f"""
A product is not ranking well in AI recommendations for this query:
{query}

Give 3 short actionable suggestions to improve:
- product naming
- description
- positioning
"""
        with st.spinner("Generating suggestions..."):
            suggestions = get_gemini_response(suggest_prompt)
            st.session_state.suggestions = suggestions
            st.session_state.analysis_done = True
            
            # Initialize/Reset chat history for a new analysis
            st.session_state.chat_history = [
                {"role": "assistant", "content": "I have analyzed your product. How can I help you implement these suggestions?"}
            ]

    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

# Display Analysis if done
if st.session_state.analysis_done:
    score = st.session_state.score
    
    st.subheader("📊 Visibility Score")
    st.metric("Score", f"{score}%")

    if score == 0:
        st.error("❌ Your product is NOT visible in AI recommendations")
    elif score < 50:
        st.warning("⚠️ Your product has LOW visibility")
    else:
        st.success("✅ Your product is performing well")

    st.subheader("🧠 AI Recommendations")
    st.write(st.session_state.response_text)

    st.subheader("💡 AI Suggestions to Improve")
    st.write(st.session_state.suggestions)

    st.markdown("---")
    st.subheader("💬 Ask How to Implement")
    
    # Display Chat History
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            
    # Chat Input
    if follow_up := st.chat_input("Ask a follow-up question..."):
        # Display the user message immediately
        st.session_state.chat_history.append({"role": "user", "content": follow_up})
        with st.chat_message("user"):
            st.write(follow_up)
            
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # Build context-aware prompt using previous analysis
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

st.markdown("---")
st.caption("Built by Samarth Agarwal 🚀")
st.write("Using Gemini only ✅")