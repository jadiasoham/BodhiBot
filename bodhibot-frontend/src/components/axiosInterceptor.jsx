import axios from "axios";

const axiosService = axios.create();

axiosService.interceptors.request.use(
	(config) => {
		const token = localStorage.getItem('access_token');
		if (token) {
			config.headers['Authorization'] = `Bearer ${token}`;
		}
		return config
	},
	(error) => {
		return Promise.reject(error);
	}
);

axiosService.interceptors.response.use(
	(response) => response,
	(error) => {
		console.error(error);
		return Promise.reject(error);
	} 
);

export default axiosService;