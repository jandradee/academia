<template>
<section class="wrap">
 <h1 style="font-size:30px">Mis certificados</h1>
 <p class="meta">Cada curso aprobado genera tu certificado de finalización. Puedes verlo e imprimirlo o guardarlo en PDF.</p>
 <div class="grid" style="margin-top:18px">
  <article v-for="c in certs" :key="c.id" class="card" style="text-align:left">
   <div style="width:52px;height:52px;border-radius:14px;background:var(--tint);display:flex;align-items:center;justify-content:center"><svg width="27" height="27" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="9" r="5.5" style="stroke:var(--amarillo)" stroke-width="2"/><path d="M8.8 13.5 7 21l5-2.6L17 21l-1.8-7.5" style="stroke:var(--amarillo)" stroke-width="2" stroke-linejoin="round"/></svg></div>
   <h3 style="margin:.3em 0">{{courseTitle(c.course)}}</h3>
   <p class="meta" style="margin:2px 0">Completado el {{fmtDate(c.completion_date)}} · {{fmtDur(c.recognized_duration_minutes)}} reconocidas</p>
   <p class="meta" style="margin:2px 0">Identificador: {{BRAND.certificatePrefix}}-{{yearOf(c)}}-{{String(c.id).padStart(6,'0')}}</p>
   <router-link :to="`/certificado/${c.id}`" class="btn btn-outline btn-sm" style="margin-top:10px">Ver certificado</router-link>
  </article>
 </div>
 <div v-if="!certs.length" class="empty" style="margin-top:18px"><strong>Todavía no tienes certificados</strong>Cuando apruebes tu primer curso, aparecerá aquí.</div>
</section>
</template>
<script setup>
import {ref, onMounted} from 'vue'; import api from '../services/api'; import {BRAND} from '../config/brand'
const certs=ref([]); const courses=ref([])
const courseTitle=id=> courses.value.find(c=>c.id===id)?.title || ('Curso #'+id)
const fmtDate=d=> d? new Date(d+'T12:00:00').toLocaleDateString('es',{day:'numeric',month:'long',year:'numeric'}) : ''
const fmtDur=min=>{ if(!min) return ''; const h=Math.floor(min/60), m=min%60; return h? `${h} h ${String(m).padStart(2,'0')} min` : `${m} min` }
const yearOf=c=> (c.completion_date||'2026').slice(0,4)
onMounted(async()=>{ try{ certs.value=(await api.get('/certificates/')).data.results||[] }catch{}; try{ courses.value=(await api.get('/courses/')).data.results||[] }catch{} })
</script>
