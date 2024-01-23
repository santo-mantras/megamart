export default {
    template: `<div> 
    <input type ="text" placeholder="category_name" v-model="resource.category_name" />
    <input type ="text" placeholder="category_descr" v-model="resource.category_descr" />
    <button @click="createResource"> Create Category </button>  
    </div>`,

    data() {
        return {
            resource : {
                category_name:null,
                category_descr:null,
            },
            token: localStorage.getItem('auth-token'),
        }
    },
    methods: {
      async createResource() {
          const res = await fetch ('/api/category_section', {
            method: 'POST', 
            headers: {
              'Authentication-Token': this.token,
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(this.resource),
          })
          const data = await res.json()
          console.log(data)
          if (res.ok) {
            alert(data.message)
            this.$router.go(0)
          }
      },
    },       
}