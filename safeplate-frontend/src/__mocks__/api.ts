const mockApi = {
  get: jest.fn(),
  post: jest.fn(),
  put: jest.fn(),
  delete: jest.fn(),
  defaults: {
    baseURL: 'http://127.0.0.1:8000',
    headers: { 'Content-Type': 'application/json' },
    withCredentials: true
  },
  interceptors: {
    request: { use: jest.fn(), handlers: [] },
    response: { use: jest.fn(), handlers: [] }
  }
};

export default mockApi;