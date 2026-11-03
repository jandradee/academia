<template>
<section>
 <div class="hero" style="background:var(--azul)"><div class="wrap" style="padding-top:18px;padding-bottom:18px"><strong style="font-size:18px">{{branding.platform_name}} · Administración</strong></div></div>
 <div class="admin-shell">
  <aside class="admin-side">
   <button :class="{on:sec==='tema'}" @click="sec='tema'">Personalización</button>
   <button :class="{on:sec==='reportes'}" @click="sec='reportes'">Reportes</button>
   <button :class="{on:sec==='usuarios'}" @click="sec='usuarios'">Usuarios y roles</button>
   <button :class="{on:sec==='resumen'}" @click="sec='resumen'">Resumen</button>
  </aside>
  <div class="admin-main">
   <div v-if="sec==='tema'">
    <h1 style="font-size:27px">Personalización de la plataforma</h1>
    <p class="meta">Nombre, logo y colores que ven todos los usuarios. Los cambios se aplican al instante.</p>
    <div class="card" style="max-width:720px;margin-top:14px">
     <label>Nombre de la compañía<input v-model="form.company_name"/></label>
     <label>Nombre de la plataforma<input v-model="form.platform_name"/></label>
     <label>Lema / tagline<input v-model="form.tagline"/></label>
     <div style="display:grid;grid-template-columns:1fr 1fr;gap:0 14px">
      <label>Color principal<input type="color" v-model="form.primary_color" style="height:46px;padding:4px"/></label>
      <label>Color de acento<input type="color" v-model="form.accent_color" style="height:46px;padding:4px"/></label>
      <label>Color neutro<input type="color" v-model="form.beige_color" style="height:46px;padding:4px"/></label>
      <label>Color de alerta<input type="color" v-model="form.danger_color" style="height:46px;padding:4px"/></label>
     </div>
     <label>URL del logo (externa)<input v-model="form.logo_url" placeholder="https://…"/></label>
     <label>O sube el logo (imagen)<input type="file" accept="image/*" @change="e=>logoFile=e.target.files[0]"/></label>
     <label>Correo de soporte<input v-model="form.support_email"/></label>
     <label>Texto del pie de página<input v-model="form.footer_text"/></label>
     <button @click="save">Guardar cambios</button><p v-if="msg" style="color:var(--verde);font-weight:600">{{msg}}</p>
     <div style="margin-top:16px;padding:16px;border-radius:12px" :style="{background:form.primary_color,color:'#fff'}">Vista previa · <strong>{{form.platform_name}}</strong> — {{form.company_name}} <span class="pill" :style="{background:form.accent_color,color:'#191904'}">Acento</span></div>
    </div>
   </div>
   <div v-if="sec==='reportes' || sec==='resumen'">
    <div style="display:flex;justify-content:space-between;align-items:start;gap:14px;flex-wrap:wrap">
     <div><h1 style="font-size:27px">Estadísticas de capacitación</h1><p class="meta" style="margin:0">Avance general de la compañía en tiempo real.</p></div>
     <button @click="exportXlsx">Exportar a Excel</button>
    </div>
    <div class="stat-row">
     <div class="stat-card"><small>Completados</small><strong>{{ov.progress?.completed ?? '—'}}</strong></div>
     <div class="stat-card"><small>En progreso</small><strong>{{ov.progress?.in_progress ?? '—'}}</strong></div>
     <div class="stat-card"><small>No iniciados</small><strong>{{ov.progress?.not_started ?? '—'}}</strong></div>
     <div class="stat-card"><small>Certificados</small><strong>{{ov.totals?.certificates ?? '—'}}</strong></div>
    </div>
    <div class="card" style="margin-top:8px"><h3>Cursos más populares</h3><Bars :items="popularItems"/></div>
    <div class="card" style="margin-top:16px"><h3>Avance por curso</h3>
     <table><thead><tr><th>Curso</th><th>Participantes</th><th>Completado</th><th>Calificación</th></tr></thead>
     <tbody><tr v-for="c in ov.per_course||[]" :key="c.id"><td><strong>{{c.title}}</strong></td><td>{{c.enrollments_count}}</td><td><div class="progress" style="width:150px;display:inline-block;vertical-align:middle"><i :style="{width:c.completion_rate+'%'}"></i></div> {{c.completion_rate}} %</td><td>{{avgOf(c.id)}}</td></tr></tbody></table>
    </div>
   </div>
   <div v-if="sec==='usuarios'">
    <h1 style="font-size:27px">Usuarios y roles</h1>
    <p class="meta">Asigna los roles de cada usuario. Un usuario puede tener más de un rol. Los cambios se aplican al instante y se reflejan en su próximo ingreso.</p>
    <label style="max-width:340px;display:block">Buscar usuario<input v-model="uq" placeholder="Nombre o usuario" style="margin-bottom:0"/></label>
    <div class="card" style="margin-top:16px;padding:6px 18px">
     <div v-for="u in filteredUsers" :key="u.id" style="display:flex;gap:14px;align-items:center;padding:14px 0;border-bottom:1px solid var(--borde);flex-wrap:wrap">
      <span class="avatar">{{initialsOf(u)}}</span>
      <div style="min-width:190px;flex:1">
       <strong>{{u.display_name || u.username}}</strong>
       <div class="meta">{{u.username}}<span v-if="u.department"> · {{u.department}}</span><span v-if="u.id===me.id"> · <em>tu cuenta</em></span></div>
      </div>
      <div style="display:flex;gap:8px;flex-wrap:wrap">
       <button v-for="r in ROLE_DEFS" :key="r.code" class="btn btn-sm" :class="sel[u.id]?.includes(r.code) ? 'btn-blue':'btn-ghost'" :disabled="u.id===me.id" @click="toggleRole(u.id, r.code)" :title="u.id===me.id ? 'No puedes cambiar tus propios roles' : ''">{{r.label}}</button>
      </div>
      <button class="btn-sm" :disabled="!changed(u) || u.id===me.id" @click="saveRoles(u)">Guardar</button>
      <span v-if="savedId===u.id" style="color:var(--verde);font-weight:700">Roles actualizados</span>
     </div>
     <p v-if="!filteredUsers.length" class="meta" style="padding:12px 0">Sin usuarios que coincidan.</p>
    </div>
    <p class="meta" style="margin-top:10px">Por seguridad no puedes modificar los roles de tu propia cuenta administradora.</p>
   </div>
  </div>
 </div>
</section>
</template>
<script setup>
import {ref, onMounted, computed, reactive} from 'vue'; import api from '../services/api'; import Bars from '../components/Bars.vue'; import {branding, loadBranding, me} from '../services/branding'; import {BRAND} from '../config/brand'
const sec=ref('resumen')
const form=reactive({company_name:BRAND.companyName,platform_name:BRAND.platformName,tagline:BRAND.tagline,primary_color:BRAND.primaryColor,accent_color:BRAND.accentColor,beige_color:BRAND.neutralColor,danger_color:BRAND.dangerColor,logo_url:'',support_email:'',footer_text:BRAND.footerText})
const logoFile=ref(null); const msg=ref(''); const ov=ref({})
const popularItems=computed(()=> (ov.value.popular_courses||[]).map(c=>({label:c.title, value:c.enrollments_count, display:c.enrollments_count+' participaciones · ★ '+(c.avg_rating? Number(c.avg_rating).toFixed(1):'—')})))
const avgOf=id=>{ const p=(ov.value.popular_courses||[]).find(x=>x.id===id); return p && p.avg_rating ? '★ '+Number(p.avg_rating).toFixed(1)+' ('+p.ratings_count+')' : '—' }
const ROLE_DEFS=[{code:'ADMIN',label:'Administrador'},{code:'GESTOR',label:'Gestor'},{code:'COLABORADOR',label:'Estudiante'}]
const usersList=ref([]); const sel=ref({}); const uq=ref(''); const savedId=ref(null)
const initialsOf=u=> (u.display_name||u.username||'?').split(' ').filter(Boolean).slice(0,2).map(w=>w[0]).join('').toUpperCase()
const filteredUsers=computed(()=> usersList.value.filter(u=> !uq.value || ((u.display_name||'')+' '+u.username).toLowerCase().includes(uq.value.toLowerCase())))
function toggleRole(uid, code){ const cur=sel.value[uid]||[]; sel.value[uid]= cur.includes(code) ? cur.filter(c=>c!==code) : [...cur, code]; savedId.value=null }
function changed(u){ const orig=(u.roles||[]).map(r=>r.code).sort().join(','); const now=[...(sel.value[u.id]||[])].sort().join(','); return orig!==now }
async function saveRoles(u){ const {data}=await api.post(`/auth/users/${u.id}/set_roles/`, {role_codes: sel.value[u.id]||[]}); const i=usersList.value.findIndex(x=>x.id===u.id); if(i>=0) usersList.value[i]=data; sel.value[u.id]=(data.roles||[]).map(r=>r.code); savedId.value=u.id }
async function loadUsers(){ try{ usersList.value=(await api.get('/auth/users/')).data.results||[]; usersList.value.forEach(u=> sel.value[u.id]=(u.roles||[]).map(r=>r.code)) }catch{} }
async function load(){ try{ Object.assign(form,(await api.get('/branding/admin/')).data) }catch{}; try{ ov.value=(await api.get('/reports/overview/')).data }catch{}; loadUsers() }
async function save(){ const fd=new FormData(); Object.entries(form).forEach(([k,v])=>{ if(v!==null && v!==undefined) fd.append(k,v) }); if(logoFile.value) fd.append('logo_file',logoFile.value); await api.put('/branding/admin/',fd); msg.value='Cambios guardados y aplicados a toda la plataforma.'; loadBranding() }
async function exportXlsx(){ const r=await api.get('/reports/export.xlsx',{responseType:'blob'}); const a=document.createElement('a'); a.href=URL.createObjectURL(r.data); a.download='reporte-capacitacion.xlsx'; a.click() }
onMounted(load)
</script>
