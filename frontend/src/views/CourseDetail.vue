<template>
<section class="wrap" v-if="course">
 <div class="crumbs"><router-link to="/">Inicio</router-link> / <router-link to="/catalogo">Catálogo</router-link> / <strong>{{course.title}}</strong></div>
 <div class="cols">
  <div>
   <div class="player">
    <video v-if="currentVideo && currentVideo.storage_key" :key="currentVideo.id" ref="player" controls preload="metadata" :poster="course.cover||undefined" :src="streamUrl(currentVideo.id)" @loadedmetadata="onLoaded" @timeupdate="onTime" @pause="reportNow" @ended="reportNow"></video>
    <div v-else style="aspect-ratio:16/7;display:flex;flex-direction:column;align-items:center;justify-content:center;color:rgba(255,255,255,.75);gap:12px"><span style="width:64px;height:64px;border-radius:50%;border:2px solid rgba(255,255,255,.35);display:flex;align-items:center;justify-content:center;color:#fff;font-size:22px;padding-left:4px">▶</span><span>Selecciona un módulo para ver su video</span></div>
    <div class="pfoot"><span>{{currentModule ? currentModule.title : ''}}</span><span>{{course.code}}</span></div>
   </div>
   <h1 style="font-size:28px;margin-top:20px">{{course.title}}</h1>
   <p style="color:var(--gris);max-width:70ch">{{course.description || course.short_description}}</p>
   <div class="tabs">
    <button :class="{on:tab==='modulos'}" @click="tab='modulos'">Módulos</button>
    <button :class="{on:tab==='recursos'}" @click="tab='recursos'">Recursos</button>
    <button :class="{on:tab==='quiz'}" @click="tab='quiz'">Quiz</button>
   </div>
   <div v-if="tab==='modulos'">
    <button v-for="(m,i) in course.modules||[]" :key="m.id" class="mod-row" :class="{now: currentModule && currentModule.id===m.id}" @click="selectModule(m)">
     <span class="n">{{i+1}}</span>
     <span style="flex:1"><strong>{{m.title}}</strong><br/><small class="meta">{{m.videos?.length||0}} video(s)<span v-if="m.resources?.length"> · {{m.resources.length}} recurso(s)</span></small></span>
     <span v-if="m.videos?.length" style="color:var(--azul)">▶</span>
    </button>
    <p v-if="!(course.modules||[]).length" class="meta">Este curso aún no tiene módulos publicados.</p>
   </div>
   <div v-if="tab==='recursos'">
    <div v-for="m in course.modules||[]" :key="m.id">
     <div v-for="r in m.resources||[]" :key="r.id" class="mod-row" @click="download(r.id)">
      <span class="n"><svg width="15" height="15" viewBox="0 0 24 24" fill="none"><path d="M7 3h7l5 5v13a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1Z" style="stroke:var(--gris)" stroke-width="1.8"/><path d="M14 3v5h5" style="stroke:var(--gris)" stroke-width="1.8"/></svg></span><span style="flex:1"><strong>{{r.title}}</strong><br/><small class="meta">{{m.title}}</small></span><span v-if="viewedResources.has(r.id)" class="pill pill-completado">✓ Visto</span><span class="btn btn-outline btn-sm">Descargar</span>
     </div>
    </div>
    <p v-if="!allResources.length" class="meta">Sin recursos descargables por ahora.</p>
   </div>
   <div v-if="tab==='quiz'">
    <div v-for="q in quizzes" :key="q.id" class="card" style="margin:12px 0">
     <h3>{{q.title}}</h3><p class="meta">Aprobación: {{q.pass_score}} % · {{q.questions?.length||0}} preguntas<span v-if="attemptsOf(q.id).length"> · Intentos realizados: <strong>{{attemptsOf(q.id).length}}</strong></span><span v-if="q.max_attempts"> · Máximo: {{q.max_attempts}}</span></p>
     <div v-if="attemptsOf(q.id).length" style="margin:8px 0"><div v-for="a in attemptsOf(q.id)" :key="a.id" class="meta">Intento {{a.attempt_number}} — {{a.submitted_at ? (a.score+' % · '+(a.passed?'✅ Aprobado':'❌ No aprobado')) : 'en curso'}}</div></div>
     <button v-if="!activeQuiz || activeQuiz.id!==q.id" @click="startQuiz(q)">{{ attemptsOf(q.id).some(a=>a.passed) ? 'Presentar de nuevo' : (attemptsOf(q.id).length ? 'Realizar un nuevo intento' : 'Presentar quiz') }}</button>
     <p v-if="startError && activeQuiz===null" style="color:var(--rojo)">{{startError}}</p>
     <div v-else>
      <div v-for="qq in q.questions" :key="qq.id" style="margin:14px 0"><p><strong>{{qq.question_text}}</strong></p>
       <label v-for="o in qq.options" :key="o.id" style="display:block;font-weight:400;margin:5px 0"><input type="radio" style="width:auto" :name="'q'+qq.id" :value="o.id" v-model="answers[qq.id]"/> {{o.option_text}}</label>
      </div>
      <button @click="submitQuiz(q)">Enviar respuestas</button>
      <p v-if="quizResult" style="margin-top:10px">Resultado del intento {{quizResult.attempt_number}}: <strong>{{quizResult.score}} %</strong> — {{quizResult.passed ? '✅ Aprobado. ¡Buen trabajo!' : '❌ No aprobado.'}}</p>
      <button v-if="quizResult && !quizResult.passed" class="btn btn-blue" style="margin-top:6px" @click="startQuiz(q)">🔁 Realizar un nuevo intento</button>
     </div>
    </div>
    <p v-if="!quizzes.length" class="meta">Este curso no tiene quiz asociado.</p>
   </div>
  </div>
  <aside>
   <div class="side-card"><h3>Tu avance</h3>
    <div class="progress"><i :style="{width:(myProg?.progress_percent||0)+'%'}"></i></div>
    <p><strong>{{myProg?.progress_percent||0}} % completado</strong> · {{myProg?.status==='aprobado'?'Aprobado':(myProg?'En progreso':'Sin iniciar')}}</p>
    <p class="meta">Para completar el curso debes consumir más del 95 % del contenido y aprobar el 100 % de los quizzes asociados.</p>
    <table style="margin-top:6px">
     <tr><td class="meta">Duración</td><td style="text-align:right"><strong>{{fmtDur(course.estimated_duration_minutes)}}</strong></td></tr>
     <tr><td class="meta">Reconocida</td><td style="text-align:right"><strong>{{fmtDur(course.recognized_duration_minutes)}}</strong></td></tr>
     <tr><td class="meta">Quiz final</td><td style="text-align:right"><strong>Mínimo {{quizzes[0]?.pass_score ?? 70}} %</strong></td></tr>
    </table>
    <button class="btn" style="width:100%;margin-top:12px" @click="goContinue">Continuar con el curso</button>
   </div>
   <div class="side-card"><h3>Tu opinión</h3>
    <div style="display:flex;align-items:center;gap:8px"><Stars :value="Math.round(rating.average||0)" readonly/><span v-if="rating.average"><strong>{{rating.average}}</strong> ({{rating.count}})</span><span v-else class="meta">Sin calificaciones aún</span></div>
    <p class="meta" style="margin-bottom:4px">¿Qué te pareció este curso?</p>
    <Stars :value="rating.my_rating?.stars||0" @rate="rate"/>
    <p v-if="ratingMsg" class="meta">{{ratingMsg}}</p>
   </div>
  </aside>
 </div>
</section>
<p v-else class="wrap">Cargando curso…</p>
</template>
<script setup>
import {ref, onMounted, reactive, computed} from 'vue'; import api from '../services/api'; import Stars from '../components/Stars.vue'
const props=defineProps({id:String})
const course=ref(null); const quizzes=ref([]); const rating=ref({}); const ratingMsg=ref('')
const tab=ref('modulos'); const currentModule=ref(null); const currentVideo=ref(null); const myProg=ref(null)
const activeQuiz=ref(null); const answers=reactive({}); const quizResult=ref(null); let attemptId=null
const player=ref(null); const attemptsByQuiz=ref({}); const startError=ref(''); const viewedResources=ref(new Set()); let lastReport=0
const attemptsOf=qid=> attemptsByQuiz.value[qid]||[]
async function loadAttempts(){ for(const q of quizzes.value){ try{ attemptsByQuiz.value[q.id]=(await api.get('/quiz-attempts/',{params:{quiz:q.id}})).data.results||[] }catch{} } }
async function reportNow(){ const v=player.value; if(!v || !currentVideo.value) return; try{ const {data}=await api.post(`/videos/${currentVideo.value.id}/report/`, {position_seconds: Math.floor(v.currentTime||0), duration_seconds: Math.floor(v.duration||0)}); if(myProg.value){ myProg.value.progress_percent=data.course_progress_percent; myProg.value.status=data.course_status } }catch{} }
function onTime(){ const now=Date.now(); if(now-lastReport>10000){ lastReport=now; reportNow() } }
async function onLoaded(){ try{ const ps=(await api.get('/video-progress/',{params:{video:currentVideo.value.id}})).data.results||[]; const mine=ps[0]; if(mine && mine.last_position_seconds>5 && player.value) player.value.currentTime=mine.last_position_seconds }catch{} }
const token=()=>localStorage.getItem('access')||''
const streamUrl=id=>`/api/videos/${id}/stream/?token=${token()}`
const fmtDur=min=>{ if(!min) return '—'; const h=Math.floor(min/60), m=min%60; return h? `${h} h ${String(m).padStart(2,'0')} min` : `${m} min` }
const allResources=computed(()=> (course.value?.modules||[]).flatMap(m=>m.resources||[]))
function selectModule(m){ currentModule.value=m; currentVideo.value=(m.videos||[])[0]||null }
function goContinue(){ const mods=course.value?.modules||[]; const nx=mods.find(m=>(m.videos||[]).length) || mods[0]; if(nx){ selectModule(nx); tab.value='modulos'; window.scrollTo({top:0,behavior:'smooth'}) } }
async function download(rid){ const r=await api.get(`/resources/${rid}/download/`,{responseType:'blob'}); viewedResources.value=new Set([...viewedResources.value, rid]); const a=document.createElement('a'); a.href=URL.createObjectURL(r.data); a.download='recurso'; a.click() }
async function loadRating(){ try{ rating.value=(await api.get(`/courses/${props.id}/my-rating/`)).data }catch{} }
async function rate(n){ await api.post(`/courses/${props.id}/my-rating/`,{stars:n}); ratingMsg.value='¡Gracias! Tu calificación quedó registrada.'; loadRating() }
async function startQuiz(q){ startError.value=''; try{ const {data}=await api.post('/quiz-attempts/',{quiz:q.id}); attemptId=data.id; activeQuiz.value=q; quizResult.value=null; Object.keys(answers).forEach(k=>delete answers[k]) }catch(e){ activeQuiz.value=null; startError.value=(e.response && e.response.data && (e.response.data[0]||e.response.data.detail)) || 'No se pudo iniciar el intento.' } }
async function submitQuiz(q){ for(const qq of q.questions){ if(answers[qq.id]) await api.post(`/quiz-attempts/${attemptId}/answer/`,{question:qq.id, selected_option:answers[qq.id]}) } const {data}=await api.post(`/quiz-attempts/${attemptId}/submit/`); quizResult.value=data; activeQuiz.value=null; loadAttempts(); try{ const ps=(await api.get('/course-progress/',{params:{course:props.id}})).data.results||[]; myProg.value=ps[0]||myProg.value }catch{} }
onMounted(async()=>{
 try{ course.value=(await api.get(`/courses/${props.id}/`)).data; const first=(course.value.modules||[]).find(m=>(m.videos||[]).length) || (course.value.modules||[])[0]; if(first) selectModule(first) }catch{}
 try{ quizzes.value=(await api.get('/quizzes/',{params:{course:props.id}})).data.results||[] }catch{}
 try{ const ps=(await api.get('/course-progress/',{params:{course:props.id}})).data.results||[]; myProg.value=ps[0]||null }catch{}
 try{ const rs=(await api.get('/resource-progress/')).data.results||[]; viewedResources.value=new Set(rs.map(r=>r.resource)) }catch{}
 loadAttempts(); loadRating()
})
</script>
