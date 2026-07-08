import { useState } from "react";
import { motion } from "framer-motion";
import { Pen } from "lucide-react";
import { JOB_TITLES, INDUSTRIES } from "../constants";

export default function StepOne({ formData, updateField, nextStep }: any) {
  const [customJob, setCustomJob] = useState(!JOB_TITLES.includes(formData.job_title) && formData.job_title !== "");
  const [customIndustry, setCustomIndustry] = useState(!INDUSTRIES.includes(formData.industry) && formData.industry !== "");

  return (
    <motion.div
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: -20 }}
      transition={{ duration: 0.3 }}
    >
      <div className="step-header">
        <div className="step-title-group">
          <span className="step-number">01</span>
          <div className="step-titles">
            <h2>The Role</h2>
            <p>What do you do?</p>
          </div>
        </div>
        <div className="step-indicators">
          <div className="indicator active"></div>
          <div className="indicator inactive"></div>
          <div className="indicator inactive"></div>
        </div>
      </div>

      <div className="section">
        <h3>JOB TITLE</h3>
        <div className="pill-grid">
          {JOB_TITLES.map((job) => (
            <button 
              key={job} 
              type="button"
              className={`pill-btn ${formData.job_title === job && !customJob ? 'active' : ''}`}
              onClick={() => { setCustomJob(false); updateField("job_title", job); }}
            >
              {job}
            </button>
          ))}
          {customJob ? (
            <input
              type="text"
              className="pill-input"
              placeholder="Enter Title..."
              value={formData.job_title}
              onChange={(e) => updateField("job_title", e.target.value)}
              autoFocus
            />
          ) : (
            <button 
              type="button"
              className="pill-btn"
              onClick={() => { setCustomJob(true); updateField("job_title", ""); }}
            >
              <Pen size={14} /> Other
            </button>
          )}
        </div>
      </div>

      <div className="section">
        <h3>INDUSTRY</h3>
        <div className="pill-grid">
          {INDUSTRIES.map((ind) => (
            <button 
              key={ind} 
              type="button"
              className={`pill-btn ${formData.industry === ind && !customIndustry ? 'active' : ''}`}
              onClick={() => { setCustomIndustry(false); updateField("industry", ind); }}
            >
              {ind}
            </button>
          ))}
          {customIndustry ? (
            <input
              type="text"
              className="pill-input"
              placeholder="Enter Industry..."
              value={formData.industry}
              onChange={(e) => updateField("industry", e.target.value)}
              autoFocus
            />
          ) : (
            <button 
              type="button"
              className="pill-btn"
              onClick={() => { setCustomIndustry(true); updateField("industry", ""); }}
            >
              <Pen size={14} /> Other
            </button>
          )}
        </div>
      </div>

      <div className="card-footer" style={{ justifyContent: 'flex-end' }}>
        <button className="nav-btn primary" onClick={nextStep} disabled={!formData.job_title || !formData.industry}>
          Continue &rarr;
        </button>
      </div>
    </motion.div>
  );
}
