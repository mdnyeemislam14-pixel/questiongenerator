import streamlit as st

# পেজ কনফিগারেশন (Wide layout)
st.set_page_config(page_title="স্কুল প্রশ্নপত্র জেনারেটর", layout="wide")

# কাস্টম CSS স্টাইল (A4 সাইজ এবং প্রিন্ট ফ্রেন্ডলি করার জন্য)
st.markdown("""
    <style>
    /* সাধারণ স্টাইল */
    .main-title {
        text-align: center;
        font-family: 'SolaimanLipi', Arial, sans-serif;
    }
    
    /* প্রিন্ট স্টাইল: প্রিন্ট করার সময় শুধু প্রশ্নপত্রটুকু দেখাবে, বাকি সাইডবার বা বাটন লুকিয়ে থাকবে */
    @media print {
        body {
            background-color: white;
            color: black;
        }
        .stButton, .stTabs, header, footer {
            display: none !important;
        }
        .printable-area {
            width: 100% !important;
            padding: 0px !important;
            margin: 0px !important;
            box-shadow: none !important;
        }
    }

    /* A4 পেপার প্রিভিউ বক্স */
    .printable-area {
        background-color: white;
        color: black;
        padding: 40px;
        margin: 20px auto;
        max-width: 800px;
        border: 1px solid #ddd;
        box-shadow: 0 0 10px rgba(0,0,0,0.1);
        font-family: 'SolaimanLipi', Arial, sans-serif;
    }
    .school-header {
        text-align: center;
        border-bottom: 2px solid black;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# সেশন স্টেট ইনিশিয়ালাইজেশন (প্রশ্নগুলো মেমোরিতে ধরে রাখার জন্য)
if 'mcq_list' not in st.session_state:
    st.session_state.mcq_list = []
if 'creative_list' not in st.session_state:
    st.session_state.creative_list = []

st.title("🏫 স্কুল প্রশ্নপত্র জেনারেটর (GitHub + Streamlit)")
st.write("আপনার স্কুলের প্রশ্ন তৈরি করুন এবং সরাসরি প্রিন্ট বা PDF করুন।")
st.markdown("---")

# ১. পরীক্ষার সাধারণ তথ্য (হেডিং)
st.subheader("📋 ১. পরীক্ষার সাধারণ তথ্য সেট করুন")
col1, col2, col3 = st.columns(3)
with col1:
    school_name = st.text_input("স্কুলের নাম", "কালীগঞ্জ সরকারি বালিকা উচ্চ বিদ্যালয়, গাজীপুর")
    exam_name = st.text_input("পরীক্ষার নাম", "ষাণ্মাসিক মূল্যায়ন - ২০২৬")
with col2:
    subject = st.text_input("বিষয়", "তথ্য ও যোগাযোগ প্রযুক্তি")
    class_name = st.text_input("শ্রেণি", "নবম")
with col3:
    time = st.text_input("সময়", "১ ঘণ্টা ৩০ মিনিট")
    marks = st.text_input("পূর্ণমান", "৫০")

st.markdown("---")

# ২. আলাদা ট্যাব তৈরি (MCQ এবং সৃজনশীল)
tab_mcq, tab_creative = st.tabs(["📌 বহু নির্বাচনী (MCQ) সেকশন", "📝 সৃজনশীল প্রশ্ন সেকশন"])

# --- MCQ সেকশন ---
with tab_mcq:
    st.header("বহু নির্বাচনী প্রশ্ন (MCQ) সংযোজন")
    
    with st.form("mcq_form", clear_on_submit=True):
        mcq_question = st.text_area("প্রশ্ন লিখুন:")
        
        col_opt1, col_opt2 = st.columns(2)
        with col_opt1:
            opt_a = st.text_input("ক. অপশন")
            opt_c = st.text_input("গ. অপশন")
        with col_opt2:
            opt_b = st.text_input("খ. অপশন")
            opt_d = st.text_input("ঘ. অপশন")
            
        submitted_mcq = st.form_submit_button("➕ এই MCQ টি যোগ করুন")
        if submitted_mcq:
            if mcq_question and opt_a and opt_b:
                st.session_state.mcq_list.append({
                    "question": mcq_question,
                    "a": opt_a,
                    "b": opt_b,
                    "c": opt_c,
                    "d": opt_d
                })
                st.success("MCQ সফলভাবে যোগ করা হয়েছে!")
            else:
                st.error("দয়া করে প্রশ্ন এবং কমপক্ষে দুটি অপশন লিখুন।")

    # বর্তমান যুক্ত করা MCQ গুলোর তালিকা দেখানোর জন্য
    if st.session_state.mcq_list:
        st.write(f"সর্বমোট যুক্ত হওয়া MCQ: **{len(st.session_state.mcq_list)}** টি")
        if st.button("সব MCQ মুছে ফেলুন"):
            st.session_state.mcq_list = []
            st.rerun()

# --- সৃজনশীল সেকশন ---
with tab_creative:
    st.header("সৃজনশীল প্রশ্ন সংযোজন")
    
    with st.form("creative_form", clear_on_submit=True):
        stem_text = st.text_area("উদ্দীপক লিখুন:")
        
        q_k = st.text_input("(ক) জ্ঞানমূলক প্রশ্ন (নম্বর: ১)")
        q_kh = st.text_input("(খ) অনুধাবনমূলক প্রশ্ন (নম্বর: ২)")
        q_g = st.text_input("(গ) প্রয়োগমূলক প্রশ্ন (নম্বর: ৩)")
        q_gh = st.text_input("(ঘ) উচ্চতর দক্ষতামূলক প্রশ্ন (নম্বর: ৪)")
        
        submitted_creative = st.form_submit_button("➕ এই সৃজনশীল প্রশ্নটি যোগ করুন")
        if submitted_creative:
            if stem_text and q_k:
                st.session_state.creative_list.append({
                    "stem": stem_text,
                    "k": q_k,
                    "kh": q_kh,
                    "g": q_g,
                    "gh": q_gh
                })
                st.success("সৃজনশীল প্রশ্ন সফলভাবে যোগ করা হয়েছে!")
            else:
                st.error("দয়া করে উদ্দীপক এবং অন্তত ক-এর প্রশ্নটি লিখুন।")

    # বর্তমান যুক্ত করা সৃজনশীল প্রশ্নগুলোর তালিকা দেখার জন্য
    if st.session_state.creative_list:
        st.write(f"সর্বমোট যুক্ত হওয়া সৃজনশীল প্রশ্ন: **{len(st.session_state.creative_list)}** টি")
        if st.button("সব সৃজনশীল প্রশ্ন মুছে ফেলুন"):
            st.session_state.creative_list = []
            st.rerun()

st.markdown("---")

# ৩. A4 সাইজ প্রিন্ট প্রিভিউ সেকশন
st.subheader("🖨️ চূড়ান্ত প্রশ্নপত্র প্রিভিউ (A4 সাইজ)")
st.write("নিচে আপনার প্রশ্নপত্রটি প্রফেশনাল ফরম্যাটে দেখা যাচ্ছে। প্রিন্ট করতে ব্রাউজারের প্রিন্ট অপশন (`Ctrl + P`) ব্যবহার করুন।")

# প্রিভিউ কন্টেইনার (A4 লুক)
st.markdown(f"""
<div class="printable-area">
    <div class="school-header">
        <h2>{school_name}</h2>
        <h3>{exam_name}</h3>
        <p><b>বিষয়:</b> {subject} | <b>শ্রেণি:</b> {class_name} | <b>সময়:</b> {time} | <b>পূর্ণমান:</b> {marks}</p>
    </div>
""", unsafe_allow_html=True)

# MCQ অংশ রেন্ডার করা
if st.session_state.mcq_list:
    st.markdown("#### **অংশ-ক: বহু নির্বাচনী প্রশ্ন (MCQ)**")
    st.markdown("সকল প্রশ্নের উত্তর দাও। প্রতিটি প্রশ্নের মান ১।")
    for idx, item in enumerate(st.session_state.mcq_list, 1):
        st.markdown(f"**{idx}. {item['question']}**")
        st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;ক) {item['a']} &nbsp;&nbsp;&nbsp;&nbsp; খ) {item['b']} &nbsp;&nbsp;&nbsp;&nbsp; গ) {item['c']} &nbsp;&nbsp;&nbsp;&nbsp; ঘ) {item['d']}")
    st.markdown("<br>", unsafe_allow_html=True)

# সৃজনশীল অংশ রেন্ডার করা
if st.session_state.creative_list:
    st.markdown("#### **অংশ-খ: সৃজনশীল প্রশ্ন**")
    st.markdown("নির্দেশনা: নিচের উদ্দীপকগুলো মনোযোগ দিয়ে পড়ো এবং সংশ্লিষ্ট প্রশ্নগুলোর উত্তর দাও।")
    for idx, item in enumerate(st.session_state.creative_list, 1):
        st.markdown(f"**উদ্দীপক-{idx}:** {item['stem']}")
        st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;(ক) {item['k']} <b>[১]</b>")
        st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;(খ) {item['kh']} <b>[২]</b>")
        st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;(গ) {item['g']} <b>[৩]</b>")
        st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;(ঘ) {item['gh']} <b>[৪]</b>")
        st.markdown("<br>", unsafe_allow_html=True)

if not st.session_state.mcq_list and not st.session_state.creative_list:
    st.info("⚠️ এখনো কোনো প্রশ্ন যোগ করা হয়নি। উপরে ট্যাব থেকে MCQ বা সৃজনশীল প্রশ্ন যোগ করুন।")

st.markdown("</div>", unsafe_allow_html=True)
