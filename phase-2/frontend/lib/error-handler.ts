// Generic error handler for frontend operations
export class ErrorHandler {
  static handle(error: any, context: string = 'Operation'): Error {
    console.error(`${context} failed:`, error);

    // Handle network errors
    if (!error.response) {
      return new Error(`${context} failed: Network error or server is unreachable`);
    }

    // Handle HTTP status codes
    const status = error.response.status;
    const message = error.response.data?.detail || error.message;

    switch (status) {
      case 400:
        return new Error(`${context} failed: Invalid request (${message})`);
      case 401:
        return new Error(`${context} failed: Unauthorized. Please log in.`);
      case 403:
        return new Error(`${context} failed: Access denied. Insufficient permissions.`);
      case 404:
        return new Error(`${context} failed: Resource not found.`);
      case 409:
        return new Error(`${context} failed: Conflict (${message})`);
      case 500:
        return new Error(`${context} failed: Server error. Please try again later.`);
      default:
        return new Error(`${context} failed: ${message || 'Unknown error occurred'}`);
    }
  }
}

// Specific error handlers
export const handleAuthError = (error: any): Error => {
  return ErrorHandler.handle(error, 'Authentication');
};

export const handleTaskError = (error: any): Error => {
  return ErrorHandler.handle(error, 'Task operation');
};