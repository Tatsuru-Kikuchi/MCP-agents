# Healthcare AI Agents Simulation & Cost Analysis
# Generates synthetic healthcare data and demonstrates ROI potential

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import random
from dataclasses import dataclass
from typing import List, Dict
import warnings
warnings.filterwarnings('ignore')

@dataclass
class Patient:
    """Patient data structure for simulation."""
    id: str
    age: int
    condition: str
    severity: str
    arrival_time: datetime
    wait_time: float = 0
    treatment_duration: float = 0
    cost: float = 0
    ai_assisted: bool = False

class HealthcareSimulator:
    def __init__(self):
        """Initialize healthcare simulation parameters."""
        
        self.conditions = {
            'Routine Checkup': {'base_duration': 30, 'cost_base': 15000, 'complexity': 1},
            'Hypertension': {'base_duration': 45, 'cost_base': 25000, 'complexity': 2},
            'Diabetes': {'base_duration': 60, 'cost_base': 35000, 'complexity': 3},
            'Heart Disease': {'base_duration': 90, 'cost_base': 80000, 'complexity': 4},
            'Emergency': {'base_duration': 120, 'cost_base': 150000, 'complexity': 5}
        }
        
        self.age_weights = {
            (0, 18): 0.12,
            (19, 39): 0.23,
            (40, 64): 0.35,
            (65, 80): 0.22,
            (81, 100): 0.08
        }
        
        self.ai_improvements = {
            1: {'time_reduction': 0.25, 'cost_reduction': 0.15, 'error_reduction': 0.30},
            2: {'time_reduction': 0.35, 'cost_reduction': 0.20, 'error_reduction': 0.40},
            3: {'time_reduction': 0.40, 'cost_reduction': 0.25, 'error_reduction': 0.50},
            4: {'time_reduction': 0.45, 'cost_reduction': 0.30, 'error_reduction': 0.60},
            5: {'time_reduction': 0.30, 'cost_reduction': 0.20, 'error_reduction': 0.45}
        }

    def generate_patient(self, patient_id: str, timestamp: datetime, ai_enabled: bool = False) -> Patient:
        """Generate a synthetic patient with realistic characteristics."""
        
        age_range = np.random.choice(
            list(self.age_weights.keys()),
            p=list(self.age_weights.values())
        )
        age = np.random.randint(age_range[0], age_range[1] + 1)
        
        if age < 40:
            condition_probs = [0.5, 0.2, 0.1, 0.1, 0.1]
        elif age < 65:
            condition_probs = [0.3, 0.3, 0.2, 0.15, 0.05]
        else:
            condition_probs = [0.2, 0.25, 0.25, 0.25, 0.05]
        
        condition = np.random.choice(
            list(self.conditions.keys()),
            p=condition_probs
        )
        
        if condition == 'Emergency':
            severity = np.random.choice(['High', 'Critical'], p=[0.6, 0.4])
        else:
            severity = np.random.choice(['Low', 'Medium', 'High'], p=[0.5, 0.3, 0.2])
        
        base_duration = self.conditions[condition]['base_duration']
        base_cost = self.conditions[condition]['cost_base']
        complexity = self.conditions[condition]['complexity']
        
        age_multiplier = 1 + (age - 40) * 0.01 if age > 40 else 1
        severity_multiplier = {'Low': 0.8, 'Medium': 1.0, 'High': 1.3, 'Critical': 1.8}[severity]
        
        treatment_duration = base_duration * age_multiplier * severity_multiplier
        cost = base_cost * age_multiplier * severity_multiplier
        
        if ai_enabled:
            improvements = self.ai_improvements[complexity]
            treatment_duration *= (1 - improvements['time_reduction'])
            cost *= (1 - improvements['cost_reduction'])
        
        treatment_duration *= np.random.normal(1, 0.1)
        cost *= np.random.normal(1, 0.05)
        
        return Patient(
            id=patient_id,
            age=age,
            condition=condition,
            severity=severity,
            arrival_time=timestamp,
            treatment_duration=max(15, treatment_duration),
            cost=max(5000, cost),
            ai_assisted=ai_enabled
        )

    def simulate_hospital_day(self, date: datetime, ai_enabled: bool = False, num_patients: int = 200) -> List[Patient]:
        """Simulate a full day of hospital operations."""
        
        patients = []
        start_time = date.replace(hour=8, minute=0, second=0)
        
        for i in range(num_patients):
            hour_weights = [0.15, 0.18, 0.16, 0.14, 0.12, 0.10, 0.08, 0.05, 0.02]
            hour_offset = np.random.choice(range(10), p=hour_weights)
            minute_offset = np.random.randint(0, 60)
            
            arrival_time = start_time + timedelta(hours=hour_offset, minutes=minute_offset)
            
            patient = self.generate_patient(f"P{date.strftime('%Y%m%d')}_{i:03d}", arrival_time, ai_enabled)
            patients.append(patient)
        
        patients.sort(key=lambda p: p.arrival_time)
        
        current_time = start_time
        active_treatments = []
        
        for patient in patients:
            active_treatments = [t for t in active_treatments if t > patient.arrival_time]
            
            if len(active_treatments) > 10:
                patient.wait_time = (len(active_treatments) - 10) * 15
            else:
                patient.wait_time = max(0, np.random.normal(10, 5))
            
            if ai_enabled:
                patient.wait_time *= 0.6
            
            treatment_end = patient.arrival_time + timedelta(
                minutes=patient.wait_time + patient.treatment_duration
            )
            active_treatments.append(treatment_end)
        
        return patients

    def run_comparative_simulation(self, days: int = 30) -> Dict:
        """Run simulation comparing AI vs non-AI scenarios."""
        
        start_date = datetime(2025, 1, 1)
        
        traditional_results = []
        ai_results = []
        
        print(f"Running {days}-day hospital simulation...")
        
        for day in range(days):
            current_date = start_date + timedelta(days=day)
            
            traditional_patients = self.simulate_hospital_day(current_date, ai_enabled=False)
            traditional_results.extend(traditional_patients)
            
            ai_patients = self.simulate_hospital_day(current_date, ai_enabled=True)
            ai_results.extend(ai_patients)
            
            if (day + 1) % 10 == 0:
                print(f"Completed {day + 1} days...")
        
        return {
            'traditional': traditional_results,
            'ai_enabled': ai_results,
            'simulation_period': f"{days} days"
        }

    def analyze_results(self, simulation_results: Dict) -> Dict:
        """Analyze simulation results and calculate key metrics."""
        
        traditional = simulation_results['traditional']
        ai_enabled = simulation_results['ai_enabled']
        
        trad_df = pd.DataFrame([
            {
                'patient_id': p.id,
                'age': p.age,
                'condition': p.condition,
                'severity': p.severity,
                'wait_time': p.wait_time,
                'treatment_duration': p.treatment_duration,
                'total_time': p.wait_time + p.treatment_duration,
                'cost': p.cost,
                'scenario': 'Traditional'
            }
            for p in traditional
        ])
        
        ai_df = pd.DataFrame([
            {
                'patient_id': p.id,
                'age': p.age,
                'condition': p.condition,
                'severity': p.severity,
                'wait_time': p.wait_time,
                'treatment_duration': p.treatment_duration,
                'total_time': p.wait_time + p.treatment_duration,
                'cost': p.cost,
                'scenario': 'AI-Enabled'
            }
            for p in ai_enabled
        ])
        
        metrics = {
            'traditional': {
                'avg_wait_time': trad_df['wait_time'].mean(),
                'avg_treatment_time': trad_df['treatment_duration'].mean(),
                'avg_total_time': trad_df['total_time'].mean(),
                'avg_cost_per_patient': trad_df['cost'].mean(),
                'total_cost': trad_df['cost'].sum(),
                'total_patients': len(trad_df),
            },
            'ai_enabled': {
                'avg_wait_time': ai_df['wait_time'].mean(),
                'avg_treatment_time': ai_df['treatment_duration'].mean(),
                'avg_total_time': ai_df['total_time'].mean(),
                'avg_cost_per_patient': ai_df['cost'].mean(),
                'total_cost': ai_df['cost'].sum(),
                'total_patients': len(ai_df),
            }
        }
        
        improvements = {
            'wait_time_reduction': ((metrics['traditional']['avg_wait_time'] - 
                                   metrics['ai_enabled']['avg_wait_time']) / 
                                  metrics['traditional']['avg_wait_time']) * 100,
            'treatment_time_reduction': ((metrics['traditional']['avg_treatment_time'] - 
                                        metrics['ai_enabled']['avg_treatment_time']) / 
                                       metrics['traditional']['avg_treatment_time']) * 100,
            'cost_reduction': ((metrics['traditional']['avg_cost_per_patient'] - 
                              metrics['ai_enabled']['avg_cost_per_patient']) / 
                             metrics['traditional']['avg_cost_per_patient']) * 100,
            'total_cost_savings': metrics['traditional']['total_cost'] - metrics['ai_enabled']['total_cost']
        }
        
        return {
            'metrics': metrics,
            'improvements': improvements,
            'combined_data': pd.concat([trad_df, ai_df], ignore_index=True)
        }

def main():
    """Main function to run the healthcare simulation and analysis."""
    
    print("🏥 Healthcare AI Agents Simulation Starting...")
    print("=" * 60)
    
    simulator = HealthcareSimulator()
    
    print("Running 30-day comparative simulation...")
    results = simulator.run_comparative_simulation(days=30)
    
    print("\nAnalyzing results...")
    analysis = simulator.analyze_results(results)
    
    print("\n📊 KEY FINDINGS:")
    print("=" * 40)
    improvements = analysis['improvements']
    
    print(f"💰 Cost Reduction: {improvements['cost_reduction']:.1f}%")
    print(f"⏱️  Wait Time Reduction: {improvements['wait_time_reduction']:.1f}%")
    print(f"💵 Total Cost Savings (30 days): ¥{improvements['total_cost_savings']:,.0f}")
    print(f"📈 Annualized Savings: ¥{improvements['total_cost_savings'] * 365 / 30:,.0f}")
    
    annual_savings = improvements['total_cost_savings'] * 365 / 30
    implementation_cost = 250_000_000
    five_year_savings = annual_savings * 5 * 1.1
    roi_percentage = ((five_year_savings - implementation_cost) / implementation_cost) * 100
    
    print(f"\n🎯 5-YEAR ROI PROJECTION:")
    print(f"Implementation Cost: ¥{implementation_cost:,.0f}")
    print(f"5-Year Savings: ¥{five_year_savings:,.0f}")
    print(f"ROI: {roi_percentage:.0f}%")
    
    return analysis

if __name__ == "__main__":
    results = main()
    print("\n✅ Healthcare AI Agents simulation completed successfully!")