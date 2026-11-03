<template>
<section class="wrap" style="max-width:440px">
 <div class="card" style="margin-top:44px;text-align:center;padding:38px 34px;box-shadow:var(--sombra-lg)">
  <span class="mark" style="width:58px;height:58px;border-radius:15px;background:linear-gradient(135deg,var(--azul),color-mix(in srgb, var(--azul) 62%, #111827));display:inline-flex;align-items:center;justify-content:center;box-shadow:0 8px 18px color-mix(in srgb, var(--azul) 35%, transparent)"><svg width="31" height="31" viewBox="0 0 24 24" fill="none"><path d="M12 5c-1.8-1.5-4.2-2-8-2v14c3.8 0 6.2.5 8 2 1.8-1.5 4.2-2 8-2V3c-3.8 0-6.2.5-8 2Z" style="fill:var(--amarillo)"/><path d="M12 5v14" style="stroke:var(--azul)" stroke-width="1.6"/></svg></span>
  <h1 style="font-size:26px;margin-top:16px">Bienvenido de nuevo</h1>
  <p class="meta">Ingresa a {{branding.platform_name}}<template v-if="branding.company_name"> de {{branding.company_name}}</template> para continuar tus cursos.</p>
  <form @submit.prevent="login" style="text-align:left;margin-top:12px">
   <label>Usuario<input v-model="u" required autocomplete="username" placeholder="tu.usuario"/></label>
   <label>Contraseña<input v-model="p" type="password" required autocomplete="current-password" placeholder="••••••••••"/></label>
   <button style="width:100%;margin-top:4px">Ingresar</button>
   <p v-if="err" style="color:var(--rojo);font-weight:600">{{err}}</p>
  </form>
  <p class="meta" style="font-size:12.5px;margin-top:16px">Acceso exclusivo para personal autorizado de tu organización.</p>
 </div>
</section>
</template>
<script setup>
import {ref} from 'vue'; import {useRouter, useRoute} from 'vue-router'; import api from '../services/api'; import {branding} from '../services/branding'
const u=ref(''); const p=ref(''); const err=ref(''); const r=useRouter(); const route=useRoute()
async function login(){ try{ const {data}=await api.post('/auth/token/',{username:u.value,password:p.value}); localStorage.setItem('access',data.access); localStorage.setItem('refresh',data.refresh); const nx=route.query.next; const dest=(typeof nx==='string' && nx.startsWith('/') && !nx.startsWith('//')) ? nx : '/'; r.push(dest).then(()=>location.reload()) }catch{ err.value='Credenciales inválidas o servicio no disponible. Revisa tus datos e inténtalo de nuevo.' } }
</script>
