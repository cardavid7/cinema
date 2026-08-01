export interface User {
  id: number;
  username: string;
  email: string;
  is_active: boolean;
}

export interface AuthCredentials {
  email: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}
