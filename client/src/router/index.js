import Vue from 'vue'
import VueRouter from 'vue-router'
import MainView from "@/views/MainView";
import LoginView from "@/views/LoginView";
import RegisterView from "@/views/RegisterView";
import BookingFunction from "@/components/BookingFunction";
import ManageView from "@/views/ManageView";
import RoomManagement from "@/components/RoomManagement";
import UserManagement from "@/components/UserManagement";
import BookingManagement from "@/components/BookingManagement";
import PaymentView from "@/views/PaymentView";
import ProfileFunction from "@/components/ProfileFunction";
import ChangePasswordFunction from "@/components/ChangePasswordFunction";
import ChangePasswordView from "@/views/ChangePasswordView";
import SearchOrderFunction from "@/components/SearchOrderFunction";
import UserInfoFunction from "@/components/UserInfoFunction";

Vue.use(VueRouter)

const routes = [
    {
        path: '/',
        name: 'MainView',
        component: MainView,
        children: [
            {path: 'profile', component: ProfileFunction},
            {path: 'booking', component: BookingFunction},
            {path: 'change-password', component: ChangePasswordFunction},
            {path: 'searchorder', component: SearchOrderFunction},
            {path: 'userinfo', component: UserInfoFunction}
            // {path: 'remark', redirect: 'booking'}
        ]
    },
    {
        path: '/login',
        name: 'LoginView',
        component: LoginView
    },
    {
        path: '/register',
        name: 'RegisterView',
        component: RegisterView
    },
    {
        path: '/manage',
        name: 'ManageView',
        component: ManageView,
        children: [
            {path: 'room', component: RoomManagement},
            {path: 'user', component: UserManagement},
            {path: 'booking', component: BookingManagement},
        ]
    },
    {
        path: '/payment',
        name: 'PaymentView',
        component: PaymentView
    },
    {
        path: '/change_pwd',
        name: 'ChangePasswordView',
        component: ChangePasswordView
    }

]

const router = new VueRouter({
    mode: 'history',

    routes
})

export default router
