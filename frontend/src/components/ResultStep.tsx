import { useEffect, useState } from "react";
import { motion, useSpring } from "framer-motion";

export default function ResultStep({ salary, error, resetFlow }: any) {
  const [displayValue, setDisplayValue] = useState(0);
  
  const springValue = useSpring(0, {
    bounce: 0,
    duration: 2000,
  });

  useEffect(() => {
    if (salary) springValue.set(salary);
  }, [salary, springValue]);

  useEffect(() => {
    return springValue.on("change", (v) => {
      setDisplayValue(Math.round(v));
    });
  }, [springValue]);

  const formattedSalary = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    maximumFractionDigits: 0,
  }).format(displayValue);

  if (error) {
    return (
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        style={{ textAlign: 'center', padding: '3rem 1rem' }}
      >
        <h2 style={{ color: '#ff4d4f', marginBottom: '1rem' }}>Something went wrong.</h2>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '3rem' }}>{error}</p>
        <button className="nav-btn secondary" onClick={resetFlow} style={{ margin: '0 auto' }}>
          &larr; Try Again
        </button>
      </motion.div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      style={{ textAlign: 'center', padding: '4rem 1rem' }}
    >
      <motion.h2 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        style={{ fontSize: '1.25rem', color: 'var(--text-secondary)', marginBottom: '1rem' }}
      >
        YOUR ESTIMATED VALUE
      </motion.h2>
      
      <motion.div 
        initial={{ opacity: 0, scale: 0.5 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ delay: 0.4, type: "spring", stiffness: 100 }}
        style={{ fontSize: '5rem', fontWeight: 800, marginBottom: '4rem', letterSpacing: '-0.05em' }}
      >
        {formattedSalary}
      </motion.div>

      <motion.button 
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1 }}
        className="nav-btn secondary" 
        onClick={resetFlow} 
        style={{ margin: '0 auto' }}
      >
        &larr; Recalculate
      </motion.button>
    </motion.div>
  );
}
