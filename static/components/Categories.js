export default {
    template: `<div class="card" style="width: 18rem;">
    <div class="card-body">
      <h5 class="card-title">{{resource.category_name}}</h5>
      <h6 v-if="role=='admin'" class="card-subtitle mb-2 text-body-secondary">Creator- {{resource.creator}}</h6>
      <p> {{resource.category_descr}} </p>
      <a v-if="role=='storemanager'" href="#" class="btn btn-primary">Add Products</a>
      <a v-if="role=='storemanager'" href="#" class="btn btn-primary" @click='deleteCategory'>Delete </a>
      <button v-if="!resource.is_approved && role=='admin'" class="btn btn-success" @click='approveResource'> Approve </button>
      <button v-if="resource.to_delete && role=='admin'" class="btn btn-success" @click='deleteCategoryAdmin'> Approve Delete Request </button>
      <br><br>
      <button v-if="role=='storemanager' || role=='admin'" class="btn btn-primary" type="button" data-bs-toggle="collapse" data-bs-target="#collapseWidthExample" aria-expanded="false" aria-controls="collapseWidthExample"
       @click="editCategory" > Edit Category </button> 
    </div>
    
    </div>`,
    props: ['resource'],
    data(){
        return {
            resource : {
                category_name:null,
                category_descr:null,
            },
            role: localStorage.getItem('role'),
            authToken: localStorage.getItem('auth-token'),
        }
    },
    methods: {
        async approveResource() {
            const res = await fetch(`/category-resource/${this.resource.id}/approve`, {
                headers: {
                    'Authentication-Token' : this.authToken,
                },
            })
            const data = await res.json()
            if (res.ok) {
                alert(data.message)
                this.$router.go(0)
            }
            else{
                alert(data.message)
            }

        },
        async deleteCategory() {
            const res = await fetch (`category-resource/${this.resource.id}/category_delete`, {
                headers: {
                    'Authentication-Token' : this.authToken,
                },
            })
            const data = await res.json()
            if (res.ok) {
                alert(data.message)
                this.$router.go(0)
            }
            else{
                alert(data.message)
            }
        },
        async deleteCategoryAdmin() {
            const res = await fetch (`category-resource/${this.resource.id}/category_delete_admin`, {
                headers: {
                    'Authentication-Token' : this.authToken,
                },
            })
            const data = await res.json()
            if (res.ok) {
                alert(data.message)
                this.$router.go(0)
            }
            else{
                alert(data.message)
            }
        },
        editCategory() {
            this.$router.push({path:`${this.resource.id}/edit-Category`})
        },
    },
}