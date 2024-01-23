import router from "./routers.js"
import Navbar from "./components/Navbar.js"
import Login from "./components/Login.js"

//router.beforeEach((to, from, next) => {
//    if (to.name !== 'Login' && !localStorage.getItem('auth-token') ? true : false) 
//        next({name:'Login'}) 
//    else next()
//  })

new Vue({
    el: "#app",
    template: `<div>
    <Navbar :key='changed'/>
    <router-view class="m-3" /> </div>`,
    router,
    components: {
        Navbar,
    },
    data: {
        changed:true,
    },
    watch: {
        $route(to, from) {
            this.changed = !this.changed
        },
    },
})