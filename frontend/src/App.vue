<template>
<header v-if="!bare" class="site"><div class="bar">
  <router-link to="/" class="logo">
    <span class="mark" v-if="!branding.logo"><svg width="22" height="22" viewBox="0 0 24 24" fill="none"><path d="M12 5c-1.8-1.5-4.2-2-8-2v14c3.8 0 6.2.5 8 2 1.8-1.5 4.2-2 8-2V3c-3.8 0-6.2.5-8 2Z" style="fill:var(--amarillo)"/><path d="M12 5v14" style="stroke:var(--azul)" stroke-width="1.6"/></svg></span>
    <img v-else :src="branding.logo" alt="logo" style="height:40px;border-radius:8px"/>
    <span><span class="w1">{{branding.platform_name}}</span><span class="w2" v-if="branding.company_name">{{branding.company_name}}</span></span>
  </router-link>
  <nav class="main">
    <router-link to="/">Inicio</router-link>
    <router-link to="/catalogo">Catálogo</router-link>
    <router-link to="/">Mis cursos</router-link>
    <router-link to="/certificados">Certificados</router-link>
    <router-link v-if="isManager()" to="/gestion">Gestión</router-link>
    <router-link v-if="isAdmin()" to="/admin-consola">Administración</router-link>
  </nav>
  <div class="userbox">
    <template v-if="me.display_name"><span style="font-weight:600;font-size:14.5px">{{me.display_name}}</span><span class="avatar">{{initials}}</span><button class="linkbtn" @click="logout">Salir</button></template>
    <router-link v-else to="/login" class="btn btn-sm">Ingresar</router-link>
  </div>
</div></header>
<main><router-view/></main>
<footer v-if="!bare" class="site">{{branding.footer_text}}<span v-if="branding.tagline"> · {{branding.tagline}}</span></footer>
</template>
<script setup>
import {computed, onMounted} from 'vue'; import {useRoute, useRouter} from 'vue-router'
import {branding, me, loadBranding, loadMe, isAdmin, isManager} from './services/branding'
const route = useRoute(); const router = useRouter()
const bare = computed(()=> route.name === 'certificado')
const initials = computed(()=> (me.display_name||'?').split(' ').filter(Boolean).slice(0,2).map(w=>w[0]).join('').toUpperCase())
function logout(){ localStorage.removeItem('access'); localStorage.removeItem('refresh'); location.href='/login' }
onMounted(()=>{ loadBranding(); loadMe() })
</script>
