<template>
<section>
 <div class="hero" style="background:var(--azul)"><div class="wrap" style="padding-top:18px;padding-bottom:18px"><strong style="font-size:18px">{{branding.platform_name}} · Gestión de cursos</strong></div></div>
 <div class="admin-shell">
  <aside class="admin-side">
   <button :class="{on:sec==='cursos'}" @click="sec='cursos'">Cursos</button>
   <button :class="{on:sec==='contenido'}" @click="sec='contenido'">Contenido y videos</button>
   <button :class="{on:sec==='quiz'}" @click="sec='quiz'">Quiz</button>
   <button :class="{on:sec==='asignar'}" @click="sec='asignar'">Asignaciones</button>
  </aside>
  <div class="admin-main">
   <div style="display:flex;justify-content:space-between;align-items:start;gap:14px;flex-wrap:wrap">
    <div><h1 style="font-size:27px">{{ {cursos:'Cursos', nuevo:'Nuevo curso', contenido:'Contenido y videos', quiz:'Quiz', asignar:'Asignaciones'}[sec] || 'Cursos' }}</h1><p class="meta" style="margin:0">Consola del gestor de cursos.</p></div>
    <button @click="sec='nuevo'">+ Nuevo curso</button>
   </div>

   <div v-if="sec==='cursos'">
   <div class="stat-row">
    <div class="stat-card"><small>Publicados</small><strong>{{countBy('publicado')}}</strong></div>
    <div class="stat-card"><small>Borradores</small><strong>{{countBy('borrador')}}</strong></div>
    <div class="stat-card"><small>Archivados</small><strong>{{countBy('archivado')}}</strong></div>
    <div class="stat-card"><small>Empleados</small><strong>{{users.length}}</strong></div>
   </div>
   <div class="card" style="margin-bottom:18px"><h3 style="margin-bottom:8px">Cursos registrados</h3>
    <table><thead><tr><th>Curso</th><th>Tipo</th><th>Estado</th><th></th></tr></thead>
    <tbody><tr v-for="c in courses" :key="c.id" :style="selCourseId===c.id?{background:'var(--tint)'}:{}"><td><strong>{{c.title}}</strong></td><td>{{c.course_type==='obligatorio'?'Obligatorio':'Opcional'}}</td><td><span class="pill" :class="'pill-'+c.status">{{c.status}}</span></td><td style="text-align:right"><a href="#" @click.prevent="selCourseId=c.id; loadDetail()">Editar</a></td></tr></tbody></table>
    <label style="margin-top:12px">Curso en edición<select v-model="selCourseId" @change="loadDetail"><option v-for="c in courses" :key="c.id" :value="c.id">{{c.title}}</option></select></label>
    <div v-if="detail" style="display:flex;gap:14px;align-items:center;margin-top:10px;flex-wrap:wrap">
     <img v-if="detail.cover" :src="detail.cover" alt="miniatura" style="width:150px;height:86px;object-fit:cover;border-radius:10px;border:1px solid var(--borde)"/>
     <div v-else class="cover" style="width:150px;height:86px">Sin imagen</div>
     <label style="flex:1;min-width:220px">Imagen miniatura del curso (se muestra en todo el sitio)<input type="file" accept="image/*" @change="e=>uploadCover(e)"/></label>
    </div>
    <p v-if="detail"><button class="btn btn-blue btn-sm" @click="setStatus('publicado')">Publicar</button> <button class="btn btn-ghost btn-sm" @click="setStatus('archivado')">Archivar</button> <span class="meta">Estado actual: {{detail.status}}</span></p>
   </div>
   </div>

   <div v-if="sec==='nuevo'" class="card"><h3>Nuevo curso</h3>
    <label>Título<input v-model="nc.title"/></label>
    <label>Descripción corta<input v-model="nc.short_description"/></label>
    <label>Descripción detallada<textarea v-model="nc.description" rows="3"></textarea></label>
    <label>Imagen miniatura (portada del curso)<input type="file" accept="image/*" @change="e=>coverFile=e.target.files[0]"/></label>
    <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:0 12px"><label>Tipo<select v-model="nc.course_type"><option value="obligatorio">Obligatorio</option><option value="opcional">Opcional</option></select></label><label>Duración estimada (min)<input type="number" v-model="nc.estimated_duration_minutes"/></label><label>Duración reconocida (min)<input type="number" v-model="nc.recognized_duration_minutes"/></label></div>
    <button @click="createCourse">Crear curso (borrador)</button><p v-if="msg" style="color:var(--verde);font-weight:600">{{msg}}</p>
   </div>

   <div v-if="sec==='contenido' && detail" class="card"><h3>Módulos, videos y recursos</h3>
        <label>Curso en edición<select v-model="selCourseId" @change="loadDetail"><option v-for="c in courses" :key="c.id" :value="c.id">{{c.title}}</option></select></label>
    <div v-for="m in detail.modules" :key="m.id" style="border:1px solid var(--borde);border-radius:12px;padding:14px;margin:10px 0"><strong>{{m.title}}</strong>
     <div style="margin:8px 0" class="meta">Videos: <span v-for="v in m.videos" :key="v.id" style="margin-right:8px">{{v.title}}</span><span v-if="!m.videos.length">ninguno</span></div>
     <label>Subir video a este módulo<input type="file" accept="video/*" @change="e=>uploadVideo(m.id, e)"/></label>
     <div style="margin:8px 0" class="meta">Recursos: <span v-for="r in m.resources" :key="r.id" style="margin-right:8px">{{r.title}}</span><span v-if="!m.resources.length">ninguno</span></div>
     <label>Subir recurso (PDF/Office)<input type="file" @change="e=>uploadResource(m.id, e)"/></label>
    </div>
    <label>Nuevo módulo: título<input v-model="nm.title" placeholder="Ej. Módulo 1 — Introducción"/></label><button @click="addModule">Añadir módulo</button>
   </div>

   <div v-if="sec==='quiz' && detail" class="card"><h3>Quiz del curso</h3>
        <label>Curso en edición<select v-model="selCourseId" @change="loadDetail"><option v-for="c in courses" :key="c.id" :value="c.id">{{c.title}}</option></select></label>
    <label>Título del quiz<input v-model="nq.title" placeholder="Evaluación final"/></label><button class="btn btn-blue" @click="createQuiz">Crear quiz</button>
    <div v-if="quiz" style="margin-top:14px"><p>Quiz activo: <strong>{{quiz.title}}</strong> ({{quiz.questions?.length||0}} preguntas)</p>
     <label>Pregunta<input v-model="nquest.question_text"/></label>
     <div v-for="(o,i) in nquest.options" :key="i" style="display:flex;gap:8px;align-items:center;margin:4px 0"><input v-model="o.option_text" :placeholder="'Opción '+(i+1)" style="flex:1;margin:0"/><label style="font-size:13px;white-space:nowrap"><input type="radio" style="width:auto" name="correcta" :value="i" v-model="nquest.correct"/> correcta</label></div>
     <button @click="addQuestion" style="margin-top:8px">Añadir pregunta</button>
    </div>
   </div>

   <div v-if="sec==='asignar' && detail" class="card"><h3>Asignar «{{detail.title}}» a empleados</h3>
        <label>Curso en edición<select v-model="selCourseId" @change="loadDetail"><option v-for="c in courses" :key="c.id" :value="c.id">{{c.title}}</option></select></label>
    <label>Fecha límite (opcional)<input type="date" v-model="assign.due"/></label>
    <label style="display:block;margin:8px 0"><input type="checkbox" style="width:auto" v-model="assign.mandatory"/> Es obligatorio</label>
    <div style="max-height:200px;overflow:auto;border:1px solid var(--borde);border-radius:10px;padding:10px"><label v-for="u in users" :key="u.id" style="display:block;margin:4px 0;font-weight:400"><input type="checkbox" style="width:auto" :value="u.id" v-model="assign.selected"/> {{u.display_name||u.username}} <span class="meta">{{u.department}}</span></label></div>
    <button @click="doAssign" style="margin-top:10px">Asignar a los seleccionados ({{assign.selected.length}})</button>
    <p v-if="assignMsg" style="color:var(--verde);font-weight:600">{{assignMsg}}</p>
   </div>
   <p v-if="!detail && (sec==='contenido' || sec==='quiz' || sec==='asignar')" class="meta">Selecciona un curso en la sección «Cursos» para trabajar en esta sección.</p>
  </div>
 </div>
</section>
</template>
<script setup>
import {ref, onMounted, reactive} from 'vue'; import api from '../services/api'; import {branding} from '../services/branding'
const sec=ref('cursos')
const courses=ref([]); const users=ref([]); const selCourseId=ref(null); const detail=ref(null); const msg=ref(''); const assignMsg=ref('')
const nc=reactive({title:'',short_description:'',description:'',course_type:'obligatorio',estimated_duration_minutes:60,recognized_duration_minutes:60})
const nm=reactive({title:''}); const nq=reactive({title:''}); const quiz=ref(null)
const nquest=reactive({question_text:'', correct:0, options:[{option_text:''},{option_text:''},{option_text:''},{option_text:''}]})
const assign=reactive({due:'', mandatory:true, selected:[]})
const countBy=s=> courses.value.filter(c=>c.status===s).length
async function loadCourses(){ courses.value=(await api.get('/courses/')).data.results||[]; if(courses.value.length && !selCourseId.value){ selCourseId.value=courses.value[0].id; loadDetail() } }
const coverFile=ref(null)
async function createCourse(){ const {data}=await api.post('/courses/',nc); msg.value='Curso creado: '+data.title; selCourseId.value=data.id; if(coverFile.value){ const fd=new FormData(); fd.append('file', coverFile.value); await api.post(`/courses/${data.id}/cover/`, fd); coverFile.value=null } await loadCourses(); loadDetail(); sec.value='contenido' }
async function uploadCover(e){ const f=e.target.files[0]; if(!f || !selCourseId.value) return; const fd=new FormData(); fd.append('file', f); await api.post(`/courses/${selCourseId.value}/cover/`, fd); loadDetail(); loadCourses() }
async function loadDetail(){ if(!selCourseId.value) return; detail.value=(await api.get(`/courses/${selCourseId.value}/`)).data; const qs=(await api.get('/quizzes/',{params:{course:selCourseId.value}})).data.results||[]; quiz.value=qs[0]||null }
async function setStatus(s){ await api.patch(`/courses/${selCourseId.value}/`,{status:s}); await loadCourses(); loadDetail() }
async function addModule(){ await api.post('/modules/',{course:selCourseId.value, title:nm.title, sort_order:(detail.value.modules?.length||0)+1}); nm.title=''; loadDetail() }
async function uploadVideo(moduleId, e){ const fd=new FormData(); fd.append('file', e.target.files[0]); fd.append('module', moduleId); fd.append('title', e.target.files[0].name); await api.post('/videos/upload/', fd); loadDetail() }
async function uploadResource(moduleId, e){ const fd=new FormData(); fd.append('file', e.target.files[0]); fd.append('module', moduleId); fd.append('title', e.target.files[0].name); await api.post('/resources/upload/', fd); loadDetail() }
async function createQuiz(){ const {data}=await api.post('/quizzes/',{course:selCourseId.value, title:nq.title||'Evaluación', pass_score:70}); quiz.value=data; loadDetail() }
async function addQuestion(){ const opts=nquest.options.map((o,i)=>({option_text:o.option_text, is_correct:i===nquest.correct})); await api.post(`/quizzes/${quiz.value.id}/add_question/`,{question_text:nquest.question_text, options:opts}); nquest.question_text=''; loadDetail() }
async function doAssign(){ const body={course:selCourseId.value, user_ids:assign.selected, is_mandatory:assign.mandatory}; if(assign.due) body.due_at=assign.due+'T23:59:59'; const {data}=await api.post('/assignments/bulk/', body); assignMsg.value=`Asignados: ${data.created_user_ids.length} · Ya lo tenían: ${data.already_assigned_user_ids.length}` }
onMounted(async()=>{ try{ users.value=(await api.get('/auth/users/')).data.results||[] }catch{}; loadCourses() })
</script>
