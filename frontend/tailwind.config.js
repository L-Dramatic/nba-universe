/** @type {import('tailwindcss').Config} */
import defaultTheme from 'tailwindcss/defaultTheme' // 导入默认主题

export default {
    content: [
        "./index.html",
        "./src/**/*.{vue,js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            fontFamily: {
                // 将'sans'字体族设置为Inter，并提供备用字体
                sans: ['Inter', ...defaultTheme.fontFamily.sans],
            },
            colors: {
                // 定义品牌颜色
                'brand-blue': '#1D4ED8',
                'brand-red': '#BE123C',
            }
        },
    },
    plugins: [],
}