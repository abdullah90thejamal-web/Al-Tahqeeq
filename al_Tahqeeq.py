import sqlite3
import pandas as pd
import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Al-Tahqeeq Research Hub", page_icon="📚", layout="wide"
)

# Database connection
DB_NAME = "al_tahqeeq_hub.db"

def execute_query(query, params=()):
  try:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()
    return True
  except Exception as e:
    return False

# App Header
st.title("📚 Al-Tahqeeq: Fiqhi Research Hub")
st.markdown("---")

# Sidebar navigation
menu = st.sidebar.selectbox(
    "Navigation",
    ["Dashboard", "Search & Research", "Add New Entry", "Manage Database"],
)

if menu == "Dashboard":
  st.subheader("📊 خوش آمدید - فقہی ریسرچ ڈیش بورڈ")
  st.info(
    "یہ نظام فقہی تحقیقات، مسائل اور حنفی فتاویٰ کو محفوظ اور تلاش کرنے کے لیے بنایا گیا ہے۔"
  )
  try:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    tables = cursor.fetchall()
    conn.close()
    if tables:
      st.success(f"ڈیٹا بیس کامیابی سے منسلک ہے! کل موجودہ ٹیبلز: {len(tables)}")
    else:
      st.warning("ڈیٹا بیس میں فی الحال کوئی ٹیبل موجود نہیں ہے۔")
  except Exception as e:
    st.error("ڈیٹا بیس سے رابطہ قائم کرنے میں مسئلہ پیش آیا۔")

elif menu == "Search & Research":
  st.subheader("🔍 فقہی تلاش و تحقیق (حنفی فتاویٰ و مسائل)")
  search_keyword = st.text_input("کوئی بھی مسئلہ، عنوان یا کی ورڈ درج کریں (مثلاً: نماز، روزہ، نکاح وغیرہ):")
  
  if st.button("تلاش شروع کریں"):
    if search_keyword.strip() != "":
      try:
        conn = sqlite3.connect(DB_NAME)
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';"
        tables_df = pd.read_sql_query(query, conn)

        if not tables_df.empty:
          found_results = False
          for table_name in tables_df["name"]:
            try:
              # یہ کوڈ آپ کے ڈیٹا بیس کے تمام ٹیبلز میں title، details یا content کے کالمز میں تلاش کرے گا
              search_query = f"SELECT * FROM {table_name} WHERE title LIKE ? OR details LIKE ? OR content LIKE ?"
              pattern = f"%{search_keyword}%"
              df = pd.read_sql_query(search_query, conn, params=(pattern, pattern, pattern))
              
              if not df.empty:
                st.success(f"ٹیبل '{table_name}' میں درج ذیل نتائج پائے گئے:")
                st.dataframe(df)
                found_results = True
            except Exception:
              continue

          if not found_results:
            st.warning("اس کی ورڈ سے متعلق ڈیٹا بیس میں کوئی نتیجہ نہیں ملا۔")
        else:
          st.warning("ڈیٹا بیس میں تلاش کے لیے کوئی ٹیبل موجود نہیں ہے۔")
        conn.close()
      except Exception as e:
        st.error(f"تلاش کے دوران خرابی پیش آئی: {e}")
    else:
      st.warning("براہ کرم تلاش کے لیے کوئی لفظ درج کریں۔")

elif menu == "Add New Entry":
  st.subheader("➕ نیا تحقیقی اندراج شامل کریں")
  with st.form("research_form"):
    title = st.text_input("عنوان (Topic Title)")
    category = st.selectbox("فقہی باب / کیٹیگری", ["عبادات", "معاملات", "نکاح و طلاق", "جنایات", "متفرق"])
    details = st.text_area("تحقیقی تفصیلات و حوالہ جات")
    submitted = st.form_submit_button("محفوظ کریں")

    if submitted:
      if title and details:
        query = "CREATE TABLE IF NOT EXISTS research_entries (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, category TEXT, details TEXT);"
        execute_query(query)
        insert_query = "INSERT INTO research_entries (title, category, details) VALUES (?, ?, ?);"
        success = execute_query(insert_query, (title, category, details))
        if success:
          st.success("کامیابی کے ساتھ ڈیٹا محفوظ ہو گیا!")
        else:
          st.error("ڈیٹا محفوظ کرتے وقت خرابی پیش آئی۔")
      else:
        st.warning("براہ کرم عنوان اور تفصیل درج کریں۔")

elif menu == "Manage Database":
  st.subheader("⚙️ ڈیٹا بیس مینجمنٹ")
  st.text("یہاں آپ اپنی ڈیٹا بیس فائل کی حالت دیکھ سکتے ہیں۔")
  if st.button("تمام ٹیبلز دکھائیں"):
    try:
      conn = sqlite3.connect(DB_NAME)
      df = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", conn)
      conn.close()
      st.dataframe(df)
    except Exception as e:
      st.error(f"خرابی: {e}")