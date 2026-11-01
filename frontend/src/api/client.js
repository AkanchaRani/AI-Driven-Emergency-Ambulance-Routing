// One place that knows how to talk to the FastAPI backend.
const BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export class ApiError extends Error {
  constructor(message, status, fieldErrors = {}) {
    super(message);
    this.status = status;
    this.fieldErrors = fieldErrors; // { fieldName: "message" } for 422 responses
  }
}

// FastAPI sends 422 errors as a list: [{ loc: ["body","caller_phone"], msg: "..." }]
function readDetail(detail) {
  if (typeof detail === "string") return { message: detail, fieldErrors: {} };
  if (Array.isArray(detail)) {
    const fieldErrors = {};
    detail.forEach((d) => {
      const field = d.loc?.[d.loc.length - 1];
      if (field && field !== "body") fieldErrors[field] = d.msg.replace(/^Value error, /, "");
    });
    return { message: "Some fields need to be corrected.", fieldErrors };
  }
  return { message: "Request failed.", fieldErrors: {} };
}

export async function request(path, options = {}) {
  let response;
  try {
    response = await fetch(`${BASE_URL}${path}`, {
      headers: { "Content-Type": "application/json" },
      ...options,
    });
  } catch {
    throw new ApiError(
      `Cannot reach the backend at ${BASE_URL}. Check that FastAPI is running.`,
      0
    );
  }

  if (!response.ok) {
    let body = {};
    try {
      body = await response.json();
    } catch {
      /* response was not JSON */
    }
    const { message, fieldErrors } = readDetail(body.detail);
    throw new ApiError(message, response.status, fieldErrors);
  }
  return response.json();
}
