import request from '@/utils/request' // 引入封装的request.js文件

export async function exampleGet(params,data,headers) {
    return request({
        method: 'post',
        url: '/post',
        params,
        data,
        // headers
        // headers: {
        //     'Content-Type': 'application/x-www-form-urlencoded'
        //   },
    })
}


// 获取文件
export async function getfile(url){
    return request({
        method:'get',
        url:url,
        responseType:'arraybuffer'
    })
}
//登录
export async function login(data){
    return request({
        method:'post',
        url:'/login/',
        data
    })
}
//注册
export async function register(data){
    return request({
        method:'post',
        url:'/register/',
        data
    })
}
//新增项目
export async function builiProject(data){
    return request({
        method:'post',
        url:'/build_project/',
        data
    })
}
//获取项目
export async function getProjects(data){
    return request({
        method:'post',
        url:'/get_projects/',
        data
    })
}
//更新项目
export async function updateProject(data){
    return request({
        method:'post',
        url:'/update_project/',
        data
    })
}
//删除项目
export async function deleteProject(data){
    return request({
        method:'post',
        url:'/delete_project/',
        data
    })
}
//项目关联集合
export async function joinSets(data){
    return request({
        method:'post',
        url:'/join_sets/',
        data
    })
}

//新增集合
export async function buildSet(data){
    return request({
        method:'post',
        url:'/build_set/',
        data
    })
}
//获取集合
export async function getSets(data){
    return request({
        method:'post',
        url:'/get_sets/',
        data
    })
}
//更新集合
export async function updateSet(data){
    return request({
        method:'post',
        url:'/update_set/',
        data
    })
}
//删除集合
export async function deleteSet(data){
    return request({
        method:'post',
        url:'/delete_set/',
        data
    })
}
//分割预测
export async function segPredict(data){
    return request({
        method:'post',
        url:'/seg_predict/',
        data
    })
}
//三维重建
export async function build3D(data){
    return request({
        method:'post',
        url:'/build_3D/',
        data
    })
}
//获得标签
export async function getLabel(data){
    return request({
        method:'post',
        url:'/get_label/',
        data
    })
}
//获得标签
export async function exportLabel(data){
    return request({
        method:'post',
        url:'/export_label/',
        data
    })
}

//登出
export async function logout(data){
    return request({
        method:'post',
        url:'/logout/',
        data
    })
}

export async function getPostData(data){
    return request({
        method:'post',
        url:'http://127.0.0.1:8888/upload/',
        data
    })
}

