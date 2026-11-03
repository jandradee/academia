<template>
<header v-if="!bare" class="site"><div class="bar">
  <router-link to="/" class="logo">
    <span class="mark" v-if="!branding.logo"><svg width="22" height="22" viewBox="0 0 24 24" fill="none"><path d="M12 5c-1.8-1.5-4.2-2-8-2v14c3.8 0 6.2.5 8 2 1.8-1.5 4.2-2 8-2V3c-3.8 0-6.2.5-8 2Z" style="fill:var(--amarillo)"/><path d="M12 5v14" style="stroke:var(--azul)" stroke-width="1.6"/></svg></span>
    <img v-else :src="branding.logo" alt="logo" style="height:40px;border-radius:8px"/>
    <span><span class="w1">{{branding.platform_name}}</span><span class="w2" v-if="branding.company_name">{{branding.company_name}}</span></span>
  </router-link>
  <nav class="main">
    <router-link to="/">{{t('nav_home')}}</router-link>
    <router-link to="/catalogo">{{t('nav_catalog')}}</router-link>
    <router-link to="/">{{t('nav_my')}}</router-link>
    <router-link to="/certificados">{{t('nav_certs')}}</router-link>
    <router-link v-if="isManager()" to="/gestion">{{t('nav_manager')}}</router-link>
    <router-link v-if="isAdmin()" to="/admin-consola">{{t('nav_admin')}}</router-link>
  </nav>
  <div class="userbox">
    <template v-if="me.display_name">
      <div class="profile-menu" ref="menuRoot">
        <button class="avatar-btn" @click="open=!open" :aria-expanded="open" :title="me.display_name">
          <img v-if="me.avatar_blob" :src="me.avatar_blob" alt="" class="avatar-img"/>
          <span v-else class="avatar">{{initials}}</span>
        </button>
        <div v-if="open" class="dropdown">
          <div class="dd-head">
            <img v-if="me.avatar_blob" :src="me.avatar_blob" alt="" class="avatar-img lg"/>
            <span v-else class="avatar lg">{{initials}}</span>
            <span class="dd-id"><strong>{{me.display_name}}</strong><small>{{me.email || me.username}}</small></span>
          </div>
          <router-link to="/perfil" class="dd-item" @click="open=false">{{t('menu_profile')}}</router-link>
          <router-link to="/perfil#preferencias" class="dd-item" @click="open=false">{{t('menu_prefs')}}</router-link>
          <div class="dd-item dd-lang"><span>{{t('menu_language')}}</span>
            <span class="lang-switch"><button :class="{on: locale.lang==='es'}" @click="changeLang('es')">ES</button><button :class="{on: locale.lang==='en'}" @click="changeLang('en')">EN</button></span>
          </div>
          <button class="dd-item dd-logout" @click="logout">{{t('menu_logout')}}</button>
        </div>
      </div>
    </template>
    <router-link v-else to="/login" class="btn btn-sm">{{t('sign_in')}}</router-link>
  </div>
</div></header>
<main><router-view/></main>
<footer v-if="!bare" class="site">{{branding.footer_text}}<span v-if="branding.tagline"> · {{branding.tagline}}</span></footer>
</template>
<script setup>
import {computed, onMounted, onBeforeUnmount, ref, watch} from 'vue'; import {useRoute, useRouter} from 'vue-router'
import {branding, me, loadBranding, loadMe, isAdmin, isManager} from './services/branding'
import {locale, t, setLang} from './services/i18n'
import api from './services/api'
const route = useRoute(); const router = useRouter()
const open = ref(false); const menuRoot = ref(null)
function onDocClick(e){ if(open.value && menuRoot.value && !menuRoot.value.contains(e.target)) open.value=false }
onMounted(()=> document.addEventListener('click', onDocClick))
onBeforeUnmount(()=> document.removeEventListener('click', onDocClick))
watch(()=>route.fullPath, ()=>{ open.value=false })
async function changeLang(lang){ setLang(lang); try{ await api.patch('/auth/me/', {language: lang}) }catch{} }
const bare = computed(()=> route.name === 'certificado')
const initials = computed(()=> (me.display_name||'?').split(' ').filter(Boolean).slice(0,2).map(w=>w[0]).join('').toUpperCase())
function logout(){ localStorage.removeItem('access'); localStorage.removeItem('refresh'); location.href='/login' }
onMounted(()=>{ loadBranding(); loadMe() })
</script>
