import sqlite3
import pandas as pd
import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Al-Tahqeeq Research Hub", page_icon="📚", layout="wide"
)

# Database connection function
DB_NAME = "al_tahqeeq_hub.db"


def run_query(query, params=()):
  try:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(query, params)
    result = cursor.fetchall()
    conn.close()
    return result
  except Exception as e:
    return None


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
    "یہ نظام فقہی تحقیقات، مسائل اور حوالجات کو محفوظ اور منظم کرنے کے لیے بنایا"
    " گیا ہے۔"
  )

  # Basic statistics from database if table exists
  try:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Check tables
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE"
        " 'sqlite_%';"
    )
    tables = cursor.fetchall()
    conn.close()

    if tables:
      st.success(
          f"ڈابٹ بیس کامیابی سے منسلک ہے! کل موجودہ ٹیبلز: {len(tables)}"
      )
    else:
      st.warning(
          "ڈابٹ بیس میں فی الحال کوئی ٹیبل موجود نہیں ہے۔ براہ کرم نیا ڈیٹا شامل"
          " کریں۔"
      )
  except Exception as e:
    st.error(
        "ڈابٹ بیس سے رابطہ قائم کرنے میں مسئلہ پیش آیا۔ براہ کرم یقینی بنائیں کہ"
        " `al_tahqeeq_hub.db` موجود ہے۔"
    )

elif menu == "Search & Research":
  st.subheader("🔍 فقہی تلاش و تحقیق (حنفی فتاویٰ و مسائل)")

  # Search input
  search_keyword = st.text_input(
      "کوئی بھی مسئلہ، عنوان یا کی ورڈ درج کریں (مثلاً: نماز، روزہ، نکاح"
      " وغیرہ):"
  )

  if st.button("تلاش شروع کریں"):
    if search_keyword.strip() != "":
      try:
        conn = sqlite3.connect(DB_NAME)
        # ییہاں آپ اپنے ٹیبل کا نام اور کالم کا نام اپنی مرضی سے بدل سکتے ہیں
        # فی الحال ہم تمام ٹیبلز میں سرچ کرنے کی کوشش کرتے ہیں یا ایک عام ٹیبل مان لیتے ہیں
        query = (
            "SELECT * FROM sqlite_master WHERE type='table' AND name NOT LIKE"
            " 'sqlite_%';"
        )
        tables_df = pd.read_sql_query(query, conn)

        if not tables_df.empty:
          found_results = False
          for table_name in tables_df["name"]:
            # ہر ٹیبل میں تلاش کریں (فرض کرتے ہیں کالمز میں title یا details موجود ہیں)
            try:
              search_query = f"SELECT * FROM {table_name} WHERE title LIKE ? OR details LIKE ? OR content LIKE ?"
              pattern = f"%{search_keyword}%"
              df = pd.read_sql_query(
                  search_query, conn, params=(pattern, pattern, pattern)
              )
              if not df.empty:
                st.success(
                    f"ٹیبل '{table_name}' میں نتائج پائے گئے:"
                )
                st.dataframe(df)
                found_results = True
            except Exception:
              # اگر کسی ٹیبل میں یہ کالم نہ ہوں تو اگلا ٹیبل چیک کرے
              continue

          if not found_results:
            st.warning(
                "اس کی ورڈ سے متعلق ڈیٹا بیس میں کوئی نتیجہ نہیں ملا۔ براہ کرم"
                " کوئی دوسرا لفظ تلاش کریں۔"
            )
        else:
          st.warning("ڈیٹا بیس میں کوئی ٹیبل موجود نہیں ہے۔")
        conn.close()
      except Exception as e:
        st.error(f"تلاش کے دوران خرابی پیش آئی: {e}")
    else:
      st.warning("براہ کرم تلاش کے لیے کوئی لفظ درج کریں۔")

elif menu == "Add New Entry":
  st.subheader("➕ نیا تحقیقی اندراج شامل کریں")
  with st.form("research_form"):
    title = st.text_input("عنوان (Topic Title)")
    category = st.selectbox(
        "فقہی باب / کیٹیگری",
        ["عبادات", "معاملات", "نکاح و طلاق", "جنایات", "متفرق"],
    )
    details = st.text_area("تحقیقی تفصیلات و حوالہ جات")
    submitted = st.form_submit_button("محفوظ کریں")

    if submitted:
      if title and details:
        # Example insertion query (adjust table columns as per your actual db structure)
        query = "CREATE TABLE IF NOT EXISTS research_entries (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, category TEXT, details TEXT);"
        execute_query(query)

        insert_query = "INSERT INTO research_entries (title, category, details) VALUES (?, ?, ?);"
        success = execute_query(insert_query, (title, category, details))

        if success:
          st.success("کامیابی کے ساتھ ڈیٹا محفوظ ہو گیا!")
        else:
          st.error("ڈیٹا محفوظ کرتے وقت خرابی پیش آئی۔")
      else:
        st.warning("براہ کرم کم از کم عنوان اور تفصیل درج کریں۔")

elif menu == "Manage Database":
  st.subheader("⚙️ ڈاٹا بیس مینجمنٹ")
  st.text("یہاں آپ اپنی ڈاٹا بیس فائل کی حالت دیکھ سکتے ہیں۔")
  if st.button("تمام ٹیبلز دکھائیں"):
    try:
      conn = sqlite3.connect(DB_NAME)
      df = pd.read_sql_query(
          "SELECT name FROM sqlite_master WHERE type='table';", conn
      )
      conn.close()
      st.dataframe(df)
    except Exception as e:
      st.error(f"خرابی: {e}")