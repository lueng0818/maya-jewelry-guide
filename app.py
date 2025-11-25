import os
import calendar
from PIL import Image

import pandas as pd
import streamlit as st

# ────────────── Path Setup ──────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
IMG_DIR  = os.path.join(BASE_DIR, "images")

# ────────────── 1. General Jewelry Data (通用能量建議 - 男女分流) ──────────────
totem_general = {
    # 🔴 東方紅色家族
    "紅龍": {
        "F": {"gem": "紅寶石、石榴石", "design": "古幣造型項鍊、圓形浮雕", "metal": "玫瑰金", "vibe": "滋養、古老智慧"},
        "M": {"gem": "紅石榴石、紅碧玉", "design": "古董銀幣戒指、龍鱗紋路手環", "metal": "古銅金 / 舊化銀", "vibe": "開創、霸氣、底蘊"}
    },
    "紅蛇": {
        "F": {"gem": "紅瑪瑙、紅碧玉", "design": "蛇形戒指、K金細鍊", "metal": "玫瑰金 / 黃K金", "vibe": "熱情、魅力"},
        "M": {"gem": "紅瑪瑙、黑瑪瑙", "design": "編織皮繩手環、蛇骨鍊", "metal": "純銀 / 皮革", "vibe": "本能、生命力、生存"}
    },
    "紅月": {
        "F": {"gem": "月光石、珍珠", "design": "水滴型切割、新月造型", "metal": "玫瑰金 / 銀", "vibe": "溫柔、流動"},
        "M": {"gem": "月光石 (灰月光)、黑珍珠", "design": "海浪圖騰寬戒、霧面金屬", "metal": "霧銀 / 白金", "vibe": "淨化、深層情感"}
    },
    "紅天行者": {
        "F": {"gem": "紅紋石、紅碧璽", "design": "羽毛雕刻、指南針造型", "metal": "玫瑰金", "vibe": "自由、探索"},
        "M": {"gem": "紅碧璽、孔雀石", "design": "羅盤圖騰、飛行員墨鏡風格飾品", "metal": "鋼 / 銀", "vibe": "冒險、空間感"}
    },
    "紅地球": {
        "F": {"gem": "煙水晶、琥珀", "design": "樹枝狀紋理、花草圖騰", "metal": "復古金", "vibe": "接地、自然"},
        "M": {"gem": "茶晶、木化石", "design": "岩石紋理戒指、原木結合金屬", "metal": "黃銅 / 舊化銀", "vibe": "穩重、核心、進化"}
    },
    # ⚪ 北方白色家族
    "白風": {
        "F": {"gem": "白玉髓、蛋白石", "design": "鏤空蕾絲、流蘇耳線", "metal": "白金 / 純銀", "vibe": "靈性、輕盈"},
        "M": {"gem": "白松石、白水晶", "design": "極簡幾何線條、羽毛銀飾", "metal": "925純銀", "vibe": "溝通、呼吸、傳遞"}
    },
    "白世界橋": {
        "F": {"gem": "拉長石、銀曜石", "design": "鎖鏈造型、雙指戒", "metal": "白金 / 銀", "vibe": "連結、跨越"},
        "M": {"gem": "銀曜石、黑曜石", "design": "橋樑結構意象、古巴鍊 (Cuban Link)", "metal": "鈦鋼 / 銀", "vibe": "結構、決斷、機會"}
    },
    "白狗": {
        "F": {"gem": "粉晶、摩根石", "design": "心型切割、繩結設計", "metal": "玫瑰金", "vibe": "愛、溫暖"},
        "M": {"gem": "白水晶、白瑪瑙", "design": "忠誠圖騰 (如狼/犬)、家族徽章", "metal": "白金 / 鋼", "vibe": "忠誠、夥伴、守護"}
    },
    "白巫師": {
        "F": {"gem": "紫水晶、紫鋰輝", "design": "貓眼石、神祕符號墜飾", "metal": "白金 / 銀", "vibe": "魔法、神祕"},
        "M": {"gem": "紫水晶 (深紫)、紫龍晶", "design": "圖騰圖章戒指、法器造型", "metal": "純銀 (燻黑處理)", "vibe": "永恆、意志、顯化"}
    },
    "白鏡": {
        "F": {"gem": "白水晶、白拓帕石", "design": "祖母綠切割、鏡面拋光", "metal": "白金 / 銀", "vibe": "清澈、映照"},
        "M": {"gem": "白水晶、黑鑽", "design": "銳利切角戒指、鏡面金屬牌", "metal": "亮面銀 / 鋼", "vibe": "秩序、真相、果斷"}
    },
    # 🔵 西方藍色家族
    "藍夜": {
        "F": {"gem": "青金石、藍砂石", "design": "星月造型、星空琺瑯", "metal": "K白金", "vibe": "夢幻、直覺"},
        "M": {"gem": "青金石、藍寶石", "design": "午夜藍錶盤搭配、星象圖騰", "metal": "深藍電鍍 / 銀", "vibe": "豐盛、潛意識、沉穩"}
    },
    "藍手": {
        "F": {"gem": "綠松石、海藍寶", "design": "療癒系水晶、疊戴戒指", "metal": "K白金 / 銀", "vibe": "療癒、實作"},
        "M": {"gem": "綠松石、天河石", "design": "工匠手作感銀飾、手環", "metal": "純銀 / 銅", "vibe": "創造、知曉、完成"}
    },
    "藍猴": {
        "F": {"gem": "多彩剛玉、磷灰石", "design": "不對稱耳環、童趣墜飾", "metal": "K白金", "vibe": "幽默、玩樂"},
        "M": {"gem": "變色石、藍晶石", "design": "幾何拼接、拼圖造型", "metal": "混合金屬", "vibe": "幻象、遊戲、解構"}
    },
    "藍鷹": {
        "F": {"gem": "坦桑石、藍寶石", "design": "翅膀意象、V型項鍊", "metal": "K白金", "vibe": "視野、優雅"},
        "M": {"gem": "藍寶石 (深藍)、鷹眼石", "design": "老鷹/羽翼浮雕、領帶夾", "metal": "白金 / 鋼", "vibe": "格局、洞察、領袖"}
    },
    "藍風暴": {
        "F": {"gem": "紫龍晶、堇青石", "design": "閃電造型、不規則熔岩感", "metal": "黑金 / 銀", "vibe": "蛻變、能量"},
        "M": {"gem": "黑隕石、舒俱徠石", "design": "閃電紋路、鍛敲質感金屬", "metal": "黑銀 / 鈦", "vibe": "催化、改革、力量"}
    },
    # 🟡 南方黃色家族
    "黃種子": {
        "F": {"gem": "橄欖石、綠碧璽", "design": "花苞造型、藤蔓纏繞", "metal": "18K黃金", "vibe": "生長、潛能"},
        "M": {"gem": "橄欖石、綠幽靈", "design": "簡約圓弧戒、種子刻紋", "metal": "霧面金 / 黃銅", "vibe": "目標、專注、紮根"}
    },
    "黃星星": {
        "F": {"gem": "黃鑽、鋯石", "design": "八芒星造型、密釘鑲款式", "metal": "18K黃金", "vibe": "藝術、美麗"},
        "M": {"gem": "黃水晶、白鑽", "design": "星芒圖騰戒指、袖扣", "metal": "亮面金", "vibe": "優雅、美學、焦點"}
    },
    "黃人": {
        "F": {"gem": "黃水晶、托帕石", "design": "單鑽鎖骨鍊、箴言牌鍊", "metal": "18K黃金", "vibe": "智慧、自由"},
        "M": {"gem": "黃水晶、鈦晶", "design": "刻字軍牌 (Dog tag)、方戒", "metal": "黃金 / 鋼", "vibe": "意志、邏輯、影響力"}
    },
    "黃戰士": {
        "F": {"gem": "黃鐵礦、鈦晶", "design": "盾牌造型、鉚釘元素", "metal": "黑金 / 黃金", "vibe": "無畏、勇氣"},
        "M": {"gem": "黃鐵礦、黑髮晶", "design": "鎧甲鍊、幾何盾牌戒", "metal": "古銅 / 黑銀", "vibe": "才智、提問、戰略"}
    },
    "黃太陽": {
        "F": {"gem": "太陽石、琥珀", "design": "放射狀太陽光芒、大圓耳環", "metal": "18K黃金", "vibe": "溫暖、開悟"},
        "M": {"gem": "太陽石、金珀", "design": "太陽圖騰印戒、厚實金戒", "metal": "純金 / 銅", "vibe": "生命、大氣、普照"}
    }
}

# ────────────── 2. Tru-Mi Product Mapping (品牌產品對應 - 男女分流) ──────────────
totem_trumi = {
    "紅龍": {
        "F": {"series": "Memory 系列", "item": "Memory 樹枝款耳環/戒指", "desc": "Memory系列的樹枝紋理，如同家族與生命的根系，連結大地母親的能量。", "url": "https://www.tru-mi.com/collections/memory"},
        "M": {"series": "Memory 系列 (中性款)", "item": "Memory 樹枝紋寬版戒", "desc": "選擇較寬版的樹枝紋理戒指，象徵古老家族的榮耀與穩固的根基。", "url": "https://www.tru-mi.com/collections/memory"}
    },
    "紅蛇": {
        "F": {"series": "Resilience 系列", "item": "Resilience 斜紋/領帶系列", "desc": "斜紋設計與俐落切角，象徵在都市叢林中靈活穿梭的韌性與魅力。", "url": "https://www.tru-mi.com/collections/resilience"},
        "M": {"series": "Resilience 系列", "item": "Resilience 幾何領帶夾/戒指", "desc": "Resilience 系列的幾何切面象徵蛻變，非常適合作為職場上的力量護身符。", "url": "https://www.tru-mi.com/collections/resilience"}
    },
    "紅月": {
        "F": {"series": "Minilife 系列", "item": "Minilife 夢想的海洋", "desc": "海洋元素的溫柔波浪，接住妳的情緒，療癒每一滴眼淚與歡笑。", "url": "https://www.tru-mi.com/collections/minilife"},
        "M": {"series": "Flawless 系列", "item": "Flawless 滾珠銀戒", "desc": "選擇簡約的銀飾，如同平靜的月光照耀海面，穩定你內在的情緒潮汐。", "url": "https://www.tru-mi.com/collections/flawless"}
    },
    "紅天行者": {
        "F": {"series": "Morning Star 系列", "item": "晨星系列-星願項鍊", "desc": "星芒如同夜空中的羅盤，為喜愛探索與冒險的妳，指引正確的方向。", "url": "https://www.tru-mi.com/collections/morning-star"},
        "M": {"series": "專屬訂製", "item": "客製化經緯度/羅盤飾品", "desc": "推薦訂製刻有特殊地點經緯度的飾品，紀念你的每一次空間探索。", "url": "https://www.tru-mi.com/custom-jewelry"}
    },
    "紅地球": {
        "F": {"series": "Memory 系列", "item": "Memory 單花/樹枝款", "desc": "保留植物有機的生長紋理，時刻保持與自然接地的穩定頻率。", "url": "https://www.tru-mi.com/collections/memory"},
        "M": {"series": "Memory 系列", "item": "Memory 樹枝紋理戒 (霧面)", "desc": "粗獷的樹枝紋理搭配霧面處理，展現如同大地般厚實可靠的質感。", "url": "https://www.tru-mi.com/collections/memory"}
    },
    "白風": {
        "F": {"series": "Flawless 系列", "item": "Flawless 孔珠套鍊", "desc": "極簡的孔珠設計，象徵話語的圓滿與通透，讓溝通如風般自由。", "url": "https://www.tru-mi.com/collections/flawless"},
        "M": {"series": "Flawless 系列", "item": "Flawless 極簡銀戒", "desc": "乾淨、無多餘裝飾的銀戒，象徵你言語的真實與純粹。", "url": "https://www.tru-mi.com/collections/flawless"}
    },
    "白世界橋": {
        "F": {"series": "婚戒/對戒系列", "item": "Tru-Mi 雙色拼接對戒", "desc": "象徵跨越個體、連結彼此的神聖承諾，連結兩個世界的通道。", "url": "https://www.tru-mi.com/wedding"},
        "M": {"series": "婚戒/對戒系列", "item": "Tru-Mi 幾何切面對戒", "desc": "結構性強的對戒設計，代表著建立連結所需的穩定與結構。", "url": "https://www.tru-mi.com/wedding"}
    },
    "白狗": {
        "F": {"series": "Beloved 系列", "item": "Beloved 鈴鐺/寵物訂製", "desc": "無論是寵物珠寶或溫暖設計，都滋養著妳充滿愛與忠誠的心輪。", "url": "https://www.tru-mi.com/baby-gifts-beloved"},
        "M": {"series": "Mi 系列", "item": "Mi 刻字手鍊 (皮革/銀)", "desc": "刻上重要夥伴或家人的名字，象徵你對守護對象的承諾。", "url": "https://www.tru-mi.com/collections/mi"}
    },
    "白巫師": {
        "F": {"series": "Minilife 系列", "item": "Minilife 秘密花園", "desc": "精緻微小的設計，彷彿施了魔法的護身符，提醒妳向內觀看。", "url": "https://www.tru-mi.com/collections/minilife"},
        "M": {"series": "Memory 系列", "item": "Memory 沉穩款戒指", "desc": "選擇設計內斂、帶有手作溫度的飾品，安住當下，展現意志的力量。", "url": "https://www.tru-mi.com/collections/memory"}
    },
    "白鏡": {
        "F": {"series": "Flawless 系列", "item": "Flawless 滾珠銀戒 (亮面)", "desc": "精細拋光的銀飾，如鏡面般映照出真實的自己，展現秩序之美。", "url": "https://www.tru-mi.com/collections/flawless"},
        "M": {"series": "Flawless 系列", "item": "Flawless 平面銀戒 (亮面)", "desc": "如刀鋒般俐落的亮面銀戒，象徵你洞察真相的決斷力。", "url": "https://www.tru-mi.com/collections/flawless"}
    },
    "藍夜": {
        "F": {"series": "Morning Star 系列", "item": "晨星系列-星願項鍊", "desc": "象徵將直覺與夢境顯化為現實，守護妳內在那個豐盛璀璨的星空。", "url": "https://www.tru-mi.com/collections/morning-star"},
        "M": {"series": "Resilience 系列", "item": "Resilience 幾何造型", "desc": "以幾何結構捕捉夢想的形狀，將潛意識的豐盛顯化為具體的物質。", "url": "https://www.tru-mi.com/collections/resilience"}
    },
    "藍手": {
        "F": {"series": "專屬訂製", "item": "Tru-Mi 手作體驗課程", "desc": "推薦參與「手作體驗」，親手打造飾品，讓其成為妳療癒與創造的證明。", "url": "https://www.tru-mi.com/custom-jewelry"},
        "M": {"series": "專屬訂製", "item": "全訂製工藝服務", "desc": "藍手重視實作，透過訂製服務，將你的想法透過工藝轉化為現實。", "url": "https://www.tru-mi.com/custom-jewelry"}
    },
    "藍猴": {
        "F": {"series": "Beloved 系列", "item": "Beloved 搖搖馬/兔手鍊", "desc": "充滿童心的設計，喚醒妳內在小孩的幽默與純真快樂。", "url": "https://www.tru-mi.com/baby-gifts-beloved"},
        "M": {"series": "Mi 系列", "item": "Mi 趣味刻字/圖騰訂製", "desc": "不拘泥於形式，訂製一款帶有幽默語句或特殊圖騰的飾品，展現玩心。", "url": "https://www.tru-mi.com/collections/mi"}
    },
    "藍鷹": {
        "F": {"series": "Resilience 系列", "item": "Resilience 領帶耳環/項鍊", "desc": "領帶造型象徵專業與願景，助妳在事業藍圖中展翅高飛。", "url": "https://www.tru-mi.com/collections/resilience"},
        "M": {"series": "Resilience 系列", "item": "Resilience 領帶夾/袖扣", "desc": "專為男士設計的領帶造型或結構飾品，展現你的遠見與領袖氣場。", "url": "https://www.tru-mi.com/collections/resilience"}
    },
    "藍風暴": {
        "F": {"series": "Minilife 系列", "item": "Minilife 夢想的海洋 (波浪)", "desc": "起伏的波浪線條，象徵妳擁抱變動、轉化能量的本質。", "url": "https://www.tru-mi.com/collections/minilife"},
        "M": {"series": "Memory 系列", "item": "Memory 敲擊紋理戒", "desc": "表面充滿鍛敲痕跡的戒指，象徵經歷風暴洗禮後的堅韌與力量。", "url": "https://www.tru-mi.com/collections/memory"}
    },
    "黃種子": {
        "F": {"series": "Memory 系列", "item": "Memory 單花耳環", "desc": "花朵造型象徵耐心與成長，祝福夢想的種子順利破土而出。", "url": "https://www.tru-mi.com/collections/memory"},
        "M": {"series": "Memory 系列", "item": "Memory 簡約圈戒", "desc": "看似簡單的圈戒，蘊含著無限生機，象徵專注於目標的持續成長。", "url": "https://www.tru-mi.com/collections/memory"}
    },
    "黃星星": {
        "F": {"series": "Morning Star 系列", "item": "晨星系列 (星鑽款)", "desc": "閃耀光芒呼應了妳天生要在人群中發光發熱的藝術家特質。", "url": "https://www.tru-mi.com/collections/morning-star"},
        "M": {"series": "Morning Star 系列", "item": "晨星系列 (無鑽K金)", "desc": "選擇線條優雅的K金飾品，展現你不凡的品味與藝術眼光。", "url": "https://www.tru-mi.com/collections/morning-star"}
    },
    "黃人": {
        "F": {"series": "Mi 系列", "item": "Mi 告白項鍊 (刻字)", "desc": "將人生格言刻在飾品上，時刻提醒自己做出有意識的選擇。", "url": "https://www.tru-mi.com/collections/mi"},
        "M": {"series": "Mi 系列", "item": "Mi 刻字寬版手環", "desc": "將信念或座右銘刻在寬版手環上，象徵自由意志與智慧的展現。", "url": "https://www.tru-mi.com/collections/mi"}
    },
    "黃戰士": {
        "F": {"series": "Resilience 系列", "item": "Resilience 幾何造型戒", "desc": "如同隱形鎧甲，幾何結構象徵才智與勇氣，陪伴妳面對挑戰。", "url": "https://www.tru-mi.com/collections/resilience"},
        "M": {"series": "Resilience 系列", "item": "Resilience 盾牌意象飾品", "desc": "結構感強烈的設計，如同戰士的盾牌，賦予你無畏前行的勇氣。", "url": "https://www.tru-mi.com/collections/resilience"}
    },
    "黃太陽": {
        "F": {"series": "Morning Star 系列", "item": "晨星系列 (金色款)", "desc": "金色的飾品象徵妳無私溫暖的光芒，展現大氣的領袖風範。", "url": "https://www.tru-mi.com/collections/morning-star"},
        "M": {"series": "婚戒/對戒系列", "item": "厚實K金戒指", "desc": "選擇厚實、有份量的K金戒指，象徵太陽般恆久不變的能量與守護。", "url": "https://www.tru-mi.com/wedding"}
    }
}

# ────────────── 3. Tone Advice (13調性-結構建議 - 男女分流) ──────────────
tone_advice = {
    1:  {
        "name": "磁性 (Magnetic)", 
        "F": {"structure": "單鑽 / 單墜", "style": "鎖骨鍊上只有一顆主石，聚焦能量。"},
        "M": {"structure": "印章戒指 (Signet Ring)", "style": "單一且有份量的戒指，象徵唯一的目標與權威。"}
    },
    2:  {
        "name": "月亮 (Lunar)", 
        "F": {"structure": "雙石 / 對稱", "style": "Toi et Moi 雙主石戒指，或成對耳環，平衡二元性。"},
        "M": {"structure": "異材質拼接", "style": "金銀拼接或亮霧面雙色設計，展現挑戰與穩定並存。"}
    },
    3:  {
        "name": "電力 (Electric)", 
        "F": {"structure": "三角形 / 垂墜", "style": "三角形切割，或會擺動的耳環，啟動連結能量。"},
        "M": {"structure": "功能性飾品", "style": "具有扣環設計的手環，或與科技配件(如手錶)結合的飾品。"}
    },
    4:  {
        "name": "自我存在 (Self-Existing)", 
        "F": {"structure": "方形 / 結構", "style": "公主方切割或方形金屬框，建立穩定的能量場。"},
        "M": {"structure": "方戒 / 幾何", "style": "線條剛硬的方形戒指或立方體墜飾，象徵定義與形式。"}
    },
    5:  {
        "name": "超頻 (Overtone)", 
        "F": {"structure": "五角星 / 光圈", "style": "主石周圍有一圈光圈 (Halo) 的款式，彰顯核心光芒。"},
        "M": {"structure": "霸氣主戒", "style": "體積較大、存在感強烈的主戒指，展現領導力。"}
    },
    6:  {
        "name": "韻律 (Rhythmic)", 
        "F": {"structure": "六邊形 / 平衡", "style": "蜂巢六角形設計，或長度剛好平衡的垂墜飾品。"},
        "M": {"structure": "鍊條 / 節奏", "style": "規律排列的古巴鍊或環環相扣的手鍊，象徵組織與流動。"}
    },
    7:  {
        "name": "共振 (Resonant)", 
        "F": {"structure": "Y字鍊 / 中軸", "style": "拉長頸部線條的Y字鍊，對應身體中軸與脈輪。"},
        "M": {"structure": "簡約墜飾", "style": "垂直線條的墜飾或長方牌，象徵通道與調頻。"}
    },
    8:  {
        "name": "銀河 (Galactic)", 
        "F": {"structure": "無限符號 / 交織", "style": "無限符號 (Infinity) 或雙環交扣，整合內在信念。"},
        "M": {"structure": "編織紋理", "style": "金屬編織紋理的戒指或手環，象徵和諧與整合。"}
    },
    9:  {
        "name": "太陽 (Solar)", 
        "F": {"structure": "流蘇 / 動態", "style": "隨動作擺動的流蘇設計，或太陽光芒刻紋。"},
        "M": {"structure": "放射狀圖騰", "style": "刻有太陽放射線條的飾品，象徵意圖的脈動。"}
    },
    10: {
        "name": "行星 (Planetary)", 
        "F": {"structure": "排鑽 / 實心", "style": "永恆戒 (Eternity Band)，顯化意念的具體完美。"},
        "M": {"structure": "實心寬版", "style": "實心且厚實的寬版戒指或手鐲，象徵顯化與落實。"}
    },
    11: {
        "name": "光譜 (Spectral)", 
        "F": {"structure": "彩虹 / 漸層", "style": "漸層色寶石排列，或蛋白石，釋放多彩光譜。"},
        "M": {"structure": "不規則 / 破壞", "style": "帶有不規則切面或做舊處理的設計，象徵釋放與解構。"}
    },
    12: {
        "name": "水晶 (Crystal)", 
        "F": {"structure": "圓形 / 串珠", "style": "經典圓形切割或珍珠，象徵圓融合作。"},
        "M": {"structure": "圓弧 / 連結", "style": "圓弧線條的戒指，或象徵連結的繩結金工設計。"}
    },
    13: {
        "name": "宇宙 (Cosmic)", 
        "F": {"structure": "螺旋 / 全知", "style": "螺旋造型戒指，彷彿銀河系的漩渦，包容一切。"},
        "M": {"structure": "留白 / 素面", "style": "極簡的素面寬戒，無多餘雕飾，象徵超越與存在。"}
    }
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
        width: 100%;
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
      <p>探索妳/你的靈魂印記，遇見專屬於你的 Tru-Mi 故事珠寶</p>
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
st.sidebar.header("📅 輸入資訊，尋找命定飾品")
# 性別選擇
gender_input = st.sidebar.radio("心理性別 (Psychological Gender)", ["女性 (Female)", "男性 (Male)"])
gender_key = "M" if "男" in gender_input else "F"

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

# Get Mapped Data (Based on Gender)
general_data = totem_general.get(totem, {})
general_rec  = general_data.get(gender_key, {}) # Get F or M

trumi_data   = totem_trumi.get(totem, {})
trumi_rec    = trumi_data.get(gender_key, {})   # Get F or M

tone_data    = tone_advice.get(tone_number, {})
tone_rec     = tone_data.get(gender_key, {})    # Get F or M
tone_name    = tone_data.get("name", str(tone_number))

st.markdown(f"### 🔮 你的靈魂印記：{kin} {totem} (調性 {tone_number})")

col_img, col_info = st.columns([1, 4])
with col_img:
    img_file = os.path.join(IMG_DIR, f"{totem}.png")
    if os.path.exists(img_file):
        st.image(Image.open(img_file), use_container_width=True)

with col_info:
    if general_rec:
        st.success(f"**核心能量：{general_rec['vibe']}**")
        st.write(f"推薦金屬：**{general_rec['metal']}**")
    else:
        st.warning("目前尚無此圖騰對應資料")

# ────────────── 選品顧問主區塊 (整合版) ──────────────
st.divider()

col1, col2 = st.columns(2)

# 左欄：靈魂材質建議 (通用建議)
with col1:
    st.markdown("#### 💎 靈魂材質建議 (Soul Material)")
    st.caption("由你的太陽圖騰決定")
    
    if general_rec:
        with st.container(border=True):
            st.markdown(f"**✨ 命定寶石：**")
            st.write(general_rec['gem'])
            
            st.markdown(f"**🎨 推薦設計意象：**")
            st.write(general_rec['design'])
            
            st.info("💡 **能量原理**：選擇含有這些元素的飾品，能協助放大原生天賦，與靈魂頻率共振。")

# 右欄：Tru-Mi 品牌對應 (產品推薦)
with col2:
    st.markdown("#### 💍 Tru-Mi 系列推薦 (Collection)")
    st.caption("為你的故事挑選專屬珠寶")
    
    if trumi_rec:
        with st.container(border=True):
            st.markdown(f"**🌟 能量共振系列：Tru-Mi {trumi_rec['series']}**")
            st.write(f"推薦單品：{trumi_rec['item']}")
            st.write(trumi_rec['desc'])
            
            # Button to Tru-Mi Website
            btn_text = "前往 Tru-Mi 官網逛逛 👉"
            if "訂製" in trumi_rec['series']:
                btn_text = "前往 Tru-Mi 專屬訂製頁面 👉"
            st.markdown(f'<a href="{trumi_rec["url"]}" target="_blank" class="btn-trumi">{btn_text}</a>', unsafe_allow_html=True)

# ────────────── 調性結構與專家整合 ──────────────
st.divider()
st.markdown(f"#### 📐 結構與搭配建議 (Structure & Style)")
st.caption(f"由你的銀河調性 {tone_number} 決定")

col_tone, col_expert = st.columns([1, 2])

with col_tone:
    with st.container(border=True):
        st.markdown(f"**🎵 調性：{tone_name}**")
        st.markdown(f"**🎯 推薦結構：{tone_rec.get('structure', '')}**")
        st.write(tone_rec.get('style', ''))

with col_expert:
    st.info("✨ **專家推薦：今日能量選品**")
    summary_text = f"""
    想像一下，戴上一款 **{general_rec.get('metal', '金屬')}** 的 **{tone_rec.get('structure', '飾品')}**。
    
    材質選用 **{general_rec.get('gem', '').split('、')[0]}**，並在 **Tru-Mi 的 {trumi_rec.get('series', '').split(' ')[0]}** 中尋找靈感。
    這不僅是一件飾品，更是啟動你「{general_rec.get('vibe', '')}」能量的專屬按鈕。
    """
    st.markdown(summary_text)

# ────────────── 能量啟動儀式 ──────────────
with st.expander("🕯️ 查看：星際輕珠寶・能量啟動儀式 (The Activation Ritual)"):
    st.markdown(
        """
        <div class="ritual-box">
        <p>這個儀式只需要 3-5 分鐘。在注入新能量前，我們先歸零。</p>
        
        <h4>1. 淨化 (Purification)</h4>
        <p>如果是水晶，用清水沖洗30秒；若是金屬，觀想白光包圍它。心念：「我淨化此物，回歸純淨本質。」</p>
        
        <h4>2. 連結 (Connection)</h4>
        <p>將飾品放在左手掌心，右手覆蓋其上，置於胸口(心輪)。深呼吸三次，想像光流經你的心傳遞給飾品。</p>
        
        <h4>3. 注入意圖 (Imprinting the Intention)</h4>
        <p>保持雙手握著飾品，在心中說：「我邀請你與我共振。請協助我開啟 <strong>{}</strong> 的能量。」語畢，對飾品用力吹一口氣(白風之氣)封存。</p>
        
        <h4>4. 佩戴 (Wearing)</h4>
        <p>戴上的瞬間，想像金色的保護罩將你包圍。確認它現在是你能量系統的一部分。</p>
        </div>
        """.format(general_rec.get('vibe', '專屬')), 
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
