<template>
<section class="wrap">
 <div style="display:flex;justify-content:space-between;gap:20px;flex-wrap:wrap;align-items:end">
  <div><h1 style="font-size:32px">Catálogo de cursos</h1><p class="meta" style="margin:0">{{courses.length}} cursos disponibles para tu área y sede.</p></div>
  <div style="display:flex;gap:12px;flex-wrap:wrap">
   <label style="flex:1;min-width:200px">Buscar<input v-model="q" placeholder="Nombre del curso" style="margin-bottom:0"/></label>
   <label>Tipo<select v-model="tipo" style="margin-bottom:0"><option value="">Todos</option><option value="obligatorio">Obligatorios</option><option value="opcional">Opcionales</option></select></label>
  </div>
 </div>
 <div style="display:flex;gap:10px;flex-wrap:wrap;margin:18px 0 22px">
  <button class="btn btn-sm" :class="catSel===null?'btn-blue':'btn-ghost'" @click="catSel=null">Todas</button>
  <button v-for="c in categories" :key="c.id" class="btn btn-sm" :class="catSel===c.id?'btn-blue':'btn-ghost'" @click="catSel=c.id">{{c.name}}</button>
 </div>
 <div class="grid">
  <article v-for="c in filtered" :key="c.id" class="card course-card">
   <div class="cover"><img v-if="c.cover" :src="c.cover" alt="" style="width:100%;height:100%;object-fit:cover"/><span v-else class="play">▶</span></div>
   <div class="body">
    <span class="pill" :class="c.course_type==='obligatorio'?'pill-obligatorio':'pill-opcional'" style="align-self:flex-start">{{c.course_type==='obligatorio'?'Obligatorio':'Opcional'}}</span>
    <h3 style="font-size:19px;margin:0">{{c.title}}</h3>
    <p class="meta" style="margin:0">{{c.short_description}}</p>
    <p class="meta" style="margin:0">{{fmtDur(c.estimated_duration_minutes)}}<span v-if="ratings[c.id]"> · ★ {{ratings[c.id].toFixed(1)}}</span><span v-if="prog[c.id]"> · {{prog[c.id]}} % avanzado</span></p>
    <router-link :to="`/curso/${c.id}`" :class="prog[c.id] ? 'btn' : 'btn btn-outline'">{{prog[c.id] ? 'Continuar' : 'Ver curso'}}</router-link>
   </div>
  </article>
 </div>
 <div v-if="!filtered.length" class="empty" style="margin-top:6px"><strong>Sin resultados para ese filtro</strong>Prueba con otra categoría o ajusta la búsqueda.</div>
</section>
</template>
<script setup>
import {ref, onMounted, computed} from 'vue'; import api from '../services/api'
const courses=ref([]); const categories=ref([]); const q=ref(''); const tipo=ref(''); const catSel=ref(null); const prog=ref({}); const ratings=ref({})
const fmtDur=min=>{ if(!min) return ''; const h=Math.floor(min/60), m=min%60; return h? `${h} h ${String(m).padStart(2,'0')} min` : `${m} min` }
const filtered=computed(()=> courses.value.filter(c=> (!q.value || (c.title+' '+c.short_description).toLowerCase().includes(q.value.toLowerCase())) && (!tipo.value || c.course_type===tipo.value) && (catSel.value===null || c.category===catSel.value)))
onMounted(async()=>{
 try{ courses.value=(await api.get('/courses/')).data.results||[] }catch{}
 try{ categories.value=(await api.get('/categories/')).data.results||[] }catch{}
 try{ const ps=(await api.get('/course-progress/')).data.results||[]; ps.forEach(p=> prog.value[p.course]=p.progress_percent) }catch{}
 for(const c of courses.value){ try{ const r=(await api.get(`/courses/${c.id}/my-rating/`)).data; if(r.average) ratings.value[c.id]=r.average }catch{} }
})
</script>
