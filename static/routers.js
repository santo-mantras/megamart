import Home from "./components/Home.js"
import Login from "./components/Login.js"
import Users from "./components/Users.js"
import Category_form from "./components/Category_form.js"
import registration from "./components/registration.js"
import Category_update from "./components/EditCategory_form.js"
import EditSection from "./components/EditSection.js"

const routes = [
    { path: '/', component: Home, name: 'Home' },
    { path: '/login', component: Login, name: 'Login' },
    { path: '/users', component: Users },
    { path: '/create-category', component: Category_form },
    { path: '/user-signup', component: registration, name: 'registration' },
    { path: '/:id/edit-Category', component: Category_update },
    { path: '/edited-category', component: EditSection},
]

export default new VueRouter({
    routes,
})