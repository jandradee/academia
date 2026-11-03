<template>
<section class="wrap" style="max-width:860px">
  <h1 style="font-size:28px">{{t('profile_title')}}</h1>
  <p class="meta">{{t('profile_sub')}}</p>

  <div class="card" style="margin-top:18px">
    <h2>{{t('photo')}}</h2>
    <div style="display:flex;align-items:center;gap:18px;flex-wrap:wrap;margin-top:10px">
      <img v-if="preview || me.avatar_blob" :src="preview || me.avatar_blob" alt="" class="avatar-img xl"/>
      <span v-else class="avatar xl">{{initials}}</span>
      <div>
        <label class="btn btn-sm" style="cursor:pointer">{{ me.avatar_url ? t('photo_change') : t('photo_upload') }}
          <input type="file" accept="image/*" hidden @change="onFile"/>
        </label>
        <button v-if="me.avatar_url" class="linkbtn" style="margin-left:10px" @click="removePhoto">{{t('photo_remove')}}</button>
        <p class="meta" style="margin-top:8px">{{t('photo_hint')}}</p>
      </div>
    </div>
  </div>

  <form class="card" style="margin-top:16px" @submit.prevent="save">
    <h2>{{t('data')}}</h2>
    <div class="grid2">
      <label>{{t('full_name')}}<input v-model="form.display_name"/></label>
      <label>{{t('email')}}<input :value="me.email" disabled/></label>
      <label>{{t('username')}}<input :value="me.username" disabled/></label>
      <label>{{t('department')}}<input v-model="form.department"/></label>
      <label>{{t('job_title')}}<input v-model="form.job_title"/></label>
      <label>{{t('office')}}<input v-model="form.office_location"/></label>
    </div>
    <p class="meta" style="margin-top:10px">{{t('member_roles')}}: {{ (me.role_codes||[]).join(', ') || '—' }}</p>

    <h2 id="preferencias" style="margin-top:26px">{{t('prefs')}}</h2>
    <div class="grid2">
      <label>{{t('language')}}
        <select v-model="form.language">
          <option value="es">Español</option>
          <option value="en">English</option>
        </select>
      </label>
      <label style="display:flex;gap:10px;align-items:center;margin-top:22px">
        <input type="checkbox" v-model="form.email_notifications" style="width:auto"/>
        <span>{{t('notifications')}}<br/><small class="meta">{{t('notifications_hint')}}</small></span>
      </label>
    </div>

    <div style="margin-top:20px;display:flex;gap:12px;align-items:center">
      <button type="submit" :disabled="saving">{{ saving ? t('saving') : t('save') }}</button>
      <span v-if="msg" style="color:var(--verde);font-weight:600">{{msg}}</span>
      <span v-if="err" style="color:var(--rojo);font-weight:600">{{err}}</span>
    </div>
  </form>
</section>
</template>
<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import api from '../services/api'
import { me, loadMe } from '../services/branding'
import { t, setLang } from '../services/i18n'

const form = reactive({ display_name:'', department:'', job_title:'', office_location:'', language:'es', email_notifications:true })
const saving = ref(false); const msg = ref(''); const err = ref(''); const preview = ref('')
const initials = computed(()=> (me.display_name||'?').split(' ').filter(Boolean).slice(0,2).map(w=>w[0]).join('').toUpperCase())

function fill(){ Object.assign(form, { display_name: me.display_name||'', department: me.department||'', job_title: me.job_title||'', office_location: me.office_location||'', language: me.language||'es', email_notifications: me.email_notifications !== false }) }
onMounted(async ()=>{ if(!me.loaded) await loadMe(); fill() })
watch(()=>me.loaded, fill)

async function onFile(e){
  const f = e.target.files && e.target.files[0]; if(!f) return
  preview.value = URL.createObjectURL(f)
  const fd = new FormData(); fd.append('avatar', f)
  try{ await api.patch('/auth/me/', fd); await loadMe(); msg.value = t('saved') }catch{ err.value = 'Error' }
}
async function removePhoto(){
  try{ await api.delete('/auth/me/avatar/'); preview.value=''; await loadMe(); msg.value = t('saved') }catch{ err.value = 'Error' }
}
async function save(){
  saving.value = true; msg.value=''; err.value=''
  try{
    await api.patch('/auth/me/', { ...form })
    setLang(form.language)
    await loadMe(); fill(); msg.value = t('saved')
  }catch{ err.value = 'Error' }
  saving.value = false
}
</script>
