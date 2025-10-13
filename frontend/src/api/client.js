// src/api/client.js
import axios from 'axios';

// 创建一个Axios的实例
const apiClient = axios.create({
    // 预先配置好所有请求的基础URL
    baseURL: 'http://127.0.0.1:8000',

    // 预先配置好所有请求的通用请求头
    headers: {
        'Content-Type': 'application/json',
        // 如果以后需要API Key，也可以在这里统一添加
        // 'Authorization': 'Bearer YOUR_TOKEN' 
    },

    // 预先配置好所有请求的超时时间 (例如10秒)
    timeout: 10000
});

// 导出这个配置好的实例，以便其他文件可以使用
export default apiClient;