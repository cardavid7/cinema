export type MovieFormat = '2D' | '2D_SUB' | '3D' | '3D_SUB';

export interface Movie {
  id: number;
  title: string;
  description: string;
  duration: number;
  format: MovieFormat;
}

export interface MovieCreate {
  title: string;
  description: string;
  duration: number;
  format: MovieFormat;
}

export type MovieUpdate = Partial<MovieCreate>;
