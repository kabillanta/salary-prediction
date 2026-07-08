import { useState } from "react";
import { motion } from "framer-motion";
import { Pen } from "lucide-react";
import { EDU_LEVELS, SIZES, LOCATIONS, WORK_MODES } from "../constants";

export default function StepThree({ formData, updateField, prevStep, submitForm, isLoading }: any) {
  const [customEdu, setCustomEdu] = useState(!EDU_LEVELS.includes(formData.education_level) && formData.education_level !== "");
  const [customLoc, setCustomLoc] = useState(!LOCATIONS.includes(formData.location) && formData.location !== "");

  return (
    <motion.div
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: -20 }}
      transition={{ duration: 0.3 }}
    >
      <div className="step-header">
        <div className="step-title-group">
          <span className="step-number">03</span>
          <div className="step-titles">
            <h2>The Environment</h2>
            <p>Where and how do you work?</p>
          </div>
        </div>
        <div className="step-indicators">
          <div className="indicator inactive"></div>
          <div className="indicator inactive"></div>
          <div className="indicator active"></div>
        </div>
      </div>

      <div className="section">
        <h3>EDUCATION LEVEL</h3>
        <div className="pill-grid">
          {EDU_LEVELS.map((edu) => (
            <button 
              key={edu} 
              type="button"
              className={`pill-btn ${formData.education_level === edu && !customEdu ? 'active' : ''}`}
              onClick={() => { setCustomEdu(false); updateField("education_level", edu); }}
            >
              {edu}
            </button>
          ))}
          {customEdu ? (
            <input
              type="text"
              className="pill-input"
              placeholder="Enter Education..."
              value={formData.education_level}
              onChange={(e) => updateField("education_level", e.target.value)}
              autoFocus
            />
          ) : (
            <button 
              type="button"
              className="pill-btn"
              onClick={() => { setCustomEdu(true); updateField("education_level", ""); }}
            >
              <Pen size={14} /> Other
            </button>
          )}
        </div>
      </div>

      <div className="section">
        <h3>COMPANY SIZE</h3>
        <div className="pill-grid">
          {SIZES.map((size) => (
            <button 
              key={size} 
              type="button"
              className={`pill-btn ${formData.company_size === size ? 'active' : ''}`}
              onClick={() => updateField("company_size", size)}
            >
              {size}
            </button>
          ))}
        </div>
      </div>

      <div className="section">
        <h3>LOCATION</h3>
        <div className="pill-grid">
          {LOCATIONS.map((loc) => (
            <button 
              key={loc} 
              type="button"
              className={`pill-btn ${formData.location === loc && !customLoc ? 'active' : ''}`}
              onClick={() => { setCustomLoc(false); updateField("location", loc); }}
            >
              {loc}
            </button>
          ))}
          {customLoc ? (
            <input
              type="text"
              className="pill-input"
              placeholder="Enter Location..."
              value={formData.location}
              onChange={(e) => updateField("location", e.target.value)}
              autoFocus
            />
          ) : (
            <button 
              type="button"
              className="pill-btn"
              onClick={() => { setCustomLoc(true); updateField("location", ""); }}
            >
              <Pen size={14} /> Other
            </button>
          )}
        </div>
      </div>

      <div className="section">
        <h3>WORK MODE</h3>
        <div className="pill-grid">
          {WORK_MODES.map((mode) => (
            <button 
              key={mode} 
              type="button"
              className={`pill-btn ${formData.remote_work === mode ? 'active' : ''}`}
              onClick={() => updateField("remote_work", mode)}
            >
              {mode}
            </button>
          ))}
        </div>
      </div>

      <div className="card-footer">
        <button className="nav-btn secondary" onClick={prevStep} disabled={isLoading}>
          &larr; Back
        </button>
        <button 
          className="nav-btn primary" 
          onClick={submitForm} 
          disabled={isLoading || !formData.education_level || !formData.company_size || !formData.location || !formData.remote_work}
        >
          {isLoading ? <div className="spinner"></div> : "Predict Salary \u2192"}
        </button>
      </div>
    </motion.div>
  );
}
