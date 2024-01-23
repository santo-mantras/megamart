export default {
    template: `
  <div class='d-flex justify-content-center' style="margin-top:10vh">
        <div class="mb-3 p-5 bg-light">
            <label for="user-email" class="form-label">Email address</label>
            <input type="email" class="form-control" id="user-email" v-model="cred.email">
            <label for="user-password" class="form-label">Password</label>
            <input type="password" class="form-control" id="user-password" v-model="cred.password">
            <button class="btn btn-primary mt-3" @click='login'>Login</button>
            <div class='text-danger'>*{{error}}</div>
        </div>
    </div>
  `,
    data() {
        return {
            cred: {
                email: null,
                password: null,
            },
            error: null,
        }
    },

    methods: {
        async login(){
            const res = await fetch('/user-login', {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json',
                },
                body: JSON.stringify(this.cred),
            })
            const data = await res.json()
            if (res.ok) { 
                localStorage.setItem('auth-token', data.token)
                localStorage.setItem('role', data.role)
                this.$router.push({ path: '/' })
            } else {
                this.error = data.message
            }
        },
    },
}