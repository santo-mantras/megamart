import CustomerHome from "./CustomerHome.js"
import StoreManagerHome from "./StoreManagerHome.js"
import AdminHome from "./AdminHome.js"
import Categories from "./Categories.js"
import registration from "./registration.js"

export default {
    template:`<div>
    <CustomerHome v-if="userRole=='customer'"/>
    <AdminHome v-if="userRole=='admin'" />
    <StoreManagerHome v-if="userRole=='storemanager'" />
    <Categories v-for="(resource, index) in resources" :key='index' :resource = "resource" />
    
    </div>`,

    data() {
        return {
            userRole: localStorage.getItem('role'),
            authToken: localStorage.getItem('auth-token'),
            resources: [],
        }
    },

    components: {
        CustomerHome,
        StoreManagerHome,
        AdminHome,
        Categories,
        //registration <registration v-if="authToken=='false'" />,

    },
    async mounted() {
        const res = await fetch('/api/category_section', {
          headers: {
            'Authentication-Token': this.authToken,
          },
        })
        const data = await res.json()
        if (res.ok) {
          this.resources = data
        } else {
          alert(data.message)
        }
    },        
}