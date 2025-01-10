import { create } from 'apisauce';

let baseURL

if (process.env.NODE_ENV === 'development') {
  baseURL = 'http://localhost:4000'
} else if (process.env.NODE_ENV === 'development-docker' as string) {
  baseURL = 'http://codeminer42_test_api:4000'
}

export default create({
  baseURL
});