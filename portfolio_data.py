"""
portfolio_data.py - Deterministic Portfolio Engine for Groww Perspective MVP
Provides realistic beginner portfolio scenarios, historical ledger transactions,
and verified arithmetic metrics for LLM contextualization.
"""

SCENARIOS = {
    "scenario_a": {
        "id": "scenario_a",
        "name": "Month 3: Market Dip / The Churn Cliff (High Anxiety)",
        "user_profile": {
            "name": "Sushant K.",
            "age": 27,
            "monthly_sip": 3000,
            "fund_name": "Parag Parikh Flexi Cap Fund - Direct Growth",
            "start_date": "August 2026",
            "current_month": "October 2026 (Month 3)",
            "goal": "Long-term Wealth Building (10-Year Horizon)",
        },
        "metrics": {
            "total_invested": 9000.0,
            "current_value": 8480.0,
            "total_return_inr": -520.0,
            "total_return_pct": -5.78,
            "one_day_return_inr": -145.0,
            "one_day_return_pct": -1.68,
            "xirr_pct": -14.2,  # Short-term annualized noise
            "total_units": 222.42,
            "current_nav": 38.12,
            "average_nav_cost": 40.46,
            "previous_average_nav": 41.65,
            "cost_basis_reduction_pct": 2.85,
            "units_bought_this_month": 78.70,
            "units_bought_last_month": 72.15,
            "additional_units_this_month": 6.55,
            "completed_instalments": 3,
            "target_instalments": 12,
            "streak_pct": 25.0,
            "market_condition": "Nifty corrected -3.2% this month due to global macroeconomic volatility."
        },
        "ledger": [
            {"month": "Month 1 (Aug)", "amount": 3000, "nav": 42.10, "units": 71.26, "running_units": 71.26},
            {"month": "Month 2 (Sep)", "amount": 3000, "nav": 41.58, "units": 72.15, "running_units": 143.41},
            {"month": "Month 3 (Oct)", "amount": 3000, "nav": 38.12, "units": 78.70, "running_units": 222.11},
        ],
        "status": "DIP_ACCUMULATION"
    },
    "scenario_b": {
        "id": "scenario_b",
        "name": "Month 5: Flat / Negligible Returns (Disillusionment)",
        "user_profile": {
            "name": "Bijoy R.",
            "age": 38,
            "monthly_sip": 5000,
            "fund_name": "Mirae Asset Large Cap Fund - Direct Growth",
            "start_date": "June 2026",
            "current_month": "October 2026 (Month 5)",
            "goal": "Retirement Corpus & Child Education",
        },
        "metrics": {
            "total_invested": 25000.0,
            "current_value": 25180.0,
            "total_return_inr": 180.0,
            "total_return_pct": 0.72,
            "one_day_return_inr": 35.0,
            "one_day_return_pct": 0.14,
            "xirr_pct": 1.15,
            "total_units": 268.45,
            "current_nav": 93.80,
            "average_nav_cost": 93.12,
            "previous_average_nav": 93.25,
            "cost_basis_reduction_pct": 0.14,
            "units_bought_this_month": 53.30,
            "units_bought_last_month": 53.10,
            "additional_units_this_month": 0.20,
            "completed_instalments": 5,
            "target_instalments": 12,
            "streak_pct": 41.6,
            "market_condition": "Broad indices trading in a tight, sideways range for the past 4 months."
        },
        "ledger": [
            {"month": "Month 1 (Jun)", "amount": 5000, "nav": 92.50, "units": 54.05, "running_units": 54.05},
            {"month": "Month 2 (Jul)", "amount": 5000, "nav": 93.10, "units": 53.70, "running_units": 107.75},
            {"month": "Month 3 (Aug)", "amount": 5000, "nav": 94.20, "units": 53.07, "running_units": 160.82},
            {"month": "Month 4 (Sep)", "amount": 5000, "nav": 94.15, "units": 53.10, "running_units": 213.92},
            {"month": "Month 5 (Oct)", "amount": 5000, "nav": 93.80, "units": 53.30, "running_units": 267.22},
        ],
        "status": "SIDEWAYS_DISCIPLINE"
    },
    "scenario_c": {
        "id": "scenario_c",
        "name": "Month 1: The First Deduction (Curious Beginner)",
        "user_profile": {
            "name": "Pradeep N.",
            "age": 25,
            "monthly_sip": 2000,
            "fund_name": "Nifty 50 Index Fund - Direct Growth",
            "start_date": "October 2026",
            "current_month": "October 2026 (Month 1)",
            "goal": "First Time Wealth Creation Habit",
        },
        "metrics": {
            "total_invested": 2000.0,
            "current_value": 2012.0,
            "total_return_inr": 12.0,
            "total_return_pct": 0.60,
            "one_day_return_inr": 8.0,
            "one_day_return_pct": 0.40,
            "xirr_pct": 0.0,  # XIRR is mathematically undefined/inapplicable on Day 1
            "total_units": 47.05,
            "current_nav": 42.76,
            "average_nav_cost": 42.50,
            "previous_average_nav": 42.50,
            "cost_basis_reduction_pct": 0.0,
            "units_bought_this_month": 47.05,
            "units_bought_last_month": 0.0,
            "additional_units_this_month": 47.05,
            "completed_instalments": 1,
            "target_instalments": 12,
            "streak_pct": 8.3,
            "market_condition": "Standard market trading following monthly SIP execution."
        },
        "ledger": [
            {"month": "Month 1 (Oct)", "amount": 2000, "nav": 42.50, "units": 47.05, "running_units": 47.05},
        ],
        "status": "FIRST_MILESTONE"
    }
}

def get_scenario(scenario_id: str):
    return SCENARIOS.get(scenario_id, SCENARIOS["scenario_a"])
