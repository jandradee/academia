<template>
<section>
<div v-if="manager">
 <div class="hero"><div class="wrap">
  <div>
   <div class="eyebrow">Panel de gestión</div>
   <h1>Hola, {{firstName}}. Así va la formación de tu equipo.</h1>
   <p>{{branding.company_name}} · {{mgr.totals.users}} usuarios asignados en {{mgr.totals.courses}} cursos.</p>
  </div>
  <div class="chips">
   <div class="chip"><small>Cursos</small><strong>{{mgr.totals.courses}}</strong></div>
   <div class="chip"><small>Asignaciones</small><strong>{{mgr.totals.assigned}}</strong></div>
   <div class="chip"><small>Completados</small><strong>{{mgr.totals.completed}}</strong></div>
  </div>
 </div></div>
 <div class="wrap" style="padding-top:22px;padding-bottom:30px">
  <div style="display:flex;justify-content:space-between;align-items:center;gap:14px;flex-wrap:wrap">
   <h2 style="font-size:22px;margin:0">Avance por curso</h2>
   <button @click="downloadExcel">Exportar a Excel</button>
  </div>
  <div class="card" style="display:flex;gap:22px;align-items:center;margin-top:14px;flex-wrap:wrap">
   <svg width="132" height="132" viewBox="0 0 132 132" role="img" aria-label="Porcentaje global de finalización">
    <circle cx="66" cy="66" r="52" fill="none" style="stroke:var(--borde)" stroke-width="14"/>
    <circle cx="66" cy="66" r="52" fill="none" style="stroke:var(--verde)" stroke-width="14" stroke-linecap="round" :stroke-dasharray="donutDash" transform="rotate(-90 66 66)"/>
    <text x="66" y="63" text-anchor="middle" font-size="22" font-weight="700" fill="var(--tinta)">{{mgr.totals.pct_completed}}%</text>
    <text x="66" y="83" text-anchor="middle" font-size="11" fill="var(--gris)">completados</text>
   </svg>
   <div style="flex:1;min-width:230px">
    <p style="margin:4px 0"><span style="display:inline-block;width:11px;height:11px;border-radius:3px;background:var(--verde);margin-right:8px"></span>Completados: <strong>{{mgr.totals.completed}}</strong> ({{mgr.totals.pct_completed}}%)</p>
    <p style="margin:4px 0"><span style="display:inline-block;width:11px;height:11px;border-radius:3px;background:var(--azul);margin-right:8px"></span>En progreso: <strong>{{mgr.totals.in_progress}}</strong></p>
    <p style="margin:4px 0"><span style="display:inline-block;width:11px;height:11px;border-radius:3px;background:var(--beige);margin-right:8px"></span>No iniciados: <strong>{{mgr.totals.not_started}}</strong></p>
    <p class="meta" style="margin-top:8px">Sobre {{mgr.totals.assigned}} asignaciones activas en total.</p>
   </div>
  </div>
  <article v-for="c in mgr.courses" :key="c.course_id" class="card" style="margin-top:14px">
   <div style="display:flex;gap:16px;align-items:flex-start;flex-wrap:wrap">
    <img v-if="c.cover" :src="c.cover" alt="" style="width:132px;height:76px;object-fit:cover;border-radius:10px;border:1px solid var(--borde)"/>
    <div style="flex:1;min-width:260px">
     <h3 style="margin:0 0 4px;font-size:18px">{{c.title}}</h3>
     <p class="meta" style="margin:0 0 10px">{{c.assigned}} usuarios asignados</p>
     <div style="display:flex;height:16px;border-radius:8px;overflow:hidden;background:#E8EDF3" role="img" :aria-label="'No iniciados '+c.pct_not_started+'%, en progreso '+c.pct_in_progress+'%, completados '+c.pct_completed+'%'">
      <div :style="{width:c.pct_not_started+'%',background:'var(--beige)'}"></div>
      <div :style="{width:c.pct_in_progress+'%',background:'var(--azul)'}"></div>
      <div :style="{width:c.pct_completed+'%',background:'var(--verde)'}"></div>
     </div>
     <div style="display:flex;gap:18px;flex-wrap:wrap;margin-top:8px;font-size:13px">
      <span><span style="display:inline-block;width:10px;height:10px;border-radius:3px;background:var(--beige);margin-right:6px"></span>No iniciados: <strong>{{c.not_started}}</strong> · {{c.pct_not_started}}%</span>
      <span><span style="display:inline-block;width:10px;height:10px;border-radius:3px;background:var(--azul);margin-right:6px"></span>En progreso: <strong>{{c.in_progress}}</strong> · {{c.pct_in_progress}}%</span>
      <span><span style="display:inline-block;width:10px;height:10px;border-radius:3px;background:var(--verde);margin-right:6px"></span>Completados: <strong>{{c.completed}}</strong> · {{c.pct_completed}}%</span>
     </div>
    </div>
   </div>
  </article>
  <div style="display:flex;justify-content:space-between;align-items:center;gap:14px;flex-wrap:wrap;margin-top:26px">
   <h2 style="font-size:22px;margin:0">Datos del dashboard <span class="meta" style="font-size:14px">(RawData)</span></h2>
   <label style="margin:0">Curso<select v-model="mgrFilter" style="width:auto;margin-left:8px"><option value="">Todos los cursos</option><option v-for="c in mgr.courses" :key="c.course_id" :value="c.course_id">{{c.title}}</option></select></label>
  </div>
  <div class="card" style="margin-top:12px;overflow:auto;max-height:520px">
   <table><thead><tr><th>Empleado</th><th>Departamento</th><th>Curso</th><th>Estado</th><th>Avance</th><th>Vence</th><th>Aprobado</th></tr></thead>
   <tbody><tr v-for="(r,i) in mgrRows" :key="i"><td><strong>{{r.user}}</strong><br/><small class="meta">{{r.username}}</small></td><td>{{r.department||'—'}}</td><td>{{r.course}}</td><td><span class="pill" :class="r.status_bucket==='completed'?'pill-completado':(r.status_bucket==='in_progress'?'pill-obligatorio':'pill-opcional')">{{r.status_label}}</span></td><td>{{r.progress_percent}}%</td><td>{{r.due_at?fmtDate(r.due_at):'—'}}</td><td>{{r.passed_at?fmtDate(r.passed_at):'—'}}</td></tr></tbody></table>
   <p v-if="!mgrRows.length" class="meta">Sin registros para el filtro seleccionado.</p>
  </div>
  <p style="margin-top:14px"><button class="btn btn-outline" @click="downloadExcel">Exportar a Excel (resumen + RawData)</button></p>
 </div>
</div>
<div v-else>
 <div class="hero"><div class="wrap">
  <div>
   <div class="eyebrow">Hola de nuevo</div>
   <h1 v-if="firstName">Hola, {{firstName}}. <template v-if="dash.mandatory_pending>0">Tienes {{dash.mandatory_pending}} curso{{dash.mandatory_pending>1?'s':''}} obligatorio{{dash.mandatory_pending>1?'s':''}} pendiente{{dash.mandatory_pending>1?'s':''}}.</template><template v-else>Estás al día con tus cursos obligatorios.</template></h1>
   <h1 v-else>Tu academia en línea, a tu ritmo.</h1>
   <p v-if="nextDue">El curso «{{nextDue.title}}» vence el {{fmtDate(nextDue.due_at)}}. ¡Vas a buen tiempo si continúas hoy!</p>
   <p v-else>{{branding.tagline}}</p>
  </div>
  <div class="chips">
   <div class="chip"><small>Horas en {{year}}</small><strong>{{dash.training_hours_current_year ?? 0}}</strong></div>
   <div class="chip"><small>En progreso</small><strong>{{dash.in_progress ?? 0}}</strong></div>
   <div class="chip"><small>Completados</small><strong>{{dash.completed ?? 0}}</strong></div>
  </div>
 </div></div>
 <div class="wrap"><div class="cols">
  <div>
   <h2 style="font-size:22px">Mis cursos</h2>
   <div v-if="!rows.length" class="empty"><strong>Aún no tienes cursos asignados</strong>Explora el <router-link to="/catalogo">catálogo</router-link> para descubrir la formación disponible.</div>
   <article v-for="r in rows" :key="r.course" class="course-row">
    <div class="cover"><img v-if="r.cover" :src="r.cover" alt="" style="width:100%;height:100%;object-fit:cover"/><span v-else class="play">▶</span></div>
    <div style="flex:1;min-width:0">
     <span class="pill" :class="r.status==='aprobado' ? 'pill-completado' : (r.mandatory ? 'pill-obligatorio':'pill-opcional')">{{ r.status==='aprobado' ? 'Completado' : (r.mandatory ? 'Obligatorio':'Opcional') }}</span>
     <h3 style="margin:.35em 0 .15em;font-size:18px">{{r.title}}</h3>
     <div class="meta">{{r.meta}}</div>
     <div class="progress" style="margin-top:10px"><i :style="{width:r.progress_percent+'%'}"></i></div>
     <div class="meta" style="margin-top:6px">{{r.progress_percent}} % completado · {{r.statusText}}</div>
    </div>
    <router-link v-if="r.status==='aprobado' && r.certId" :to="`/certificado/${r.certId}`" class="btn btn-outline btn-sm" style="flex:none">Descargar certificado</router-link>
    <router-link v-else :to="`/curso/${r.course}`" class="btn btn-sm" style="flex:none">Continuar</router-link>
   </article>
   <div class="card" style="margin-top:20px"><h3>Horas de entrenamiento por mes · {{year}}</h3>
    <div style="display:flex;align-items:flex-end;gap:8px;height:130px;margin-top:14px">
     <div v-for="(h,i) in (dash.hours_by_month||[])" :key="i" style="flex:1;text-align:center">
      <div :title="h+' h'" style="background:var(--azul);border-radius:6px 6px 0 0;margin:0 auto;width:70%" :style="{height: Math.max(4, h*8)+'px', background: i===currentMonth ? 'var(--amarillo)' : 'var(--azul)'}"></div>
      <small style="color:var(--gris);font-size:11px">{{MESES[i]}}</small>
     </div>
    </div>
    <p class="meta">Total del año: <strong>{{dash.training_hours_current_year ?? 0}} h</strong> reconocidas en cursos aprobados.</p>
   </div>
  </div>
  <aside>
   <div class="side-card"><h3>Próximos vencimientos</h3>
    <div v-for="a in dues" :key="a.id" class="due-item">
     <span class="due-badge" :class="{soft: daysLeft(a.due_at)>10}">{{daysLeft(a.due_at)}} d</span>
     <div><strong style="font-size:14.5px">{{courseTitle(a.course)}}</strong><div class="meta">Vence el {{fmtDate(a.due_at)}}</div></div>
    </div>
    <p v-if="!dues.length" class="meta">Sin vencimientos próximos.</p>
   </div>
   <div class="side-card"><h3>Certificados</h3>
    <p class="meta">Tienes <strong>{{dash.certificates_count ?? 0}}</strong> certificado{{(dash.certificates_count??0)===1?'':'s'}} disponible{{(dash.certificates_count??0)===1?'':'s'}} para descargar.</p>
    <router-link to="/certificados">Ver certificados →</router-link>
   </div>
  </aside>
 </div></div>
</div>
</section>
</template>
<script setup>
import {ref, onMounted, computed} from 'vue'; import api from '../services/api'; import {branding, me, isManager, loadMe} from '../services/branding'
const dash=ref({}); const myProgress=ref([]); const courses=ref([]); const assignments=ref([])
const year=new Date().getFullYear(); const currentMonth=new Date().getMonth()
const MESES=['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic']
const firstName=computed(()=> (me.display_name||'').split(' ')[0])
const courseById=id=> courses.value.find(c=>c.id===id)
const courseTitle=id=> courseById(id)?.title || ('Curso #'+id)
const fmtDate=d=> d? new Date(d).toLocaleDateString('es',{day:'numeric',month:'short',year:'numeric'}) : ''
const daysLeft=d=> Math.max(0, Math.ceil((new Date(d) - new Date())/86400000))
const dues=computed(()=> assignments.value.filter(a=>a.due_at && a.status==='activa' && new Date(a.due_at) >= new Date(new Date().toDateString())).sort((x,y)=> new Date(x.due_at)-new Date(y.due_at)).slice(0,3))
const nextDue=computed(()=> dues.value.length ? {title: courseTitle(dues.value[0].course), due_at: dues.value[0].due_at} : null)
const certByCourse=computed(()=>{ const m={}; (dash.value.certificates||[]).forEach(c=> m[c.course]=c.id); return m })
const fmtDur=min=>{ if(!min) return ''; const h=Math.floor(min/60), m=min%60; return h? `${h} h ${String(m).padStart(2,'0')} min` : `${m} min` }
const rows=computed(()=>{
 const order={en_progreso:0, no_iniciado:1, aprobado:2}
 return myProgress.value.map(p=>{
   const c=courseById(p.course)||{}; const a=assignments.value.find(x=>x.course===p.course)
   const parts=[]
   if(a?.due_at) parts.push('Vence '+fmtDate(a.due_at)); else if(c.estimated_duration_minutes) parts.push(fmtDur(c.estimated_duration_minutes))
   if(c.modules) parts.push(c.modules.length+' módulo'+(c.modules.length===1?'':'s'))
   return {course:p.course, cover:c.cover||'', title:c.title||('Curso #'+p.course), status:p.status, progress_percent:p.progress_percent||0, mandatory: !!a?.is_mandatory || c.course_type==='obligatorio', meta: parts.join(' · '), statusText: p.status==='aprobado'?'Aprobado':(p.status==='en_progreso'?'En progreso':'Sin iniciar'), certId: certByCourse.value[p.course]}
 }).sort((x,y)=> (order[x.status]??3)-(order[y.status]??3))
})
const manager=ref(false); const mgr=ref({totals:{courses:0,users:0,assigned:0,not_started:0,in_progress:0,completed:0,pct_completed:0}, courses:[], rows:[]}); const mgrFilter=ref('')
const mgrRows=computed(()=> mgr.value.rows.filter(r=> !mgrFilter.value || r.course_id===Number(mgrFilter.value)))
const donutDash=computed(()=> `${(mgr.value.totals.pct_completed/100)*326.73} 326.73`)
async function downloadExcel(){ const r=await api.get('/reports/dashboard.xlsx',{responseType:'blob'}); const url=URL.createObjectURL(r.data); const a=document.createElement('a'); a.href=url; a.download='dashboard-academia.xlsx'; a.click(); URL.revokeObjectURL(url) }
onMounted(async()=>{
 if(!me.loaded) await loadMe()
 if(isManager()){ manager.value=true; try{ mgr.value=(await api.get('/reports/dashboard/')).data }catch{}; return }
 try{ dash.value=(await api.get('/dashboard/me/')).data }catch{}
 try{ myProgress.value=(await api.get('/course-progress/')).data.results||[] }catch{}
 try{ courses.value=(await api.get('/courses/')).data.results||[] }catch{}
 if(me.id){ try{ assignments.value=(await api.get('/assignments/',{params:{user:me.id}})).data.results||[] }catch{} }
})
</script>
