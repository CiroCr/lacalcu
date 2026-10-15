// Verificacion de datos y motor. Uso: node tests/verificar.js   (sale con codigo 1 si algo falla)
const fs=require('fs'),vm=require('vm'),path=require('path');
const html=fs.readFileSync(path.join(__dirname,'..','calculadora-clausura-2026.html'),'utf8');
const js=html.match(/<script>\n(\/\/ \[codigo[\s\S]*?)<\/script>/)[1];
const els={};
const ctx=vm.createContext({console,Math,JSON,Object,Array,Set,Date,
  document:{getElementById:id=>els[id]||(els[id]={value:id==='selEq'?'4':'',classList:{toggle(){}},set innerHTML(v){this._h=v},get innerHTML(){return this._h}}),querySelectorAll:()=>[]},
  setTimeout:f=>{f();return 0},clearTimeout:()=>0});
vm.runInContext(js,ctx);
const lines=vm.runInContext('('+function(){
  const out=[];const log=(ok,m)=>out.push((ok?'OK     ':'FALLA  ')+m);
  const all=PAST.concat(FX);
  // --- fixture
  let badF=[];for(let f=1;f<=16;f++){const m=all.filter(x=>x[0]===f),c={};m.forEach(x=>{c[x[1]]=(c[x[1]]||0)+1;c[x[2]]=(c[x[2]]||0)+1});if(m.length!==15||Object.keys(c).length!==30||Object.values(c).some(v=>v!==1))badF.push(f)}
  log(!badF.length,'16 fechas x 15 partidos, cada equipo juega una vez por fecha');
  const pair={},inter={};ALL.forEach(t=>inter[t.c]=0);
  all.forEach(x=>{const k=[x[1],x[2]].sort().join('-');pair[k]=(pair[k]||0)+1;if(zi(x[1])!==zi(x[2])){inter[x[1]]++;inter[x[2]]++}});
  let miss=[];for(const Z of [TA,TB])for(let i=0;i<15;i++)for(let j=i+1;j<15;j++){const k=[Z[i].c,Z[j].c].sort().join('-');if(pair[k]!==1)miss.push(k)}
  log(!miss.length,'210 cruces de la misma zona exactamente una vez');
  log(Object.values(inter).every(v=>v===2),'cada equipo juega exactamente 2 interzonales (la fecha 6 es toda interzonal)');
  // --- datos base
  log(ALL.reduce((a,t)=>a+t.apGF,0)===ALL.reduce((a,t)=>a+t.apGC,0),'Apertura: goles a favor = goles en contra');
  const tot={};ALL.forEach(t=>tot[t.c]={pj:0,pts:0,gf:0,gc:0});
  PAST.forEach(x=>{const[h,a]=[x[1],x[2]],[gh,ga]=x[4];for(const[t,f,c]of[[h,gh,ga],[a,ga,gh]]){const d=tot[t];d.pj++;d.gf+=f;d.gc+=c;d.pts+=f>c?3:f===c?1:0}});
  const bad=ALL.filter(t=>{const d=tot[t.c];return d.pj!==t.clPJ||d.pts!==t.clPts||d.gf!==t.clGF||d.gc!==t.clGC});
  log(!bad.length,'resultados de las fechas 1-10 reproducen PJ/Pts/GF/GC de las 30 filas base '+bad.map(t=>t.c));
  log(ALL.every(t=>COL[t.c])&&new Set(ALL.map(t=>t.c)).size===30,'30 equipos con codigo unico y colores de escudo');
  // --- tablas tras fecha 11 (sin fecha 12) vs bolavip (11/10/2026)
  const exp={INS:[25,11,17,8],VEL:[21,11,17,11],DYJ:[21,11,16,11],BOC:[20,11,17,11],LAN:[17,11,13,9],NOB:[17,11,11,8],GEM:[17,11,14,12],IND:[17,11,11,12],EST:[13,11,13,11],UNI:[13,11,17,19],DRI:[11,11,9,11],SLO:[11,11,4,11],PLA:[10,11,11,17],CCO:[9,11,8,14],TAL:[8,11,11,18],ARG:[21,11,15,10],BEL:[19,11,12,7],ROS:[19,11,12,9],HUR:[19,11,11,8],IRI:[18,11,15,14],GLP:[18,11,16,16],SAR:[17,11,18,17],BAR:[15,11,8,9],RIV:[14,11,14,13],ATU:[13,11,9,9],TIG:[12,11,10,11],RAC:[11,11,13,17],BAN:[10,11,12,17],ALD:[8,11,12,17],ERC:[6,11,6,15]};
  const keep=FX.map((m,i)=>res[i]);FX.forEach((m,i)=>{if(m[0]>=12)res[i]=null});
  const badT=[];for(const c in exp){const p=proj(T[c]);if([p.Pts,p.PJ,p.GF,p.GC].join()!==exp[c].join())badT.push(c)}
  keep.forEach((v,i)=>res[i]=v);
  log(!badT.length,'estado tras la fecha 11 (las fechas 12 en adelante se ignoran): 30 filas coinciden con la tabla publicada '+badT);
  log(true,'resultados oficiales cargados en fechas 11-16: '+FX.filter(m=>m[4]).length+' | pendientes: '+FX.filter(m=>!m[4]).length+' | fecha por defecto: '+curF);
  // --- Elo
  log(ELO_EXTRA.length===1106,'ELO_EXTRA tiene '+ELO_EXTRA.length+' partidos (esperado 1106: 864 de fase regular y grupos + 242 de playoffs, Copa Argentina, eliminatorias CONMEBOL, Recopas, Mundial y trofeos)');
  const e=eloRun(),rk=ALL.slice().sort((a,b)=>e.R[b.c]-e.R[a.c]);
  log(rk.every(t=>isFinite(e.R[t.c])),'Elo: top5 '+rk.slice(0,5).map(t=>t.c+' '+Math.round(e.R[t.c])).join(', ')+' | ultimos '+rk.slice(-3).map(t=>t.c+' '+Math.round(e.R[t.c])).join(', '));
  log(true,'Elo: rivales fijos EXT='+Math.round(e.ref.EXT)+' BR='+Math.round(e.ref.BR)+' LOW='+Math.round(e.ref.LOW));
  // --- simulaciones: sumas esperadas
  const chk=m=>{MODEL=m;probs();const o=LAST,sm=a=>a.reduce((p,q)=>p+q,0)/NS,exp={ca:1,po:16,lib:4,sud:6,da:1,dp:1};
    return KEYS.every(k=>Math.abs(sm(o[k])-exp[k])<1e-9)};
  log(chk('goles'),'simulacion (modelo goles): sumas ca=1 po=16 lib=4 sud=6 da=1 dp=1');
  log(chk('elo'),'simulacion (modelo Elo): mismas sumas');
  MODEL='elo';probs();
  const o=LAST;log(o.lib[BI]===NS&&o.sud[BI]===0,'Belgrano (campeon Apertura) = 100% Libertadores y 0% Sudamericana por la anual');
  log(ALL.every((t,i)=>o.da[i]+o.dp[i]<=NS),'ningun equipo desciende dos veces (regla AFA)');
  // --- backtest fechas 7-12
  const M=PAST.map(m=>({f:m[0],h:m[1],a:m[2],gh:m[4][0],ga:m[4][1]})).concat(FX.filter(m=>m[4]).map(m=>({f:m[0],h:m[1],a:m[2],gh:m[4][0],ga:m[4][1]})));
  const oc=(a,b)=>a>b?0:a===b?1:2;
  const pG=(f,h,a)=>{let G=0,N=0;const st={};ALL.forEach(t=>st[t.c]={gf:t.apGF,gc:t.apGC,n:16});M.filter(m=>m.f<f).forEach(m=>{st[m.h].gf+=m.gh;st[m.h].gc+=m.ga;st[m.h].n++;st[m.a].gf+=m.ga;st[m.a].gc+=m.gh;st[m.a].n++});
    ALL.forEach(t=>{G+=st[t.c].gf;N+=st[t.c].n});const avg=G/N,K=12,A=c=>(st[c].gf+K*avg)/(st[c].n+K)/avg,D=c=>(st[c].gc+K*avg)/(st[c].n+K)/avg,lh=avg*1.1*A(h)*D(a),la=avg*.9*A(a)*D(h),pH=pwin(lh,la),pD=pdraw(lh,la);return[pH,pD,1-pH-pD]};
  const pE=(f,h,a)=>{const R=eloRun(f).R;let G=0,N=0;ALL.forEach(t=>{G+=t.apGF;N+=16});M.filter(m=>m.f<f).forEach(m=>{G+=m.gh+m.ga;N+=2});const[lh,la]=lamElo(R[h]+EL.HFA-R[a],2*G/N),pH=pwin(lh,la),pD=pdraw(lh,la);return[pH,pD,1-pH-pD]};
  const pB=f=>{const c=[1,1,1];M.filter(m=>m.f<f).forEach(m=>c[oc(m.gh,m.ga)]++);const s=c[0]+c[1]+c[2];return c.map(v=>v/s)};
  const R2={goles:[0,0],elo:[0,0],base:[0,0]};let n=0;
  for(const m of M.filter(m=>m.f>=7)){const y=oc(m.gh,m.ga);n++;for(const[k,p]of[['goles',pG(m.f,m.h,m.a)],['elo',pE(m.f,m.h,m.a)],['base',pB(m.f)]]){R2[k][0]+=-Math.log(Math.max(1e-6,p[y]));R2[k][1]+=p.indexOf(Math.max(...p))===y?1:0}}
  log(true,'backtest fechas 7-12 ('+n+' partidos): '+Object.keys(R2).map(k=>k+' log-loss '+(R2[k][0]/n).toFixed(4)+' aciertos '+R2[k][1]).join(' | '));
  return out}.toString()+')()',ctx);
console.log(lines.join('\n'));
if(lines.some(l=>l.startsWith('FALLA')))process.exit(1);
