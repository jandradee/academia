import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'; import Catalog from '../views/Catalog.vue'; import Login from '../views/Login.vue'; import CourseDetail from '../views/CourseDetail.vue'; import AdminConsole from '../views/AdminConsole.vue'; import ManagerConsole from '../views/ManagerConsole.vue'; import Certificates from '../views/Certificates.vue'; import CertificateView from '../views/CertificateView.vue'; import Profile from '../views/Profile.vue'
const routes=[{path:'/',component:Home},{path:'/catalogo',component:Catalog},{path:'/login',component:Login},{path:'/curso/:id',component:CourseDetail,props:true},{path:'/admin-consola',component:AdminConsole},{path:'/gestion',component:ManagerConsole},{path:'/certificados',component:Certificates},{path:'/certificado/:id',component:CertificateView,props:true,name:'certificado'},{path:'/perfil',component:Profile}]
const router=createRouter({history:createWebHistory(),routes})
// Sin sesión activa, todo va a la pantalla de login (y de vuelta al destino tras ingresar).
router.beforeEach((to)=>{
  const has=!!localStorage.getItem('access')
  if(to.path!=='/login' && !has) return {path:'/login', query:{next:to.fullPath}}
  if(to.path==='/login' && has) return {path:'/'}
  return true
})
export default router
