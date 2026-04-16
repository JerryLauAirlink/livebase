import streamlit as st
import math

# --- 1. 語言字典 (完整補齊中英文，確保完全對稱) ---
LANG = {
    'zh': {
        'title': "LIVE 智能辦公室系統規劃建議",
        'subtitle': "針對非技術用戶設計：自動匹配 HID 硬件、LIVE 軟件與 Server 架構。",
        'load_setting': "ACCESS CONTROL 硬件系統類型規劃 (每台主控板連接口數上限)",
        'load_stable': "最穩定 (16)",
        'load_standard': "標準 (32)",
        'load_extreme': "極限 (64)",
        'step1': "1. 請輸入您的場所規模",
        'step2': "2. 系統規劃評估與架構分析",
        'step3': "3. 建議方案硬件與伺服器清單",
        'step4': "4. 專業功能對比",
        'readers': "預計安裝門數 / 讀卡機數量",
        'ipc': "監控攝像頭 (IPC) 數量",
        'face': "人臉辨識面板機數量",
        'desktop': "管理電腦數量",
        'inputs': "特殊報警輸入 (感應器/按鈕)",
        'outputs': "特殊控制輸出 (電梯/連動)",
        'aero_title': "HID Aero 方案 (X1100A)",
        'aero_desc': "最高安全性：內建加密晶片 (SIO)，與 HID 讀卡機整合度最高，適合追求原廠極致加密的企業。",
        'merc_title': "HID Mercury 方案 (MP4502)",
        'merc_desc': "最高擴展性：Series 3 最新硬體，記憶體最大，未來整合第三方法務、電梯或錄影系統兼容性最強。",
        'hw_tab': "🛠️ 建議硬件清單",
        'sw_tab': "🔑 所需系統授權",
        'sv_tab': "🖥️ Server 架構清單",
        'comp_item': "比較項目",
        'note': "提示：主控制器負責網絡與邏輯處理，讀卡機透過擴充模組接入以確保隔離與穩定。",
        'eval_title': "📊 主控板負載評估",
        'server_eval_title': "🖥️ Server 架構建議",
        'eval_16_title': "最穩定配置 (16 Reader)",
        'eval_16_desc': "這是大型金融機構或數據中心最常採用的「黃金比例」。",
        'eval_16_list': ["RS-485 延遲：極低 (<200ms)。", "故障風險：極小 (範圍約 1.3%)。", "記憶體負荷：極輕，適連動邏輯。", "性能表現：在此負載下表現完美。"],
        'eval_32_title': "標準配置 (32 Reader)",
        'eval_32_desc': "這是大多數甲級寫字樓或政府項目的標準做法。",
        'eval_32_list': ["RS-485 延遲：輕微 (300-500ms)。", "故障風險：中等 (範圍約 2.6%)。", "記憶體負荷：適中，大數據下載略慢。", "性能表現：Mercury 較為穩定。"],
        'eval_64_title': "極限風險 (64 Reader)",
        'eval_64_desc': "這是規格書上的「物理極限」，大型案場中屬於危險配置。",
        'eval_64_list': ["RS-485 延遲：高風險 (>1s)。", "故障風險：極高 (範圍約 5.3%)。", "記憶體負荷：飽和，升級易失敗。", "性能表現：實務上易需重啟。"],
        'lv1_title': "Level 1: 中小型規模 (1-128 Reader)",
        'lv1_desc': "目標：簡單、成本效益、單機運作",
        'lv1_list': ["Server 數量：1 台 (Single Server)", "做法：DB、服務與介面裝在同一台 VM。", "限制：建議 SQL Express (10GB 限制)。", "風險：Server 故障失去管理能力。"],
        'lv2_title': "Level 2: 中大型規模 (128-1,000 Reader)",
        'lv2_desc': "目標：分流處理、高可用性 (HA)",
        'lv2_list': ["Server 數量：2 - 3 台", "配置：DB/Main + Comm Server + Failover(選配)。", "做法：必須使用 SQL Standard。通訊服務獨立。", "轉折點：超過 500 門建議強制拆分。"],
        'lv3_title': "Level 3: 企業級/園區規模 (1,000-2,000+ Reader)",
        'lv3_desc': "目標：多重備援、負載平衡、災難復原",
        'lv3_list': ["Server 數量：4 - 6 台 (或更多)", "配置：DB(P/M) + App Server + 多台分區 Comm Server。", "做法：採用分區管理 (Segmentation)。", "備援：配合 VMware HA 或系統 Failover 授權。"]
    },
    'en': {
        'title': "LIVE Intelligent Office Planning Guide",
        'subtitle': "Automatic HID Hardware, Software & Server Architecture matching.",
        'load_setting': "Access Control System Design Load (Max Readers per Controller)",
        'load_stable': "Stable (16)",
        'load_standard': "Standard (32)",
        'load_extreme': "Extreme (64)",
        'step1': "1. Site Requirements",
        'step2': "2. Evaluation & Architecture Analysis",
        'step3': "3. Hardware & Server List",
        'step4': "4. Technical Comparison",
        'readers': "Total Readers / Doors",
        'ipc': "CCTV (IPC) Qty",
        'face': "Face Panels Qty",
        'desktop': "Workstations",
        'inputs': "Alarm Inputs",
        'outputs': "Control Outputs",
        'aero_title': "HID Aero Solution (X1100A)",
        'aero_desc': "Max Security: Built-in SIO chip for best integration with HID readers. Ideal for original ecosystem.",
        'merc_title': "HID Mercury Solution (MP4502)",
        'merc_desc': "Max Scalability: Series 3 hardware with max memory. Best for 3rd party, elevator, or VMS integrations.",
        'hw_tab': "🛠️ Hardware List",
        'sw_tab': "🔑 Software Licenses",
        'sv_tab': "🖥️ Server Arch List",
        'comp_item': "Comparison Item",
        'note': "Note: Controllers manage logic; readers connect via interfaces.",
        'eval_title': "📊 Controller Eval",
        'server_eval_title': "🖥️ Server Arch",
        'eval_16_title': "Stable Config (16 Readers)",
        'eval_16_desc': "The 'Golden Ratio' for Financial Institutions & Data Centers.",
        'eval_16_list': ["Latency: Minimal (<200ms).", "Risk: Minimal (~1.3%).", "Memory: Light load."],
        'eval_32_title': "Standard Config (32 Readers)",
        'eval_32_desc': "Standard practice for Grade-A Offices.",
        'eval_32_list': ["Latency: Slight (300-500ms).", "Risk: Moderate (~2.6%).", "Memory: Moderate load."],
        'eval_64_title': "Extreme Config (64 Readers)",
        'eval_64_desc': "Physical limit; High risk for large-scale sites.",
        'eval_64_list': ["Latency: High (>1s).", "Risk: Critical (~5.3%).", "Memory: Saturated."],
        'lv1_title': "Level 1: Small-Medium (1-128 Readers)",
        'lv1_desc': "Standalone Architecture.",
        'lv1_list': ["Server: 1 Unit", "SQL: SQL Express recommended.", "Risk: Single point of failure."],
        'lv2_title': "Level 2: Mid-Large (128-1,000 Readers)",
        'lv2_desc': "Distributed Architecture.",
        'lv2_list': ["Server: 2-3 Units", "SQL: SQL Standard Required.", "Split: Recommend split for >500 readers."],
        'lv3_title': "Level 3: Enterprise (1,000-2,000+ Readers)",
        'lv3_desc': "High Redundancy Architecture.",
        'lv3_list': ["Server: 4-6 Units", "Setup: DB Mirroring + App Server.", "Method: Segmentation."]
    }
}

# --- 2. 方案對比數據 (TLS 版本對比) ---
COMP_DATA = {
    'zh': {
        'items': ["安全性加密", "持卡人容量", "處理速度", "適用場所"],
        'aero': ["TLS 1.2 標準加密", "250,000 人", "中等速度", "中型辦公室 / 一般企業"],
        'merc': ["TLS 1.3 銀行級 (FIPS 140-3)", "2,000,000 人", "極速處理 (大流量)", "數據中心 / 金融機構"]
    },
    'en': {
        'items': ["Security Encryption", "Cardholders", "Processing Speed", "Application"],
        'aero': ["TLS 1.2 Standard", "250,000", "Moderate", "SME / Office"],
        'merc': ["TLS 1.3 / FIPS 140-3", "2,000,000", "Ultra-Fast", "Enterprise / Bank"]
    }
}

# --- 3. 計算邏輯 ---
def get_recommendation(readers, face, ipc, desktop, inputs, outputs, load_limit, L):
    num_controllers = math.ceil(readers / load_limit) if readers > 0 else 0
    num_reader_interfaces = math.ceil(readers / 2) if readers > 0 else 0
    
    # 硬體
    aero_hw = [{"n": "HID-X1100A Controller", "q": num_controllers}, {"n": "HID-X100A Reader Interface", "q": num_reader_interfaces}]
    if inputs > 0: aero_hw.append({"n": "HID-X200A Input Module", "q": math.ceil(inputs / 19)})
    if outputs > 0: aero_hw.append({"n": "HID-X300A Output Module", "q": math.ceil(outputs / 12)})

    merc_hw = [{"n": "HID-MP4502 Controller", "q": num_controllers}, {"n": "HID-MR52-S3 Reader Interface", "q": num_reader_interfaces}]
    if inputs > 0: merc_hw.append({"n": "HID-MR16IN-S3 Input", "q": math.ceil(inputs / 16)})
    if outputs > 0: merc_hw.append({"n": "HID-MR16OUT-S3 Output", "q": math.ceil(outputs / 16)})

    # 授權
    sw = [{"m": "LV-SWS-AC", "n": "Base Platform (Incl. 8RD/1DT)" if L=='en' else "基礎平台授權 (含 8門/1DT)", "q": 1}]
    if readers > 8: sw.append({"m": "LV-SWI-RD8", "n": "8-Reader Ext." if L=='en' else "8門門禁授權擴充", "q": math.ceil((readers-8)/8)})
    if desktop > 1: sw.append({"m": "LV-SWC-ACD", "n": "Extra Client" if L=='en' else "額外客戶端", "q": desktop-1})
    if ipc > 0: sw.append({"m": "LV-SWI-CV", "n": "CCTV License" if L=='en' else "CCTV 頻道授權", "q": ipc})
    if face > 0:
        sw.append({"m": "LV-SWI-FRT", "n": "Face Base Module" if L=='en' else "人臉識別基礎功能模組", "q": 1})
        sw.append({"m": "LV-SWI-FRD", "n": "Face Panel License" if L=='en' else "人臉面板機接入授權", "q": face})
    
    # Server 清單
    sv = []
    if readers <= 128:
        sv.append({"n": "Management Server (AIO)", "q": 1})
    elif readers <= 1000:
        sv.append({"n": "Database/Directory Server", "q": 1})
        sv.append({"n": "Communication Server", "q": 1})
    else:
        sv.append({"n": "Primary DB Server", "q": 1})
        sv.append({"n": "Mirror DB Server", "q": 1})
        sv.append({"n": "App Server", "q": 1})
        sv.append({"n": "Comm Servers (Segmentation)", "q": math.ceil(readers / 600)})

    return aero_hw, merc_hw, sw, sv

# --- 4. 初始化 ---
def init_session():
    keys = {'s_readers': 0, 's_ipc': 0, 's_face': 0, 's_desktop': 1, 's_inputs': 0, 's_outputs': 0, 's_load': 16}
    for k, v in keys.items():
        if k not in st.session_state: st.session_state[k] = v

# --- 5. 主介面 ---
def main():
    st.set_page_config(layout="wide", page_title="LIVE Planning Specialist")
    init_session()

    with st.sidebar:
        lang_choice = st.radio("Language / 語言", ["中文", "English"], horizontal=True)
        L = 'zh' if lang_choice == "中文" else 'en'

    st.title(f"🏢 {LANG[L]['title']}")
    st.divider()

    # Step 1: Input
    st.subheader(LANG[L]['step1'])
    with st.container(border=True):
        st.write(f"**{LANG[L]['load_setting']}**")
        # 修正語法：確保列表後無孤立逗號
        load_val = st.radio(
            "Design Load",
            [16, 32, 64],
            format_func=lambda x: {16: LANG[L]['load_stable'], 32: LANG[L]['load_standard'], 64: LANG[L]['load_extreme']}[x],
            horizontal=True, key='s_load', label_visibility="collapsed"
        )
        
        c1, c2, c3, c4 = st.columns(4)
        readers = c1.number_input(LANG[L]['readers'], 0, 8192, key='s_readers')
        ipc = c2.number_input(LANG[L]['ipc'], 0, 5000, key='s_ipc')
        face = c3.number_input(LANG[L]['face'], 0, 1000, key='s_face')
        desktop = c4.number_input(LANG[L]['desktop'], 1, 100, key='s_desktop')
        
        with st.expander(f"{LANG[L]['inputs']} / {LANG[L]['outputs']}"):
            cc1, cc2 = st.columns(2)
            inputs = cc1.number_input(LANG[L]['inputs'], 0, 4000, key='s_inputs')
            outputs = cc2.number_input(LANG[L]['outputs'], 0, 4000, key='s_outputs')

    # Step 2: 分析評估
    st.divider()
    st.subheader(LANG[L]['step2'])
    col_e, col_s = st.columns(2, gap="medium")
    
    with col_e:
        st.write(f"#### {LANG[L]['eval_title']}")
        if load_val == 16: box, t, d, l = st.success, LANG[L]['eval_16_title'], LANG[L]['eval_16_desc'], LANG[L]['eval_16_list']
        elif load_val == 32: box, t, d, l = st.info, LANG[L]['eval_32_title'], LANG[L]['eval_32_desc'], LANG[L]['eval_32_list']
        else: box, t, d, l = st.warning, LANG[L]['eval_64_title'], LANG[L]['eval_64_desc'], LANG[L]['eval_64_list']
        box(f"**{t}**\n\n*{d}*\n\n" + "\n".join([f"- {i}" for i in l]), icon="📊")

    with col_s:
        st.write(f"#### {LANG[L]['server_eval_title']}")
        if readers <= 128: sb, stitle, sdesc, slist = st.success, LANG[L]['lv1_title'], LANG[L]['lv1_desc'], LANG[L]['lv1_list']
        elif readers <= 1000: sb, stitle, sdesc, slist = st.info, LANG[L]['lv2_title'], LANG[L]['lv2_desc'], LANG[L]['lv2_list']
        else: sb, stitle, sdesc, slist = st.error, LANG[L]['lv3_title'], LANG[L]['lv3_desc'], LANG[L]['lv3_list']
        sb(f"**{stitle}**\n\n*{sdesc}*\n\n" + "\n".join([f"- {i}" for i in slist]), icon="🖥️")

    # Step 3: 清單
    st.divider()
    st.subheader(LANG[L]['step3'])
    ah, mh, sw, sv = get_recommendation(readers, face, ipc, desktop, inputs, outputs, load_val, L)
    
    ca, cm = st.columns(2, gap="large")
    with ca:
        st.info(f"### {LANG[L]['aero_title']}")
        st.write(f"*{LANG[L]['aero_desc']}*")
        t1, t2, t3 = st.tabs([LANG[L]['hw_tab'], LANG[L]['sw_tab'], LANG[L]['sv_tab']])
        with t1:
            for h in ah: st.write(f"● {h['n']} : **{h['q']}**")
        with t2:
            for s in sw: st.write(f"● **{s['m']}** | {s['n']} : **{s['q']}**")
        with t3:
            for v in sv: st.write(f"● {v['n']} : **{v['q']}**")
    with cm:
        st.success(f"### {LANG[L]['merc_title']}")
        st.write(f"*{LANG[L]['merc_desc']}*")
        t1, t2, t3 = st.tabs([LANG[L]['hw_tab'], LANG[L]['sw_tab'], LANG[L]['sv_tab']])
        with t1:
            for h in mh: st.write(f"● {h['n']} : **{h['q']}**")
        with t2:
            for s in sw: st.write(f"● **{s['m']}** | {s['n']} : **{s['q']}**")
        with t3:
            for v in sv: st.write(f"● {v['n']} : **{v['q']}**")

    # Step 4: 對比表格
    st.divider()
    st.subheader(LANG[L]['step4'])
    st.table({
        LANG[L]['comp_item']: COMP_DATA[L]['items'],
        "HID Aero": COMP_DATA[L]['aero'],
        "HID Mercury": COMP_DATA[L]['merc']
    })

if __name__ == "__main__":
    main()
