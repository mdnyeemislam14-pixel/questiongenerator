import json
import os
import streamlit as st

# পেজ কনফিগারেশন
st.set_page_config(
    page_title="স্মার্ট স্কুল প্রশ্নপত্র জেনারেটর", layout="wide"
)

# ডেটা সেভ রাখার জন্য ফাইল পাথ
DB_FILE = "question_bank.json"


def load_data():
  if os.path.exists(DB_FILE):
    with open(DB_FILE, "r", encoding="utf-8") as f:
      try:
        return json.load(f)
      except:
        return {"mcq": [], "creative": [], "short": []}
  return {"mcq": [], "creative": [], "short": []}


def save_data(data):
  with open(DB_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)


if "db" not in st.session_state:
  st.session_state.db = load_data()

# পাসওয়ার্ড প্রটেকশন (পাসওয়ার্ড: qwerty)
if "authenticated" not in st.session_state:
  st.session_state.authenticated = False

if not st.session_state.authenticated:
  st.title("🔐 অ্যাডমিন লগইন - স্মার্ট স্কুল প্রশ্নপত্র জেনারেটর")
  st.markdown("দয়া করে সিস্টেমটি ব্যবহার করতে পাসওয়ার্ড দিন।")

  with st.form("login_form"):
    password_input = st.text_input("পাসওয়ার্ড লিখুন:", type="password")
    submit_login = st.form_submit_button("লগইন করুন")

    if submit_login:
      if password_input == "qwerty":
        st.session_state.authenticated = True
        st.success("লগইন সফল হয়েছে!")
        st.rerun()
      else:
        st.error("ভুল পাসওয়ার্ড! সঠিক পাসওয়ার্ড দিন (পাসওয়ার্ড হলো: qwerty)।")
  st.stop()

# লগইন সফল হলে মূল অ্যাপ শুরু হবে
st.title("🏫 স্মার্ট স্কুল প্রশ্নপত্র ও পরীক্ষা ব্যবস্থাপনা সিস্টেম")
st.markdown("সৃজনশীল, বহু নির্বাচনী এবং সংক্ষিপ্ত প্রশ্ন তৈরি ও প্রিন্ট প্ল্যাটফর্ম।")
st.markdown("---")

# পেপার লেআউট ও ডিজাইন (সাইডবার)
st.sidebar.header("⚙️ পেপার লেআউট ও ডিজাইন")
orientation = st.sidebar.selectbox(
    "পেপারের Orientation", ["Portrait (লম্বালম্বি)", "Landscape (আড়াআড়ি)"]
)
columns_layout = st.sidebar.selectbox(
    "কলাম বিন্যাস", ["এক কলাম (Single Column)", "দুই কলাম (Two Columns - MCQ)"]
)
font_size = st.sidebar.slider("ফন্ট সাইজ", 10, 16, 12)

st.sidebar.markdown("---")
st.sidebar.header("📋 পরীক্ষার হেডিং তথ্য")
school_name = st.sidebar.text_input(
    "স্কুলের নাম", "কালীগঞ্জ সরকারি বালিকা উচ্চ বিদ্যালয়, গাজীপুর"
)
exam_name = st.sidebar.text_input("পরীক্ষার নাম", "ষাণ্মাসিক মূল্যায়ন - ২০২৬")
subject = st.sidebar.text_input("বিষয়", "তথ্য ও যোগাযোগ প্রযুক্তি")
class_name = st.sidebar.text_input("শ্রেণি", "নবম")
time_limit = st.sidebar.text_input("সময়", "১ ঘণ্টা ৩০ মিনিট")
total_marks = st.sidebar.text_input("পূর্ণমান", "৫০")

st.sidebar.markdown("---")
st.sidebar.header("📌 বিভাগ ও নম্বর বিন্যাস")
mcq_mark_per_q = st.sidebar.number_input(
    "প্রতিটি MCQ এর নম্বর", min_value=0.5, value=1.0, step=0.5
)
mcq_total_q_to_answer = st.sidebar.number_input(
    "MCQ কয়টি দিতে হবে?", min_value=1, value=15
)

short_mark_per_q = st.sidebar.number_input(
    "প্রতিটি সংক্ষিপ্ত প্রশ্নের নম্বর", min_value=1, value=2
)
short_total_q_to_answer = st.sidebar.number_input(
    "সংক্ষিপ্ত প্রশ্ন কয়টি দিতে হবে?", min_value=1, value=5
)

creative_total_q_to_answer = st.sidebar.number_input(
    "সৃজনশীল প্রশ্ন কয়টি দিতে হবে?", min_value=1, value=3
)

if st.sidebar.button("🔒 লগআউট"):
  st.session_state.authenticated = False
  st.rerun()

# মূল ট্যাবসমূহ
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📌 বহু নির্বাচনী (MCQ)",
    "📝 সৃজনশীল প্রশ্ন",
    "✍️ সংক্ষিপ্ত প্রশ্ন",
    "🗂️ সংরক্ষিত প্রশ্ন ব্যাংক",
    "🖨️ ফাইনাল প্রিভিউ ও ডাউনলোড/প্রিন্ট",
])

# --- ট্যাব ১: MCQ ---
with tab1:
  st.header("বহু নির্বাচনী প্রশ্ন (MCQ) সংযোজন")
  mcq_mode = st.radio(
      "ইনপুট পদ্ধতি:", ["একক প্রশ্ন যোগ", "বাল্ক পেস্ট (একাধিক প্রশ্ন একসাথে)"]
  )

  if mcq_mode == "একক প্রশ্ন যোগ":
    with st.form("single_mcq_form", clear_on_submit=True):
      q_text = st.text_area("প্রশ্ন লিখুন:")
      c1, c2 = st.columns(2)
      with c1:
        opt_a = st.text_input("ক. অপশন")
        opt_c = st.text_input("গ. অপশন")
      with c2:
        opt_b = st.text_input("খ. অপশন")
        opt_d = st.text_input("ঘ. অপশন")
      correct_ans = st.selectbox("সঠিক উত্তর", ["ক", "খ", "গ", "ঘ"])

      if st.form_submit_button("MCQ সংরক্ষণ করুন"):
        if q_text and opt_a:
          st.session_state.db["mcq"].append({
              "q": q_text,
              "a": opt_a,
              "b": opt_b,
              "c": opt_c,
              "d": opt_d,
              "ans": correct_ans,
          })
          save_data(st.session_state.db)
          st.success("MCQ সংরক্ষিত হয়েছে!")
        else:
          st.error("প্রশ্ন ও অপশন পূরণ করুন।")
  else:
    st.info(
        "প্রতিটি প্রশ্ন নতুন লাইনে দিন এবং অপশনগুলো ক, খ, গ, ঘ আকারে লিখুন।"
    )
    bulk_mcq_text = st.text_area(
        "এখানে আপনার MCQ গুলো পেস্ট করুন:", height=150
    )
    if st.button("বাল্ক MCQ সেভ করুন"):
      if bulk_mcq_text:
        for line in bulk_mcq_text.split("\n"):
          if line.strip():
            st.session_state.db["mcq"].append({
                "q": line.strip(),
                "a": "অপশন ক",
                "b": "অপশন খ",
                "c": "অপশন গ",
                "d": "অপশন ঘ",
                "ans": "ক",
            })
        save_data(st.session_state.db)
        st.success("বাল্ক MCQ সফলভাবে যুক্ত হয়েছে!")

# --- ট্যাব ২: সৃজনশীল প্রশ্ন ---
with tab2:
  st.header("সৃজনশীল প্রশ্ন সংযোজন")
  with st.form("creative_form_main", clear_on_submit=True):
    stem = st.text_area("উদ্দীপক লিখুন:")
    qk = st.text_input("(ক) জ্ঞানমূলক প্রশ্ন")
    qkh = st.text_input("(খ) অনুধাবনমূলক প্রশ্ন")
    qg = st.text_input("(গ) প্রয়োগমূলক প্রশ্ন")
    qgh = st.text_input("(ঘ) উচ্চতর দক্ষতামূলক প্রশ্ন")

    if st.form_submit_button("সৃজনশীল প্রশ্ন সংরক্ষণ করুন"):
      if stem and qk:
        st.session_state.db["creative"].append({
            "stem": stem,
            "k": qk,
            "kh": qkh,
            "g": qg,
            "gh": qgh,
        })
        save_data(st.session_state.db)
        st.success("সৃজনশীল প্রশ্ন সংরক্ষিত হয়েছে!")
      else:
        st.error("উদ্দীপক এবং অন্তত ক-এর প্রশ্ন দিন।")

# --- ট্যাব ৩: সংক্ষিপ্ত প্রশ্ন ---
with tab3:
  st.header("সংক্ষিপ্ত প্রশ্ন সংযোজন")
  with st.form("short_form_main", clear_on_submit=True):
    short_q = st.text_area("সংক্ষিপ্ত প্রশ্ন লিখুন:")
    short_ans = st.text_input("উত্তর (ঐচ্ছিক):")

    if st.form_submit_button("সংক্ষিপ্ত প্রশ্ন সংরক্ষণ করুন"):
      if short_q:
        st.session_state.db["short"].append({"q": short_q, "ans": short_ans})
        save_data(st.session_state.db)
        st.success("সংক্ষিপ্ত প্রশ্ন সংরক্ষিত হয়েছে!")
      else:
        st.error("প্রশ্ন লিখুন।")

# --- ট্যাব ৪: প্রশ্ন ব্যাংক (Edit/Delete) ---
with tab4:
  st.header("🗂️ সংরক্ষিত প্রশ্ন ব্যাংক (Delete)")
  db = st.session_state.db
  sub1, sub2, sub3 = st.tabs(
      ["MCQ তালিকা", "সৃজনশীল তালিকা", "সংক্ষিপ্ত প্রশ্ন"]
  )

  with sub1:
    for i, item in enumerate(db["mcq"]):
      c1, c2 = st.columns([8, 2])
      with c1:
        st.write(f"**{i+1}. {item['q']}**")
      with c2:
        if st.button("ডিলিট", key=f"d_mcq_{i}"):
          db["mcq"].pop(i)
          save_data(db)
          st.rerun()

  with sub2:
    for i, item in enumerate(db["creative"]):
      c1, c2 = st.columns([8, 2])
      with c1:
        st.write(f"**উদ্দীপক-{i+1}:** {item['stem'][:60]}...")
      with c2:
        if st.button("ডিলিট", key=f"d_cr_{i}"):
          db["creative"].pop(i)
          save_data(db)
          st.rerun()

  with sub3:
    for i, item in enumerate(db["short"]):
      c1, c2 = st.columns([8, 2])
      with c1:
        st.write(f"**{i+1}. {item['q']}**")
      with c2:
        if st.button("ডিলিট", key=f"d_sh_{i}"):
          db["short"].pop(i)
          save_data(db)
          st.rerun()

# --- ট্যাব ৫: ফাইনাল প্রিভিউ ও ডাউনলোড/প্রিন্ট ---
with tab5:
  st.header("🖨️ ফাইনাল প্রশ্নপত্র প্রিভিউ ও ডাউনলোড/প্রিন্ট")
  show_answers = st.checkbox("উত্তরমালা সহ প্রদর্শন করুন (Answer Key)")

  page_orient = (
      "size: landscape;" if "Landscape" in orientation else "size: portrait;"
  )
  col_rule = "column-count: 2;" if "দুই কলাম" in columns_layout else ""

  db = st.session_state.db

  html_content = f"""
    <!DOCTYPE html>
    <html lang="bn">
    <head>
        <meta charset="UTF-8">
        <title>{exam_name} - {subject}</title>
        <style>
            @page {{ {page_orient} margin: 20mm; }}
            body {{ font-family: 'SolaimanLipi', Arial, sans-serif; font-size: {font_size}px; color: black; background: white; line-height: 1.6; }}
            .paper-container {{ max-width: 900px; margin: 0 auto; padding: 20px; }}
            .school-header {{ text-align: center; border-bottom: 2px solid black; padding-bottom: 10px; margin-bottom: 20px; }}
            .question-section {{ {col_rule} column-gap: 30px; }}
            .mb {{ margin-bottom: 15px; }}
        </style>
    </head>
    <body>
        <div class="paper-container">
            <div class="school-header">
                <h2>{school_name}</h2>
                <h3>{exam_name}</h3>
                <p><b>বিষয়:</b> {subject} | <b>শ্রেণি:</b> {class_name} | <b>সময়:</b> {time_limit} | <b>পূর্ণমান:</b> {total_marks}</p>
            </div>
    """

  if db["mcq"]:
    html_content += f"""
        <h4><b>অংশ-ক: বহু নির্বাচনী প্রশ্ন (MCQ)</b> [মান: {mcq_mark_per_q} × {mcq_total_q_to_answer} = {mcq_mark_per_q*mcq_total_q_to_answer}]</h4>
        <p>(যেকোনো {mcq_total_q_to_answer} টি প্রশ্নের উত্তর দাও)</p>
        <div class="question-section">
    """
    for idx, item in enumerate(db["mcq"], 1):
      html_content += f"""
            <div class="mb">
                <b>{idx}. {item['q']}</b><br>
                &nbsp;&nbsp;&nbsp;&nbsp;ক) {item['a']} &nbsp;&nbsp; খ) {item['b']} &nbsp;&nbsp; গ) {item['c']} &nbsp;&nbsp; ঘ) {item['d']}
            </div>
        """
    html_content += "</div><br>"

  if db["short"]:
    html_content += f"""
        <h4><b>অংশ-খ: সংক্ষিপ্ত প্রশ্ন</b> [মান: {short_mark_per_q} × {short_total_q_to_answer} = {short_mark_per_q*short_total_q_to_answer}]</h4>
        <p>(যেকোনো {short_total_q_to_answer} টি প্রশ্নের উত্তর দাও)</p>
    """
    for idx, item in enumerate(db["short"], 1):
      html_content += f"""
            <div class="mb">
                <b>{idx}. {item['q']}</b> ______ [{short_mark_per_q}]
            </div>
        """
    html_content += "<br>"

  if db["creative"]:
    html_content += "<h4><b>অংশ-গ: সৃজনশীল প্রশ্ন</b></h4>"
    html_content += (
        f"<p>(যেকোনো {creative_total_q_to_answer} টি প্রশ্নের উত্তর দাও)</p>"
    )
    for idx, item in enumerate(db["creative"], 1):
      html_content += f"""
            <div class="mb">
                <b>উদ্দীপক-{idx}:</b> {item['stem']}<br>
                &nbsp;&nbsp;&nbsp;&nbsp;(ক) {item['k']} <b>[১]</b><br>
                &nbsp;&nbsp;&nbsp;&nbsp;(খ) {item['kh']} <b>[২]</b><br>
                &nbsp;&nbsp;&nbsp;&nbsp;(গ) {item['g']} <b>[৩]</b><br>
                &nbsp;&nbsp;&nbsp;&nbsp;(ঘ) {item['gh']} <b>[৪]</b>
            </div>
        """

  if show_answers:
    html_content += "<hr><h3>🔑 উত্তরমালা (Answer Key)</h3>"
    if db["mcq"]:
      ans_str = ", ".join(
          [f"{i+1}. ({item['ans']})" for i, item in enumerate(db["mcq"])]
      )
      html_content += f"<p><b>MCQ উত্তর:</b> {ans_str}</p>"
    if db["short"]:
      html_content += "<p><b>সংক্ষিপ্ত প্রশ্নের উত্তর:</b></p><ul>"
      for i, item in enumerate(db["short"], 1):
        if item["ans"]:
          html_content += f"<li>{i}. {item['ans']}</li>"
      html_content += "</ul>"

  html_content += """
        </div>
    </body>
    </html>
    """

  st.download_button(
      label="📥 প্রশ্নপত্র ডাউনলোড করুন (HTML ফাইল - সহজে PDF করুন)",
      data=html_content,
      file_name="question_paper.html",
      mime="text/html",
      type="primary",
  )

  st.info(
      "💡 **টিপস:** ডাউনলোড করা HTML ফাইলটিতে ডাবল ক্লিক করে যেকোনো ব্রাউজারে"
      " ওপেন করুন এবং কিবোর্ডের **Ctrl + P** চেপে সরাসরি **Save as PDF** করে"
      " নিন।"
  )

  st.markdown("---")

  st.markdown("### 👀 লাইভ স্ক্রিন প্রিভিউ")
  st.markdown(
      f"""
    <div style="background-color: white; color: black; padding: 40px; border: 1px solid #ccc; border-radius: 5px;">
        <div style="text-align: center; border-bottom: 2px solid black; padding-bottom: 10px; margin-bottom: 20px;">
            <h2>{school_name}</h2>
            <h3>{exam_name}</h3>
            <p><b>বিষয়:</b> {subject} | <b>শ্রেণি:</b> {class_name} | <b>সময়:</b> {time_limit} | <b>পূর্ণমান:</b> {total_marks}</p>
        </div>
    """,
      unsafe_allow_html=True,
  )

  if db["mcq"]:
    st.markdown(
        f"#### **অংশ-ক: বহু নির্বাচনী প্রশ্ন (MCQ)** [মান: {mcq_mark_per_q} ×"
        f" {mcq_total_q_to_answer} = {mcq_mark_per_q*mcq_total_q_to_answer}]"
    )
    for idx, item in enumerate(db["mcq"], 1):
      st.markdown(f"**{idx}. {item['q']}**")
      st.markdown(
          f"&nbsp;&nbsp;&nbsp;&nbsp;ক) {item['a']} &nbsp;&nbsp; খ)"
          f" {item['b']} &nbsp;&nbsp; গ) {item['c']} &nbsp;&nbsp; ঘ)"
          f" {item['d']}"
      )
    st.markdown("<br>", unsafe_allow_html=True)

  if db["short"]:
    st.markdown(
        f"#### **অংশ-খ: সংক্ষিপ্ত প্রশ্ন** [মান: {short_mark_per_q} ×"
        f" {short_total_q_to_answer} = {short_mark_per_q*short_total_q_to_answer}]"
    )
    for idx, item in enumerate(db["short"], 1):
      st.markdown(f"**{idx}. {item['q']}** ______ [{short_mark_per_q}]")
    st.markdown("<br>", unsafe_allow_html=True)

  if db["creative"]:
    st.markdown("#### **অংশ-গ: সৃজনশীল প্রশ্ন**")
    for idx, item in enumerate(db["creative"], 1):
      st.markdown(f"**উদ্দীপক-{idx}:** {item['stem']}")
      st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;(ক) {item['k']} **[১]**")
      st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;(খ) {item['kh']} **[২]**")
      st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;(গ) {item['g']} **[৩]**")
      st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;(ঘ) {item['gh']} **[৪]**")
      st.markdown("<br>", unsafe_allow_html=True)

  if show_answers:
    st.markdown("<hr>### 🔑 উত্তরমালা (Answer Key)", unsafe_allow_html=True)
    if db["mcq"]:
      ans_str = ", ".join(
          [f"{i+1}. ({item['ans']})" for i, item in enumerate(db["mcq"])]
      )
      st.markdown(f"**MCQ উত্তর:** {ans_str}")
    if db["short"]:
      st.markdown("**সংক্ষিপ্ত প্রশ্নের উত্তর:**")
      for i, item in enumerate(db["short"], 1):
        if item["ans"]:
          st.markdown(f"{i}. {item['ans']}")

  st.markdown("</div>", unsafe_allow_html=True)
