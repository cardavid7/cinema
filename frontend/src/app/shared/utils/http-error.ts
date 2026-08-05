import { HttpErrorResponse } from '@angular/common/http';

export function extractErrorMessage(err: unknown, fallback: string): string {
  if (err instanceof HttpErrorResponse) {
    if (err.status === 0) {
      return 'No se pudo conectar con el servidor.';
    }
    const detail = err.error?.detail;
    if (typeof detail === 'string') {
      return detail;
    }
  }
  return fallback;
}
