#!/usr/bin/env python3
"""
Healthcare AI Agents Demo
Demonstrates the ROI and productivity benefits of AI agents in healthcare
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from analysis.ai_agents_roi_analyzer import AIAgentsROIAnalyzer
from analysis.healthcare_simulation import HealthcareSimulator

def create_healthcare_demo():
    print("🏥 Healthcare AI Agents ROI Demonstration")
    print("=" * 50)
    
    roi_analyzer = AIAgentsROIAnalyzer()
    healthcare_sim = HealthcareSimulator()
    
    hospital_params = {
        'name': 'Tokyo Metropolitan Hospital',
        'employees': 2500,
        'beds': 500,
        'annual_revenue': 15_000_000_000,  # 15B yen
        'annual_patients': 50000
    }
    
    print(f"\n📊 Analyzing: {hospital_params['name']}")
    print(f"• Employees: {hospital_params['employees']:,}")
    print(f"• Annual Revenue: ¥{hospital_params['annual_revenue']:,}")
    
    # Calculate ROI
    roi_results = roi_analyzer.calculate_roi_by_industry(
        'Healthcare', 
        hospital_params['employees'], 
        hospital_params['annual_revenue'] / 150
    )
    
    print(f"\n💰 Financial Analysis:")
    print(f"• 5-Year ROI: {roi_results['roi_percentage']:.1f}%")
    print(f"• Payback Period: {roi_results['payback_period_months']} months")
    
    # Run simulation
    simulation_results = healthcare_sim.run_comparative_simulation(days=30)
    analysis = healthcare_sim.analyze_results(simulation_results)
    
    improvements = analysis['improvements']
    print(f"\n📈 Simulation Results:")
    print(f"• Wait Time Reduction: {improvements['wait_time_reduction']:.1f}%")
    print(f"• Cost Reduction: {improvements['cost_reduction']:.1f}%")
    print(f"• Annual Savings: ¥{improvements['total_cost_savings'] * 365 / 30:,.0f}")
    
    return analysis

if __name__ == "__main__":
    create_healthcare_demo()
