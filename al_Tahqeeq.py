import tkinter as tk
from tkinter import messagebox
import sqlite3

DB_NAME = 'al_tahqeeq_hub.db'

def setup_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS fatawa_hub
                      (id INTEGER PRIMARY KEY, unwan TEXT, kitab_naam TEXT, jild_safha TEXT, arabi_matan TEXT, poori_tafseel TEXT)''')
    
    cursor.execute("SELECT COUNT(*) FROM fatawa_hub")
    count = cursor.fetchone()[0]
    
    if count == 0:
        sample_data = [
            ("كتاب الصلاة - شرائط الصلاة وتعيين الأوقات", "الهدية شرح بداية المبتدي (Al-Hidayah)", "المجلد الأول، صفحة 124", 
             "«شرائط الصلاة خمسة: الطهارة عن الحدث والخبث، ستر العورة، استقبل القبلة، الوقت، النية...»", 
             "Hidayah ki is ibarat mein namaz ki sharaait ka tafseeli bayan hai. Imam Al-Marghinani (Rahmatullah Alaih) farmate hain ke namaz ke sihat ke liye 5 buniyadi shartein hain: 1. Taharat (wuzu ya ghusl), 2. Satr-e-awrah, 3. Istiqbal-e-Qiblah, 4. Waqt ka dakhil hona, 5. Niyat. Fiqh-e-Hanafi ke mutabiq waqt ka dakhil hona aisi shart hai ke agar waqt se pehle namaz ada ki jaye toh bilkul durust nahi hoti."),
            
            ("كتاب البيوع - باب البيع الفاسد والباطل", "رد المحتار على الدر المختار (Fatawa Shami)", "المجلد الخامس، صفحة 52", 
             "«البيع الفاسد ما هو مشروع بأصله دون وصفه، كالبيع بثمن مجهول جهالة فاحشة...»", 
             "Allama Ibn Abideen Shami (Rahmatullah Alaih) Fatawa Shami mein likhte hain ke Fiqh-e-Hanafi ke nazdeek 'Bai' (Transaction) ki do qismein hain jo mamnu hain: Bai' Batil aur Bai' Fasid. Bai' Fasid woh hai jo asal ke aitbaar se jaiz ho lekin kisi kharji wasf (quality) ki wajah se mamnu ho jaye (jaise price mein aisi jahalat jo naza ka sabab bane)."),
            
            ("كتاب الطلاق - صريح الطلاق وكناياته", "الفتاوى الهندية (Fatawa Alamgiri)", "المجلد الأول، صفحة 355", 
             "«الطلاق الصريح يقع به الطلاق الرجعي، ولا يحتاج إلى النية...»", 
             "Fatawa Alamgiri mein darj hai ke Talaq-e-Sareeh (waazeh alfaz jaise 'tujhe talaq hai') se talaq-e-raj'i waqie ho jati hai, aur isme shohar ki niyat ki zaroorat nahi hoti. Albatta, agar alfaz kinaayat (ambiguous) hon toh wahan niyat ya hal-e-mazakarat ki shart hoti hai."),
            
            ("كتاب الربا والصرف - أحكام المعاملات المصرفية المعاصرة", "فتاوى عثماني (Fatawa Usmani)", "المجلد الثالث، صفحة 210", 
             "«حكم الأوراق النقديّة أنها تقوم مقام الذهب والفضة في أحكام الربا والزكاة...»", 
             "Mufti Taqi Usmani (Hafizahullah) Fatawa Usmani mein tahqeeq farmate hain ke jadid kaagzi currency (Fiat Currency) shar'i aitebaar se 'Saman-e-Asli' (Medium of Exchange) ke hukm mein hai. Isliye is par wohi ahkaam jari honge jo Sona aur Chandi par jari hote hain.")
        ]
        cursor.executemany("INSERT INTO fatawa_hub (unwan, kitab_naam, jild_safha, arabi_matan, poori_tafseel) VALUES (?, ?, ?, ?, ?)", sample_data)
        conn.commit()
    
    conn.close()

current_records = []

def search_fatawa():
    global current_records
    keyword = entry_search.get().strip()
    
    list_box.delete(0, tk.END)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM fatawa_hub WHERE unwan LIKE ? OR kitab_naam LIKE ? OR arabi_matan LIKE ? OR poori_tafseel LIKE ?", 
                   ('%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%'))
    current_records = cursor.fetchall()
    
    for row in current_records:
        list_box.insert(tk.END, f"📜 [ {row[1]} ]  --->  {row[2]}  ({row[3]})")
        
    if not current_records:
        list_box.insert(tk.END, "Koi munasib nateeja nahi mila! Mazeed alfaz badal kar talash karein.")
        
    conn.close()

def open_detail_window(row_data):
    detail_win = tk.Toplevel(app)
    detail_win.title(f"Al-Tahqeeq - Jiza: {row_data[1]}")
    detail_win.geometry("750x600")
    detail_win.config(bg="#f8fafc")
    
    nav_frame = tk.Frame(detail_win, bg="#e2e8f0", height=40)
    nav_frame.pack(fill=tk.X, padx=5, pady=5)
    
    def go_back():
        detail_win.destroy()

    btn_back = tk.Button(nav_frame, text=" ⬅️️ Wapas (Back) ", command=go_back, bg="#cbd5e1", font=("Arial", 9, "bold"))
    btn_back.pack(side=tk.LEFT, padx=5, pady=5)
    
    btn_home = tk.Button(nav_frame, text=" 🏠 Main Menu ", command=detail_win.destroy, bg="#cbd5e1", font=("Arial", 9, "bold"))
    btn_home.pack(side=tk.LEFT, padx=5, pady=5)
    
    tk.Label(nav_frame, text="Al-Tahqeeq Research Viewer", bg="#e2e8f0", fg="#475569", font=("Arial", 9, "italic")).pack(side=tk.RIGHT, padx=10)

    tk.Label(detail_win, text=row_data[1], font=("Arial", 12, "bold", "underline"), fg="#1e3a8a", bg="#f8fafc", wraplength=700).pack(pady=10)
    tk.Label(detail_win, text=f"📖 Kitab: {row_data[2]}  |  📍 Hawala: {row_data[3]}", font=("Arial", 10, "bold"), fg="#0d9488", bg="#f8fafc").pack(pady=2)
    
    tk.Label(detail_win, text="Arabi Matan (اصل عبارت):", bg="#f8fafc", font=("Arial", 9, "bold"), fg="#b45309").pack(anchor="w", padx=25, pady=2)
    arabi_box = tk.Text(detail_win, wrap=tk.WORD, width=82, height=4, font=("Traditional Arabic", 12), bg="#fffbeb", fg="#78350f")
    arabi_box.pack(pady=2, padx=20)
    arabi_box.insert(tk.END, row_data[4])
    arabi_box.config(state=tk.DISABLED)
    
    tk.Label(detail_win, text="Mufassal Fiqhi Tafseel wa Sharh (تفصیلی بحث):", bg="#f8fafc", font=("Arial", 9, "bold"), fg="#1e3a8a").pack(anchor="w", padx=25, pady=5)
    text_area = tk.Text(detail_win, wrap=tk.WORD, width=82, height=14, font=("Arial", 10), bg="#ffffff")
    text_area.pack(pady=2, padx=20)
    text_area.insert(tk.END, row_data[5])
    text_area.config(state=tk.DISABLED)

def show_details(event):
    selected_index = list_box.curselection()
    if not selected_index:
        return
    index = selected_index[0]
    if index < len(current_records):
        open_detail_window(current_records[index])

# --- MAIN APP INTERFACE ---
setup_db()

app = tk.Tk()
app.title("Al-Tahqeeq: Fatawa & Fiqh-e-Hanafi Index")
app.geometry("800x680")
app.config(bg="#f1f5f9")

header_frame = tk.Frame(app, bg="#1e3a8a", height=60)
header_frame.pack(fill=tk.X)
tk.Label(header_frame, text="🏛️ Al-Tahqeeq (التحقيق) - Research Hub", bg="#1e3a8a", fg="white", font=("Arial", 15, "bold")).pack(pady=12)

search_frame = tk.Frame(app, bg="#f1f5f9")
search_frame.pack(pady=15)

tk.Label(search_frame, text="Kutub mein Lafz talash karein (اردو / عربی):", bg="#f1f5f9", font=("Arial", 10, "bold"), fg="#334155").pack(side=tk.LEFT, padx=5)
entry_search = tk.Entry(search_frame, width=40, font=("Arial", 12))
entry_search.pack(side=tk.LEFT, padx=5)

btn_search = tk.Button(search_frame, text=" 🔍 Talash Karein ", command=search_fatawa, bg="#0d9488", fg="white", font=("Arial", 10, "bold"))
btn_search.pack(side=tk.LEFT, padx=5)

tk.Label(app, text="💡 Kisi bhi nateejay par Double-Click karein taake Arabi matan aur poori tafseel khul jaye:", bg="#f1f5f9", fg="#c2410c", font=("Arial", 9, "bold")).pack(pady=2)

list_box = tk.Listbox(app, width=110, height=22, font=("Arial", 10), bg="#ffffff", selectbackground="#0d9488")
list_box.pack(pady=10, padx=20)
list_box.bind("<Double-Button-1>", show_details)

def load_initial():
    entry_search.delete(0, tk.END)
    search_fatawa()

load_initial()

app.mainloop()
