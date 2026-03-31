import re

file_path = "sound-keyword-expander_7.html"
with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

new_ucs_dims = """const UCS = [
  { id:'AMB', name:'Ambience', zh:'環境音 / 氛圍', color:'#4dd9ac',
    subs:['Forest 森林','Rain 雨聲','Wind 風聲','Ocean 海洋','River 河流','Cave 洞穴','Urban 城市','Room Tone 室內底噪'],
    keywords:{ en:['ambience','atmosphere','room tone','environment','nature','forest','rain','wind','ocean','river','cave','urban','city','night','outdoor','indoor','background','soundscape','birds','insects'], zh:['環境音','氣氛/氛圍','室內底噪/寂靜','周遭環境','大自然','森林','雨聲','風聲','海浪/海洋','河流/溪流','洞穴/山洞','市區','城市','夜晚','戶外','室內','背景音','音景','鳥叫','蟲鳴'] }
  },
  { id:'AMUS', name:'Amusement / Board Game', zh:'遊樂場 / 棋牌桌遊', color:'#5b9fff',
    subs:['Casino 賭場','Card 撲克牌','Mahjong 麻將','Dice 骰子','Slot 輪盤','Coin 硬幣'],
    keywords:{ en:['amusement','casino','arcade','slot machine','jackpot','roulette','gamble','pinball','coin drop','win','collect','chip','bonus','card','poker','mahjong','dice','shuffle','deal','board game'], zh:['遊樂場/遊樂園','賭場/娛樂城','電玩機台','老虎機/拉霸機','中大獎','輪盤','博弈賭博','彈珠台','投幣/掉幣','獲勝/贏錢','收集/贏取','籌碼/代幣','紅利/獎勵','撲克牌/卡牌','撲克','麻將/牌墊','骰子','洗牌/切牌','發牌','桌遊/棋盤遊戲'] }
  },
  { id:'CART', name:'Cartoon / Comedy', zh:'卡通 / 綜藝', color:'#ffb347',
    subs:['Boing 彈跳','Fall Drop 墜落','Slip 滑倒','Wah-wah 失敗','Laugh 笑聲','Drum roll 鼓陣'],
    keywords:{ en:['cartoon','comedy','boing','fall','drop','slip','wah-wah','laugh track','rimshot','drum roll','squeak','slide whistle','accent','funny','comic','glissando','bounce','bonk','plop','whoosh comedy','spring','tumble'], zh:['卡通動畫','喜劇綜藝','彈簧ㄉㄨㄞ','墜落/掉落','掉落/落下','滑倒意外','失敗挫折音效','罐頭笑聲','節目鼓邊敲擊','打鼓鋪陳','吱吱聲','滑音笛','強調重音','搞笑幽默','滑稽好笑','滑音','彈跳/彈起','敲頭/打頭','撲通聲','搞笑呼嘯/掠過','彈簧','翻滾/跌撞'] }
  },
  { id:'DSGN', name:'Sound Design', zh:'設計音 / 預告片', color:'#5b9fff',
    subs:['Rise 爬升','Drop 墜落','Hit 重擊','Braam 銅管重音','Sweep 掃過','Flash 閃現'],
    keywords:{ en:['sound design','rise','riser','drop','downer','braam','boom','hit','impact','sweep','swoosh','whoosh hit','glitch','tension','cinematic','trailer','build-up','sub bass','reverse','stutter','whoosh sting','flash','shimmer'], zh:['影視音效設計','升起/起飛','情緒爬升','情緒墜落','下沉特效音','銅管重低音','巨大轟鳴','重擊打擊','衝擊震撼','掃過/掃描','咻聲/飛過','打擊掠過','數位故障音效','緊張感/懸疑感','電影感/史詩感','預告片/廣告宣傳','情緒鋪陳','超低頻震動','反轉音效/倒轉','結巴/卡頓音效','刺耳掠過','閃光/閃現/刺眼','微光/法術閃爍'] }
  },
  { id:'ELEC', name:'Electricity', zh:'電流 / 電子', color:'#c8f060',
    subs:['Spark 火花','Zap 電擊','Shock 觸電','Arc 電弧','Hum 電流聲','Flash 閃爍'],
    keywords:{ en:['electricity','electric','elecetric','spark','zap','shock','static','arc','buzz','hum','short circuit','power','flash','lightning','energy'], zh:['電力設備','電力的/通電','電流/帶電','電火花/火星','快速電擊/雷射','觸電/電擊休克','靜電/雜訊','電弧放電','蜂鳴聲/電流叫聲','電流嗡嗡聲','短路故障','能源/能量','閃爍/閃光','閃電落雷','純粹能量'] }
  },
  { id:'EXP', name:'Explosion', zh:'爆炸 / 爆破', color:'#ff6b5b',
    subs:['Bomb 炸彈','Firework 煙火','Gas 氣體爆炸','Nuclear 核爆','Debris 碎片','Shockwave 衝擊波'],
    keywords:{ en:['explosion','boom','blast','bang','detonation','burst','bomb','grenade','dynamite','shockwave','debris','rubble','fire','nuclear','gas explosion','underwater explosion','firework','crack','rumble','tail'], zh:['劇烈爆炸','轟鳴/巨響','猛烈爆發','砰響聲','引爆過程','爆裂炸開','炸彈炸藥','手榴彈','TNT炸藥','強大衝擊波','四散碎片','倒塌瓦礫','火焰燃燒/火災','核子試爆','瓦斯氣爆','水下沉悶爆炸','煙火/慶典煙火','鞭炮爆竹聲','低頻轟隆餘震','殘響尾音'] }
  },
  { id:'FOL', name:'Foley', zh:'擬音 / 道具音', color:'#ffb347',
    subs:['Footsteps 腳步','Clothing 衣物','Props 道具','Keys 鑰匙','Paper 紙','Zipper 拉鍊'],
    keywords:{ en:['foley','footstep','walk','run','clothing','rustle','keys','paper','zipper','prop','movement','body','handling','pickup','put down','sit','stand','cloth','fabric','leather','creak'], zh:['電影擬音','腳步聲','走路/步行','跑步/狂奔','衣物衣裝','摩擦聲/沙沙聲','鑰匙/鑰匙圈','紙張/文件','拉鍊拉動','小道具/物件','發生動作','身體移動','操作/拿取物品','拿起物品','放下物品','坐下動作','站起來','布料摩擦','織物材質','皮革衣物','吱呀摩擦聲'] }
  },
  { id:'FST', name:'Footsteps', zh:'腳步聲', color:'#c8f060',
    subs:['Concrete 混凝土','Wood 木板','Gravel 碎石','Grass 草地','Metal 金屬','Sand 沙地','Snow 雪地','Mud 泥地'],
    keywords:{ en:['footstep','walk','run','jog','sprint','stomp','creep','sneak','boots','heels','sneakers','barefoot','concrete','wood','gravel','grass','metal','sand','snow','mud','carpet','tile','puddle','stairs'], zh:['腳步','走路','跑步','慢跑','衝刺','重踩','輕步走','悄悄移動','靴子','高跟鞋','運動球鞋','赤腳','混凝土','木板','碎石','草地','金屬','沙地','雪地','泥地','地毯','磁磚','水坑','樓梯'] }
  },
  { id:'GORE', name:'Gore / Flesh', zh:'血肉 / 血腥', color:'#f06090',
    subs:['Blood 噴血','Flesh 撕肉','Bone 骨折','Stab 刺入','Slice 切割','Squelch 黏稠'],
    keywords:{ en:['gore','flesh','blood','splatter','squelch','guts','bone break','bone crack','stab','slice','rip','tear','eviscerate','dismember','slurp','meat','visceral','crunch'], zh:['血腥暴力','血肉之軀','血液流出','噴血/濺血四散','黏稠擠壓黏液聲','流出內臟','骨頭受到斷裂','骨折/骨碎','鋒利穿刺','割開鮮肉','皮肉撕裂','大力撕開','開膛破肚','殘忍肢解','吸溜/令人作嘔聲','肉塊掉落','內臟攪動感','骨頭碎裂聲'] }
  },
  { id:'HIT', name:'Hit / Impact', zh:'打擊 / 衝擊', color:'#f06090',
    subs:['Punch 拳擊','Kick 踢擊','Melee 近戰','Body 肉體','Object 物件','Muffled 悶聲'],
    keywords:{ en:['hit','impact','punch','kick','strike','smack','slam','bash','whack','thud','crack','knock','bang','slap','clunk','collision','crash','melee','flesh','body hit','hard hit','soft hit','muffled','dull','sharp','stab','blunt'], zh:['打擊動作','強烈衝擊','拳頭拳擊','腳步踢擊','攻擊打碎','猛力揮打','用力砸門/猛擊','用力敲砸','沉重打擊','悶悶的打擊','清脆的撞擊','連續敲擊','砰撞巨響','狠狠摑打','沉悶的厚重撞擊','發生碰撞','墜毀/撞毀/撞車','近戰肉搏','肉體接觸','身體受到撞擊','用力過猛打擊','輕輕的打擊','被悶住的聲音','鈍鈍的聲音','銳利的金屬聲','刺入/扎入','鈍器重擊'] }
  },
  { id:'MAG', name:'Magic / Sci-Fi', zh:'魔法 / 科幻', color:'#5b9fff',
    subs:['Magic 魔法','Fire Magic 火系','Lightning 閃電','Shine 閃耀','Spell Cast 施法','Shield 護盾'],
    keywords:{ en:['magic','spell','cast','enchant','arcane','mystical','shimmer','sparkle','twinkle','shine','flash','glow','portal','teleport','laser','beam','energy','shield','barrier','lightning','thunder','sci-fi','futuristic','electric','plasma','charge','heal','buff'], zh:['魔法奇幻','魔法咒語','施法動作','附魔/強化裝備','奧術法術','神秘的/不可思議的','微光閃爍','閃耀/微明','星光閃爍','發光閃耀','閃現/一閃即逝','發出光圈','空間傳送門','瞬間移動','雷射/光束','粗大光束','純粹能量','圓形護盾','防禦屏障','閃電落下','雷鳴/雷光','科幻/未來世界','充滿未來感','電流/電擊','電漿/離子','聚神蓄力','治癒/補血','增益狀態/Buff'] }
  },
  { id:'MUSC', name:'Musical / Synth', zh:'音樂 / 合成器', color:'#5b9fff',
    subs:['Drone 低頻','Pad 氛圍','Stinger 短刺','Bass 重低音','Loop 循環','Synth 合成'],
    keywords:{ en:['musical','synth','synthesizer','drone','pad','stinger','808','sub bass','loop','beat','drum kit','arpeggio','chord','melody','harmony','rhythm','texture','splice','EDM'], zh:['音樂/樂曲','電子合成器','硬體合成器','持續低頻/無人機聲','氛圍鋪底墊音','音樂短刺/提示音','808低音鼓機','超重低頻極低音','音樂無縫循環樂句','節奏節拍','爵士鼓組','合成器琶音','和弦/和聲','主旋律','和聲/合唱','節奏律動','聲音材質音色','音效素材庫','電子舞曲'] }
  },
  { id:'WAT', name:'Water', zh:'水聲 / 液體', color:'#4dd9ac',
    subs:['Splash 濺水','Drip 滴水','Pour 倒水','Underwater 水下','Ocean 海浪','Rain 雨','Bubble 氣泡','Stream 溪流'],
    keywords:{ en:['water','splash','drip','pour','drop','bubble','stream','river','ocean','rain','underwater','submerge','plunge','plop','gurgle','trickle','flow','wave','foam','spray','mist','puddle','pool','liquid','flood','drain','sink'], zh:['水/清水','水花四濺/拍水','滴答滴水','倒水/傾倒','一顆水滴','水中氣泡','小溪流','河川河流','海洋汪洋','天空雨水','水面下/潛水','沉沒入水','快速投入水中','噗通入水聲','咕嚕咕嚕聲','涓涓細流','水流動','波浪/海浪','白色泡沫','噴灑/噴水','水霧/細霧','地上水窪','游泳池/水池','液體/流體','洪水氾濫','排水洞下水道','洗手槽/水槽'] }
  },
  { id:'WPN', name:'Weapons', zh:'武器 / 兵器', color:'#ff6b5b',
    subs:['Sword 劍','Arrow 箭矢','Gun 槍','Reload 換彈','Knife 刀','Bow 弓'],
    keywords:{ en:['gunshot','gunfire','shot','fire','shoot','pistol','rifle','shotgun','sniper','automatic','silenced','reload','cock','empty click','shell drop','casing','trigger','sword','blade','slash','swing','arrow','bow','knife','stab','draw','sheathe','gun','weapon','firearm','bullet','charge attack','blaster'], zh:['開槍聲/單發','連續槍擊/掃射','子彈成功射出','開火射擊','射擊動作','手槍','步槍/突擊步槍','散彈槍','狙擊槍','全自動步槍','安裝消音管','重新裝彈/換彈匣','拉槍機/上膛','空槍卡搭聲','彈殼掉落地面','彈殼/金屬空殼','扣動扳機','劍/長劍','刀刃/鋒利','用力揮砍','揮動武器','箭矢/羽箭','弓/長弓','小刀/匕首','刺入/捅入','拔出武器/拔刀','收入刀鞘/收刀','槍枝總稱','裝備武器','近代火器','單枚子彈','蓄力猛烈攻擊','科幻雷射槍'] }
  },
  { id:'WHO', name:'Whoosh / Swish', zh:'呼嘯 / 掠過', color:'#c8f060',
    subs:['Fast 快速','Slow 緩慢','Magical 魔法','Air 空氣','Fabric 布料','Blade 刀刃'],
    keywords:{ en:['whoosh','swoosh','swish','whiz','whizz','zip','zoom','rush','dart','streak','blur','air','wind','blast','gust','displacement','draft','sword whoosh','blade','arrow','bullet','cloth','cape','transition','pass','fly','sweep','stinger','heavy whoosh','light whoosh'], zh:['空氣呼嘯','嗖的一聲','用力揮動聲','呼茲聲','飛嘯而過','疾速穿飛','急速變速/縮放','衝刺上前','如飛鏢般掠過','劃過天際','視覺模糊聲','新鮮空氣','冷冽的風','強烈氣爆','一陣陣風','空氣阻力排開','細微冷風','劍氣呼嘯聲','刀刃破空聲','箭矢飛掠過','子彈飛過耳邊','衣服布料抖動','英雄披風揮動','畫面轉場','物體經過','飛行經過','掃過畫面','短刺的呼嘯','厚重的呼嘯','輕薄的呼嘯'] }
  },
  { id:'UI', name:'UI / Notification', zh:'介面音效 / 通知', color:'#5b9fff',
    subs:['Notification 通知','Chime 鐘聲','Win 勝利','Collect 收集','Gain 獲得','Game UI 遊戲'],
    keywords:{ en:['notification','alert','ping','ding','chime','beep','pop','success','complete','win','unlock','reward','level up','collect','gain','get','acquire','positive','error','fail','wrong','deny','buzz','decline','click','tap','toggle','swipe','transition','UI','interface','game sound','achievement','coin','inventory','typing'], zh:['系統通知音','警告/提醒通知','清脆Ping聲','叮咚聲/叮的聲','鐘聲音效/風鈴','電子嗶嗶聲','彈出視窗/氣泡聲','任務成功','動作完成','遊戲勝利','解鎖新要素','獲得豐厚獎勵','等級提升/升等','收集物資/道具','獲得/增加好處','成功取得','順利獲取','正向良好反饋','發生錯誤','遭遇失敗的聲音','覺得錯了的音效','拒絕操作/不允許','錯誤蜂鳴聲','婉拒/退回','滑鼠點擊/按鍵','手指輕觸畫面','切換開關/Toggle','手指滑動畫面','視覺過渡轉場','使用者總介面','介面音效操作','遊戲內部音效','成就順利達成','順利獲得金幣','開啟背包/物品欄','打字聲/鍵盤敲擊'] }
  },
  { id:'NAT', name:'Nature / Animals', zh:'自然 / 動物', color:'#c8f060',
    subs:['Thunder 雷聲','Wind 風','Fire 火','Animal 動物','Birds 鳥鳴','Insects 昆蟲'],
    keywords:{ en:['thunder','lightning strike','wind gust','storm','fire crackling','fire','flame','animal','creature','beast','bird','wolf','bear','horse','insect','cricket','frog','earth','rock','gravel','leaves','branch','tree','nature'], zh:['巨大雷聲','閃電擊中地面','強風陣陣吹來','狂風暴雨','柴火劈啪作響','兇猛火焰','溫暖火苗','各種動物','未知生物','凶狠的野獸','清脆鳥鳴','狼嚎叫','熊吼叫','馬匹嘶鳴','各種昆蟲','蟋蟀叫聲','青蛙呱呱叫','泥土/大地','巨大岩石','碎石/礫石','掉落的樹葉','掉落的樹枝','樹木本體','大自然環境'] }
  },
  { id:'MEC', name:'Mechanical', zh:'機械 / 工業', color:'#ffb347',
    subs:['Engine 引擎','Gear 齒輪','Motor 馬達','Industrial 工業','Door 門','Lock 鎖','Switch 開關'],
    keywords:{ en:['mechanical','machine','engine','motor','gear','industrial','factory','robot','servo','hydraulic','pneumatic','door','lock','switch','lever','button','crank','ratchet','click mechanical','clank','hum','whir','grind','metallic','metal'], zh:['機械的/機械感','機器設備/機器人','汽車機車引擎','電動馬達','轉動齒輪','工業的/重工業','工廠環境/廠房','大型機器人/機甲','微小伺服馬達','油壓/液壓系統','氣動系統/氣壓','厚重的大門','上鎖解鎖門鎖','電源開關','拉動拉桿','按鈕動作','曲柄轉動','棘輪結構','機械點擊組合聲','金屬碰撞撞擊聲','嗡嗡低嗚運轉','轉動/旋轉聲','研磨摩擦刺耳聲','金屬特質/金屬聲','實心金屬'] }
  },
  { id:'BRK', name:'Break / Destroy', zh:'破壞 / 碎裂', color:'#f06090',
    subs:['Glass 玻璃','Wood 木頭','Metal 金屬','Concrete 混凝土','Ice 冰','Plastic 塑膠'],
    keywords:{ en:['break','crack','smash','shatter','crumble','collapse','destroy','glass','wood','metal','concrete','ice','plastic','ceramic','bone','wall','debris','crunch','snap','rip','tear','splinter','fracture'], zh:['應聲破裂','產生裂開裂痕','粉碎/砸爛','完全打碎飛散','緩慢崩解/崩落','建築物倒塌','進行破壞','玻璃製品','純木頭','堅硬金屬','堅硬混凝土/水泥','急凍冰塊','塑膠製品','陶瓷器/瓷碗','生物骨骼/腿骨','一面牆壁','漫天碎片','碎裂聲/咀嚼聲','脆生生的折斷','從中撕開/撕破','用力暴力撕裂','木片裂開/刺碎','猛烈斷裂/骨折'] }
  }
];

const DIMS = {
  genre:{ label:'Genre / Media', zh:'媒體與風格', color:'#5b9fff', tokens:{
    'comedy|variety|cartoon|綜藝|搞笑|喜劇|趣味|罐頭音效|綜藝摔|烏鴉飛過|好笑|大爆笑|綜藝節目':{ en:['comedy','variety show','cartoon','funny','silly','boing','laugh track','rimshot','funny slide'], zh:['喜劇','綜藝節目','卡通','搞笑','滑稽的','彈簧/ㄉㄨㄞ','罐頭笑聲','鼓邊敲擊','搞笑滑音'] },
    'cinematic|trailer|dsgn|廣告|預告|電影|宣傳|設計音|影視|大片|震撼':{ en:['cinematic','trailer','sound design','epic','dramatic','boom','braam','movie','promo'], zh:['電影感','預告片','音效設計','史詩浩瀚','充滿戲劇張力','巨大轟鳴','銅管重低音','電影性質','宣傳短片'] },
    'game|8-bit|retro|遊戲|電玩|手遊|8位元|像素|電動|主機|紅白機|街機':{ en:['game','video game','8-bit','retro','arcade','chiptune','level up','coin','UI'], zh:['遊戲性質','電子遊戲','8位元','復古風','大型街機','晶片音樂','升級','獲得金幣','使用者介面'] },
    'splice|edm|music|電子|節拍|音樂|合成器|素材|舞曲|歌|弦律':{ en:['EDM','synth','musical','beat','splice material','loop','bass','techno'], zh:['電子舞曲','合成器','音樂性質','節拍','套裝素材','無縫循環','重低音','Techno電音'] },
    'board|card|casino|arcade|賭場|博弈|拉霸|老虎機|麻將|撲克牌|紙牌|牌|桌遊|棋類|骰子|擲骰|籌碼':{ en:['board game','card game','casino','arcade','slot machine','mahjong','dice','poker','chip','gamble'], zh:['桌遊/棋盤遊戲','紙牌/撲克牌','賭場','大型機台','老虎機','麻將','骰子','博弈賭博','籌碼','下注賭博'] }
  }},
  emotion:{ label:'Emotion / Vibe', zh:'情緒 / 氛圍', color:'#ffb347', tokens:{
    'tense|suspense|緊張|懸疑|壓迫|恐懼|恐怖|可怕|嚇|驚悚':{ en:['tense','suspense','thriller','horror','creepy','eerie','dread','build-up','heartbeat'], zh:['緊張局勢','懸疑感','驚悚片','恐怖性質','令人毛骨悚然','怪異氣氛','恐懼感','情緒鋪陳','心跳加速'] },
    'epic|triumph|史詩|壯闊|勝利|震撼|浩大|大場面|宏偉':{ en:['epic','triumph','massive','huge','victorious','majestic','grand'], zh:['史詩壯闊','獲得勝利感','龐大的','巨大的','旗開得勝','雄偉的','宏大的'] },
    'positive|happy|win|正向|開心|愉悅|成功|肯定|贏|得|答對|正確':{ en:['positive','happy','cheerful','success','confirm','accept','reward','win','gain'], zh:['正向情緒','開心的','愉快的','成功完成','確認','接受','獎勵感','獲勝贏得','獲得'] },
    'negative|sad|fail|負面|悲傷|失敗|拒絕|錯誤|錯|敗|不|難過|傷心|慘|無效|答錯':{ en:['negative','sad','fail','error','deny','wrong','wah-wah','decline'], zh:['負面情緒','悲傷的','失敗感','錯誤發生','拒絕發生','不對的聲音','失敗滑音','婉拒'] }
  }},
  material:{ label:'Material', zh:'材質', color:'#ffb347', tokens:{
    'plastic|塑膠|塑料|塑膠管|管子|硬質|合成|保麗龍':{ en:['plastic','hollow plastic','hard plastic','synthetic','rigid','PVC','tube','pipe'], zh:['塑膠','空心塑膠','硬質塑膠','合成材料','堅硬的','PVC材質','管子','水管/管線'] },
    'wood|木|木頭|木板|木門|木製|原木|硬木|地板|木質|木製品|樹幹':{ en:['wood','wooden','timber','plank','log','hardwood','floorboard','lumber'], zh:['木頭','木製的','木材','木板塊','原木圓木','硬木','木質地板','厚木板'] },
    'metal|金屬|鐵|鋼|鋁|銅|鐵管|黃銅|鋼鐵|鋁管':{ en:['metal','metallic','steel','iron','aluminum','copper','brass','tin','chrome'], zh:['金屬材質','金屬的','鋼鐵','鐵','鋁','銅','黃銅','錫板','鍍鉻'] },
    'glass|玻璃|玻璃杯|玻璃瓶|陶瓷|瓷器|水晶|杯子':{ en:['glass','crystal','ceramic','porcelain','bottle','jar'], zh:['玻璃','水晶','陶瓷','瓷器','玻璃瓶','玻璃罐'] },
    'stone|石|岩|混凝土|concrete|磚|碎石|磚塊|岩石|石頭|水泥|柏油':{ en:['stone','rock','concrete','gravel','rubble','brick','tile','cobblestone'], zh:['石頭材質','岩石','混凝土','碎石子','瓦礫堆','磚頭','磁磚','鵝卵石'] },
    'cloth|布|織物|fabric|衣服|衣物|布料|絲綢|棉花|皮革|皮|毛巾':{ en:['cloth','fabric','textile','silk','cotton','leather','clothing','rustle'], zh:['布料','織物','紡織品','絲綢','棉花','皮革','衣物衣裝','摩擦聲'] },
    'ice|冰|冰塊|結冰|霜|冰晶|冰裂|凍|寒':{ en:['ice','frozen','frost','crystal ice','ice crack','freeze'], zh:['冰塊','結冰的','結霜','水晶冰塊','冰塊裂開','凍結'] },
    'paper|紙|紙張|書|厚紙板|報紙|書頁|摺紙':{ en:['paper','cardboard','newspaper','book','page','crumple','tear paper'], zh:['紙張','厚紙板','報紙','書籍','書頁','揉紙團','撕紙張'] },
    'rubber|橡膠|輪胎|球|彈性|彈跳|橡皮|矽膠':{ en:['rubber','bounce','ball','tire','elastic','squeak'], zh:['橡膠','彈跳','皮球','輪胎','彈性特質','橡膠摩擦吱吱聲'] },
    'liquid|液體|汽水|飲料|油|泥|黏液|特調|藥水':{ en:['liquid','fluid','slime','mud','oil','viscous','gooey'], zh:['液體的','流體','史萊姆黏液','泥漿','油水','黏稠特質','沾黏感'] },
    'bone|骨|骨頭|骨骼|關節|骨折|骷髏':{ en:['bone','crack bone','crunch','snap','skeletal','joint'], zh:['骨頭','斷骨聲','咀嚼/碎裂聲','清脆折斷','骨骼的','關節處'] },
    'flesh|meat|肉|血肉|人體|內臟|血|噴血|肉塊|身體|器官':{ en:['flesh','meat','blood','splatter','squelch','guts','visceral'], zh:['血肉','肉類','血水','噴濺濺出','黏稠擠壓聲','內臟','直覺/內臟的'] },
    'rope|chain|繩|鐵鍊|鍊子|鐵絲|纜繩|絲|鎖鏈':{ en:['rope','chain','wire','cable','rattle chain'], zh:['繩子','鐵鍊','鋼絲鐵絲','纜線','鐵鍊碰撞聲'] },
  }},
  action:{ label:'Action', zh:'動作', color:'#f06090', tokens:{
    'fall|drop|落|掉|落下|跌|跌倒|墜落|摔|摔倒|摔落|倒下|塌|墜|跌落|倒地':{ en:['fall','drop','tumble','trip','stumble','collapse','topple','plop','body fall','thud fall','descend'], zh:['落下','掉落','翻滾','絆倒','踉蹌','倒塌','傾倒','噗通掉落','身體倒地','沉悶跌落聲','下降'] },
    'hit|strike|打|擊|撞|拍|砸|敲|捶|重擊|猛擊|打到|碰到|揍|尻|撞擊|擊打|揍打':{ en:['hit','impact','strike','smack','slam','bash','collision','pound','thump','knock','whack'], zh:['擊中/打擊','衝擊','攻擊打碎','拍擊','用力摔門','猛擊','碰撞','連續捶打','重擊碰響聲','敲打','重重的一擊'] },
    'break|shatter|crack|碎|裂|打碎|破|爆裂|破碎|裂開|碎掉|骨折|斷裂|崩塌':{ en:['break','crack','shatter','smash','crunch','snap','fracture','splinter','burst','bone crack'], zh:['破裂','裂開','粉碎','砸碎','碎裂聲','折斷','斷裂','木片碎裂','爆開','骨頭斷裂'] },
    'slide|scrape|滑|刮|拖|摩擦|刮擦|滑動|打滑|拖拉|拉動|擦':{ en:['slide','scrape','scratch','drag','grind','friction','skid','scuff'], zh:['滑動','刮擦','抓撓','拖拉','研磨','摩擦','打滑','腳步刮地'] },
    'open|close|門|開|關|推|拉門|關門|開門|門軸|門縫|打開|關閉':{ en:['open','close','door open','door close','creak','latch','slam door','shut','hinge'], zh:['打開','關閉','開門','關門','吱呀作響','門閂','用力關門','關上','鉸鏈門軸'] },
    'roll|滾|翻滾|滾動|旋轉|滾落|轉動|轉|迴旋':{ en:['roll','tumble','spin','rotate','barrel roll','rolling'], zh:['滾動','翻滾','快速旋轉','轉動','桶狀翻滾','持續滾動'] },
    'fly|whoosh|飛|掠過|穿過|飛行|飛翔|劃過|閃過|劃|飆過':{ en:['whoosh','fly','pass','sweep','zip','dart','rush','soar','swish'], zh:['呼嘯而過','飛行','掠過經過','掃過','快速拉開','如飛鏢般穿過','衝刺而過','翱翔高飛','揮動物品'] },
    'slash|swing|揮|砍|劈|揮舞|揮動|揮砍|劈砍|切|割':{ en:['slash','swing','swipe','chop','cleave','cut','slice','sword swing'], zh:['劈砍','揮動','大力揮過','砍柴','劈開','切割','切片','揮劍'] },
    'shoot|release|射|發射|射箭|射擊|開槍|射出|丟出|投射':{ en:['shoot','release','fire','launch','bowstring','gunshot','arrow release'], zh:['射擊','釋放射出','開火','發射','弓弦拉緊/彈出','槍擊','箭矢射出'] },
    'jump|leap|跳|跳躍|起跳|彈跳|彈起|落地|跳起|蹦':{ en:['jump','leap','hop','spring','bounce','land','landing','jump land'], zh:['跳躍','飛躍','小跳步','彈跳/彈簧','重複彈起','降落','落地瞬間','跳躍著地'] },
    'throw|toss|丟|投|拋|扔|投擲|拋出|丟出|甩出':{ en:['throw','toss','hurl','fling','launch','projectile'], zh:['投擲','拋出','用力扔出','猛拋','發射出去','拋射物'] },
    'punch|kick|拳|踢|揍|踹|拳擊|踢擊|揮拳|踹踢|迴力踢':{ en:['punch','kick','strike','jab','uppercut','roundhouse','stomp','martial arts'], zh:['出拳','踢腳','攻擊擊打','刺拳','上勾拳','迴旋踢','用力重踩','武術動作'] },
    'grab|grasp|抓|握|抱|拉扯|扭打|搏鬥|抓住|扯':{ en:['grab','grasp','grip','clutch','tackle','grapple','wrestle'], zh:['抓取','緊握','握把/緊緊抓住','死命抓住','擒抱','近身搏鬥','摔角扭打'] },
    'explosion|burst|爆|炸|爆炸|爆裂|炸開|爆發|firework|煙火|爆破':{ en:['explosion','blast','boom','burst','bang','detonate','shockwave','firework','crack'], zh:['爆炸','爆發','巨大轟鳴','爆開/炸裂','砰響','引爆炸彈','衝擊波','煙火','鞭炮聲響'] },
    'crash|衝撞|碰撞|撞車|墜機|撞擊|相撞|撞|車禍':{ en:['crash','collision','impact','wreck','smash','crunch','vehicle crash'], zh:['墜毀/撞毀','碰撞','衝擊打擊','殘骸/失事','用力砸碎','粉碎聲響','車輛撞擊'] },
    'pour|倒|潑|灑|流|倒水|潑灑|倒出':{ en:['pour','splash','spill','drip','trickle','flow','gush'], zh:['傾倒水流','水花四濺','潑灑溢出','滴滴答答','細密水流','流動','大量噴湧'] },
    'rip|tear|撕|撕裂|撕破|撕開|撕掉':{ en:['rip','tear','shred','fabric tear','paper tear','flesh tear'], zh:['撕裂','撕開','切成碎片','衣物撕破','紙張撕除','血肉撕裂'] },
    'stab|pierce|刺|穿刺|插入|刺穿|刺進|扎入':{ en:['stab','pierce','puncture','impale','thrust'], zh:['刺入','穿透','刺穿爆胎','刺穿身體','猛力推進'] },
    'knock|敲門|叩|敲擊|叩門|敲打門|敲':{ en:['knock','rap','tap','bang door','door knock'], zh:['敲擊','快速敲聲','輕敲','用力拍門','敲門聲'] },
    'squeeze|壓|擠|壓扁|擠壓|壓縮|扁':{ en:['squeeze','crush','compress','squish','press'], zh:['擠壓','壓碎','壓縮','黏稠擠壓','按壓壓迫'] },
    'swim|splash|游|游泳|入水|跳水|潛水|破水':{ en:['swim','splash','dive','plunge','water entry','underwater movement'], zh:['游泳','潑水','潛水','投入水中','入水瞬間','水下移動'] },
    'eat|drink|咬|嚼|喝|吞|咀嚼|飲食|吃|吸溜':{ en:['bite','chew','drink','swallow','eat','munch','slurp'], zh:['咬一口','咀嚼','喝水','吞嚥','吃東西','用力咀嚼','吸溜喝湯'] },
    'charge|riser|rise|build|蓄力|聚能|爬升|集氣|充能|蓄|漸強|越來越大':{ en:['charge','charge up','riser','rise','build-up','power up','crescendo','swell'], zh:['蓄力','充能完畢','情緒爬升','升起','氣氛鋪陳','威力提升','漸強音','聲勢漸漲'] },
    'collect|gain|get|收集|獲得|取得|得到|撿起|收|得|拿|拾取|裝備':{ en:['collect','gain','get','acquire','pickup','obtain','receive'], zh:['收集','獲得收益','取得','獲得/擁有','撿起','獲取','收到/接收'] },
    'shuffle|deal|洗牌|發牌|翻牌|切牌|打牌':{ en:['shuffle','deal','card flip','draw','card slide'], zh:['撲克洗牌/麻將洗牌','發牌','翻牌/翻翻看','抽牌/摸牌','卡牌摩擦'] },
    'roll|擲骰|丟骰子|骰子|甩子|搖骰':{ en:['roll dice','dice roll','tumble dice','scatter dice','shake dice'], zh:['擲骰子','骰子滾動','骰子翻滾','散落骰子','搖骰盅'] },
  }},
  weapon:{ label:'Weapon Type', zh:'武器類型', color:'#ff6b5b', tokens:{
    'sword|劍|武士刀|katana|sabre|長劍|闊劍|西洋劍|刀鳴|劍鳴|拔劍|入鞘':{ en:['sword','blade','sabre','katana','longsword','broadsword','rapier','sword draw','sword sheathe','sword whoosh'], zh:['劍','刀刃','軍刀','武士刀','長劍','闊劍','西洋劍','拔劍聲','收劍入鞘','劍氣呼嘯'] },
    'knife|dagger|刀|匕首|小刀|刺刀|細刃|短刀':{ en:['knife','dagger','stiletto','blade','switchblade','combat knife'], zh:['小刀','匕首','短劍/細劍','刀鋒','彈簧刀','戰鬥匕首'] },
    'arrow|bow|弓|箭|弩|箭矢|弓弦|羽箭|箭袋|射箭':{ en:['arrow','bow','bowstring','crossbow','quiver','fletching','arrow fly','arrow hit'], zh:['箭矢','弓','弓弦','十字弩','箭袋','羽毛箭','箭矢飛行','射中目標'] },
    'axe|斧|戰斧|斧頭|小斧|劈斧':{ en:['axe','hatchet','battle axe','cleave','axe swing'], zh:['斧頭','小手斧','戰鬥斧','劈開','揮舞斧頭'] },
    'spear|lance|矛|長矛|刺擊|標槍|長槍':{ en:['spear','lance','pike','thrust','javelin','polearm'], zh:['矛','長槍騎槍','長柄槍','突刺','標槍','長柄武器'] },
    'gun|pistol|rifle|槍|手槍|步槍|槍聲|槍擊|開火|子彈|彈殼|換彈|消音|散彈|狙擊|機槍':{ en:['gunshot','pistol','rifle','shotgun','sniper','automatic','silenced','reload','shell drop','bullet','firearm','cock','trigger','machine gun'], zh:['開槍聲','手槍','步槍','散彈槍','狙擊槍','自動化步槍','安裝消音管','重新裝彈','彈殼掉落','子彈','火器武器','拉開保險','扣下扳機','機關槍'] },
    'bomb|explosives|炸彈|手榴彈|炸藥|地雷|爆裂物|煙火|鞭炮':{ en:['bomb','grenade','dynamite','mine','explosive','detonate'], zh:['炸彈','手榴彈','炸藥','地雷','爆裂物','引爆'] },
    'blaster|sci-fi gun|雷射槍|光線槍|科幻武器|電漿槍|雷射|光束':{ en:['blaster','sci-fi gun','plasma rifle','laser gun','stun gun','ray gun'], zh:['爆能槍','科幻槍枝','電漿步槍','雷射槍','電擊槍','光線槍'] },
  }},
  environment:{ label:'Environment', zh:'環境 / 空間', color:'#4dd9ac', tokens:{
    'water|水|水中|入水|濺水|沉入|水下|撲通|液體|潮濕|水聲':{ en:['water','splash','submerge','underwater','plunge','plop','gurgle','drip','stream','water drop'], zh:['水','濺起水花','沉沒','水底下','投入水中','撲通聲','咕嚕咕嚕聲','滴漏','溪流','水滴落'] },
    'rain|雨|毛毛雨|大雨|雨滴|降雨|雨聲|下雨|陣雨|雷雨':{ en:['rain','drizzle','downpour','raindrop','rainfall','storm rain','light rain','heavy rain'], zh:['下雨','毛毛細雨','傾盆大雨','雨滴','降水量','暴風雨','輕微小雨','豪雨'] },
    'snow|雪|降雪|暴風雪|雪粉|積雪|雪地|下雪|白雪':{ en:['snow','snowfall','blizzard','powder snow','snow crunch','snow footstep'], zh:['雪','降雪量','暴風雪','粉雪','踩雪聲','雪地腳步聲'] },
    'fire|flame|火|火焰|燃燒|噼啪|餘燼|篝火|火災|火堆|火焰聲|火苗|著火':{ en:['fire','flame','burning','crackle','ember','campfire','wildfire','torch','fire roar'], zh:['火','火焰','燃燒中','劈啪作響','餘燼火苗','營火帳篷','野火熊熊','火炬','火焰燃爆'] },
    'wind|風|陣風|強風|狂風|微風|風吹|颳風|冷風|熱風|起風|颱風':{ en:['wind','gust','breeze','howl','wind blast','blowing wind','strong wind','light wind'], zh:['風','陣風','微風','呼嘯寒風','強烈氣流','吹風','強風','微弱和風'] },
    'thunder|lightning|雷|閃電|雷聲|打雷|暴風雨|雷電|閃電聲|落雷':{ en:['thunder','lightning','thunderstorm','rumble thunder','crack thunder','thunder roll'], zh:['雷鳴','閃電','雷雨交加','轟隆雷聲','清脆打雷聲','雷聲翻滾'] },
    'cave|洞|洞穴|回響|迴聲|隧道|殘響|空曠|回音|空洞|空間感|山洞':{ en:['cave','reverb','echo','cavern','tunnel','reverberant','large space','stone room'], zh:['洞穴','殘響效果','回音現象','大岩洞','隧道內','充滿回音的','廣大空間','石室'] },
    'forest|林|森林|樹林|叢林|自然|樹葉|樹枝|樹木|林中|大自然':{ en:['forest','jungle','nature','leaves','branch','birds','woodland','rustling leaves'], zh:['森林','叢林雨林','大自然','樹葉','樹木枝幹','鳥類','林地','樹葉沙沙聲'] },
    'ocean|sea|海|海浪|海洋|波浪|海灘|浪聲|漲潮|退潮':{ en:['ocean','sea','waves','beach','surf','underwater','tide','ocean ambience'], zh:['海洋','大海','海浪拍打','海灘','衝浪海域','海底','潮汐現象','海洋環境音'] },
    'river|stream|河|溪|溪流|河流|流水|水流|小溪':{ en:['river','stream','creek','flowing water','babbling brook','rapids'], zh:['河流','溪流','小溪水','流動的水','潺潺小溪','激流急流'] },
    'city|urban|城市|都市|街道|交通|車聲|人群|市區|馬路|街上':{ en:['city','urban','traffic','street','crowd','city ambience','bus','subway'], zh:['城市地帶','都會區','交通車流','街道巷弄','人群','城市環境音','巴士公車','地鐵捷運'] },
    'outdoor|室外|戶外|開放|外面|野外|戶外空間|外':{ en:['outdoor','exterior','open air','field','meadow','open space'], zh:['戶外地帶','外部空間','露天空曠處','遼闊田野','草原','空地空間'] },
    'indoor|室內|房間|密閉|房子|屋內|室內空間|內':{ en:['indoor','interior','room','enclosed','inside','hallway','corridor'], zh:['室內','內部空間','房間內','密閉空間','在裡面','玄關大廳','走廊通道'] },
    'night|夜晚|夜間|深夜|夜裡|黑夜|夜|晚上':{ en:['night','crickets','night ambience','nocturnal','night insects'], zh:['夜晚','蟋蟀蟲鳴','夜間氛圍','夜行性的','夜晚昆蟲'] },
    'space|太空|宇宙|外太空|星球|星':{ en:['space','sci-fi ambience','cosmic','vacuum','spacecraft'], zh:['太空','科幻環境音','宇宙的','真空狀態','太空船內部'] },
  }},
  creature:{ label:'Creature / Animal', zh:'生物 / 動物', color:'#c8f060', tokens:{
    'animal|beast|creature|動物|生物|猛獸|野獸|寵物':{ en:['animal','creature','beast','monster','wildlife'], zh:['動物','生物怪物','猛獸','怪物','野生動物'] },
    'bird|鳥|鳥鳴|鳥叫|雀|鷹|烏鴉|翅膀|振翅|羽毛|飛禽|海鷗':{ en:['bird','tweet','chirp','crow','eagle','flap wings','bird call','songbird','hawk'], zh:['鳥類','鳴叫聲','啁啾聲','烏鴉','老鷹','拍打翅膀','鳥鳴叫','鳴禽','老鷹'] },
    'wolf|dog|狼|狗|犬|狼嚎|吠叫|嚎叫|狗吠|犬吠|狼叫':{ en:['wolf','howl','dog bark','growl','snarl','whimper','dog'], zh:['狼','狼嚎叫','狗吠聲','低吼聲','呲牙咧嘴聲','嗚咽聲','小狗'] },
    'cat|貓|喵|貓叫|貓嚎|貓咪|小貓|幼貓':{ en:['cat','meow','hiss','purr','cat screech','cat yowl'], zh:['貓','喵喵叫','嘶嘶聲','呼嚕聲','貓尖叫','貓哀嚎'] },
    'horse|馬|馬蹄|嘶鳴|馬嘶|奔馬|馬跑|馬叫':{ en:['horse','neigh','whinny','gallop','hooves','horse snort','horse run'], zh:['馬匹','馬嘶鳴','輕聲嘶鳴','策馬奔騰','馬蹄聲','馬噴鼻息','奔跑的馬'] },
    'bear|monster|creature|熊|怪物|野獸|巨獸|咆哮|嘶吼|怒吼|生化|變異|外星|異形':{ en:['bear','monster','roar','growl','creature','beast','snarl','creature scream','mutant','alien'], zh:['熊','怪物','巨大咆哮','低沉嘶吼','未知生物','野獸','怒吼聲','怪物尖叫','突變體','外星異形'] },
    'insect|bug|蟲|蟋蟀|蟬|蟲鳴|蚊子|蜜蜂|蟲聲|昆蟲|蒼蠅':{ en:['insect','cricket','cicada','buzz','mosquito','bee','fly','bug'], zh:['昆蟲','蟋蟀','蟬鳴','嗡嗡聲','蚊子','蜜蜂','蒼蠅','蟲子'] },
    'frog|snake|青蛙|蛇|爬蟲|蜥蜴|鱷魚':{ en:['frog','croak','snake','hiss','reptile','lizard'], zh:['青蛙','青蛙呱呱叫','蛇','蛇吐信聲','爬蟲類','蜥蜴'] },
    'dragon|龍|巨龍|魔獸|飛龍|噴火龍':{ en:['dragon','roar','wing flap','fire breath','creature roar','dragon cry'], zh:['龍','巨龍咆哮','拍打巨大翅膀','噴火聲音','生物吼叫','龍的鳴叫'] },
  }},
  mechanical:{ label:'Mechanical', zh:'機械 / 工業', color:'#ffb347', tokens:{
    'engine|motor|引擎|馬達|發動機|啟動|轉動|引擎聲':{ en:['engine','motor','rev','start','idle','engine rumble','turbine','engine roar'], zh:['引擎','馬達','催油門','啟動引擎','怠速運轉','引擎低吼','渦輪引擎','引擎咆哮'] },
    'gear|齒輪|機械|咬合|棘輪|機械聲':{ en:['gear','cog','ratchet','mechanical click','machinery','gear shift'], zh:['齒輪','齒輪咬合','棘輪','機械點擊聲','機械機關','排檔換檔'] },
    'door|lock|門|鎖|門鉸|開鎖|上鎖|門把|門鈴|轉門|鐵門':{ en:['door','lock','unlock','latch','hinge','doorbell','knob','deadbolt','metal door'], zh:['門','上鎖聲','解鎖聲','門閂','門鉸鏈','門鈴聲','門把轉動','大門門栓','金屬鐵門'] },
    'switch|button|開關|按鈕|切換|撥動|按下|觸碰|按鍵':{ en:['switch','button','click','toggle','flip','power on','power off'], zh:['開關','按鈕','點擊聲','切換開關','撥動按鈕','開啟電源','關閉電源'] },
    'robot|機器人|機械臂|電子|伺服|自動化|機甲':{ en:['robot','servo','mechanical arm','hydraulic','pneumatic','sci-fi mechanical','android'], zh:['機器人','伺服馬達轉動','機械手臂','油壓系統','氣動設計','科幻機械聲','仿生人'] },
    'factory|industrial|工廠|工業|機器|生產線|車間':{ en:['factory','industrial','machinery','production','conveyor','steam','industrial hum'], zh:['工廠','工業性質','機器設備','生產作業','輸送帶','蒸氣排氣','工業電樞低鳴'] },
    'electric|elecetric|spark|zap|電流|電力|火花|觸電|靜電|電|短路|漏電':{ en:['electric','electricity','elecetric','spark','zap','shock','static','arc','surge'], zh:['電子的','電力','通電','電火花','快速電擊','觸電休克','靜電干擾','電弧放電','電流湧浪'] },
    'hum|whir|嗡嗡|轉動聲|電流聲|嗡嗡聲|電子聲':{ en:['hum','whir','buzz','drone','electrical hum','motor hum','electric'], zh:['嗡嗡聲','轉動聲','蟲鳴般嗡聲','持續低鳴','電流嗡嗡聲','馬達運轉聲','電力的聲響'] },
    'vehicle|car|車|汽車|引擎聲|煞車|輪胎|喇叭|開車|停車|騎車|機車':{ en:['car','vehicle','engine start','brake','tire screech','horn','drive by','parking'], zh:['汽車','車輛','發動引擎','踩煞車','輪胎刺耳摩擦','按喇叭','開車路過','停車熄火'] },
  }},
  magic:{ label:'Magic / Sci-Fi', zh:'魔法 / 科幻', color:'#5b9fff', tokens:{
    'magic|spell|魔法|咒語|施法|附魔|奧術|神秘|魔力|法術|魔':{ en:['magic','spell','cast','enchant','arcane','mystical','incantation','magic cast'], zh:['魔法','咒語','施放法術','附魔強化','奧術魔法','神秘超自然','吟唱咒語','魔法施展'] },
    'fire magic|火系|火焰魔法|火球|烈火|火焰術':{ en:['fire magic','fireball','flame burst','fire spell','combustion','fire whoosh'], zh:['火系魔法','火球','火焰爆發','火焰法術','燃燒魔法','火焰呼嘯'] },
    'ice magic|冰系|冰凍|冰魔法|冰封|凍結|冰|結冰':{ en:['ice magic','freeze','frost','ice spell','blizzard magic','ice crack'], zh:['冰系魔法','凍結','結霜','冰法術','暴風雪魔法','極冰碎裂'] },
    'lightning|thunder magic|閃電|雷電|電擊|閃電魔法|電魔法|電':{ en:['lightning','electric','elecetric','thunder magic','shock','zap','spark','lightning strike'], zh:['閃電','電力的','通電','雷電魔法','電擊傷害','電擊聲','電火花','雷電打擊'] },
    'portal|teleport|傳送門|傳送|瞬移|召喚|異次元|傳入|傳出':{ en:['portal','teleport','warp','summon','dimensional','portal open','portal close'], zh:['傳送門','瞬間移動','扭曲空間傳送','召喚儀式','異次元的','傳送門開啟','傳送門關閉'] },
    'shield|barrier|護盾|屏障|防護|防禦|結界|盾|罩':{ en:['shield','barrier','force field','deflect','magical shield','bubble shield'], zh:['護盾','屏障','力場防護','彈開攻擊','魔法護盾','泡泡防護罩'] },
    'laser|beam|雷射|光束|能量|射線|光砲|死光':{ en:['laser','beam','energy','ray','plasma','charge up','laser shot'], zh:['雷射射線','光束','能量','射線','電漿','蓄力充滿體','雷射射擊'] },
    'shimmer|sparkle|shine|flash|光芒|閃爍|魔法粒子|閃耀|光效|粒子|閃現|發光|閃|光|亮':{ en:['shimmer','sparkle','twinkle','shine','flash','glow','glare','fairy','magical glow','particle'], zh:['微波閃爍','火光閃爍','星星閃爍','發光閃耀','閃現/閃光','發出光圈','刺眼強光','精靈音效','魔法光芒','魔法粒子'] },
    'dark magic|暗黑|黑魔法|詛咒|腐蝕|暗影|黑暗|暗|死靈':{ en:['dark magic','curse','corruption','shadow','void','necromancy','dark energy'], zh:['黑魔法','詛咒','腐蝕魔法','暗影能量','虛空','死靈法術','黑暗能量'] },
    'sci-fi|futuristic|科幻|未來感|太空|電子|賽博|外星':{ en:['sci-fi','futuristic','space','electronic','digital','cyber','hologram'], zh:['科幻的','充滿未來感','太空的','電子聲響','數位感','賽博龐克','全息投影'] },
    'heal|buff|治癒|補血|補魔|藥水|增益|狀態恢復|補|藥|回血|體力':{ en:['heal','mana potion','health potion','buff','restore','resurrect','magic chime'], zh:['治癒回血','魔力藥水','生命藥水','增益狀態','恢復原狀','復活','魔法鐘聲'] },
  }},
  ui:{ label:'UI / Interface', zh:'介面音效', color:'#5b9fff', tokens:{
    'notification|alert|通知|提醒|提示|警告|訊息|新訊息|信|跳出':{ en:['notification','alert','ping','ding','chime','message','remind','pop up'], zh:['系統通知','警告提醒','Ping聲','叮咚聲','鐘聲音效','收到訊息','提醒提示','彈出視窗'] },
    'success|complete|win|成功|完成|勝利|解鎖|升級|獎勵|達成|任務|獲勝|贏|勝|答對':{ en:['success','complete','win','unlock','reward','level up','achievement','fanfare','triumph','quest complete'], zh:['成功','完成任務','贏得勝利','解鎖新要素','獲得獎勵','等級提升','解鎖成就','勝利號角','旗開得勝','任務完成'] },
    'error|fail|wrong|錯誤|失敗|拒絕|不對|無效|出錯|錯|敗|不|答錯|否|退回':{ en:['error','fail','wrong','deny','buzz','decline','invalid','negative','error tone'], zh:['錯誤','失敗的聲音','錯了的音效','拒絕操作','錯誤蜂鳴','婉拒','無效操作','負面反饋','錯誤提示音'] },
    'click|tap|點擊|輕觸|按下|點選|按鍵|點一下|按|點|滑鼠':{ en:['click','tap','button press','select','UI click','mouse click','touch'], zh:['點擊聲','輕觸畫面','按下實體按鍵','選擇介面','介面點擊','滑鼠點擊','觸碰螢幕'] },
    'transition|sweep|轉場|過渡|切換畫面|滑入|切換|滑出|翻頁':{ en:['transition','sweep','swipe','UI transition','whoosh UI','scene change'], zh:['過渡轉場','掃過畫面','滑動畫面','介面轉場','介面特殊呼嘯','場景切換'] },
    'game|遊戲|音效|得分|扣血|命中|拾取|撿起|遊戲音|金幣|背包|裝備|錢|道具':{ en:['game sound','score','damage','hit marker','pickup','collect','game UI','coin','health','inventory','equip'], zh:['遊戲音效','加分','受到傷害','命中提示','撿起道具','收集物品','遊戲介面','獲得金幣','補充體力','打開背包','裝備武器'] },
    'gain|get|collect|獲得|取得|得到|收集|獲取|得|收|拿|收穫|賺':{ en:['gain','get','collect','acquire','receive','obtain','fetch'], zh:['獲得收益','取得','收集','獲取','收到','獲得','拿回來'] },
    'beep|chime|type|叮|嗶|鐘聲|提示音|嗶嗶|叮叮|打字聲|滴|鈴聲':{ en:['beep','chime','ding','ping','tone','blip','bell','notification sound','typing','typewriter'], zh:['嗶嗶聲','風鈴鐘聲','叮的一聲','Ping聲響','單一聲調','遊戲電子閃爍音','鈴鐺聲','通知音效','鍵盤打字聲','復古打字機'] },
  }}
};"""

start_str = "const UCS = ["
end_str = "};\n\nlet mode = 'search';"

start_idx = text.find(start_str)
end_idx = text.find(end_str)

if start_idx != -1 and end_idx != -1:
    new_text = text[:start_idx] + new_ucs_dims + "\n\n" + text[end_idx + 4:]
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_text)
    print("Replacement success.")
else:
    print("Could not find boundaries", start_idx, end_idx)
