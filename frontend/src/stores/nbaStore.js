// src/stores/nbaStore.js
import { defineStore } from 'pinia';
import apiClient from '@/api/client.js'; 

export const useNbaStore = defineStore('nba', {
    /**
     * State: 定义我们仓库中需要管理的所有数据。
     * 把它们想象成组件中的 `ref` 或 `reactive` 对象。
     */
    state: () => ({
        // 用于搜索结果
        teams: [],
        players: [],

        // 用于缓存详情页数据，避免重复请求
        // key是唯一的标识符（如 teamName 或 playerId），value是获取到的数据
        teamDetails: {},
        playerDetails: {},

        // 用于赛程页和榜单页
        schedule: [],
        leaders: {}, // key是类别(e.g., 'points'), value是榜单数组

        // 全局状态
        isLoading: false, // 全局加载状态，方便任何组件显示加载动画
        error: null,      // 全局错误信息
    }),

    /**
     * Getters: 类似于state的计算属性 (computed properties)。
     * 用于从state派生出一些新的状态，或者进行一些数据的查找。
     */
    getters: {
        // 示例：通过ID从已加载的球队列表中查找球队
        getTeamById: (state) => (teamId) => {
            return state.teams.find((team) => team.id === teamId);
        },
    },

    /**
     * Actions: 定义所有的数据获取和业务逻辑。
     * 这里是所有异步操作和修改state的地方。
     */
    actions: {
        // 这是一个内部使用的辅助函数，用于统一处理错误
        _handleApiError(message, err) {
            this.error = message;
            console.error(`${message}:`, err);
        },

        /**
         * 根据查询词搜索球队和球员
         * @param {string} query - 搜索关键词
         */
        async searchAll(query) {
            if (query.length < 3) {
                this.teams = [];
                this.players = [];
                return;
            }
            this.isLoading = true;
            this.error = null;
            try {
                const response = await apiClient.get('/search', { params: { query } });
                this.teams = response.data.teams;
                this.players = response.data.players;
            } catch (err) {
                this._handleApiError(`Search failed for query "${query}"`, err);
                this.teams = [];
                this.players = [];
            } finally {
                this.isLoading = false;
            }
        },

        /**
         * 获取并缓存球队的详细信息
         * @param {string} teamName - 球队名称
         */
        async fetchTeamDetails(teamName) {
            // 如果缓存中已有，则直接从缓存返回，避免重复API调用
            if (this.teamDetails[teamName]) {
                console.log('Fetching team details from cache:', teamName);
                return this.teamDetails[teamName];
            }

            this.isLoading = true;
            this.error = null;
            try {
                const response = await apiClient.get(`/team-details/${teamName}`);
                // 请求成功后，将结果存入state中的缓存对象
                this.teamDetails[teamName] = response.data;
                return response.data;
            } catch (err) {
                this._handleApiError(`Failed to fetch details for team ${teamName}`, err);
                return null; // 返回null表示失败
            } finally {
                this.isLoading = false;
            }
        },

        // In frontend/src/stores/nbaStore.js, inside actions object

        async fetchPlayerDetails(playerId, season) { // 移除 season 的默认值
            // 缓存键现在只跟playerId有关，因为后端一次返回所有信息
            // 但为了在切换赛季时能重新获取数据，我们暂时禁用这个缓存或使其更智能
            // 一个简单的解决方法是每次都重新请求，后端有自己的缓存

            this.isLoading = true;
            this.error = null;
            try {
                const params = {};
                if (season) {
                    params.season = season;
                }
                // 关键改动：将 season 作为查询参数传递
                const response = await apiClient.get(`/player-details/${playerId}`, { params });

                // 我们不再在Pinia中做缓存，让组件自己管理数据
                return response.data;
            } catch (err) {
                this._handleApiError(`Failed to fetch details for player ${playerId}`, err);
                return null;
            } finally {
                this.isLoading = false;
            }
        },

        /**
         * 获取指定日期的赛程
         * @param {string} date - 日期 (YYYY-MM-DD)
         */
        async fetchSchedule(date) {
            this.isLoading = true;
            this.error = null;
            try {
                const response = await apiClient.get(`/schedule/${date}`);
                this.schedule = response.data;
            } catch (err) {
                this._handleApiError(`Failed to fetch schedule for date ${date}`, err);
                this.schedule = [];
            } finally {
                this.isLoading = false;
            }
        },

        /**
         * 获取并缓存联盟球员榜单
         * @param {string} category - 榜单类别 (points, rebounds, etc.)
         */
        async fetchLeaders(category) {
            if (this.leaders[category]) {
                return this.leaders[category];
            }
            this.isLoading = true;
            this.error = null;
            try {
                const response = await apiClient.get(`/leaders/${category}`);
                this.leaders[category] = response.data;
                return response.data;
            } catch (err) {
                this._handleApiError(`Failed to fetch leaders for category ${category}`, err);
                return null;
            } finally {
                this.isLoading = false;
            }
        },
    },
});