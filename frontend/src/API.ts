import { create } from 'apisauce';

let baseURL

if (process.env.NODE_ENV === 'development') {
  baseURL = 'http://localhost:8080'
} else if (process.env.NODE_ENV === 'development-docker' as string) {
  baseURL = 'http://localhost:8080'
}

export default create({
  baseURL
});