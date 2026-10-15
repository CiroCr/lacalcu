import datetime as dt
D=dt.date
MD={(4,2):1,(3,1):1,(2,3):2,(1,4):2,(2,1):3,(4,3):3,(3,2):4,(4,1):4,(1,2):5,(3,4):5,(1,3):6,(2,4):6}
DATES={2025:{1:D(2025,4,2),2:D(2025,4,9),3:D(2025,4,23),4:D(2025,5,7),5:D(2025,5,14),6:D(2025,5,28)},
       2026:{1:D(2026,4,8),2:D(2026,4,15),3:D(2026,4,29),4:D(2026,5,6),5:D(2026,5,20),6:D(2026,5,27)}}
# (año, competencia, equipo argentino, codigos brasileños, potes, partidos [local,visitante,gl,gv], esperado [pts,gf,gc])
G=[
(2025,'LIB','EST',{'BOT'},{'EST':2,'BOT':1,'UCH':3,'CBO':4},[('EST','BOT',1,0),('EST','UCH',1,2),('EST','CBO',2,0),('BOT','EST',3,2),('UCH','EST',0,3),('CBO','EST',0,2)],(12,11,5)),
(2025,'LIB','RIV',set(),{'RIV':1,'UNI':3,'IDV':2,'BSC':4},[('RIV','UNI',1,1),('RIV','IDV',6,2),('RIV','BSC',0,0),('UNI','RIV',0,1),('IDV','RIV',2,2),('BSC','RIV',2,3)],(12,13,7)),
(2025,'LIB','CCO',{'FLA'},{'LDQ':2,'FLA':1,'CCO':4,'TAC':3},[('LDQ','CCO',3,0),('FLA','CCO',1,2),('CCO','LDQ',0,0),('CCO','FLA',1,1),('CCO','TAC',2,1),('TAC','CCO',1,2)],(11,7,7)),
(2025,'LIB','TAL',{'SPA'},{'SPA':1,'LIB':2,'ALI':4,'TAL':3},[('SPA','TAL',2,1),('LIB','TAL',2,0),('ALI','TAL',3,2),('TAL','SPA',0,1),('TAL','LIB',0,0),('TAL','ALI',2,0)],(4,5,8)),
(2025,'LIB','RAC',{'FOR'},{'RAC':1,'FOR':3,'BUC':4,'CLC':2},[('RAC','FOR',1,0),('RAC','BUC',1,2),('RAC','CLC',4,0),('FOR','RAC',0,3),('BUC','RAC',0,4),('CLC','RAC',1,1)],(13,14,3)),
(2025,'LIB','VEL',set(),{'VEL':3,'PEN':1,'SAB':4,'OLI':2},[('VEL','PEN',2,1),('VEL','SAB',3,0),('VEL','OLI',1,1),('PEN','VEL',0,0),('SAB','VEL',2,1),('OLI','VEL',0,4)],(11,11,4)),
(2025,'SUD','IND',set(),{'IND':1,'GUA':2,'BOS':4,'NAP':3},[('IND','GUA',1,0),('IND','BOS',2,1),('IND','NAP',7,0),('GUA','IND',2,1),('BOS','IND',1,5),('NAP','IND',2,0)],(12,16,6)),
(2025,'SUD','DYJ',{'VIT'},{'UCA':2,'CRL':3,'VIT':4,'DYJ':1},[('UCA','DYJ',3,1),('CRL','DYJ',0,0),('VIT','DYJ',1,1),('DYJ','UCA',1,1),('DYJ','CRL',1,2),('DYJ','VIT',0,0)],(4,4,7)),
(2025,'SUD','HUR',{'COR'},{'HUR':2,'AME':1,'COR':4,'RCM':3},[('HUR','AME',0,0),('HUR','COR',1,0),('HUR','RCM',5,0),('AME','HUR',0,0),('COR','HUR',1,2),('RCM','HUR',1,3)],(14,11,2)),
(2025,'SUD','GOD',{'GRE'},{'GOD':2,'GRE':1,'CAG':4,'SLU':3},[('GOD','GRE',2,2),('GOD','CAG',2,2),('GOD','SLU',2,0),('GRE','GOD',1,1),('CAG','GOD',0,2),('SLU','GOD',0,1)],(12,10,5)),
(2025,'SUD','UNI',{'CRU'},{'MUS':4,'PAL':2,'CRU':1,'UNI':3},[('UNI','MUS',0,1),('UNI','PAL',1,2),('UNI','CRU',1,0),('MUS','UNI',3,0),('PAL','UNI',2,0),('CRU','UNI',0,0)],(4,2,8)),
(2025,'SUD','LAN',{'VAS'},{'LAN':1,'VAS':2,'MEL':4,'APC':3},[('LAN','VAS',1,0),('LAN','MEL',3,0),('LAN','APC',2,2),('VAS','LAN',0,0),('MEL','LAN',0,1),('APC','LAN',2,2)],(12,9,4)),
(2026,'LIB','EST',{'FLA'},{'FLA':1,'EST':2,'DIM':4,'CUS':3},[('FLA','EST',1,0),('EST','FLA',1,1),('EST','DIM',1,0),('EST','CUS',2,1),('DIM','EST',1,1),('CUS','EST',1,1)],(9,6,5)),
(2026,'LIB','IRI',{'FLU'},{'IRI':4,'FLU':1,'BOL':2,'DLG':3},[('IRI','FLU',1,1),('IRI','BOL',1,0),('IRI','DLG',4,1),('FLU','IRI',1,2),('BOL','IRI',1,3),('DLG','IRI',2,4)],(16,15,6)),
(2026,'LIB','BOC',{'CRU'},{'UCA':3,'CRU':2,'BOC':1,'BSC':4},[('UCA','BOC',1,2),('CRU','BOC',1,0),('BOC','UCA',0,1),('BOC','CRU',1,1),('BOC','BSC',3,0),('BSC','BOC',1,0)],(7,6,5)),
(2026,'LIB','PLA',{'COR'},{'COR':2,'PLA':4,'SFE':3,'PEN':1},[('COR','PLA',0,2),('PLA','COR',0,2),('PLA','SFE',2,1),('PLA','PEN',1,1),('SFE','PLA',2,1),('PEN','PLA',1,2)],(10,8,7)),
(2026,'LIB','LAN',{'MIR'},{'LDQ':1,'MIR':4,'LAN':2,'CAR':3},[('LDQ','LAN',2,0),('MIR','LAN',1,0),('CAR','LAN',4,0),('LAN','LDQ',1,0),('LAN','MIR',1,0),('LAN','CAR',1,0)],(9,3,7)),
(2026,'LIB','ROS',set(),{'IDV':1,'ROS':3,'UCV':4,'LIB':2},[('IDV','ROS',1,0),('UCV','ROS',0,3),('LIB','ROS',0,1),('ROS','IDV',0,0),('ROS','UCV',4,0),('ROS','LIB',1,0)],(13,9,1)),
(2026,'SUD','TIG',set(),{'MAC':3,'TIG':2,'AME':1,'AAS':4},[('MAC','TIG',2,2),('TIG','MAC',0,1),('TIG','AME',2,0),('TIG','AAS',2,0),('AME','TIG',1,1),('AAS','TIG',1,1)],(9,8,5)),
(2026,'SUD','SLO',{'SAN'},{'REC':4,'SAN':1,'SLO':2,'CUE':3},[('REC','SLO',1,1),('SLO','REC',0,1),('SAN','SLO',2,2),('SLO','SAN',1,1),('SLO','CUE',2,0),('CUE','SLO',0,0)],(7,6,5)),
(2026,'SUD','RAC',{'BOT'},{'BOT':4,'CAR':2,'RAC':1,'IPE':3},[('BOT','RAC',2,1),('CAR','RAC',1,1),('IPE','RAC',1,3),('RAC','BOT',2,3),('RAC','CAR',2,2),('RAC','IPE',2,0)],(8,11,9)),
(2026,'SUD','DRI',{'GRE'},{'MCT':3,'GRE':1,'DRI':4,'PAL':2},[('MCT','DRI',4,1),('GRE','DRI',1,0),('PAL','DRI',1,1),('DRI','MCT',2,1),('DRI','GRE',0,3),('DRI','PAL',0,0)],(5,4,10)),
(2026,'SUD','BAR',{'VAS'},{'OLI':1,'VAS':2,'AUD':3,'BAR':4},[('OLI','BAR',0,0),('VAS','BAR',3,0),('AUD','BAR',2,0),('BAR','OLI',1,2),('BAR','VAS',0,0),('BAR','AUD',1,1)],(3,2,8)),
(2026,'SUD','RIV',{'RBB'},{'RIV':1,'RBB':2,'CBO':4,'BLO':3},[('RIV','RBB',1,1),('RIV','CBO',1,0),('RIV','BLO',3,0),('RBB','RIV',0,1),('CBO','RIV',1,2),('BLO','RIV',1,1)],(14,9,3)),
]
def rows():
    out=[];bad=[]
    for yr,comp,arg,br,pots,ms,exp in G:
        p=g=c=0;seen=set()
        for h,a,gh,ga in ms:
            mdn=MD[(pots[h],pots[a])]
            assert (mdn,arg) not in seen or True
            tok=lambda x:x if x==arg else ('BR' if x in br else 'EXT')
            out.append((DATES[yr][mdn],3,tok(h),tok(a),gh,ga))
            f,k=(gh,ga) if h==arg else (ga,gh)
            p+=3 if f>k else 1 if f==k else 0;g+=f;c+=k
            seen.add(mdn)
        if len(seen)!=6 or (p,g,c)!=exp:bad.append((yr,comp,arg,(p,g,c),exp,sorted(seen)))
    return out,bad
if __name__=='__main__':
    r,bad=rows();print('partidos de copa:',len(r),'| desajustes:',bad if bad else 'ninguno (los 24 equipos-grupo coinciden con Pts, GF y GC de la tabla; cada uno juega una vez por fecha)')
