import axios from 'axios'
const api = axios.create({ baseURL: import.meta.env.VITE_API_BASE_URL || '/api' })
api.interceptors.request.use(c=>{ const t=localStorage.getItem('access'); if(t) c.headers.Authorization='Bearer '+t; return c })
let refreshing=null
api.interceptors.response.use(r=>r, async (error)=>{
  const cfg=error.config||{}
  const isAuthCall=(cfg.url||'').includes('/auth/token')
  if(error.response && error.response.status===401 && !cfg._retry && !isAuthCall){
    const refresh=localStorage.getItem('refresh')
    if(refresh){
      cfg._retry=true
      try{
        refreshing=refreshing||axios.post((import.meta.env.VITE_API_BASE_URL || '/api')+'/auth/token/refresh/',{refresh}).finally(()=>{ refreshing=null })
        const {data}=await refreshing
        localStorage.setItem('access',data.access); if(data.refresh) localStorage.setItem('refresh',data.refresh)
        cfg.headers=cfg.headers||{}; cfg.headers.Authorization='Bearer '+data.access
        return api(cfg)
      }catch{ /* la sesión ya no es válida: se fuerza el login abajo */ }
    }
    localStorage.removeItem('access'); localStorage.removeItem('refresh')
    if(location.pathname!=='/login') location.href='/login?next='+encodeURIComponent(location.pathname+location.search)
  }
  return Promise.reject(error)
})
export default api
