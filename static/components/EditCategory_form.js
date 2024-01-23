export default {
    template: `<div> 
    <h3> Enter New Category Details </h3>
    <form name='Category-Edit'>
    <input type ="text" name="category_name" placeholder="category_name" v-model="resource.category_name" />
    <input type ="text" name="category_descr" placeholder="category_descr" v-model="resource.category_descr" />
    <br> <br>
    <button class="btn btn-primary" @click="updateCategory"> Update Category </button>  
    </form>
    </div>`,

    data() {
        return {
            resource : {
                id: this.$route.params.id,
                category_name:null,
                category_descr:null,
            },
            token: localStorage.getItem('auth-token'),
        }
    },
    methods: {
        async updateCategory() {
            //const res = await fetch(`/api/${this.resource.id}/editCategory`, {
            const res = await fetch('/api/editCategory', {
            //const res = await fetch(`/category-resource/${this.resource.id}/editedCategory`, {  
              method: 'POST', 
              headers: {
                'Authentication-Token': this.token,
                'Content-Type': 'application/json',
              },
              body: JSON.stringify(this.resource),
            })
            const data = await res.json()
            if (res.ok) {
              alert(data.message)
              this.$router.go(-1)
            }
            else{
              alert(data.message)
              this.$router.go(-1)
          }
        },
    },       
}