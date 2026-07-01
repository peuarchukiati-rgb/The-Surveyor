// Shared share helper — builds Google Maps URL with waypoints, opens modal with QR + copy + native share.
// Used by all 3 designs.
(function(){
  const STYLE = `
    .sh-back{position:fixed;inset:0;background:rgba(0,0,0,.6);z-index:9999;display:flex;align-items:center;justify-content:center;padding:20px;backdrop-filter:blur(4px);}
    .sh-modal{background:#fff;color:#111;border-radius:14px;max-width:480px;width:100%;max-height:90vh;overflow:auto;box-shadow:0 24px 60px rgba(0,0,0,.4);font-family:'Sarabun',system-ui,sans-serif;}
    .sh-head{padding:16px 20px;border-bottom:1px solid #e5e7eb;display:flex;justify-content:space-between;align-items:center;}
    .sh-head h3{margin:0;font-size:16px;}
    .sh-x{background:none;border:0;font-size:22px;cursor:pointer;color:#6b7280;line-height:1;}
    .sh-body{padding:20px;}
    .sh-warn{background:#fef3c7;color:#92400e;padding:10px 12px;border-radius:8px;font-size:12px;margin-bottom:14px;line-height:1.5;}
    .sh-warn b{font-weight:700;}
    .sh-qr{text-align:center;padding:14px;background:#f9fafb;border-radius:10px;margin-bottom:14px;}
    .sh-qr img{max-width:200px;display:block;margin:0 auto 8px;border-radius:8px;}
    .sh-qr p{margin:0;font-size:11px;color:#6b7280;}
    .sh-url{display:flex;gap:6px;margin-bottom:10px;}
    .sh-url input{flex:1;padding:9px 12px;border:1px solid #d1d5db;border-radius:8px;font-size:11px;color:#374151;background:#f9fafb;}
    .sh-url button{padding:9px 14px;background:#111827;color:#fff;border:0;border-radius:8px;cursor:pointer;font-size:12px;white-space:nowrap;}
    .sh-url button:hover{background:#374151;}
    .sh-btns{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:6px;}
    .sh-btns button{padding:10px;border:1px solid #d1d5db;background:#fff;border-radius:8px;cursor:pointer;font-size:12px;display:flex;align-items:center;justify-content:center;gap:6px;}
    .sh-btns button:hover{background:#f3f4f6;}
    .sh-btns .pri{background:#10b981;color:#fff;border-color:#10b981;}
    .sh-btns .pri:hover{background:#059669;}
    .sh-seg{margin-top:14px;padding-top:14px;border-top:1px solid #e5e7eb;}
    .sh-seg h4{margin:0 0 8px;font-size:12px;color:#374151;}
    .sh-seg-item{padding:8px 12px;background:#f3f4f6;border-radius:8px;margin-bottom:6px;font-size:11px;display:flex;justify-content:space-between;align-items:center;gap:8px;}
    .sh-seg-item button{padding:5px 10px;background:#1e90ff;color:#fff;border:0;border-radius:6px;cursor:pointer;font-size:11px;}
    .sh-toast{position:fixed;bottom:30px;left:50%;transform:translateX(-50%);background:#10b981;color:#fff;padding:10px 18px;border-radius:24px;font-size:13px;z-index:10001;box-shadow:0 8px 24px rgba(16,185,129,.5);}
  `;
  const st=document.createElement('style'); st.textContent=STYLE; document.head.appendChild(st);

  function gmapsURL(pts){
    // pts: [{lat,lng,code,...}]   travelmode=driving
    if(pts.length<1) return null;
    if(pts.length===1){
      const p=pts[0];
      return `https://www.google.com/maps/search/?api=1&query=${p.lat},${p.lng}`;
    }
    const origin = `${pts[0].lat},${pts[0].lng}`;
    const dest = `${pts[pts.length-1].lat},${pts[pts.length-1].lng}`;
    const mid = pts.slice(1,-1).map(p=>`${p.lat},${p.lng}`).join('|');
    let u = `https://www.google.com/maps/dir/?api=1&origin=${origin}&destination=${dest}&travelmode=driving`;
    if(mid) u += `&waypoints=${encodeURIComponent(mid)}`;
    return u;
  }

  function segmentURLs(pts, maxPerSeg=10){
    // Google Maps free supports ~9 waypoints between origin/destination = 11 total stops
    // Split into overlapping segments so end of one = start of next
    const segs=[]; let i=0;
    while(i < pts.length-1){
      const end = Math.min(i+maxPerSeg, pts.length);
      segs.push(pts.slice(i, end));
      i = end-1;
    }
    return segs.map((seg,idx)=>({
      idx:idx+1, n:seg.length, url:gmapsURL(seg),
      from:seg[0].code||`#${seg[0].lat.toFixed(3)}`,
      to:seg[seg.length-1].code||`#${seg[seg.length-1].lat.toFixed(3)}`,
    }));
  }

  function toast(msg){
    const t=document.createElement('div'); t.className='sh-toast'; t.textContent=msg;
    document.body.appendChild(t); setTimeout(()=>t.remove(),2200);
  }

  async function copyText(s){
    try{ await navigator.clipboard.writeText(s); toast('คัดลอกลิงก์แล้ว'); }
    catch{
      const ta=document.createElement('textarea'); ta.value=s; document.body.appendChild(ta);
      ta.select(); document.execCommand('copy'); ta.remove(); toast('คัดลอกลิงก์แล้ว');
    }
  }

  async function nativeShare(url, title){
    if(navigator.share){
      try{ await navigator.share({title:title||'BKK Shelter Route', text:'เส้นทางสำรวจศาลา', url}); }
      catch(e){/* user cancelled */}
    } else {
      copyText(url); toast('เบราว์เซอร์นี้ไม่รองรับ Share — คัดลอกลิงก์ให้แล้ว');
    }
  }

  function buildQR(url){
    return `https://api.qrserver.com/v1/create-qr-code/?size=240x240&margin=2&data=${encodeURIComponent(url)}`;
  }

  // Drag-and-drop reorder helper
  // Pass: container element, the waypoints array (mutated in place), and onReorder callback.
  // Marks every direct child with data-wp-idx as a drag handle/drop target.
  window.enableWPDrag = function(container, waypoints, onReorder){
    const items = container.querySelectorAll('[data-wp-idx]');
    items.forEach(el=>{
      el.draggable = true;
      el.style.cursor = 'grab';
      el.addEventListener('dragstart', e=>{
        el.style.opacity = '0.4';
        e.dataTransfer.effectAllowed = 'move';
        e.dataTransfer.setData('text/plain', el.dataset.wpIdx);
      });
      el.addEventListener('dragend', ()=>{
        el.style.opacity = '';
        items.forEach(x=>x.style.borderTop = x.style.borderBottom = '');
      });
      el.addEventListener('dragover', e=>{
        e.preventDefault();
        e.dataTransfer.dropEffect = 'move';
        const r = el.getBoundingClientRect();
        const before = (e.clientY - r.top) < r.height/2;
        items.forEach(x=>x.style.borderTop = x.style.borderBottom = '');
        el.style[before?'borderTop':'borderBottom'] = '3px solid #10b981';
      });
      el.addEventListener('dragleave', ()=>{
        el.style.borderTop = el.style.borderBottom = '';
      });
      el.addEventListener('drop', e=>{
        e.preventDefault();
        const fromIdx = parseInt(e.dataTransfer.getData('text/plain'), 10);
        const toIdxRaw = parseInt(el.dataset.wpIdx, 10);
        if(isNaN(fromIdx) || isNaN(toIdxRaw) || fromIdx === toIdxRaw) return;
        const r = el.getBoundingClientRect();
        const before = (e.clientY - r.top) < r.height/2;
        let toIdx = before ? toIdxRaw : toIdxRaw + 1;
        if(fromIdx < toIdx) toIdx--;
        const [moved] = waypoints.splice(fromIdx, 1);
        waypoints.splice(toIdx, 0, moved);
        if(onReorder) onReorder();
      });
    });
  };

  window.shareRoute = function(waypoints){
    if(!waypoints || waypoints.length===0){ toast('ยังไม่มี waypoint'); return; }
    const useSeg = waypoints.length > 10;
    const back=document.createElement('div'); back.className='sh-back';
    back.onclick=e=>{if(e.target===back)back.remove();};
    const modal=document.createElement('div'); modal.className='sh-modal';

    let html = `<div class="sh-head"><h3>📤 แชร์เส้นทางไปมือถือ</h3><button class="sh-x">×</button></div><div class="sh-body">`;

    if(useSeg){
      html += `<div class="sh-warn">⚠️ Google Maps รองรับสูงสุด <b>10 จุด/ลิงก์</b> — คุณมี <b>${waypoints.length}</b> จุด แบ่งเป็นหลายช่วงด้านล่าง</div>`;
      const segs=segmentURLs(waypoints,10);
      const firstURL=segs[0].url;
      const qr=buildQR(firstURL);
      html += `<div class="sh-qr"><img src="${qr}" alt="QR"><p>QR ของช่วงที่ 1 — สแกนเปิดในมือถือ</p></div>`;
      html += `<div class="sh-btns"><button class="pri" id="sh-native">📱 Share ช่วงที่ 1</button><button id="sh-open">🗺️ เปิดใน Maps</button></div>`;
      html += `<div class="sh-seg"><h4>ทั้งหมด ${segs.length} ช่วง:</h4>`;
      segs.forEach(s=>{
        html += `<div class="sh-seg-item"><span><b>ช่วง ${s.idx}</b> · ${s.n} จุด<br><span style="color:#6b7280;">${s.from} → ${s.to}</span></span><div style="display:flex;gap:4px;"><button onclick="window.open('${s.url}','_blank')">🗺️</button><button onclick="navigator.clipboard.writeText('${s.url}').then(()=>{const t=document.createElement('div');t.className='sh-toast';t.textContent='คัดลอกช่วง ${s.idx} แล้ว';document.body.appendChild(t);setTimeout(()=>t.remove(),2000);})">📋</button></div></div>`;
      });
      html += `</div>`;
      modal.innerHTML = html + `</div>`;
      back.appendChild(modal); document.body.appendChild(back);
      modal.querySelector('#sh-native').onclick=()=>nativeShare(firstURL,'BKK Shelter Route ช่วง 1');
      modal.querySelector('#sh-open').onclick=()=>window.open(firstURL,'_blank');
    } else {
      const url=gmapsURL(waypoints);
      const qr=buildQR(url);
      html += `<div class="sh-qr"><img src="${qr}" alt="QR"><p>📱 สแกน QR ด้วยกล้องมือถือ → เปิด Google Maps</p></div>`;
      html += `<div class="sh-url"><input id="sh-input" value="${url}" readonly><button id="sh-copy">📋 Copy</button></div>`;
      html += `<div class="sh-btns"><button class="pri" id="sh-native">📱 Share ไปมือถือ</button><button id="sh-open">🗺️ เปิดใน Maps</button></div>`;
      html += `<div style="margin-top:14px;padding:10px 12px;background:#f0f9ff;border-radius:8px;font-size:11px;color:#0369a1;line-height:1.6;">
        <b>วิธีใช้:</b><br>
        • <b>มือถือ:</b> สแกน QR ด้วยกล้อง<br>
        • <b>หรือ:</b> กด "Share" → ส่งใน Line / LINE Notify / Email<br>
        • <b>คอมพิวเตอร์:</b> กด "เปิดใน Maps" แล้วใช้ฟีเจอร์ Send to phone ใน Google Maps
      </div>`;
      modal.innerHTML = html + `</div>`;
      back.appendChild(modal); document.body.appendChild(back);
      modal.querySelector('#sh-copy').onclick=()=>copyText(url);
      modal.querySelector('#sh-native').onclick=()=>nativeShare(url);
      modal.querySelector('#sh-open').onclick=()=>window.open(url,'_blank');
    }
    modal.querySelector('.sh-x').onclick=()=>back.remove();
  };
})();
