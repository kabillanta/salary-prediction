import { motion } from "framer-motion";

export default function StepTwo({ formData, updateField, nextStep, prevStep }: any) {
  return (
    <motion.div
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: -20 }}
      transition={{ duration: 0.3 }}
    >
      <div className="step-header">
        <div className="step-title-group">
          <span className="step-number">02</span>
          <div className="step-titles">
            <h2>The Experience</h2>
            <p>How deep does your expertise run?</p>
          </div>
        </div>
        <div className="step-indicators">
          <div className="indicator inactive"></div>
          <div className="indicator active"></div>
          <div className="indicator inactive"></div>
        </div>
      </div>

      <div className="section">
        <div className="slider-group">
          <div className="slider-info">
            <div className="slider-labels">
              <h4>Years of Experience</h4>
              <p>Total professional experience</p>
            </div>
            <div className="slider-value">
              {formData.experience_years}<span>yrs</span>
            </div>
          </div>
          <input 
            type="range" 
            min="0" max="30" 
            className="custom-range"
            value={formData.experience_years}
            onChange={(e) => updateField("experience_years", parseInt(e.target.value))}
          />
          <div className="slider-limits">
            <span>0</span>
            <span>30</span>
          </div>
        </div>

        <div className="slider-group" style={{ marginTop: '3rem' }}>
          <div className="slider-info">
            <div className="slider-labels">
              <h4>Skills Count</h4>
              <p>Technical and soft skills combined</p>
            </div>
            <div className="slider-value">
              {formData.skills_count}
            </div>
          </div>
          <input 
            type="range" 
            min="1" max="40" 
            className="custom-range"
            value={formData.skills_count}
            onChange={(e) => updateField("skills_count", parseInt(e.target.value))}
          />
          <div className="slider-limits">
            <span>1</span>
            <span>40</span>
          </div>
        </div>

        <div className="slider-group" style={{ marginTop: '3rem' }}>
          <div className="slider-info">
            <div className="slider-labels">
              <h4>Certifications</h4>
              <p>Professional certifications held</p>
            </div>
            <div className="slider-value">
              {formData.certifications}
            </div>
          </div>
          <input 
            type="range" 
            min="0" max="15" 
            className="custom-range"
            value={formData.certifications}
            onChange={(e) => updateField("certifications", parseInt(e.target.value))}
          />
          <div className="slider-limits">
            <span>0</span>
            <span>15</span>
          </div>
        </div>
      </div>

      <div className="card-footer">
        <button className="nav-btn secondary" onClick={prevStep}>
          &larr; Back
        </button>
        <button className="nav-btn primary" onClick={nextStep}>
          Continue &rarr;
        </button>
      </div>
    </motion.div>
  );
}
