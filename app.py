import os
import calendar
from PIL import Image

import pandas as pd
import streamlit as st

# ────────────── Path Setup ──────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
IMG_DIR  = os.path.join(BASE_DIR, "images")

# ────────────── 1. Jewelry Data: Totems (20圖騰-寶石與設計) ──────────────
totem_jewelry = {
    # 🔴 東方紅色家族
    "紅龍": {
        "gem": "紅寶石 (Ruby)、紅色石榴石 (Garnet)",
        "design": "古幣造型項鍊、誕生石系列、圓形浮雕 (Cameo)",
        "metal": "玫瑰金 (Rose Gold)",
        "vibe": "生命力、啟動、古老智慧"
    },
    "紅蛇": {
        "gem": "紅瑪瑙 (Carnelian)、紅碧玉",
        "design": "細緻的蛇形戒指 (Snake ring)、貼合肌膚的K金細鍊 (Body chain)、紅繩手鍊",
        "metal": "玫瑰金 / 黃K金",
        "vibe": "熱情、本能、身體意識"
    },
    "紅月": {
        "gem": "月光石 (Moonstone)、珍珠 (Pearl)、珊瑚",
        "design": "水滴型切割 (Teardrop)、新月造型、波浪紋路的金屬戒指",
        "metal": "玫瑰金 / 銀",
        "vibe": "流動、淨化、柔美"
    },
    "紅天行者": {
        "gem": "紅紋石、紅碧璽",
        "design": "羽毛雕刻、指南針造型、長鍊設計 (Long necklace)",
        "metal": "玫瑰金",
        "vibe": "探索、空間、自由"
    },
    "紅地球": {
        "gem": "煙水晶 (Smoky Quartz)、琥珀、木化石",
        "design": "保留原礦紋理的設計、樹枝狀金屬紋理、大地色系的彩寶",
        "metal": "復古金 / 銅",
        "vibe": "接地、進化、自然"
    },
    # ⚪ 北方白色家族
    "白風": {
        "gem": "白玉髓、蛋白石 (Opal)",
        "design": "鏤空設計 (Filigree) 象徵透氣、精靈般的耳骨夾 (Ear cuff)、流蘇耳線",
        "metal": "白金 / 925純銀",
        "vibe": "靈性、溝通、輕盈"
    },
    "白世界橋": {
        "gem": "拉長石 (Labradorite)、銀曜石",
        "design": "鎖鏈造型 (Chain link)、極簡的金屬幾何線條、雙指戒",
        "metal": "白金 / 銀",
        "vibe": "連結、跨越、結構"
    },
    "白狗": {
        "gem": "粉晶 (Rose Quartz)、摩根石 (Morganite)",
        "design": "心型切割鑽石/寶石、玫瑰金材質、象徵連結的繩結設計 (Knots)",
        "metal": "玫瑰金 / 白金",
        "vibe": "愛、忠誠、溫暖"
    },
    "白巫師": {
        "gem": "紫水晶 (Amethyst)、紫鋰輝",
        "design": "貓眼石 (Cat's eye)、帶有神祕符號 (如荷魯斯之眼) 的墜飾、單顆靈擺造型項鍊",
        "metal": "白金 / 銀",
        "vibe": "魔法、永恆、神祕"
    },
    "白鏡": {
        "gem": "白水晶 (Clear Quartz)、白拓帕石",
        "design": "祖母綠切割 (Emerald Cut, 俐落長方)、鏡面拋光的寬版銀戒、對稱設計",
        "metal": "白金 / 銀",
        "vibe": "映照、秩序、清澈"
    },
    # 🔵 西方藍色家族
    "藍夜": {
        "gem": "青金石 (Lapis Lazuli)、藍砂石",
        "design": "星月造型 (Celestial motifs)、鑲嵌碎鑽的星空感設計、深藍色琺瑯",
        "metal": "K白金 / 黃K金",
        "vibe": "直覺、夢想、豐盛"
    },
    "藍手": {
        "gem": "綠松石 (Turquoise)、海藍寶 (Aquamarine)",
        "design": "疊戴戒指 (Stacking rings, 強調手部)、手掌造型 (Hamsa Hand)、療癒系水晶",
        "metal": "K白金 / 銀",
        "vibe": "實作、療癒、知曉"
    },
    "藍猴": {
        "gem": "磷灰石、多彩剛玉 (Multi-colored Sapphire)",
        "design": "不對稱耳環 (Asymmetrical)、可拆卸組合的Charm墜飾、童趣圖案",
        "metal": "K白金",
        "vibe": "遊戲、幻象、幽默"
    },
    "藍鷹": {
        "gem": "藍寶石 (Blue Sapphire)、坦桑石",
        "design": "翅膀意象 (Wings)、馬眼形切割 (Marquise Cut, 像眼睛)、V型項鍊",
        "metal": "K白金",
        "vibe": "視野、心智、創造"
    },
    "藍風暴": {
        "gem": "紫龍晶、堇青石 (Iolite)",
        "design": "閃電造型小耳釘、帶有光暈變化的寶石、不規則熔岩質感金屬",
        "metal": "K白金 / 黑金",
        "vibe": "蛻變、能量、催化"
    },
    # 🟡 南方黃色家族
    "黃種子": {
        "gem": "橄欖石 (Peridot)、綠碧璽",
        "design": "蛋面切割 (Cabochon, 像種子)、花苞造型、藤蔓纏繞設計",
        "metal": "18K黃金",
        "vibe": "目標、生長、潛能"
    },
    "黃星星": {
        "gem": "黃鑽、鋯石 (Zircon)、極致閃亮的寶石",
        "design": "八芒星/五芒星造型、密釘鑲 (Pave) 的閃亮款式、藝術家聯名款",
        "metal": "18K黃金",
        "vibe": "優雅、藝術、美麗"
    },
    "黃人": {
        "gem": "黃水晶 (Citrine)、托帕石 (Imperial Topaz)",
        "design": "經典單鑽 (Solitaire)、智慧之杯 (Chalice) 意象、刻有箴言的牌鍊",
        "metal": "18K黃金",
        "vibe": "智慧、自由、意志"
    },
    "黃戰士": {
        "gem": "黃鐵礦 (Pyrite)、鈦晶",
        "design": "盾牌造型 (Shield shape)、鉚釘元素 (Studs)、幾何三角形耳環",
        "metal": "18K黃金 / 黑金",
        "vibe": "無畏、才智、提問"
    },
    "黃太陽": {
        "gem": "太陽石 (Sunstone)、琥珀",
        "design": "放射狀太陽光芒設計 (Sunburst)、大圓圈耳環 (Hoops)、純金/厚金質感",
        "metal": "18K黃金",
        "vibe": "生命、開悟、溫暖"
    }
}

# ────────────── 2. Jewelry Data: Tones (13調性-款式結構) ──────────────
tone_jewelry = {
    1:  {"name": "磁性 (Magnetic)", "structure": "單鑽 / 單墜", "style": "鎖骨鍊上只有一顆主石，聚焦能量。"},
    2:  {"name": "月亮 (Lunar)", "structure": "雙石 / 對稱", "style": "Toi et Moi (你和我) 雙主石戒指，或強調存在感的成對耳環。"},
    3:  {"name": "電力 (Electric)", "structure": "三角形 / 三石", "style": "三角形切割 (Trillion Cut)，或三顆寶石排列的項鍊 (過去、現在、未來)。"},
    4:  {"name": "自我存在 (Self-Existing)", "structure": "方形 / 結構", "style": "公主方切割 (Princess Cut)，方形金屬框設計，盒鍊 (Box chain)。"},
    5:  {"name": "超頻 (Overtone)", "structure": "五角星 / 核心", "style": "五角星設計，或是有主石周圍有一圈光圈 (Halo) 的款式。"},
    6:  {"name": "韻律 (Rhythmic)", "structure": "六邊形 / 平衡", "style": "蜂巢六角形設計，或長度剛好平衡的垂墜耳環。"},
    7:  {"name": "共振 (Resonant)", "structure": "Y字鍊 / 中軸", "style": "長款Y字項鍊 (拉長頸部線條)，七脈輪寶石設計。"},
    8:  {"name": "銀河 (Galactic)", "structure": "無限符號 / 交織", "style": "無限符號 (Infinity)，雙環交扣的項鍊或戒指。"},
    9:  {"name": "太陽 (Solar)", "structure": "流蘇 / 動態", "style": "會隨著動作擺動的耳線，有太陽光芒刻紋的圓牌。"},
    10: {"name": "行星 (Planetary)", "structure": "排鑽 / 實心", "style": "永恆戒 (Eternity Band)，實心K金手鐲 (Bangle)，顯化意念的具體化。"},
    11: {"name": "光譜 (Spectral)", "structure": "彩虹 / 漸層", "style": "漸層色寶石排列 (Ombre)，隨著光線變色的蛋白石。"},
    12: {"name": "水晶 (Crystal)", "structure": "圓形 / 串珠", "style": "經典圓形明亮式切割 (Round Brilliant)，珍珠手鍊，圓珠設計。"},
    13: {"name": "宇宙 (Cosmic)", "structure": "螺旋 / 全知", "style": "螺旋造型 (Spiral) 戒指，彷彿銀河系的漩渦設計。"}
}

# ────────────── Page Config & CSS ──────────────
st.set_page_config(page_title="Maya 輕珠寶能量顧問", layout="wide", page_icon="💎")
st.markdown(
    """<style>
    .hero {padding:3rem 2rem; text-align:center; background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%); border-radius: 15px; margin-bottom: 2rem;}
    .hero h1 {font-size:2.5rem; font-weight:700; color: #333; margin-bottom:0.5rem;}
    .hero p  {font-size:1.1rem; color: #666;}
    
    .footer {position:fixed; bottom:0; width:100%; background:#1f2937; color:white; text-align:center; padding:1rem; z-index:999;}
    .footer a {color:#60a5fa; text-decoration:none; margin:0 0.5rem;}
    
    div[data-testid="stContainer"] {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border: 1px solid #f0f0f0;
    }
    
    /* 儀式感區塊樣式 */
    .ritual-box {
        background-color: #f8f9fa;
        padding: 20px;
        border-left: 5px solid #d4af37; /* 金色邊框 */
        margin-top: 20px;
    }
    </style>""",
    unsafe_allow_html=True,
)

# ────────────── Hero Section ──────────────
st.markdown(
    """
    <section class="hero">
      <h1>💎 Maya 輕珠寶能量顧問</h1>
      <p>輕珠寶能量指南｜為你的靈魂挑選專屬的護身符</p>
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
    st.error(f"❌ 資料載入失敗，請確認 data 資料夾中是否有必要的 CSV 檔案。\n錯誤訊息：{e}")
    st.stop()

# ────────────── Sidebar Input ──────────────
st.sidebar.header("📅 設定你的專屬密碼")
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

# 取得對應資料
jewel_t = totem_jewelry.get(totem, {})
jewel_tone = tone_jewelry.get(tone_number, {})

st.markdown(f"### 🔮 你的能量印記：{kin} {totem} (調性 {tone_number})")

# 顯示圖騰圖片與基本氛圍
col_img, col_info = st.columns([1, 4])
with col_img:
    img_file = os.path.join(IMG_DIR, f"{totem}.png")
    if os.path.exists(img_file):
        st.image(Image.open(img_file), use_container_width=True)
    else:
        st.caption("No Image")

with col_info:
    if jewel_t:
        st.success(f"**核心能量：{jewel_t['vibe']}**")
        st.write(f"推薦金屬色系：{jewel_t['metal']}")
    else:
        st.warning("尚無此圖騰資料")

# ────────────── 飾品推薦主區塊 ──────────────
st.divider()

col1, col2 = st.columns(2)

# 左欄：寶石與設計 (圖騰)
with col1:
    st.markdown("#### 💎 寶石與設計 (Material)")
    st.caption("由你的太陽圖騰決定核心材質")
    
    if jewel_t:
        with st.container(border=True):
            st.markdown(f"**✨ 命定寶石：**")
            st.write(jewel_t['gem'])
            
            st.markdown(f"**🎨 設計意象：**")
            st.write(jewel_t['design'])
            
            st.info("💡 **能量原理**：這些寶石與你的靈魂頻率共振，能協助你放大原生天賦。")

# 右欄：款式與結構 (調性)
with col2:
    st.markdown("#### 📐 款式與結構 (Structure)")
    st.caption("由你的銀河調性決定形狀")
    
    if jewel_tone:
        with st.container(border=True):
            st.markdown(f"**🎵 調性：{jewel_tone['name']}**")
            
            st.markdown(f"**🎯 推薦結構：{jewel_tone['structure']}**")
            
            st.write(jewel_tone['style'])
            
            st.info("💡 **佩戴建議**：選擇這種結構的飾品，能幫助你在生活中穩定這股能量頻率。")

# ────────────── 專家推薦 (組合句) ──────────────
st.markdown("### ✨ 專家推薦：今日能量選品")
summary_text = f"""
想像一下，戴上一款 **{jewel_t.get('metal', 'K金')}** 的 **{jewel_tone.get('structure', '飾品')}**。
主石選用 **{jewel_t.get('gem', '').split('、')[0]}**，並採用 **{jewel_t.get('design', '').split('、')[0]}** 的設計細節。
這不僅是一件飾品，更是啟動你「{jewel_t.get('vibe', '')}」能量的專屬按鈕。
"""
st.success(summary_text)

# ────────────── 能量啟動儀式 ──────────────
with st.expander("🕯️ 查看：星際輕珠寶・能量啟動儀式 (The Activation Ritual)"):
    st.markdown(
        """
        <div class="ritual-box">
        <h4>1. 淨化 (Purification)</h4>
        <p>如果是水晶，用清水沖洗30秒；若是金屬，觀想白光包圍它。心念：「我淨化此物，回歸純淨本質。」</p>
        
        <h4>2. 連結 (Connection)</h4>
        <p>將飾品放在左手掌心，右手覆蓋其上，置於胸口(心輪)。深呼吸三次，想像光流經你的心傳遞給飾品。</p>
        
        <h4>3. 注入意圖 (Imprinting)</h4>
        <p>對著飾品說：「我邀請你與我共振。請協助我開啟 <strong>{}</strong> 的能量。」語畢，對飾品用力吹一口氣(白風之氣)封存。</p>
        
        <h4>4. 佩戴 (Wearing)</h4>
        <p>戴上的瞬間，想像金色的保護罩將你包圍。確認它現在是你能量系統的一部分。</p>
        </div>
        """.format(jewel_t.get('vibe', '專屬')), 
        unsafe_allow_html=True
    )

# ────────────── 固定 Footer ──────────────
st.markdown(
    """
    <div style="margin-bottom: 80px;"></div>
    <footer class="footer">
      <a href="https://www.facebook.com/soulclean1413/" target="_blank">👉 加入粉專</a> 
      <a href="https://www.instagram.com/tilandky/" target="_blank">👉 追蹤IG</a>
      <a href="https://line.me/R/ti/p/%40690ZLAGN" target="_blank">👉 加入社群</a>
    </footer>
    """,
    unsafe_allow_html=True
)
