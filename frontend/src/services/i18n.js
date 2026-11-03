import { reactive } from 'vue'

/**
 * i18n mínimo: cubre el chrome de la app (encabezado, menú de perfil)
 * y la vista «Mi perfil». La preferencia vive en localStorage y en el
 * servidor (campo language del usuario, vía PATCH /auth/me/).
 */
const STRINGS = {
  es: {
    nav_home: 'Inicio', nav_catalog: 'Catálogo', nav_my: 'Mis cursos', nav_certs: 'Certificados',
    nav_manager: 'Gestión', nav_admin: 'Administración', sign_in: 'Ingresar',
    menu_profile: 'Mi perfil', menu_prefs: 'Preferencias', menu_language: 'Idioma',
    menu_logout: 'Cerrar sesión',
    profile_title: 'Mi perfil', profile_sub: 'Tu foto, tus datos y tus preferencias.',
    photo: 'Foto de perfil', photo_change: 'Cambiar foto', photo_upload: 'Subir foto', photo_remove: 'Quitar foto',
    photo_hint: 'Imagen de hasta 5 MB. Si no tienes foto, se muestran tus iniciales.',
    data: 'Datos personales', full_name: 'Nombre visible', department: 'Departamento',
    job_title: 'Puesto', office: 'Ubicación / oficina', username: 'Usuario', email: 'Correo',
    prefs: 'Preferencias', language: 'Idioma de la plataforma', notifications: 'Avisos por correo',
    notifications_hint: 'Recordatorios de cursos asignados y vencimientos.',
    save: 'Guardar cambios', saved: 'Cambios guardados.', saving: 'Guardando…',
    member_roles: 'Roles',
  },
  en: {
    nav_home: 'Home', nav_catalog: 'Catalog', nav_my: 'My courses', nav_certs: 'Certificates',
    nav_manager: 'Management', nav_admin: 'Administration', sign_in: 'Sign in',
    menu_profile: 'My profile', menu_prefs: 'Preferences', menu_language: 'Language',
    menu_logout: 'Sign out',
    profile_title: 'My profile', profile_sub: 'Your photo, your details and your preferences.',
    photo: 'Profile photo', photo_change: 'Change photo', photo_upload: 'Upload photo', photo_remove: 'Remove photo',
    photo_hint: 'Image up to 5 MB. Without a photo, your initials are shown.',
    data: 'Personal details', full_name: 'Display name', department: 'Department',
    job_title: 'Job title', office: 'Office location', username: 'Username', email: 'Email',
    prefs: 'Preferences', language: 'Platform language', notifications: 'Email notifications',
    notifications_hint: 'Reminders for assigned courses and due dates.',
    save: 'Save changes', saved: 'Changes saved.', saving: 'Saving…',
    member_roles: 'Roles',
  },
}

export const locale = reactive({ lang: localStorage.getItem('lang') || 'es' })
export function t(key){ return (STRINGS[locale.lang] || STRINGS.es)[key] || STRINGS.es[key] || key }
export function setLang(lang){
  locale.lang = (lang === 'en' ? 'en' : 'es')
  localStorage.setItem('lang', locale.lang)
}
