export default {
    template: `<div>
    <div v-for="(category__temp, index) in allUsers">
    <div v-if="error"> {{error}} </div> 
    <div class="card" style="width: 18rem;">
        <div class="card-body">
            <h5 class="card-title">{{category__temp.category_name}}</h5>
            <br>
            <p>{{category__temp.category_descr}}</p>
            <br>
            <p>Raised by - {{category__temp.creator_id}}</p>
            <p>Raised by - {{category__temp.creator}}</p>
            <button class="btn btn-success" @click='approveEditRequest'> Approve Edit Request </button> 
            <br><br>
            <button class="btn btn-warning" @click='rejectEditRequest'> Reject Edit Request </button>        
        </div>    
    </div>
    </div>
    </div>
    </div>`,
    data() {
        return {
            allUsers: [],
            resource : {
                cat_id: this.$route.params.cat_id,
            },
            token: localStorage.getItem('auth-token'),
            error:null,
        }
    },
    methods: {
        async approveEditRequest(){
            const res = await fetch(`category-resource/${this.resource.cat_id}/approve-edit`, {
                headers: {
                    'Authentication-Token' : this.token,
                },
            })
            const data = await res.json()
            if (res.ok){
                alert(data.message)
                this.$router.go(0)
            }
        },
        async rejectEditRequest(){
            const res = await fetch(`category-resource/${this.resource.cat_id}/reject-edit`, {
                method: 'POST', 
                headers: {
                    'Authentication-Token': this.token,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(this.resource),
            })
            const data = await res.json()
            if (res.ok){
                alert(data.message)
                this.$router.go(0)
            }
        },
    }, 
    async mounted() {
        const res = await fetch('/editrequest', {
            headers: {
                'Authentication-Token': this.token,
            },
        }) 
        const data = await res.json().catch((e)=> {})
        if (res.ok) { 
            this.allUsers = data
        }
        else{
            this.error = res.status
        } 
    },  
}