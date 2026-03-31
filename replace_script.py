import re

file_path = "sound-keyword-expander_7.html"
with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

new_ucs_dims = """const UCS = [
  { id:'AMB', name:'Ambience', zh:'環境音 / 氛圍', color:'#4dd9ac',
    subs:['Forest 森林','Rain 雨聲','Wind 風聲','Ocean 海洋','River 河流','Cave 洞穴','Urban 城市','Room Tone 室內底噪'],
    keywords:{ en:['ambience','atmosphere','room tone','environment','nature','forest','rain','wind','ocean','river','cave','urban','city','night','outdoor','indoor','background','soundscape','birds','insects'], zh:['環境音','氛圍','底噪','大自然','森林','雨','風','海浪','河流','洞穴','城市','夜晚','室外','室內','背景音','鳥叫','蟲鳴'] }
  },
  { id:'CART', name:'Cartoon / Comedy', zh:'卡通 / 綜藝', color:'#ffb347',
    subs:['Boing 彈跳','Slip 滑倒','Wah-wah 失敗','Laugh 笑聲','Drum roll 鼓陣','Accent 強調'],
    keywords:{ en:['cartoon','comedy','boing','slip','wah-wah','laugh track','rimshot','drum roll','squeak','slide whistle','accent','funny','comic','glissando','bounce','bonk','plop','whoosh comedy','spring'], zh:['卡通','綜藝','搞笑','罐頭笑聲','彈簧','彈跳','滑倒','失敗','烏鴉飛過','滑音','綜藝摔','敲頭','趣味','強調'] }
  },
  { id:'DSGN', name:'Sound Design', zh:'設計音 / 預告片', color:'#5b9fff',
    subs:['Riser 爬升','Drop 墜落','Hit 重擊','Braam 銅管重音','Sweep 掃過','Tension 緊張感'],
    keywords:{ en:['sound design','riser','drop','downer','braam','boom','hit','impact','sweep','swoosh','whoosh hit','glitch','tension','cinematic','trailer','build-up','sub bass','reverse','stutter','whoosh sting'], zh:['設計音','預告片','電影感','廣告','爬升','墜落','重擊','掃過','反轉','重低音','緊張感','故障音','鋪陳','巨大衝擊'] }
  },
  { id:'EXP', name:'Explosion', zh:'爆炸 / 爆破', color:'#ff6b5b',
    subs:['Bomb 炸彈','Grenade 手榴彈','Gas 氣體爆炸','Nuclear 核爆','Debris 碎片','Shockwave 衝擊波'],
    keywords:{ en:['explosion','boom','blast','bang','detonation','burst','bomb','grenade','dynamite','shockwave','debris','rubble','fire','nuclear','gas explosion','underwater explosion','small explosion','large explosion','rumble','tail'], zh:['爆炸','爆破','引爆','轟鳴','爆裂','炸彈','手榴彈','炸藥','衝擊波','碎片','瓦礫','核爆','水下爆炸','大爆炸','殘響尾音'] }
  },
  { id:'FOL', name:'Foley', zh:'擬音 / 道具音', color:'#ffb347',
    subs:['Footsteps 腳步','Clothing 衣物','Props 道具','Keys 鑰匙','Paper 紙','Zipper 拉鍊'],
    keywords:{ en:['foley','footstep','walk','run','clothing','rustle','keys','paper','zipper','prop','movement','body','handling','pickup','put down','sit','stand','cloth','fabric','leather','creak'], zh:['擬音','腳步','走路','跑步','衣物','摩擦聲','鑰匙','紙','拉鍊','道具','動作','拿起','放下','坐下','站起','布料','皮革','吱呀聲'] }
  },
  { id:'FST', name:'Footsteps', zh:'腳步聲', color:'#c8f060',
    subs:['Concrete 混凝土','Wood 木板','Gravel 碎石','Grass 草地','Metal 金屬','Sand 沙地','Snow 雪地','Mud 泥地'],
    keywords:{ en:['footstep','walk','run','jog','sprint','stomp','creep','sneak','boots','heels','sneakers','barefoot','concrete','wood','gravel','grass','metal','sand','snow','mud','carpet','tile','puddle','stairs'], zh:['腳步','走路','跑步','慢跑','衝刺','重踩','悄悄移動','靴子','高跟鞋','球鞋','赤腳','混凝土','木板','碎石','草地','金屬','沙地','雪地','泥地','地毯','水坑','樓梯'] }
  },
  { id:'GORE', name:'Gore / Flesh', zh:'血肉 / 血腥', color:'#f06090',
    subs:['Blood 噴血','Flesh 撕肉','Bone 骨折','Stab 刺入','Slice 切割','Squelch 黏稠'],
    keywords:{ en:['gore','flesh','blood','splatter','squelch','guts','bone break','bone crack','stab','slice','rip','tear','eviscerate','dismember','slurp','meat','visceral','crunch'], zh:['血肉','血腥','噴血','骨折','骨碎','撕裂','穿刺','黏稠','擠壓','肉塊','切割','內臟','噁心'] }
  },
  { id:'HIT', name:'Hit / Impact', zh:'打擊 / 衝擊', color:'#f06090',
    subs:['Punch 拳擊','Kick 踢擊','Melee 近戰','Body 肉體','Object 物件','Muffled 悶聲'],
    keywords:{ en:['hit','impact','punch','kick','strike','smack','slam','bash','whack','thud','crack','knock','bang','slap','clunk','collision','crash','melee','flesh','body hit','hard hit','soft hit','muffled','dull','sharp','stab','blunt'], zh:['打擊','衝擊','拳擊','踢擊','揮打','摑打','猛擊','悶擊','清脆碰撞','敲擊','碰撞','近戰','肉擊','重擊','輕擊','悶聲','鈍擊'] }
  },
  { id:'MAG', name:'Magic / Sci-Fi', zh:'魔法 / 科幻', color:'#5b9fff',
    subs:['Fire Magic 火系','Ice Magic 冰系','Lightning 閃電','Heal 治癒','Spell Cast 施法','Shield 護盾','Laser 雷射'],
    keywords:{ en:['magic','spell','cast','enchant','arcane','mystical','shimmer','sparkle','twinkle','portal','teleport','laser','beam','energy','shield','barrier','fire magic','ice magic','lightning','thunder','dark magic','holy','sci-fi','futuristic','electric','plasma','charge','heal','mana potion','buff','debuff','resurrect'], zh:['魔法','咒語','施法','附魔','奧術','神秘','光芒閃爍','傳送門','傳送','雷射','光束','能量','護盾','火系魔法','冰系魔法','閃電','暗黑魔法','神聖','科幻','電流','治癒','補血','喝藥水','增益狀態','蓄力'] }
  },
  { id:'MUSC', name:'Musical / Synth', zh:'音樂 / 合成器', color:'#5b9fff',
    subs:['Drone 低頻','Pad 氛圍','Stinger 短刺','Bass 重低音','Loop 循環','Synth 合成'],
    keywords:{ en:['musical','synth','synthesizer','drone','pad','stinger','808','sub bass','loop','beat','drum kit','arpeggio','chord','melody','harmony','rhythm','texture','splice','EDM'], zh:['音樂','合成器','低頻','氛圍','短刺','重低音','循環','節奏','鼓組','和弦','旋律','墊圈','音效素材','跳動'] }
  },
  { id:'WAT', name:'Water', zh:'水聲 / 液體', color:'#4dd9ac',
    subs:['Splash 濺水','Drip 滴水','Pour 倒水','Underwater 水下','Ocean 海浪','Rain 雨','Bubble 氣泡','Stream 溪流'],
    keywords:{ en:['water','splash','drip','pour','drop','bubble','stream','river','ocean','rain','underwater','submerge','plunge','plop','gurgle','trickle','flow','wave','foam','spray','mist','puddle','pool','liquid','flood','drain','sink'], zh:['水','濺水','滴水','倒水','水滴','氣泡','溪流','海浪','雨','水下','沉入','撲通','咕嘟','細流','流動','泡沫','噴霧','水坑','液體','洪水'] }
  },
  { id:'WPN', name:'Weapons', zh:'武器 / 兵器', color:'#ff6b5b',
    subs:['Sword 劍','Arrow 箭矢','Gun 槍','Reload 換彈','Knife 刀','Bow 弓'],
    keywords:{ en:['gunshot','gunfire','shot','fire','shoot','pistol','rifle','shotgun','sniper','automatic','silenced','reload','cock','empty click','shell drop','casing','trigger','sword','blade','slash','swing','arrow','bow','knife','stab','draw','sheathe','gun','weapon','firearm','bullet','charge attack','blaster'], zh:['槍聲','槍擊','射擊','開火','手槍','步槍','散彈槍','狙擊','消音器','換彈','拉槍機','空擊','彈殼','扳機','劍','刀刃','揮砍','弓','箭矢','匕首','刺入','拔刀','入鞘','蓄力攻擊','雷射槍'] }
  },
  { id:'WHO', name:'Whoosh / Swish', zh:'呼嘯 / 掠過', color:'#c8f060',
    subs:['Fast 快速','Slow 緩慢','Magical 魔法','Air 空氣','Fabric 布料','Blade 刀刃'],
    keywords:{ en:['whoosh','swoosh','swish','whiz','whizz','zip','zoom','rush','dart','streak','blur','air','wind','blast','gust','displacement','draft','sword whoosh','blade','arrow','bullet','cloth','cape','transition','pass','fly','sweep','stinger','heavy whoosh','light whoosh'], zh:['呼嘯','掠過','揮動','嗖嗖','飛嘯','疾速','急速','空氣','風聲','氣流','阻力','劍鳴','刀刃','箭矢','布料','披風','轉場','掃過','重型呼嘯','輕型呼嘯'] }
  },
  { id:'UI', name:'UI / Notification', zh:'介面音效 / 通知', color:'#5b9fff',
    subs:['Notification 通知','Success 成功','Error 錯誤','Click 點擊','Transition 轉場','Game UI 遊戲'],
    keywords:{ en:['notification','alert','ping','ding','chime','beep','pop','success','complete','win','unlock','reward','level up','positive','error','fail','wrong','deny','buzz','decline','click','tap','toggle','swipe','hover','select','transition','UI','interface','game sound','achievement','coin','inventory','quest','typing'], zh:['通知','提醒','提示音','叮聲','鐘聲','嗶聲','彈出音','成功','完成','勝利','解鎖','獎勵','升級','錯誤','失敗','拒絕','蜂鳴','點擊','切換','轉場','介面音','遊戲音效','金幣','背包','任務','打字聲'] }
  },
  { id:'NAT', name:'Nature / Animals', zh:'自然 / 動物', color:'#c8f060',
    subs:['Thunder 雷聲','Wind 風','Fire 火','Animals 動物','Birds 鳥鳴','Insects 昆蟲'],
    keywords:{ en:['thunder','lightning strike','wind gust','storm','fire crackling','fire','flame','animal','creature','bird','wolf','bear','horse','insect','cricket','frog','earth','rock','gravel','leaves','branch','tree','nature'], zh:['雷聲','閃電','陣風','暴風雨','木柴燃燒','火焰','動物','鳥鳴','狼嚎','馬嘶','昆蟲','蟋蟀','青蛙','岩石','樹葉','樹枝'] }
  },
  { id:'MEC', name:'Mechanical', zh:'機械 / 工業', color:'#ffb347',
    subs:['Engine 引擎','Gear 齒輪','Motor 馬達','Industrial 工業','Door 門','Lock 鎖','Switch 開關'],
    keywords:{ en:['mechanical','machine','engine','motor','gear','industrial','factory','robot','servo','hydraulic','pneumatic','door','lock','switch','lever','button','crank','ratchet','click mechanical','clank','hum','whir','grind','metallic','metal'], zh:['機械','引擎','馬達','齒輪','工業','工廠','機器人','油壓','氣壓','門','鎖','開關','按鈕','棘輪','嗡嗡聲','轉動','研磨','金屬感'] }
  },
  { id:'BRK', name:'Break / Destroy', zh:'破壞 / 碎裂', color:'#f06090',
    subs:['Glass 玻璃','Wood 木頭','Metal 金屬','Concrete 混凝土','Ice 冰','Plastic 塑膠'],
    keywords:{ en:['break','crack','smash','shatter','crumble','collapse','destroy','glass','wood','metal','concrete','ice','plastic','ceramic','bone','wall','debris','crunch','snap','rip','tear','splinter','fracture'], zh:['破裂','碎裂','粉碎','崩塌','破壞','玻璃碎','木頭斷','金屬裂','混凝土','冰裂','塑膠碎','陶瓷','骨頭','碎片','折斷','撕裂'] }
  }
];

const DIMS = {
  genre:{ label:'Genre / Media', zh:'媒體與風格', color:'#5b9fff', tokens:{
    'comedy|variety|綜藝|搞笑|喜劇|趣味|罐頭音效|綜藝摔|烏鴉飛過':{ en:['comedy','variety show','cartoon','funny','silly','boing','laugh track','rimshot','funny slide'], zh:['綜藝','搞笑','喜劇','罐頭笑聲','彈簧'] },
    'cinematic|trailer|dsgn|廣告|預告|電影|宣傳|設計音|影視':{ en:['cinematic','trailer','sound design','epic','dramatic','boom','braam','movie','promo'], zh:['電影感','預告片','廣告宣傳','設計音效'] },
    'game|8-bit|retro|遊戲|電玩|手遊|8位元|像素':{ en:['game','video game','8-bit','retro','arcade','chiptune','level up','coin','UI'], zh:['遊戲','電玩','8-bit','復古','街機'] },
    'splice|edm|music|電子|節拍|音樂|合成器|素材|舞曲':{ en:['EDM','synth','musical','beat','splice material','loop','bass','techno'], zh:['電子音樂','節拍','合成器','Loop','素材'] }
  }},
  emotion:{ label:'Emotion / Vibe', zh:'情緒 / 氛圍', color:'#ffb347', tokens:{
    'tense|suspense|緊張|懸疑|壓迫|恐懼|恐怖':{ en:['tense','suspense','thriller','horror','creepy','eerie','dread','build-up','heartbeat'], zh:['緊張','懸疑','壓迫','恐懼','恐怖'] },
    'epic|triumph|史詩|壯闊|勝利|震撼|浩大':{ en:['epic','triumph','massive','huge','victorious','majestic','grand'], zh:['史詩','壯闊','勝利','震撼'] },
    'positive|happy|正向|開心|愉悅|成功|肯定':{ en:['positive','happy','cheerful','success','confirm','accept','reward'], zh:['正向','開心','成功','肯定'] },
    'negative|sad|fail|負面|悲傷|失敗|拒絕|錯誤':{ en:['negative','sad','fail','error','deny','wrong','wah-wah','decline'], zh:['負面','失敗','拒絕','錯誤'] }
  }},
  material:{ label:'Material', zh:'材質', color:'#ffb347', tokens:{
    'plastic|塑膠|塑料|塑膠管|管子|硬質|合成':{ en:['plastic','hollow plastic','hard plastic','synthetic','rigid','PVC','tube','pipe'], zh:['塑膠','中空塑膠','硬質','管子'] },
    'wood|木|木頭|木板|木門|木製|原木|硬木|地板|木質|木製品':{ en:['wood','wooden','timber','plank','log','hardwood','floorboard','lumber'], zh:['木頭','木板','原木','硬木','地板'] },
    'metal|金屬|鐵|鋼|鋁|銅|鐵管|黃銅|鋼鐵|鋁管':{ en:['metal','metallic','steel','iron','aluminum','copper','brass','tin','chrome'], zh:['金屬','鋼','鐵','鋁','銅','黃銅'] },
    'glass|玻璃|玻璃杯|玻璃瓶|陶瓷|瓷器|水晶':{ en:['glass','crystal','ceramic','porcelain','bottle','jar'], zh:['玻璃','水晶','陶瓷','瓷器'] },
    'stone|石|岩|混凝土|concrete|磚|碎石|磚塊|岩石|石頭|水泥':{ en:['stone','rock','concrete','gravel','rubble','brick','tile','cobblestone'], zh:['石頭','岩石','混凝土','碎石','磚塊'] },
    'cloth|布|織物|fabric|衣服|衣物|布料|絲綢|棉花|皮革|皮':{ en:['cloth','fabric','textile','silk','cotton','leather','clothing','rustle'], zh:['布料','織物','絲綢','棉花','皮革','衣物'] },
    'ice|冰|冰塊|結冰|霜|冰晶|冰裂|凍':{ en:['ice','frozen','frost','crystal ice','ice crack','freeze'], zh:['冰','結冰','霜','冰晶','冰裂'] },
    'paper|紙|紙張|書|厚紙板|報紙|書頁|摺紙':{ en:['paper','cardboard','newspaper','book','page','crumple','tear paper'], zh:['紙','厚紙板','報紙','書頁'] },
    'rubber|橡膠|輪胎|球|彈性|彈跳|橡皮':{ en:['rubber','bounce','ball','tire','elastic','squeak'], zh:['橡膠','彈跳','球','輪胎','彈性'] },
    'liquid|液體|汽水|飲料|油|泥|黏液':{ en:['liquid','fluid','slime','mud','oil','viscous','gooey'], zh:['液體','泥漿','油','黏稠'] },
    'bone|骨頭|骨骼|關節|骨折':{ en:['bone','crack bone','crunch','snap','skeletal','joint'], zh:['骨頭','骨骼','關節','骨折'] },
    'flesh|meat|肉|血肉|人體|內臟|血|噴血|肉塊':{ en:['flesh','meat','blood','splatter','squelch','guts','visceral'], zh:['血肉','噴血','肉塊','內臟','黏稠'] },
    'rope|chain|繩|鐵鍊|鍊子|鐵絲|纜繩':{ en:['rope','chain','wire','cable','rattle chain'], zh:['繩子','鐵鍊','鐵絲','纜繩'] },
  }},
  action:{ label:'Action', zh:'動作', color:'#f06090', tokens:{
    'fall|drop|落|掉|落下|跌|跌倒|墜落|摔|摔倒|摔落|倒下|塌|墜|跌落|倒地':{ en:['fall','drop','tumble','trip','stumble','collapse','topple','plop','body fall','thud fall','descend'], zh:['落下','掉落','跌倒','絆倒','倒塌','墜落','倒地'] },
    'hit|strike|打|擊|撞|拍|砸|敲|捶|重擊|猛擊|打到|碰到':{ en:['hit','impact','strike','smack','slam','bash','collision','pound','thump','knock','whack'], zh:['打擊','衝擊','撞擊','拍擊','敲打','捶打'] },
    'break|shatter|crack|碎|裂|打碎|破|爆裂|破碎|裂開|碎掉|骨折|斷裂':{ en:['break','crack','shatter','smash','crunch','snap','fracture','splinter','burst','bone crack'], zh:['破裂','碎裂','粉碎','折斷','骨折'] },
    'slide|scrape|滑|刮|拖|摩擦|刮擦|滑動|打滑|拖拉|拉動':{ en:['slide','scrape','scratch','drag','grind','friction','skid','scuff'], zh:['滑動','刮擦','拖拉','研磨','摩擦','打滑'] },
    'open|close|門|開|關|推|拉門|關門|開門|門軸|門縫':{ en:['open','close','door open','door close','creak','latch','slam door','shut','hinge'], zh:['開門','關門','門軸聲','門閂','砰關門'] },
    'roll|滾|翻滾|滾動|旋轉|滾落|轉動':{ en:['roll','tumble','spin','rotate','barrel roll','rolling'], zh:['滾動','翻滾','旋轉'] },
    'fly|whoosh|飛|掠過|穿過|飛行|飛翔|劃過|閃過':{ en:['whoosh','fly','pass','sweep','zip','dart','rush','soar','swish'], zh:['飛過','掠過','穿過','飛行'] },
    'slash|swing|揮|砍|劈|揮舞|揮動|揮砍|劈砍':{ en:['slash','swing','swipe','chop','cleave','cut','slice','sword swing'], zh:['揮砍','揮動','劈砍','切割'] },
    'shoot|release|射|發射|射箭|射擊|開槍|射出':{ en:['shoot','release','fire','launch','bowstring','gunshot','arrow release'], zh:['射擊','發射','弓弦彈射','開槍'] },
    'jump|leap|跳|跳躍|起跳|彈跳|彈起|落地|跳起':{ en:['jump','leap','hop','spring','bounce','land','landing','jump land'], zh:['跳躍','起跳','落地','彈跳'] },
    'throw|toss|丟|投|拋|扔|投擲|拋出|丟出':{ en:['throw','toss','hurl','fling','launch','projectile'], zh:['投擲','拋出','扔出'] },
    'punch|kick|拳|踢|揍|踹|拳擊|踢擊|揮拳|踹踢':{ en:['punch','kick','strike','jab','uppercut','roundhouse','stomp','martial arts'], zh:['拳擊','踢擊','揮拳','踹踢'] },
    'grab|grasp|抓|握|抱|拉扯|扭打|搏鬥|抓住':{ en:['grab','grasp','grip','clutch','tackle','grapple','wrestle'], zh:['抓握','緊握','扭打','搏鬥'] },
    'explosion|burst|爆|炸|爆炸|爆裂|炸開|爆發':{ en:['explosion','blast','boom','burst','bang','detonate','shockwave'], zh:['爆炸','爆裂','爆破','衝擊波'] },
    'crash|衝撞|碰撞|撞車|墜機|撞擊|相撞':{ en:['crash','collision','impact','wreck','smash','crunch','vehicle crash'], zh:['碰撞','撞擊','墜毀','撞車'] },
    'pour|倒|潑|灑|流|倒水|潑灑|倒出':{ en:['pour','splash','spill','drip','trickle','flow','gush'], zh:['倒水','潑灑','滴落','流動'] },
    'rip|tear|撕|撕裂|撕破|撕開|撕掉':{ en:['rip','tear','shred','fabric tear','paper tear','flesh tear'], zh:['撕裂','撕破','撕開','血肉撕裂'] },
    'stab|pierce|刺|穿刺|插入|刺穿|刺進':{ en:['stab','pierce','puncture','impale','thrust'], zh:['刺入','穿刺','插入'] },
    'knock|敲門|叩|敲擊|叩門|敲打門':{ en:['knock','rap','tap','bang door','door knock'], zh:['敲門','叩門','敲擊'] },
    'squeeze|壓|擠|壓扁|擠壓|壓縮':{ en:['squeeze','crush','compress','squish','press'], zh:['擠壓','壓扁','壓縮'] },
    'swim|splash|游|游泳|入水|跳水|潛水':{ en:['swim','splash','dive','plunge','water entry','underwater movement'], zh:['游泳','入水','跳水','潛水'] },
    'eat|drink|咬|嚼|喝|吞|咀嚼|飲食':{ en:['bite','chew','drink','swallow','eat','munch','slurp'], zh:['咬','咀嚼','喝','吞嚥'] },
    'charge|riser|build|蓄力|聚能|爬升|集氣|充能':{ en:['charge','charge up','riser','build-up','power up','crescendo','swell'], zh:['蓄力','充能','爬升','聚能','鋪陳'] },
  }},
  weapon:{ label:'Weapon Type', zh:'武器類型', color:'#ff6b5b', tokens:{
    'sword|劍|武士刀|katana|sabre|長劍|闊劍|西洋劍|刀鳴|劍鳴|拔劍|入鞘':{ en:['sword','blade','sabre','katana','longsword','broadsword','rapier','sword draw','sword sheathe','sword whoosh'], zh:['劍','刀刃','武士刀','長劍','西洋劍','劍鳴','拔刀','入鞘'] },
    'knife|dagger|刀|匕首|小刀|刺刀|細刃|短刀':{ en:['knife','dagger','stiletto','blade','switchblade','combat knife'], zh:['小刀','匕首','刺刀','細刃'] },
    'arrow|bow|弓|箭|弩|箭矢|弓弦|羽箭|箭袋|射箭':{ en:['arrow','bow','bowstring','crossbow','quiver','fletching','arrow fly','arrow hit'], zh:['箭矢','弓','弓弦','弩','箭袋','羽箭'] },
    'axe|斧|戰斧|斧頭|小斧|劈斧':{ en:['axe','hatchet','battle axe','cleave','axe swing'], zh:['斧頭','小斧','戰斧'] },
    'spear|lance|矛|長矛|刺擊|標槍|長槍':{ en:['spear','lance','pike','thrust','javelin','polearm'], zh:['矛','長矛','刺擊','標槍'] },
    'gun|pistol|rifle|槍|手槍|步槍|槍聲|槍擊|開火|子彈|彈殼|換彈|消音|散彈|狙擊|機槍':{ en:['gunshot','pistol','rifle','shotgun','sniper','automatic','silenced','reload','shell drop','bullet','firearm','cock','trigger','machine gun'], zh:['槍聲','手槍','步槍','散彈槍','狙擊','子彈','彈殼','換彈'] },
    'bomb|explosives|炸彈|手榴彈|炸藥|地雷|爆裂物':{ en:['bomb','grenade','dynamite','mine','explosive','detonate'], zh:['炸彈','手榴彈','炸藥','地雷','引爆'] },
    'blaster|sci-fi gun|雷射槍|光線槍|科幻武器|電漿槍':{ en:['blaster','sci-fi gun','plasma rifle','laser gun','stun gun','ray gun'], zh:['雷射槍','光線槍','科幻武器','電漿槍'] },
  }},
  environment:{ label:'Environment', zh:'環境 / 空間', color:'#4dd9ac', tokens:{
    'water|水|水中|入水|濺水|沉入|水下|撲通|液體|潮濕|水聲':{ en:['water','splash','submerge','underwater','plunge','plop','gurgle','drip','stream','water drop'], zh:['水','濺水','沉入','水下','液體','潮濕'] },
    'rain|雨|毛毛雨|大雨|雨滴|降雨|雨聲|下雨':{ en:['rain','drizzle','downpour','raindrop','rainfall','storm rain','light rain','heavy rain'], zh:['雨','毛毛雨','大雨','雨滴','下雨'] },
    'snow|雪|降雪|暴風雪|雪粉|積雪|雪地|下雪':{ en:['snow','snowfall','blizzard','powder snow','snow crunch','snow footstep'], zh:['雪','降雪','暴風雪','雪粉','積雪'] },
    'fire|flame|火|火焰|燃燒|噼啪|餘燼|篝火|火災|火堆|火焰聲':{ en:['fire','flame','burning','crackle','ember','campfire','wildfire','torch','fire roar'], zh:['火','火焰','燃燒','噼啪聲','餘燼','篝火'] },
    'wind|風|陣風|強風|狂風|微風|風吹|颳風|冷風|熱風':{ en:['wind','gust','breeze','howl','wind blast','blowing wind','strong wind','light wind'], zh:['風','陣風','強風','微風','颱風'] },
    'thunder|lightning|雷|閃電|雷聲|打雷|暴風雨|雷電|閃電聲':{ en:['thunder','lightning','thunderstorm','rumble thunder','crack thunder','thunder roll'], zh:['雷聲','閃電','打雷','暴風雨'] },
    'cave|洞穴|回響|迴聲|隧道|殘響|空曠|回音|空洞|空間感':{ en:['cave','reverb','echo','cavern','tunnel','reverberant','large space','stone room'], zh:['洞穴','回響','迴聲','隧道','殘響'] },
    'forest|森林|樹林|叢林|自然|樹葉|樹枝|樹木|林中':{ en:['forest','jungle','nature','leaves','branch','birds','woodland','rustling leaves'], zh:['森林','叢林','自然','樹葉','樹枝'] },
    'ocean|sea|海|海浪|海洋|波浪|海灘|浪聲|漲潮|退潮':{ en:['ocean','sea','waves','beach','surf','underwater','tide','ocean ambience'], zh:['海洋','海浪','波浪','海灘','潮汐'] },
    'river|stream|河|溪|溪流|河流|流水|水流|小溪':{ en:['river','stream','creek','flowing water','babbling brook','rapids'], zh:['河流','溪流','流水','小溪'] },
    'city|urban|城市|都市|街道|交通|車聲|人群|市區':{ en:['city','urban','traffic','street','crowd','city ambience','bus','subway'], zh:['城市','街道','交通','人群','地鐵'] },
    'outdoor|室外|戶外|開放|外面|野外|戶外空間':{ en:['outdoor','exterior','open air','field','meadow','open space'], zh:['室外','戶外','野外','開放空間'] },
    'indoor|室內|房間|密閉|房子|屋內|室內空間':{ en:['indoor','interior','room','enclosed','inside','hallway','corridor'], zh:['室內','房間','密閉空間','走廊'] },
    'night|夜晚|夜間|深夜|夜裡|黑夜':{ en:['night','crickets','night ambience','nocturnal','night insects'], zh:['夜晚','夜間','蟲鳴夜聲','夜晚環境'] },
    'space|太空|宇宙|外太空|星球':{ en:['space','sci-fi ambience','cosmic','vacuum','spacecraft'], zh:['太空','宇宙','外太空','星球'] },
  }},
  creature:{ label:'Creature / Animal', zh:'生物 / 動物', color:'#c8f060', tokens:{
    'bird|鳥|鳥鳴|鳥叫|雀|鷹|烏鴉|翅膀|振翅|羽毛':{ en:['bird','tweet','chirp','crow','eagle','flap wings','bird call','songbird','hawk'], zh:['鳥鳴','鳥叫','翅膀','振翅'] },
    'wolf|dog|狼|狗|犬|狼嚎|吠叫|嚎叫|狗吠|犬吠':{ en:['wolf','howl','dog bark','growl','snarl','whimper','dog'], zh:['狼嚎','狗叫','吠叫','嚎叫','咆哮'] },
    'cat|貓|喵|貓叫|貓嚎|貓咪':{ en:['cat','meow','hiss','purr','cat screech','cat yowl'], zh:['貓叫','喵','呼嚕','嘶嘶'] },
    'horse|馬|馬蹄|嘶鳴|馬嘶|奔馬|馬跑':{ en:['horse','neigh','whinny','gallop','hooves','horse snort','horse run'], zh:['馬嘶','嘶鳴','馬蹄','奔馳'] },
    'bear|monster|creature|熊|怪物|野獸|巨獸|咆哮|嘶吼|怒吼|生化|變異':{ en:['bear','monster','roar','growl','creature','beast','snarl','creature scream','mutant','alien'], zh:['熊吼','怪物','野獸','咆哮','嘶吼','異形'] },
    'insect|bug|蟲|蟋蟀|蟬|蟲鳴|蚊子|蜜蜂|蟲聲|昆蟲':{ en:['insect','cricket','cicada','buzz','mosquito','bee','fly','bug'], zh:['蟋蟀','蟬鳴','嗡嗡','蚊子','蜜蜂'] },
    'frog|snake|青蛙|蛇|爬蟲|蜥蜴|鱷魚':{ en:['frog','croak','snake','hiss','reptile','lizard'], zh:['青蛙','蛙鳴','蛇','爬蟲'] },
    'dragon|龍|巨龍|魔獸|飛龍|噴火龍':{ en:['dragon','roar','wing flap','fire breath','creature roar','dragon cry'], zh:['龍吼','巨龍','振翅','噴火'] },
  }},
  mechanical:{ label:'Mechanical', zh:'機械 / 工業', color:'#ffb347', tokens:{
    'engine|motor|引擎|馬達|發動機|啟動|轉動|引擎聲':{ en:['engine','motor','rev','start','idle','engine rumble','turbine','engine roar'], zh:['引擎','馬達','發動','怠速','轟鳴'] },
    'gear|齒輪|機械|咬合|棘輪|機械聲':{ en:['gear','ratchet','mechanical click','cog','machinery','gear shift'], zh:['齒輪','棘輪','機械','咬合'] },
    'door|lock|門|鎖|門鉸|開鎖|上鎖|門把|門鈴|轉門|鐵門':{ en:['door','lock','unlock','latch','hinge','doorbell','knob','deadbolt','metal door'], zh:['門','鎖','開鎖','門鉸','門鈴','門把'] },
    'switch|button|開關|按鈕|切換|撥動|按下|觸碰':{ en:['switch','button','click','toggle','flip','power on','power off'], zh:['開關','按鈕','切換','撥動'] },
    'robot|機器人|機械臂|電子|伺服|自動化':{ en:['robot','servo','mechanical arm','hydraulic','pneumatic','sci-fi mechanical','android'], zh:['機器人','機械臂','伺服','油壓'] },
    'factory|industrial|工廠|工業|機器|生產線|車間':{ en:['factory','industrial','machinery','production','conveyor','steam','industrial hum'], zh:['工廠','工業','機器','輸送帶','蒸氣'] },
    'hum|whir|嗡嗡|轉動聲|電流聲|嗡嗡聲|電子聲':{ en:['hum','whir','buzz','drone','electrical hum','motor hum','electric'], zh:['嗡嗡','轉動','電流','低鳴'] },
    'vehicle|car|車|汽車|引擎聲|煞車|輪胎|喇叭|開車|停車':{ en:['car','vehicle','engine start','brake','tire screech','horn','drive by','parking'], zh:['車','汽車','煞車','輪胎','喇叭'] },
  }},
  magic:{ label:'Magic / Sci-Fi', zh:'魔法 / 科幻', color:'#5b9fff', tokens:{
    'magic|spell|魔法|咒語|施法|附魔|奧術|神秘|魔力|法術':{ en:['magic','spell','cast','enchant','arcane','mystical','incantation','magic cast'], zh:['魔法','咒語','施法','附魔','奧術'] },
    'fire magic|火系|火焰魔法|火球|烈火|火焰術':{ en:['fire magic','fireball','flame burst','fire spell','combustion','fire whoosh'], zh:['火系魔法','火球','烈焰'] },
    'ice magic|冰系|冰凍|冰魔法|冰封|凍結':{ en:['ice magic','freeze','frost','ice spell','blizzard magic','ice crack'], zh:['冰系魔法','冰凍','冰封'] },
    'lightning|thunder magic|閃電|雷電|電擊|閃電魔法|電魔法':{ en:['lightning','electric','thunder magic','shock','zap','spark','lightning strike'], zh:['閃電','電擊','雷電','閃電術'] },
    'portal|teleport|傳送門|傳送|瞬移|召喚|異次元':{ en:['portal','teleport','warp','summon','dimensional','portal open','portal close'], zh:['傳送門','傳送','瞬移','召喚'] },
    'shield|barrier|護盾|屏障|防護|防禦|結界':{ en:['shield','barrier','force field','deflect','magical shield','bubble shield'], zh:['護盾','屏障','防護罩','結界'] },
    'laser|beam|雷射|光束|能量|射線|光砲':{ en:['laser','beam','energy','ray','plasma','charge up','laser shot'], zh:['雷射','光束','能量','電漿','光砲'] },
    'shimmer|sparkle|光芒|閃爍|魔法粒子|閃耀|光效|粒子':{ en:['shimmer','sparkle','twinkle','glitter','fairy','magical glow','particle'], zh:['光芒閃爍','閃耀','魔法粒子'] },
    'dark magic|暗黑|黑魔法|詛咒|腐蝕|暗影|黑暗':{ en:['dark magic','curse','corruption','shadow','void','necromancy','dark energy'], zh:['黑魔法','詛咒','腐蝕','暗影'] },
    'sci-fi|futuristic|科幻|未來感|太空|電子|賽博':{ en:['sci-fi','futuristic','space','electronic','digital','cyber','hologram'], zh:['科幻','未來感','太空','電子','全息'] },
    'heal|buff|治癒|補血|補魔|藥水|增益|狀態恢復':{ en:['heal','mana potion','health potion','buff','restore','resurrect','magic chime'], zh:['治癒','補血','喝藥水','狀態恢復'] },
  }},
  ui:{ label:'UI / Interface', zh:'介面音效', color:'#5b9fff', tokens:{
    'notification|alert|通知|提醒|提示|警告|訊息|新訊息':{ en:['notification','alert','ping','ding','chime','message','remind','pop up'], zh:['通知','提醒','提示','警告'] },
    'success|complete|成功|完成|勝利|解鎖|升級|獎勵|達成|任務':{ en:['success','complete','win','unlock','reward','level up','achievement','fanfare','triumph','quest complete'], zh:['成功','完成','勝利','解鎖','獎勵','升級','任務完成'] },
    'error|fail|wrong|錯誤|失敗|拒絕|不對|無效|出錯':{ en:['error','fail','wrong','deny','buzz','decline','invalid','negative','error tone'], zh:['錯誤','失敗','拒絕','無效'] },
    'click|tap|點擊|輕觸|按下|點選|按鍵|點一下':{ en:['click','tap','button press','select','UI click','mouse click','touch'], zh:['點擊','輕觸','按下','按鍵'] },
    'transition|sweep|轉場|過渡|切換畫面|滑入|切換':{ en:['transition','sweep','swipe','UI transition','whoosh UI','scene change'], zh:['轉場','過渡','滑入','切換'] },
    'game|遊戲|音效|得分|扣血|命中|拾取|撿起|遊戲音|金幣|背包|裝備':{ en:['game sound','score','damage','hit marker','pickup','collect','game UI','coin','health','inventory','equip'], zh:['遊戲音效','得分','扣血','命中','拾取','金幣','背包'] },
    'beep|chime|type|叮|嗶|鐘聲|提示音|嗶嗶|叮叮|打字聲':{ en:['beep','chime','ding','ping','tone','blip','bell','notification sound','typing','typewriter'], zh:['叮','嗶','鐘聲','提示音','打字聲'] },
  }},
  ambience:{ label:'Ambience', zh:'環境音 / 氛圍', color:'#4dd9ac', tokens:{
    'ambience|atmosphere|環境音|氛圍|背景音|底噪|空間感|氣氛':{ en:['ambience','atmosphere','room tone','background','soundscape','reverb tail','environment'], zh:['環境音','氛圍','底噪','背景音'] },
    'crowd|people|人群|人聲|人潮|市場|廣場|嘈雜':{ en:['crowd','people','chatter','murmur','crowd noise','market','busy'], zh:['人群','人聲','市場','廣場','嘈雜'] },
    'cafe|restaurant|咖啡廳|餐廳|店面|室內人聲|咖啡店':{ en:['cafe','restaurant','interior ambience','chatter','cutlery','coffee shop'], zh:['咖啡廳','餐廳','室內人聲','餐具聲'] },
    'office|工作室|辦公室|室內|電腦|冷氣|辦公環境':{ en:['office','workspace','AC hum','computer fan','indoor hum','keyboard'], zh:['辦公室','冷氣','電腦風扇','室內'] },
  }},
  foley:{ label:'Foley', zh:'擬音 / 道具音', color:'#ffb347', tokens:{
    'footstep|walk|腳步|走路|腳聲|踏步|行走|走動':{ en:['footstep','walk','run','jog','sprint','stomp','creak floor','foot'], zh:['腳步','走路','跑步','踏步'] },
    'concrete|木板|碎石|草地|雪地|泥地|地毯|沙地|地面|地板|混凝土':{ en:['concrete footstep','wood footstep','gravel footstep','grass footstep','snow footstep','mud footstep','carpet footstep','sand footstep','stone footstep'], zh:['混凝土腳步','木板腳步','碎石腳步','草地腳步','雪地腳步','泥地腳步'] },
    'clothing|rustle|衣物|衣服|布料聲|摩擦聲|衣物摩擦|衣料':{ en:['clothing rustle','fabric movement','jacket','leather creak','cloth movement'], zh:['衣物摩擦','布料聲','皮革聲'] },
    'keys|鑰匙|鑰匙聲|叮叮|金屬叮噹|鑰匙圈':{ en:['keys jingle','keychain','metal jingle','small metal clink'], zh:['鑰匙','叮叮','金屬叮噹'] },
    'paper|紙張|翻頁|書頁|紙聲|摺紙|書本':{ en:['paper rustle','page turn','book','crumple','tear paper','newspaper'], zh:['翻頁','紙聲','摺紙'] },
    'zipper|拉鍊|拉開|拉合|拉鍊聲':{ en:['zipper','zip open','zip close','jacket zipper'], zh:['拉鍊','拉開','拉合'] },
    'prop|道具|拿起|放下|物品|手持|拿取|擺放':{ en:['prop','pickup','put down','handling','object move','grab object'], zh:['道具','拿起','放下','手持'] },
  }},
  size:{ label:'Size / Weight', zh:'大小 / 重量', color:'#5b9fff', tokens:{
    'large|big|heavy|大|重|厚重|巨|龐大|沉重|低沉|巨大|很重|超重':{ en:['large','heavy','massive','deep','low','huge','powerful','thick','booming','giant'], zh:['大型','沉重','厚重','低沉','巨大'] },
    'small|tiny|light|小|輕|細|微|輕柔|細小|很小|迷你':{ en:['small','light','tiny','thin','subtle','delicate','soft','high pitched','miniature'], zh:['小型','輕巧','細微','纖細','輕柔'] },
    'hollow|中空|空洞|共鳴|管狀|空心|空的':{ en:['hollow','resonant','empty','tube','pipe','cylindrical','cavern resonance'], zh:['中空','空洞','共鳴','管狀'] },
    'distant|遠|遠方|遠處|隔著|傳來|遠距離|遙遠':{ en:['distant','far away','muffled distant','echo distant','off screen'], zh:['遠方','遠處','隔著牆','遙遠'] },
    'close|近|近距離|貼近|清晰|近前|很近':{ en:['close','near','intimate','dry','anechoic','direct','up close'], zh:['近距離','貼近','清晰'] },
  }},
  texture:{ label:'Texture', zh:'質感 / 音色', color:'#c8f060', tokens:{
    'sharp|crisp|清脆|銳利|脆|清亮|俐落|清晰|鋒利':{ en:['sharp','crisp','bright','attack','snap','click','bright attack','punchy'], zh:['銳利','清脆','明亮','俐落'] },
    'soft|muffled|悶|柔|悶聲|低沉|模糊|柔和|沉悶':{ en:['soft','muffled','dull','padded','cushioned','low pass','warm'], zh:['柔和','悶聲','低沉','有緩衝'] },
    'fast|quick|快速|迅速|瞬間|短促|快|即時':{ en:['fast','quick','rapid','instant','short','staccato','snap','brief'], zh:['快速','迅速','短促','瞬間'] },
    'slow|緩慢|慢|悠長|拖長|長音|緩慢的':{ en:['slow','heavy','long','sustained','gradual','drawn out','linger'], zh:['緩慢','悠長','長音','持續'] },
    'resonant|metallic|共鳴|金屬感|鈴聲|持音|餘音|回鳴':{ en:['resonant','metallic','ring','sustain','tone','clang','reverb tail','bell like'], zh:['共鳴','金屬感','鈴聲','持音','餘音'] },
    'dry|乾燥|無殘響|直接|清晰無混響|無回音':{ en:['dry','close','anechoic','direct','no reverb','dead room'], zh:['乾燥','無殘響','直接'] },
    'wet|reverb|殘響|回響|混響|空間感|有回音':{ en:['wet','reverb','echo','hall','large room','cathedral','spring reverb'], zh:['殘響','回響','混響','空間感'] },
    'distorted|破音|失真|電子|扭曲|雜訊|破碎':{ en:['distorted','glitch','corrupt','digital distortion','crunch','noise'], zh:['破音','失真','電子雜訊'] },
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
