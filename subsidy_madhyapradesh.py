from report_madhyapradesh import generate_report_mp
import os

# No zonification in Madhyapradesh
# interest rate is new input 

# Calculation logic
def calculate_subsidy(plant_machinery, building_civil_work,
                      term_loan_amount = 0, interest_rate = 0):

    capital_investment = plant_machinery + building_civil_work

    capital_subsidy = 0 
    interest_subsidy = 0 

    # Capital Subsidy depends on Eligible Fixed Capital Investment(EFCI)
    if capital_investment<=300000000:
        capital_subsidy= min(0.40 * capital_investment, 120000000)
    elif 300000000 <= capital_investment<= 500000000:
        capital_subsidy= min(0.40 * capital_investment, 200000000)
    elif 500000000 <= capital_investment<= 1000000000:
        capital_subsidy= min(0.27 * capital_investment, 270000000)
    elif 1000000000<= capital_investment<=5000000000:
        capital_subsidy= min(0.15 * capital_investment, 750000000)
    elif 5000000000<= capital_investment<=10000000000:
        capital_subsidy= min(0.13 * capital_investment, 1300000000)
    elif 10000000000<= capital_investment<=20000000000:
        capital_subsidy= min(0.10 * capital_investment, 2000000000)
    else:
        capital_subsidy = 2000000000

    # No Stamp Duty Subsidy in Madhyapradesh

    # Interest Subsidy
    annual_interest = term_loan_amount * 0.06 * 7
    interest_paid =  interest_rate * term_loan_amount * 7
    interest_subsidy = min(annual_interest, interest_paid, 100000000) #max 10 crore

    # Total subsidy 
    total_subsidy = capital_subsidy + interest_subsidy
    
    return {
        "capital_investment_subsidy": round(capital_subsidy, 2),
        "interest_subsidy": round(interest_subsidy, 2),
        "total_subsidy": round(total_subsidy, 2)
    }    

def process_madhyapradesh(data):
    try:
        # Extract values
        plant_machinery = float(data["Plant and Machinery Investment"])
        building_civil_work = float(data["Building and Civil Work Investment"])
        term_loan_amount = float(data.get("Term Loan Amount", 0))
        interest_rate = float(data.get("Interest Rate", 0))
    
        # Perform calculations
        result = calculate_subsidy(
            plant_machinery,
            building_civil_work,
            term_loan_amount,
            interest_rate
        )

        # Generate report
        pdf_path = generate_report_mp(data, result)
        filename = os.path.basename(pdf_path)

        print('PDF link', pdf_path)
        
        return {
            "subsidy_result": result,
            "report_path": f"/download_pdf/{filename}"
        }

    except Exception as e: 
        print("Error:", str(e))
        return {
            "error": f"Error processing Madhyapradesh subsidy: {str(e)}"
        }