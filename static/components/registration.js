export default {
  template: `<div>
  <div class="container">
    <div class="jumbotron">
      <h2 class="display-6">New User Registration</h2>
    </div>
  </div>
  <div class='d-flex justify-content-center' style="margin-top:10vh">
    <div class="mb-3 p-5 bg-light">
      <p>Fields marked with * are mandatory </p>
      <label for="user-email" class="form-label">*Email address</label>
      <input type="email" class="form-control" id="user-email" v-model="cred.email" required>
      <label for="user-username" class="form-label">*Username</label>
      <input type="username" class="form-control" id="user-username" v-model="cred.username" required >
      <label for="user-password" class="form-label">*Password</label>
      <input type="password" class="form-control" id="user-password" v-model="cred.password" required >
      <div class="mb-3 row">
        <label for="user-roles" class="form-label">*Role</label>
        <div class="col-sm-5">
          <select class="form-select" id="user-roles" v-model="cred.roles">     
            <option value="storemanager">Store Manager</option>
            <option value="customer">Customer</option>
          </select>
        </div> <br>
      </div> <br>
      <button class="btn btn-primary mt-3" @click='create_user'>Register</button>
      <button class="btn btn-primary mt-3" @click='back'>Login Page</button>
    </div>
  </div>

  </div>`,

  data() {
    return {
        cred: {
            email: null,
            username: null,
            password: null,
            roles: null,
        },
        error: null,
    }
  },
  methods:{
  /*  
    create_user(){
      console.log(this.cred)
    },
     
  */ 
    async create_user(){
      const res = await fetch ('/api/user_signup', {
        method: 'POST', 
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(this.cred),
      })
      const data = await res.json()
      if (res.ok) {
        alert(data.message)
        this.$router.go(0)
      }
    },
    back(){
      this.$router.push({path:'/login'})
    },
    
  },
}
