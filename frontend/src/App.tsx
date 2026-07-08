import { useState } from 'react';
import { AnimatePresence } from 'framer-motion';
import StepOne from './components/StepOne';
import StepTwo from './components/StepTwo';
import StepThree from './components/StepThree';
import ResultStep from './components/ResultStep';
import { JOB_TITLES, INDUSTRIES, EDU_LEVELS, SIZES, LOCATIONS, WORK_MODES } from './constants';
import './App.css';

function App() {
  const [step, setStep] = useState(1);
  const [predictedSalary, setPredictedSalary] = useState<number | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [formData, setFormData] = useState({
    job_title: "",
    education_level: "",
    industry: "",
    company_size: "",
    location: "",
    remote_work: "",
    experience_years: 5,
    skills_count: 10,
    certifications: 2
  });

  const updateField = (field: string, value: any) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const submitForm = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const isCustomJob = !JOB_TITLES.includes(formData.job_title);
      const isCustomInd = !INDUSTRIES.includes(formData.industry);
      const isCustomEdu = !EDU_LEVELS.includes(formData.education_level);
      const isCustomSize = !SIZES.includes(formData.company_size);
      const isCustomLoc = !LOCATIONS.includes(formData.location);
      const isCustomMode = !WORK_MODES.includes(formData.remote_work);
      
      const hasCustomFields = isCustomJob || isCustomInd || isCustomEdu || isCustomSize || isCustomLoc || isCustomMode;

      const endpoint = hasCustomFields ? 'http://127.0.0.1:8000/predict_gemini' : 'http://127.0.0.1:8000/predict';

      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        throw new Error(`Failed to fetch prediction from ${hasCustomFields ? 'Gemini API' : 'ML Model'}. Ensure backend is running.`);
      }

      const data = await response.json();
      setPredictedSalary(data.predicted_salary);
      setStep(4); // Move to results step
    } catch (err: any) {
      setError(err.message || 'An unexpected error occurred');
      setStep(4);
    } finally {
      setIsLoading(false);
    }
  };

  const nextStep = () => setStep(s => Math.min(s + 1, 3));
  const prevStep = () => setStep(s => Math.max(s - 1, 1));
  const resetFlow = () => {
    setPredictedSalary(null);
    setError(null);
    setStep(1);
  };

  return (
    <div className="app-container">
      <div className="header">
        <div className="eyebrow">Salary Intelligence</div>
        <h1>Know your worth.</h1>
      </div>

      <div className="wizard-card">
        <AnimatePresence mode="wait">
          {step === 1 && (
            <StepOne 
              key="step1"
              formData={formData} 
              updateField={updateField} 
              nextStep={nextStep} 
            />
          )}
          {step === 2 && (
            <StepTwo 
              key="step2"
              formData={formData} 
              updateField={updateField} 
              nextStep={nextStep} 
              prevStep={prevStep}
            />
          )}
          {step === 3 && (
            <StepThree 
              key="step3"
              formData={formData} 
              updateField={updateField} 
              prevStep={prevStep} 
              submitForm={submitForm}
              isLoading={isLoading}
            />
          )}
          {step === 4 && (
            <ResultStep 
              key="result"
              salary={predictedSalary}
              error={error}
              resetFlow={resetFlow}
            />
          )}
        </AnimatePresence>
      </div>

      {step < 4 && (
        <div className="global-footer">
          STEP {step} OF 3
        </div>
      )}
    </div>
  );
}

export default App;
