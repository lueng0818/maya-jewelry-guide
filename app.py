import os
import calendar
from PIL import Image

import pandas as pd
import streamlit as st

# ────────────── Path Setup ──────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
IMG_DIR  = os.path.join(BASE_DIR, "images")

# ────────────── 1. Tru-Mi Mapping Data (更新作品名與連結) ──────────────
# 連結策略：
# - 一般系列產品 -> https://www.tru-mi.com/collections
# - 婚戒/對戒 -> https://www.tru-mi.com/ (官網首頁導航較清晰) 或 https://www.tru-mi.com/wedding
# - 專屬訂製 -> https://www.tru-mi.com/custom-jewelry

totem_trumi = {
    # 🔴 東方紅色家族
    "紅龍": {
        "series": "Memory 系列 (記憶)",
        "item": "Memory系列-樹枝款耳環 / 戒指",
        "desc": "紅龍象徵古老的記憶與滋養。Memory系列的樹枝紋理，如同家族與生命的根系，將妳與大地母親的能量緊密連結。",
        "url": "https://www.tru-mi.com/collections/memory"
    },
    "紅蛇": {
        "series": "Resilience 系列 (韌性)",
        "item": "Resilience系列-斜紋耳環 / 領帶系列",
        "desc": "紅蛇充滿生命力與生存本能。Resilience系列的斜紋設計與俐落切角，象徵在都市叢林中靈活穿梭的韌性與魅力。",
        "url": "https://www.tru-mi.com/collections/resilience"
    },
    "紅月": {
        "series": "Minilife 系列 (情緒流動)",
        "item": "Minilife系列-夢想的海洋 / 冬日的約定",
        "desc": "紅月是宇宙之水。Minilife系列中的海洋元素，以溫柔的波浪線條接住妳的情緒，療癒每一滴眼淚與歡笑。",
        "url": "https://www.tru-mi.com/collections/minilife"
    },
    "紅天行者": {
        "series": "Morning Star 系列 (指引)",
        "item": "晨星系列-星願項鍊",
        "desc": "紅天行者穿梭時空。晨星系列的星芒如同夜空中的羅盤，為喜愛探索與冒險的妳，指引正確的方向。",
        "url": "https://www.tru-mi.com/collections/morning-star"
    },
    "紅地球": {
        "series": "Memory 系列 (根植大地)",
        "item": "Memory系列-單花耳環 / 樹枝款",
        "desc": "紅地球與自然共時。Memory系列保留了植物有機的生長紋理，讓佩戴飾品的妳時刻保持接地 (Grounding) 的穩定頻率。",
        "url": "https://www.tru-mi.com/collections/memory"
    },
    # ⚪ 北方白色家族
    "白風": {
        "series": "Flawless 系列 (純粹溝通)",
        "item": "Flawless系列-孔珠套鍊 / 滾珠銀耳環",
        "desc": "白風傳遞靈性與溝通。Flawless系列極簡的孔珠設計，象徵話語的圓滿與通透，讓妳的溝通如風般自由流動。",
        "url": "https://www.tru-mi.com/shop"
    },
    "白世界橋": {
        "series": "婚戒物語 (連結與承諾)",
        "item": "Tru-Mi 雙色拼接對戒 / 婚戒訂製",
        "desc": "白世界橋是連結兩個世界的通道。Tru-Mi 的婚戒與對戒系列，象徵跨越個體、連結彼此的神聖承諾。",
        "url": "https://www.tru-mi.com/shop"
    },
    "白狗": {
        "series": "Beloved 系列 (愛與陪伴)",
        "item": "Beloved系列-鈴鐺的祝福 / 寵物珠寶訂製",
        "desc": "白狗代表無條件的愛與忠誠。無論是寵物珠寶或Beloved系列的溫暖設計，都滋養著妳充滿愛的心輪。",
        "url": "https://www.tru-mi.com/baby-gifts-beloved"
    },
    "白巫師": {
        "series": "Minilife 系列 (內在魔法)",
        "item": "Minilife系列-秘密花園 / 幸福的秘密",
        "desc": "白巫師安住在當下。Minilife系列中精緻微小的設計，彷彿施了魔法的護身符，提醒妳向內觀看，看見心中的秘密花園。",
        "url": "https://www.tru-mi.com/collections/minilife"
    },
    "白鏡": {
        "series": "Flawless 系列 (映照真實)",
        "item": "Flawless系列-滾珠銀戒指 (亮面拋光)",
        "desc": "白鏡反映真相。Flawless系列經過精細拋光的銀飾，如鏡面般映照出真實的自己，展現無窮無盡的秩序之美。",
        "url": "https://www.tru-mi.com/collections/flawless"
    },
    # 🔵 西方藍色家族
    "藍夜": {
        "series": "Morning Star 系列 (夢想顯化)",
        "item": "晨星系列-星願項鍊 (鑲鑽/寶石款)",
        "desc": "藍夜是夢想家的搖籃。佩戴晨星系列，象徵將直覺與夢境顯化為現實，守護妳內在那個豐盛璀璨的星空。",
        "url": "https://www.tru-mi.com/collections/morning-star"
    },
    "藍手": {
        "series": "專屬訂製 (創造與療癒)",
        "item": "Tru-Mi 故事訂製 / 手作體驗課程",
        "desc": "藍手是實踐與創造之手。推薦妳參與「手作體驗」或「全訂製服務」，親手打造或參與設計，讓飾品成為妳療癒與創造的證明。",
        "url": "https://www.tru-mi.com/custom-jewelry"
    },
    "藍猴": {
        "series": "Beloved 系列 (遊戲與童心)",
        "item": "Beloved系列-搖搖馬手鍊 / 兔手鍊 / 皇冠",
        "desc": "藍猴看穿幻象，享受遊戲。Beloved系列充滿童心的設計（如搖搖馬、小兔子），能喚醒妳內在小孩的幽默與純真快樂。",
        "url": "https://www.tru-mi.com/baby-gifts-beloved"
    },
    "藍鷹": {
        "series": "Resilience 系列 (視野與格局)",
        "item": "Resilience系列-領帶耳環 / 大領帶套鍊",
        "desc": "藍鷹擁有高遠的視野。Resilience系列的領帶造型象徵著專業、願景與力量，助妳在事業藍圖中展翅高飛，看見更遠的風景。",
        "url": "https://www.tru-mi.com/collections/resilience"
    },
    "藍風暴": {
        "series": "Minilife 系列 (能量蛻變)",
        "item": "Minilife系列-夢想的海洋 (波浪流動款)",
        "desc": "藍風暴帶來蛻變。海洋主題飾品中起伏的波浪線條，象徵著妳擁抱變動、轉化能量的強大本質，在風暴中心保持平靜。",
        "url": "https://www.tru-mi.com/collections/minilife"
    },
    # 🟡 南方黃色家族
    "黃種子": {
        "series": "Memory 系列 (潛能開花)",
        "item": "Memory系列-單花耳環 / 戒指",
        "desc": "黃種子蘊含開花的意圖。Memory系列中的花朵造型，象徵著耐心與成長，祝福妳心中那顆夢想的種子能順利破土而出。",
        "url": "https://www.tru-mi.com/collections/memory"
    },
    "黃星星": {
        "series": "Morning Star & Flawless (藝術之美)",
        "item": "晨星系列 (星鑽) / Flawless 極致工藝",
        "desc": "黃星星追求優雅與藝術。晨星系列的閃耀光芒，或Flawless系列的極致工藝，呼應了妳天生要在人群中發光發熱的藝術家特質。",
        "url": "https://www.tru-mi.com/collections/morning-star"
    },
    "黃人": {
        "series": "Mi 系列 (自由意志)",
        "item": "Mi系列-告白項鍊/手鍊 (刻字訂製)",
        "desc": "黃人強調智慧與自由意志。透過 Mi 系列將妳的人生格言、信念刻在飾品上，時刻提醒自己做出有意識的選擇。",
        "url": "https://www.tru-mi.com/collections/mi"
    },
    "黃戰士": {
        "series": "Resilience 系列 (無畏勇氣)",
        "item": "Resilience系列-領帶戒指 / 幾何造型",
        "desc": "黃戰士無畏提問。Resilience系列如同妳的隱形鎧甲，幾何結構象徵才智與勇氣，陪伴妳面對挑戰，勇往直前。",
        "url": "https://www.tru-mi.com/collections/resilience"
    },
    "黃太陽": {
        "series": "Morning Star 系列 (溫暖之光)",
        "item": "晨星系列 (金色款/K金)",
        "desc": "黃太陽是宇宙之火。選擇金色的晨星飾品，象徵妳無私溫暖的光芒，照亮自己也溫暖周圍的人，展現大氣的領袖風範。",
        "url": "https://www.tru-mi.com/collections/morning-star"
    }
}

# ────────────── 2. Tone Data (13調性-佩戴建議) ──────────────
tone_advice = {
    1:  {"name": "磁性", "style": "【單戴聚焦】選擇一條最能代表妳故事的項鍊，單獨佩戴，讓它成為全身能量的錨點。"},
    2:  {"name": "月亮", "style": "【對稱平衡】佩戴成對的耳環，或是選擇對戒系列，平衡內在的二元性與選擇。"},
    3:  {"name": "電力", "style": "【動態連結】選擇有垂墜感、會隨身體擺動的耳飾或手鍊，啟動連結的能量。"},
    4:  {"name": "自我存在", "style": "【結構堆疊】利用方正或線條感強的戒指進行疊戴 (Stacking)，建立穩定的能量場。"},
    5:  {"name": "超頻", "style": "【核心自信】選擇體積較大或設計感強烈的「主戒」或「長鍊」，展現妳的影響力。"},
    6:  {"name": "韻律", "style": "【舒適流動】選擇佩戴感最舒適、圓潤的 Flawless 滾珠系列，讓身心處於平衡節奏。"},
    7:  {"name": "共振", "style": "【直覺感應】閉上眼，用手觸摸 Tru-Mi 的飾品，選擇當下最有「溫度」的那一件。"},
    8:  {"name": "銀河", "style": "【和諧呼應】嘗試「項鍊+耳環」或「戒指+手鍊」的成套搭配，整合全身頻率。"},
    9:  {"name": "太陽", "style": "【意圖閃耀】選擇有鑲嵌寶石或鑽石的款式，讓光芒隨著妳的意圖向外脈動。"},
    10: {"name": "行星", "style": "【完美顯化】選擇做工最精細、金工細節最豐富的訂製款，顯化妳對完美的追求。"},
    11: {"name": "光譜", "style": "【自由混搭】打破規則！將不同系列 (如 Resilience 混搭 Memory) 自由組合，釋放真實自我。"},
    12: {"name": "水晶", "style": "【分享與愛】這是一件適合與閨蜜或伴侶一起佩戴的飾品 (如對鍊)，共享水晶般的清澈能量。"},
    13: {"name": "宇宙", "style": "【超越存在】選擇設計最簡約、甚至留白的款式 (如素銀)，象徵包容一切的宇宙虛空。"}
}

# ────────────── Page Config & CSS ──────────────
st.set_page_config(page_title="Tru-Mi × Maya 能量選品", layout="wide", page_icon="💍")
st.markdown(
    """<style>
    .hero {padding:3rem 2rem; text-align:center; background: linear-gradient(135deg, #FFF5F7 0%, #E6EEF5 100%); border-radius: 15px; margin-bottom: 2rem;}
    .hero h1 {font-size:2.5rem; font-weight:700; color: #555; margin-bottom:0.5rem; font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;}
    .hero p  {font-size:1.1rem; color: #777;}
    
    .footer {position:fixed; bottom:0; width:100%; background:#333; color:white; text-align:center; padding:1rem; z-index:999;}
    .footer a {color:#F8BBD0; text-decoration:none; margin:0 0.5rem;}
    
    div[data-testid="stContainer"] {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        border: 1px solid #f5f5f5;
    }
    
    .btn-trumi {
        display: inline-block;
        padding: 10px 20px;
        background-color: #D4AF37;
        color: white !important;
        text-decoration: none;
        border-radius: 5px;
        font-weight: bold;
        margin-top: 10px;
        text-align: center;
        transition: all 0.3s ease;
    }
    .btn-trumi:hover {
        background-color: #B59025;
        transform: translateY(-2px);
    }
    
    .ritual-box {
        background-color: #fafafa;
        padding: 20px;
        border-left: 5px solid #D4AF37;
        margin-top: 20px;
        font-size: 0.95rem;
    }
    </style>""",
    unsafe_allow_html=True,
)

# ────────────── Hero Section ──────────────
st.markdown(
    """
    <section class="hero">
      <h1>Tru-Mi × Maya 能量選品</h1>
      <p>探索妳的靈魂印記，遇見專屬於妳的 Tru-Mi 故事珠寶</p>
    </section>
    """,
    unsafe_allow_html=True,
)

# ────────────── Load Data ──────────────
try:
    kin_start   = pd.read_csv(os.path.join(DATA_DIR, "kin_start_year.csv"), index_col="年份")["起始KIN"].to_dict()
    month_accum = pd.read_csv(os.path.join(DATA_DIR, "month_day_accum.csv"),   index_col="月份")["累積天數"].to_dict()
    kin_basic   = pd.read_csv(os.path.join(DATA_DIR, "kin_basic_info.csv"))
except Exception as e:
    st.error(f"❌ 資料載入失敗：{e}")
    st.stop()

# ────────────── Sidebar Input ──────────────
st.sidebar.header("📅 輸入生日，尋找妳的命定飾品")
year = st.sidebar.selectbox("出生年份 (西元)", sorted(kin_start.keys()), index=sorted(kin_start.keys()).index(1990))
month = st.sidebar.selectbox("出生月份", list(range(1,13)), index=0)
max_day = calendar.monthrange(year, month)[1]
day = st.sidebar.slider("出生日期", 1, max_day, 1)

# ────────────── KIN & Tone Calculation ──────────────
start_kin = kin_start.get(year)
if start_kin is None:
    st.sidebar.error("⚠️ 此年份無起始 KIN")
    st.stop()

raw = start_kin + month_accum.get(month,0) + day
mod = raw % 260
kin = 260 if mod==0 else mod

tone_number = kin % 13
if tone_number == 0:
    tone_number = 13

# ────────────── 顯示基本資訊 ──────────────
subset = kin_basic[kin_basic["KIN"]==kin]
if subset.empty:
    st.error(f"❓ 找不到 KIN {kin} 資料")
    st.stop()
info = subset.iloc[0]
totem = info["圖騰"]

# Get Mapped Data
trumi_rec = totem_trumi.get(totem, {})
tone_rec = tone_advice.get(tone_number, {})

st.markdown(f"### 🔮 妳的靈魂印記：{kin} {totem} (調性 {tone_number})")

col_img, col_info = st.columns([1, 4])
with col_img:
    img_file = os.path.join(IMG_DIR, f"{totem}.png")
    if os.path.exists(img_file):
        st.image(Image.open(img_file), use_container_width=True)

with col_info:
    if trumi_rec:
        st.success(f"**能量共振系列：Tru-Mi {trumi_rec['series']}**")
        st.write(f"推薦單品：{trumi_rec['item']}")
        st.caption(trumi_rec['desc'])
        
        # 動態生成按鈕文字與連結
        btn_text = "前往 Tru-Mi 官網逛逛 👉"
        if "訂製" in trumi_rec['series']:
            btn_text = "前往 Tru-Mi 專屬訂製頁面 👉"
            
        st.markdown(f'<a href="{trumi_rec["url"]}" target="_blank" class="btn-trumi">{btn_text}</a>', unsafe_allow_html=True)
    else:
        st.warning("目前尚無此圖騰對應資料")

# ────────────── 選品顧問主區塊 ──────────────
st.divider()

col1, col2 = st.columns(2)

# 左欄：Tru-Mi 系列推薦 (What to buy)
with col1:
    st.markdown("#### 💍 命定款式推薦 (Collection)")
    st.caption("由妳的太陽圖騰決定")
    
    if trumi_rec:
        with st.container(border=True):
            st.markdown(f"**✨ 推薦系列：{trumi_rec['series']}**")
            st.write(trumi_rec['desc'])
            
            st.info("💡 **為什麼適合妳？**\n這款飾品的設計語言，能將妳內在無形的圖騰能量，轉化為有形的守護力量。")

# 右欄：佩戴風格建議 (How to wear)
with col2:
    st.markdown("#### 🎨 佩戴風格建議 (Style)")
    st.caption("由妳的銀河調性決定")
    
    if tone_rec:
        with st.container(border=True):
            st.markdown(f"**🎵 調性：{tone_rec['name']}**")
            st.write(tone_rec['style'])
            
            st.info("💡 **能量加分秘訣**\n按照這個方式佩戴，能協助妳在日常生活中穩定頻率，展現最舒服的自己。")

# ────────────── 能量啟動儀式 ──────────────
with st.expander("🕯️ 查看：Tru-Mi 飾品・能量啟動儀式 (Activation Ritual)"):
    st.markdown(
        """
        <div class="ritual-box">
        <p>當妳收到 Tru-Mi 的精美飾品後，請花 3 分鐘進行這個小儀式，讓它正式成為妳的夥伴。</p>
        
        <h4>1. 歸零 (Reset)</h4>
        <p>將飾品握在掌心，閉上眼，觀想一道白光包圍它，心念：「我淨化此物，回歸純淨。」</p>
        
        <h4>2. 連結 (Connect)</h4>
        <p>將飾品貼近胸口(心輪)。深呼吸，感受 Tru-Mi 手作金工的溫度與妳的心跳同步。</p>
        
        <h4>3. 啟動 (Activate)</h4>
        <p>對著飾品輕聲說出妳的願望或意圖 (例如：<strong>{}</strong>)。最後，對它吹一口氣封存能量。</p>
        
        <h4>4. 佩戴 (Wear)</h4>
        <p>戴上的瞬間，相信它將守護妳的故事，陪伴妳閃耀每一天。</p>
        </div>
        """.format(trumi_rec.get('desc', '守護我的夢想')[:20] + "..."), 
        unsafe_allow_html=True
    )

# ────────────── 固定 Footer ──────────────
st.markdown(
    """
    <div style="margin-bottom: 80px;"></div>
    <footer class="footer">
      <p>Designed for Tru-Mi Jewelry | 星際瑪雅能量顧問</p>
      <a href="https://www.tru-mi.com/" target="_blank">👉 Tru-Mi 官網</a> 
      <a href="https://www.facebook.com/trumi.jewelry/" target="_blank">👉 FB 粉絲頁</a>
    </footer>
    """,
    unsafe_allow_html=True
)
