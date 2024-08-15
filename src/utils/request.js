import axios from 'axios'

axios.defaults.headers.post['Content-Type'] = 'application/json'; //设置默认提交 json
axios.defaults.withCredentials = true;
// axios.defaults.headers['TOKEN'] = sessionStorage.getItem("token");

let baseUrl = "";

switch (process.env.NODE_ENV) {
    case 'development':
        baseUrl = "http://localhost:8888"  //开发环境url
        break
    case 'production':
        baseUrl = "http://www.devdemo.club:18080"  //生产环境url
        break
    default:
        baseUrl = 'http://localhost:8888'
}

// 创建axios实例
const service = axios.create({
    baseURL:baseUrl, // api的base_url
    timeout: 300000 // 请求超时时间
})

// request拦截器
service.interceptors.request.use(config => {
    // config.headers.Token = sessionStorage.getItem("token");
    // console.log(config)
    return config
}, error => {
    console.log("error: ",error)
    Promise.reject(error)
})

// respone拦截器
service.interceptors.response.use(
    response => {
        const res = response.data
        if (response.status === 200) {
            return response.data
        } else {
            console.log('err:', res.message)
            return Promise.reject('error')
        }
    },
    error => {
        console.log('err' + error)
        return Promise.reject(error)
    }
)

export default service