import { useState } from "react";
import { Link } from "react-router-dom";
import { createEmergency } from "../api/emergencies.js";
import Notice from "../components/Notice.jsx";
import PageHeader from "../components/PageHeader.jsx";
import { SEVERITY_LABELS, TYPE_LABELS } from "../utils/format.js";

const EMPTY = {
  caller_name: "", caller_phone: "", patient_name: "", patient_age: "", patient_gender: "",
  emergency_type: "", severity: "", location_address: "", latitude: "", longitude: "", description: "",
};

// Turn the form strings into the JSON the API expects (empty -> null, numbers -> numbers)
function toPayload(form) {
  const text = (v) => (v.trim() === "" ? null : v.trim());
  const num = (v) => (v.trim() === "" ? null : Number(v));
  return {
    caller_name: form.caller_name,
    caller_phone: form.caller_phone,
    patient_name: text(form.patient_name),
    patient_age: num(form.patient_age),
    patient_gender: form.patient_gender || null,
    emergency_type: form.emergency_type,
    severity: form.severity,
    location_address: form.location_address,
    latitude: num(form.latitude),
    longitude: num(form.longitude),
    description: text(form.description),
  };
}

function Field({ name, label, error, hint, children }) {
  return (
    <div className={`field ${error ? "has-error" : ""}`}>
      <label htmlFor={name}>{label}</label>
      {children}
      {hint && !error && <div className="hint">{hint}</div>}
      {error && <div className="field-error">{error}</div>}
    </div>
  );
}

export default function NewEmergency() {
  const [form, setForm] = useState(EMPTY);
  const [errors, setErrors] = useState({});
  const [formError, setFormError] = useState("");
  const [saved, setSaved] = useState(null);
  const [saving, setSaving] = useState(false);

  const set = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  // checks that run in the browser before anything is sent
  function validate() {
    const found = {};
    if (form.caller_name.trim().length < 2) found.caller_name = "Enter the caller's name.";
    if (!/^[0-9+\-\s()]{7,20}$/.test(form.caller_phone.trim())) found.caller_phone = "Enter a valid phone number.";
    if (!form.emergency_type) found.emergency_type = "Select the type of emergency.";
    if (!form.severity) found.severity = "Select a severity.";
    if (form.location_address.trim().length < 5) found.location_address = "Enter the pickup location.";
    if (form.patient_age !== "" && (Number(form.patient_age) < 0 || Number(form.patient_age) > 120))
      found.patient_age = "Age must be between 0 and 120.";
    const hasLat = form.latitude.trim() !== "";
    const hasLng = form.longitude.trim() !== "";
    if (hasLat !== hasLng) found.latitude = "Enter both latitude and longitude, or leave both empty.";
    return found;
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setSaved(null);
    setFormError("");
    const found = validate();
    setErrors(found);
    if (Object.keys(found).length) return;

    setSaving(true);
    try {
      const result = await createEmergency(toPayload(form));
      setSaved(result);
      setForm(EMPTY);
    } catch (err) {
      setErrors(err.fieldErrors || {});
      setFormError(err.message);
    } finally {
      setSaving(false);
    }
  }

  return (
    <>
      <PageHeader title="New emergency request" subtitle="The request is saved in the database with status Pending" />

      {saved && (
        <Notice kind="success">
          Request #{saved.id} saved. <Link to={`/emergencies/${saved.id}`}>Open request</Link>
          {" | "}
          <Link to="/">Go to dashboard</Link>
        </Notice>
      )}
      {formError && <Notice kind="error">{formError}</Notice>}

      <form className="panel form" onSubmit={handleSubmit} noValidate>
        <h2>Caller</h2>
        <div className="grid-2">
          <Field name="caller_name" label="Caller name" error={errors.caller_name}>
            <input id="caller_name" name="caller_name" value={form.caller_name} onChange={set} maxLength={100} />
          </Field>
          <Field name="caller_phone" label="Phone number" error={errors.caller_phone}>
            <input id="caller_phone" name="caller_phone" value={form.caller_phone} onChange={set} maxLength={20} />
          </Field>
        </div>

        <h2>Incident</h2>
        <div className="grid-2">
          <Field name="emergency_type" label="Type of emergency" error={errors.emergency_type}>
            <select id="emergency_type" name="emergency_type" value={form.emergency_type} onChange={set}>
              <option value="">Select type</option>
              {Object.entries(TYPE_LABELS).map(([k, v]) => <option key={k} value={k}>{v}</option>)}
            </select>
          </Field>
          <Field name="severity" label="Severity" error={errors.severity}
                 hint="Set by the dispatcher. Automatic severity classification is not built yet.">
            <select id="severity" name="severity" value={form.severity} onChange={set}>
              <option value="">Select severity</option>
              {Object.entries(SEVERITY_LABELS).map(([k, v]) => <option key={k} value={k}>{v}</option>)}
            </select>
          </Field>
        </div>
        <Field name="location_address" label="Pickup location" error={errors.location_address}>
          <input id="location_address" name="location_address" value={form.location_address} onChange={set} maxLength={255} />
        </Field>
        <div className="grid-2">
          <Field name="latitude" label="Latitude (optional)" error={errors.latitude}
                 hint="Map coordinates will be filled automatically once map integration is added.">
            <input id="latitude" name="latitude" type="number" step="any" value={form.latitude} onChange={set} />
          </Field>
          <Field name="longitude" label="Longitude (optional)" error={errors.longitude}>
            <input id="longitude" name="longitude" type="number" step="any" value={form.longitude} onChange={set} />
          </Field>
        </div>
        <Field name="description" label="Notes (optional)" error={errors.description}>
          <textarea id="description" name="description" rows={3} value={form.description} onChange={set} maxLength={1000} />
        </Field>

        <h2>Patient (optional)</h2>
        <p className="muted small">Use sample details only while demonstrating. Do not enter real patient information.</p>
        <div className="grid-3">
          <Field name="patient_name" label="Patient name" error={errors.patient_name}>
            <input id="patient_name" name="patient_name" value={form.patient_name} onChange={set} maxLength={100} />
          </Field>
          <Field name="patient_age" label="Age" error={errors.patient_age}>
            <input id="patient_age" name="patient_age" type="number" min="0" max="120" value={form.patient_age} onChange={set} />
          </Field>
          <Field name="patient_gender" label="Gender" error={errors.patient_gender}>
            <select id="patient_gender" name="patient_gender" value={form.patient_gender} onChange={set}>
              <option value="">Not stated</option>
              <option value="male">Male</option>
              <option value="female">Female</option>
              <option value="other">Other</option>
            </select>
          </Field>
        </div>

        <div className="form-actions">
          <button type="submit" className="btn btn-primary" disabled={saving}>
            {saving ? "Saving..." : "Save request"}
          </button>
          <button type="button" className="btn" onClick={() => { setForm(EMPTY); setErrors({}); setFormError(""); }}>
            Clear form
          </button>
        </div>
      </form>
    </>
  );
}
