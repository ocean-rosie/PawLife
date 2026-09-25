import re, shutil, time
from pathlib import Path

p = Path('index.html')
if not p.exists():
    raise SystemExit('当前目录没有 index.html，请先 cd ~/PawLife')

txt = p.read_text(encoding='utf-8')
backup = p.with_name(f"index_backup_{time.strftime('%Y%m%d_%H%M%S')}.html")
shutil.copy2(p, backup)
print('已备份到', backup.name)

def replace_between(start_marker, end_marker, new_block, name):
    global txt
    s = txt.find(start_marker)
    if s == -1:
        print(f'⚠ 未找到: {name} / start_marker={start_marker}')
        return
    e = txt.find(end_marker, s)
    if e == -1:
        print(f'⚠ 未找到: {name} / end_marker={end_marker}')
        return
    txt = txt[:s] + new_block + "\n" + txt[e:]
    print(f'✓ 已更新: {name}')

def replace_first(old, new, name):
    global txt
    if old in txt:
        txt = txt.replace(old, new, 1)
        print(f'✓ 已更新: {name}')
    else:
        print(f'⚠ 未找到: {name}')

# 1) 默认进入健康管理
replace_first("view:'home'", "view:'health'", '默认首页改为健康管理')

# 2) logo 样式：缩小、绿色底、小爪印、暖色猫爪
css1 = re.compile(r"\.brand-mark\{[^}]*\}")
if css1.search(txt):
    txt = css1.sub(".brand-mark{width:34px;height:34px;border-radius:12px;background:var(--sage-deep);display:grid;place-items:center;color:#fff;box-shadow:0 8px 20px rgba(78,99,81,.22);overflow:hidden}", txt, count=1)
    print('✓ 已更新: logo 容器样式')
else:
    print('⚠ 未找到: logo 容器样式')

css2 = re.compile(r"\.brand-mark svg\{[^}]*\}\.brand-mark \.paw-fill\{[^}]*\}")
if css2.search(txt):
    txt = css2.sub(".brand-mark svg{width:22px;height:22px;display:block}.brand-mark .paw-fill{fill:#F6D8B8}", txt, count=1)
    print('✓ 已更新: logo 爪印样式')
else:
    print('⚠ 未找到: logo 爪印样式')

new_logo = r'''function logoMark(){return `<span class="brand-mark" aria-label="PawLife 标志"><svg viewBox="0 0 32 32" aria-hidden="true">
  <g class="paw-fill" transform="translate(1 11) scale(.86)">
    <ellipse cx="4.3" cy="4.6" rx="1.8" ry="2.6" transform="rotate(-18 4.3 4.6)"/>
    <ellipse cx="8.8" cy="2.9" rx="1.8" ry="2.7" transform="rotate(-6 8.8 2.9)"/>
    <ellipse cx="13.2" cy="2.9" rx="1.8" ry="2.7" transform="rotate(6 13.2 2.9)"/>
    <ellipse cx="17.6" cy="4.7" rx="1.8" ry="2.6" transform="rotate(18 17.6 4.7)"/>
    <path d="M6.2 11.4c0-2.7 2.4-4.8 5.8-4.8 3.2 0 5.9 2.2 5.9 5.1 0 2.8-2.1 4.6-4.9 4.6-.9 0-1.8-.2-2.6-.6-.7.5-1.5.7-2.4.7-1.1 0-1.8-.6-1.8-1.5 0-.5.1-1 .4-1.4-.3-.6-.4-1.3-.4-2.1z"/>
  </g>
  <g class="paw-fill" transform="translate(17 4) scale(.55)">
    <ellipse cx="4.3" cy="4.6" rx="1.8" ry="2.6" transform="rotate(-18 4.3 4.6)"/>
    <ellipse cx="8.8" cy="2.9" rx="1.8" ry="2.7" transform="rotate(-6 8.8 2.9)"/>
    <ellipse cx="13.2" cy="2.9" rx="1.8" ry="2.7" transform="rotate(6 13.2 2.9)"/>
    <ellipse cx="17.6" cy="4.7" rx="1.8" ry="2.6" transform="rotate(18 17.6 4.7)"/>
    <path d="M6.2 11.4c0-2.7 2.4-4.8 5.8-4.8 3.2 0 5.9 2.2 5.9 5.1 0 2.8-2.1 4.6-4.9 4.6-.9 0-1.8-.2-2.6-.6-.7.5-1.5.7-2.4.7-1.1 0-1.8-.6-1.8-1.5 0-.5.1-1 .4-1.4-.3-.6-.4-1.3-.4-2.1z"/>
  </g>
</svg></span>`}'''
replace_between('function logoMark()', 'function healthTabTo', new_logo, 'logo 图形')

new_category = r'''function categoryActive(cat){
 if(cat==='health')return state.view==='health'||state.view==='records';
 if(cat==='medical')return ['vet','care'].includes(state.view);
 if(cat==='locate')return ['pawview','safety'].includes(state.view);
 if(cat==='shop')return state.view==='shop';
 if(cat==='memory')return state.view==='memory';
 if(cat==='device')return state.view==='device';
 if(cat==='account')return ['my','profile'].includes(state.view);
 return false;
}'''
replace_between('function categoryActive(cat)', 'function shell', new_category, '栏目高亮逻辑')

new_shell = r'''function shell(content,title){
 const pet=p();
 const groups=[
  ['功能导航',[
    ['health','health','♥','健康管理'],
    ['medical','vet','✚','医疗服务'],
    ['locate','pawview','⌖','视角定位'],
    ['shop','shop','▣','健康严选'],
    ['memory','memory','♡','数字生命'],
    ['device','device','⌁','设备管理'],
    ['account','my','●','我的']
  ]]
 ];
 const navHtml=groups.map(g=>`<div class="nav-group"><div class="nav-group-title">${g[0]}</div>${g[1].map(x=>`<button class="nav-btn ${categoryActive(x[0])?'active':''}" onclick="navTo('${x[1]}')"><span class="nav-ico">${x[2]}</span>${x[3]}</button>`).join('')}</div>`).join('');
 return `<div class="app">
 <aside class="sidebar"><div class="brand">${logoMark()}PawLife</div>
 <button class="pet-switch" onclick="openPetSwitcher()"><span class="pet-avatar">${pet.emoji}</span><span class="pet-meta"><b>${pet.name}</b><span>${pet.breed} · ${pet.age}</span></span><span class="chev">⌄</span></button>
 <nav class="nav">${navHtml}</nav></aside>
 <header class="topbar"><span class="top-title">${title}</span><div class="top-actions"><span class="status-pill"><i class="dot"></i>项圈在线 · 日常健康模式</span><button class="icon-btn" onclick="navTo('my','notifications')">��</button><button class="icon-btn" onclick="navTo('my','settings')">⚙</button></div></header>
 <header class="mobile-top"><div class="brand">${logoMark()}PawLife</div><button class="mini-pet" onclick="openPetSwitcher()"><span>${pet.name}</span><span class="pet-avatar">${pet.emoji}</span></button></header>
 <main class="main"><div class="screen">${content}</div></main>
 <nav class="mobile-nav">${[['health','健康'],['vet','医疗'],['pawview','定位'],['shop','严选'],['my','我的']].map(([v,n])=>`<button class="mnav ${state.view===v?'active':''}" onclick="navTo('${v}')"><span class="ico">${v==='health'?'♥':v==='vet'?'✚':v==='pawview'?'⌖':v==='shop'?'▣':'●'}</span><span>${n}</span></button>`).join('')}</nav></div>`
}'''
replace_between('function shell(content,title)', 'function header', new_shell, '左侧栏目布局')

new_device_tabs = r'''function deviceTabs(active='pawview'){const tabs=[['pawview','宠物视角'],['safety','实时定位']];return `<div class="tabs category-tabs">${tabs.map(([k,n])=>`<button class="tab ${active===k?'active':''}" onclick="navTo('${k}')">${n}</button>`).join('')}</div>`}
function equipmentTabs(active='device'){const tabs=[['device','设备状态'],['hardware','硬件结构']];return `<div class="tabs category-tabs">${tabs.map(([k,n])=>`<button class="tab ${active===k?'active':''}" onclick="${k==='hardware'?`navTo('device','hardware')`:`navTo('device')`}">${n}</button>`).join('')}</div>`}'''
replace_between('function deviceTabs', 'function lifeTabs', new_device_tabs, '视角定位与设备管理标签')
replace_first("${deviceTabs('device')}", "${equipmentTabs('device')}", '设备状态页标签')
replace_first("${deviceTabs('hardware')}", "${equipmentTabs('hardware')}", '硬件结构页标签')

new_trend = r'''function healthTrendSeries(){const m={
 today:{labels:['08','10','12','14','16','18'],activity:[100,98,99,96,97,94],jump:[100,99,97,98,95,93],sleep:[100,101,100,102,103,105]},
 '7d':{labels:['周四','周五','周六','周日','周一','周二','今天'],activity:[100,98,99,96,97,95,94],jump:[100,99,97,98,95,93,90],sleep:[100,101,100,102,104,103,106]},
 '30d':{labels:['第1周','第2周','第3周','第4周','本周'],activity:[100,96,98,91,86],jump:[100,95,96,88,82],sleep:[100,103,102,109,114]},
 long:{labels:['4月','5月','6月','7月','8月','9月'],activity:[100,99,97,98,93,89],jump:[100,98,96,94,89,84],sleep:[100,101,103,104,108,111]}
};return m[state.healthRange]||m['30d']}'''
replace_between('function healthTrendSeries()', 'function linePoints', new_trend, '健康趋势数据')

new_home = r'''function home(){return shell(`${header('健康总览','用更像真实使用场景的方式，快速看到今天最重要的信息。')}<div class="grid g2"><section class="card card-pad"><span class="tag sage">Mimi 今日概况</span><h2 style="margin:10px 0 6px">整体状态稳定，右耳抓挠值得继续观察</h2><p class="muted">今天的异常不算严重，但比平时更频繁。建议结合宠物视角回看 16:20 的片段，再决定是否发起线上问诊。</p><div class="grid g3" style="margin-top:14px"><div class="mini-stat"><b>活动量</b><span>较基线 -6%</span></div><div class="mini-stat"><b>睡眠</b><span>15.8 小时</span></div><div class="mini-stat"><b>定位状态</b><span>当前在家中</span></div></div></section><section class="card card-pad"><div class="section-title">真实使用示例</div><div class="record-list"><div class="record-item"><b>09:10 早餐前喵叫</b><p class="muted">软件识别为“妈妈我饿了”，主人直接在手机里看到了提醒。</p></div><div class="record-item"><b>16:18 连续抓右耳</b><p class="muted">系统自动保存前后 30 秒片段，并提示可发起线上问诊。</p></div><div class="record-item"><b>21:02 家中定位</b><p class="muted">定位显示 Mimi 在客厅猫爬架附近，说明它并没有跑出家门。</p></div></div></section></div><div class="grid g3" style="margin-top:16px"><section class="card card-pad"><div class="section-title">推荐动作</div><ul class="bullet-list"><li>回看 16:18 宠物视角片段</li><li>继续观察抓挠和甩头是否重复</li><li>需要时一键发送近期趋势给兽医</li></ul></section><section class="card card-pad"><div class="section-title">今天的提醒</div><ul class="bullet-list"><li>晚间关节营养补充剂 1 次</li><li>本周老年体检提醒还有 2 天</li><li>设备电量 82%，无需充电</li></ul></section><section class="card card-pad"><div class="section-title">家庭状态</div><ul class="bullet-list"><li>家庭基站在线</li><li>客厅与卧室室内定位正常</li><li>主人与家人共享可见</li></ul></section></div>`,'健康总览')}'''
replace_between('function home()', 'function health', new_home, '首页真实示例')

new_sound = r'''function healthSoundPanel(){return `<div class="grid g2"><section class="card card-pad"><div class="section-title">今天的声音理解</div>${[['16:18','短促喵叫','厨房 · 走向食盆','妈妈我饿了。'],['13:32','呼噜声','窗边 · 趴卧','我现在很放松，好舒服。'],['09:10','轻声喵叫','玄关 · 主人准备出门','妈妈你要出门了吗？我想跟着你。'],['02:41','短促叫声','卧室门口 · 夜间活动','我想找你，快看看我。']].map((x,i)=>`<div class="sound-item"><button class="icon-btn" onclick="toast('播放声音片段 ${x[0]}')">▶</button><div><b>${x[0]} · ${x[1]}</b><div class="subtle">${x[2]}</div><div class="context">智能理解：${x[3]}</div></div><span class="tag ${i===0?'amber':'sage'}">${i===0?'需要关注':'情绪理解'}</span></div>`).join('')}</section><section class="card card-pad"><div class="section-title">个体化声音档案</div><p class="muted">不是只看一条叫声，而是结合这只宠物长期的发声习惯、地点、时间和行为，逐渐学习它自己的表达方式。</p><div class="grid g2" style="margin-top:12px"><div class="mini-stat"><b>高频进食提示</b><span>多出现在厨房 / 早晚饭前</span></div><div class="mini-stat"><b>放松呼噜声</b><span>多出现在窗边 / 午后</span></div><div class="mini-stat"><b>找主人叫声</b><span>多出现在玄关 / 卧室门口</span></div><div class="mini-stat"><b>夜间短叫</b><span>本周略有增加，继续观察</span></div></div><div class="notice" style="margin-top:14px">使用时间越长，软件越能贴近 Mimi 自己的“说话方式”，输出更自然、更像主人能理解的话。</div></section></div>`}'''
replace_between('function healthSoundPanel()', 'function healthRecordsPanel', new_sound, '声音理解内容')

new_pawview = r'''function pawview(){return shell(`${header('宠物视角','不做全天无意义录像，而是在有价值的时刻给你看见宠物当时看到了什么。')}${deviceTabs('pawview')}<div class="grid g2"><section class="card card-pad"><div class="section-title">实时画面示例</div><div style="height:240px;border-radius:18px;background:linear-gradient(180deg,#F6EFE6,#E8DDD0);border:1px solid var(--line);padding:18px;display:flex;flex-direction:column;justify-content:space-between"><div style="display:flex;justify-content:space-between;align-items:center"><span class="tag sage">实时在线</span><span class="subtle">客厅 · 2 秒前更新</span></div><div><h2 style="margin:0 0 6px">Mimi 正在客厅窗边休息</h2><p class="muted" style="margin:0">主人出差时，可以直接看到它是否在睡觉、晒太阳、玩耍或者在家里四处走动。</p></div><div class="grid g3" style="gap:10px"><div class="mini-stat"><b>当前动作</b><span>趴卧 / 放松</span></div><div class="mini-stat"><b>环境</b><span>窗边猫窝</span></div><div class="mini-stat"><b>声音</b><span>轻微呼噜声</span></div></div></div><div class="grid g3" style="margin-top:14px"><div class="card" style="padding:12px;border-radius:14px;background:#FCF8F2"><b>喂食前</b><p class="muted">主人查看它是不是已经走到食盆旁边。</p></div><div class="card" style="padding:12px;border-radius:14px;background:#FCF8F2"><b>独自在家</b><p class="muted">看它是在安静休息，还是持续焦躁地找人。</p></div><div class="card" style="padding:12px;border-radius:14px;background:#FCF8F2"><b>异常行为</b><p class="muted">抓挠、甩头时自动留下关键片段。</p></div></div></section><section class="card card-pad"><div class="section-title">事件片段</div><div class="record-list">${[['16:18','连续抓右耳','自动保存前后 30 秒，已可直接发送给兽医'],['13:52','午后晒太阳','识别为放松状态，自动归档到数字生命'],['09:10','早餐前喵叫','与进食时间吻合，已同步到声音理解'],['07:42','在家中走动','起床后正常巡游，定位显示在客厅与走廊']].map(x=>`<div class="record-item"><b>${x[0]} · ${x[1]}</b><p class="muted">${x[2]}</p></div>`).join('')}</div><div class="notice" style="margin-top:14px">真实使用中，主人最关心的通常不是“看一整天”，而是“什么时候该看、看哪一段最有价值”。</div></section></div>`,'宠物视角')}'''
replace_between('function pawview()', 'function safety', new_pawview, '宠物视角页')

new_safety = r'''function safety(){return shell(`${header('实时定位','既能看外出定位，也能在家里更直观地看到宠物当前大概在哪个房间。')}${deviceTabs('safety')}<div class="grid g2"><section class="card card-pad"><div class="section-title">当前位置</div><span class="tag sage">当前在家中</span><h2 style="margin:10px 0 6px">客厅猫爬架附近</h2><p class="muted">家庭基站在线 · 室内定位模式已开启 · 最近 5 分钟主要停留在客厅与走廊之间</p><div style="margin-top:14px;border:1px solid var(--line);border-radius:18px;padding:14px;background:#FCF8F2"><div style="display:grid;grid-template-columns:1fr 1fr;gap:10px"><div style="border:1px solid var(--line);border-radius:14px;padding:12px;background:#fff"><b>卧室</b><p class="muted" style="margin:6px 0 0">今天 02:41 出现夜间叫声</p></div><div style="border:1px solid var(--line);border-radius:14px;padding:12px;background:#EAF4EA"><b>客厅</b><p style="margin:6px 0 0;color:#4E6351">�� Mimi 当前在这里</p></div><div style="border:1px solid var(--line);border-radius:14px;padding:12px;background:#fff"><b>厨房</b><p class="muted" style="margin:6px 0 0">09:10 饭前靠近食盆</p></div><div style="border:1px solid var(--line);border-radius:14px;padding:12px;background:#fff"><b>玄关</b><p class="muted" style="margin:6px 0 0">主人出门时短暂停留</p></div></div></div></section><section class="card card-pad"><div class="section-title">外出与安全</div><div class="grid g2"><div class="mini-stat"><b>电子围栏</b><span>家庭安全区已开启</span></div><div class="mini-stat"><b>最近一次外出</b><span>昨天 18:20 与主人一起下楼</span></div><div class="mini-stat"><b>卫星定位</b><span>室外可自动切换</span></div><div class="mini-stat"><b>寻宠模式</b><span>一键提高定位频率</span></div></div><div class="record-list" style="margin-top:14px">${[['今天','家中停留','主要在客厅、走廊和卧室活动'],['昨天','外出散步','17:48 离家，18:26 回家'],['本周','活动范围','未离开家庭常用活动范围']].map(x=>`<div class="record-item"><b>${x[0]} · ${x[1]}</b><p class="muted">${x[2]}</p></div>`).join('')}</div></section></div>`,'实时定位')}'''
replace_between('function safety()', 'function device(){', new_safety, '实时定位页')

replace_first("header('设备与续航'", "header('设备管理'", '设备页面标题')
replace_first("header('分布式硬件结构'", "header('硬件结构'", '硬件结构标题')

new_shop = r'''function shop(){
 const cats=['推荐','关节友好','中老年主粮','家庭改造','术后护理','检测用品'];
 const all=[
  {cat:'推荐',name:'老年猫低台阶缓坡梯',store:'喵伴居家旗舰店',price:'¥129',sales:'月销 268',tag:'推荐给 Mimi',reason:'近期跳跃减少，先降低上高处的负担'},
  {cat:'推荐',name:'宠物防滑地垫 6 片装',store:'爪爪安心生活馆',price:'¥89',sales:'月销 512',tag:'推荐给 Mimi',reason:'最近起身与转身略慢，减少地面打滑'},
  {cat:'推荐',name:'中老年猫关节营养软咀嚼',store:'宠研营养旗舰店',price:'¥158',sales:'月销 326',tag:'推荐给 Mimi',reason:'适合关节与活动力日常维护'},
  {cat:'关节友好',name:'宠物沙发踏步凳',store:'尾巴家居店',price:'¥79',sales:'月销 193',tag:'居家辅助',reason:'上下沙发更轻松'},
  {cat:'关节友好',name:'可折叠宠物坡道',store:'毛孩子康护馆',price:'¥199',sales:'月销 145',tag:'居家辅助',reason:'适合中老年猫狗日常上床上沙发'},
  {cat:'中老年主粮',name:'中老年猫低脂主粮 1.5kg',store:'喵食实验室',price:'¥118',sales:'月销 689',tag:'营养管理',reason:'控制体重，减少关节压力'},
  {cat:'中老年主粮',name:'中老年犬关节配方粮 2kg',store:'宠物慢养旗舰店',price:'¥136',sales:'月销 204',tag:'营养管理',reason:'适合中老年犬日常维护'},
  {cat:'家庭改造',name:'猫爬架防滑踏面贴',store:'家有毛孩店',price:'¥39',sales:'月销 431',tag:'家庭改造',reason:'老年宠物在家活动更稳'},
  {cat:'家庭改造',name:'低边猫砂盆',store:'猫咪便利生活馆',price:'¥66',sales:'月销 381',tag:'家庭改造',reason:'更适合中老年猫进出'},
  {cat:'术后护理',name:'术后软圈',store:'温柔护理旗舰店',price:'¥35',sales:'月销 927',tag:'术后护理',reason:'轻量佩戴，减少活动受限'},
  {cat:'术后护理',name:'喂药器 2 支装',store:'好喂药宠物店',price:'¥19',sales:'月销 1502',tag:'术后护理',reason:'复诊期家庭护理更方便'},
  {cat:'检测用品',name:'宠物尿检试纸 10 条',store:'宠物家庭检测馆',price:'¥29',sales:'月销 823',tag:'家庭检测',reason:'适合居家初筛与长期观察'},
  {cat:'检测用品',name:'宠物便检采样套装',store:'安心检测旗舰店',price:'¥24',sales:'月销 277',tag:'家庭检测',reason:'就医前可先规范留样'}
 ];
 const q=(state.shopQuery||'').trim().toLowerCase();
 const current=state.shopCat||'推荐';
 const list=all.filter(x=>(x.cat===current) && (!q || `${x.name}${x.store}${x.reason}${x.tag}`.toLowerCase().includes(q)));
 const top=list.slice(0,3);
 return shell(`${header('健康严选','结合宠物年龄、健康变化与家庭场景，给出更有针对性的购买建议。')}<div class="notice">以下为界面演示示例。推荐理由会结合年龄、健康档案、近期异常和兽医建议动态调整。</div><section class="card card-pad" style="margin-top:14px"><span class="tag sage">Mimi 个性化推荐</span><h3 style="margin:10px 0 6px">当前优先推荐</h3><p class="muted">根据 Mimi 近30天跳跃减少、活动能力略降、偶发抓挠记录，目前优先推荐关节友好、家庭改造和中老年营养管理相关商品。</p><div class="grid g3" style="margin-top:12px">${top.map(x=>`<div class="card" style="padding:14px;border-radius:16px;background:#FCF8F2"><div style="display:flex;justify-content:space-between;gap:8px"><b>${x.name}</b><span class="tag sage">${x.price}</span></div><div class="subtle" style="margin-top:4px">${x.store} · ${x.sales}</div><p class="muted" style="margin:10px 0 8px">${x.reason}</p><div class="tag amber">${x.tag}</div></div>`).join('')}</div></section><div style="display:flex;gap:10px;align-items:center;margin:16px 0 14px"><input value="${state.shopQuery||''}" oninput="state.shopQuery=this.value;render()" placeholder="搜索商品、店铺或需求，例如：坡道 / 老年猫粮 / 尿检" style="flex:1;height:42px;border:1px solid var(--line);border-radius:14px;padding:0 14px;background:#fff;font-size:14px"><button class="btn secondary" onclick="toast('当前已按关键词筛选')">搜索</button></div><div class="tabs">${cats.map(c=>`<button class="tab ${(state.shopCat||'推荐')===c?'active':''}" onclick="state.shopCat='${c}';render()">${c}</button>`).join('')}</div><div class="grid g3">${list.map(x=>`<section class="card card-pad"><div style="display:flex;justify-content:space-between;align-items:flex-start;gap:12px"><div><h3 style="margin:0 0 6px">${x.name}</h3><div class="subtle">${x.store}</div></div><span class="tag sage">${x.price}</span></div><div class="subtle" style="margin-top:8px">${x.sales} · ${x.cat}</div><p class="muted" style="margin:12px 0 10px">推荐理由：${x.reason}</p><div style="display:flex;justify-content:space-between;align-items:center"><span class="tag amber">${x.tag}</span><button class="btn secondary" onclick="toast('已收藏：${x.name}')">收藏</button></div></section>`).join('')}</div>`,'健康严选')
}'''
replace_between('function shop()', 'function memory', new_shop, '健康严选商城')

# 可能存在的标题文案微调
replace_first('设备与安全', '视角定位', '左栏旧名称替换')
replace_first('设备管理中心', '设备管理', '设备管理文案')

p.write_text(txt, encoding='utf-8')
print('\n完成：index.html 已更新为第二版。')
print('下一步：')
print('1) python3 -m http.server 8000')
print('2) 浏览器打开 http://localhost:8000')
print('3) 确认无误后：git add index.html patch_pawlife_v2.py && git commit -m "PawLife v2" && git push')
