<template>
<section class="wrap" style="max-width:1000px">
 <div class="no-print" style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px">
  <router-link to="/certificados">← Volver a mis certificados</router-link>
  <button @click="print">🖨️ Imprimir / Guardar en PDF</button>
 </div>
 <div class="cert-frame" v-if="cert">
  <div class="cert-sheet">
   <div style="display:flex;align-items:center;justify-content:center;gap:10px">
    <span style="width:46px;height:46px;border-radius:11px;background:var(--azul);display:inline-flex;align-items:center;justify-content:center"><svg width="26" height="26" viewBox="0 0 24 24" fill="none"><path d="M12 5c-1.8-1.5-4.2-2-8-2v14c3.8 0 6.2.5 8 2 1.8-1.5 4.2-2 8-2V3c-3.8 0-6.2.5-8 2Z" style="fill:var(--amarillo)"/><path d="M12 5v14" style="stroke:var(--azul)" stroke-width="1.6"/></svg></span>
    <span style="text-align:left"><span style="display:block;font-weight:800;font-size:21px;color:var(--azul);line-height:1">{{branding.platform_name}}</span><span style="display:block;font-size:12.5px;color:var(--gris)" v-if="branding.company_name">{{branding.company_name}}</span></span>
   </div>
   <p style="letter-spacing:3px;font-weight:700;color:var(--tinta);margin-top:38px">CERTIFICADO DE FINALIZACIÓN</p>
   <p class="meta">Se certifica que</p>
   <div class="cname">{{me.display_name || '—'}}</div>
   <p class="meta">completó y aprobó el curso</p>
   <p style="font-size:22px;font-weight:800;margin:.2em 0">{{courseTitle}}</p>
   <p style="max-width:56ch;margin:14px auto 0">Con una duración reconocida de {{durText}}, con fecha de aprobación del {{dateText}}.</p>
   <div style="display:flex;justify-content:space-between;align-items:flex-end;margin-top:64px;text-align:left;gap:20px;flex-wrap:wrap">
    <div style="font-size:12px;color:var(--gris)">Identificador: {{BRAND.certificatePrefix}}-{{year}}-{{String(cert.id).padStart(6,'0')}}<br/>Verifica la validez en la plataforma de capacitación.<br/><span style="font-size:10.5px">Ref. {{cert.certificate_uuid}}</span></div>
    <div style="text-align:center;font-size:13px"><div style="border-top:1.5px solid var(--tinta);padding-top:6px;min-width:220px"><strong>Responsable de capacitación</strong><br/><span class="meta">(Nombre del responsable)</span></div></div>
    <div style="text-align:center"><svg width="86" height="86" viewBox="0 0 100 100" style="border:1.5px dashed var(--borde-fuerte);border-radius:8px;background:#F8FAFC"><rect v-for="(cell,i) in qrCells" :key="i" :x="8+(cell.x*4.2)" :y="8+(cell.y*4.2)" width="4.2" height="4.2" style="fill:var(--tinta)"/></svg><div style="font-size:10.5px;color:var(--gris)">Código QR</div></div>
   </div>
  </div>
 </div>
 <p v-else>Cargando certificado…</p>
</section>
</template>
<script setup>
import {ref, onMounted, computed} from 'vue'; import api from '../services/api'; import {branding, me} from '../services/branding'; import {BRAND} from '../config/brand'
const props=defineProps({id:String})
const cert=ref(null); const courses=ref([])
const courseTitle=computed(()=> courses.value.find(c=>cert.value && c.id===cert.value.course)?.title || '')
const year=computed(()=> (cert.value?.completion_date||'2026').slice(0,4))
const durText=computed(()=>{ const min=cert.value?.recognized_duration_minutes||0; const h=Math.floor(min/60), m=min%60; const parts=[]; if(h) parts.push(h+(h===1?' hora':' horas')); if(m) parts.push(m+' minutos'); return parts.join(' y ') || '0 minutos' })
const dateText=computed(()=> cert.value?.completion_date ? new Date(cert.value.completion_date+'T12:00:00').toLocaleDateString('es',{day:'numeric',month:'long',year:'numeric'}) : '')
const qrCells=computed(()=>{ const s=(cert.value?.certificate_uuid||'cert'); const cells=[]; let seed=0; for(const ch of s) seed=(seed*31 + ch.charCodeAt(0))>>>0; let x=seed; const rnd=()=>{ x=(x*1103515245+12345)>>>0; return x/4294967296 }; for(let yy=0;yy<20;yy++) for(let xx=0;xx<20;xx++){ if(rnd()>0.52) cells.push({x:xx,y:yy}) } return cells })
function print(){ window.print() }
onMounted(async()=>{ try{ const all=(await api.get('/certificates/')).data.results||[]; cert.value=all.find(c=>String(c.id)===String(props.id)) || null }catch{}; try{ courses.value=(await api.get('/courses/')).data.results||[] }catch{} })
</script>
