import { reactive } from 'vue'
import api from './api'
import { BRAND } from '../config/brand'

/**
 * Estado de marca en tiempo de ejecución.
 * Los valores iniciales salen de src/config/brand.js (marca de fábrica);
 * si el servidor tiene personalización guardada (consola de
 * Administración → Personalización), GET /branding/ los sobrescribe.
 */
export const branding = reactive({
  company_name: BRAND.companyName,
  platform_name: BRAND.platformName,
  tagline: BRAND.tagline,
  primary_color: BRAND.primaryColor,
  accent_color: BRAND.accentColor,
  beige_color: BRAND.neutralColor,
  danger_color: BRAND.dangerColor,
  logo: BRAND.logoUrl,
  footer_text: BRAND.footerText,
})
export async function loadBranding(){
  try{ const {data}=await api.get('/branding/'); Object.assign(branding,data); applyTheme() }catch{ applyTheme() }
}
export function applyTheme(){
  const r=document.documentElement.style
  r.setProperty('--azul', branding.primary_color); r.setProperty('--amarillo', branding.accent_color); r.setProperty('--beige', branding.beige_color); r.setProperty('--rojo', branding.danger_color)
  document.title = branding.company_name ? `${branding.platform_name} · ${branding.company_name}` : branding.platform_name
}
export const me = reactive({ loaded:false, is_superuser:false, role_codes:[], display_name:'', username:'', email:'', avatar_url:'', avatar_blob:'', language:'es', email_notifications:true })
export async function loadMe(){
  if(!localStorage.getItem('access')){ me.loaded=true; return }
  try{
    const {data}=await api.get('/auth/me/'); Object.assign(me,data)
    if(data.language){ const { setLang } = await import('./i18n'); setLang(data.language) }
    if(data.avatar_url){
      try{
        const resp = await api.get(data.avatar_url, { responseType:'blob' })
        if(me.avatar_blob) URL.revokeObjectURL(me.avatar_blob)
        me.avatar_blob = URL.createObjectURL(resp.data)
      }catch{ me.avatar_blob='' }
    } else { me.avatar_blob='' }
    me.loaded=true
  }catch{ me.loaded=true }
}
export const isAdmin = () => me.is_superuser || me.role_codes.includes('ADMIN')
export const isManager = () => isAdmin() || me.role_codes.includes('GESTOR')
