import pandas as pd
import subprocess
import os

def latex_escape(text):
    if text is None:
        return ""
    return str(text).replace('&', '\\&').replace('%', '\\%').replace('_', '\\_').replace('#', '\\#').replace('{', '\\{').replace('}', '\\}').replace('$', '\\$')

def generate_report_punjab(user_data, result):
    output_dir = "reports"
    os.makedirs(output_dir, exist_ok=True)

    # A safe filename based on user's information
    safe_name = latex_escape(user_data.get("Organization Name", "user")).replace(" ", "_")
    safe_name1 = latex_escape(user_data.get("State", "user")).replace(" ", "_")
    safe_name2 = latex_escape(user_data.get("Enterprise Size", "user")).replace(" ", "_")
    filename = f"{safe_name}_{safe_name1}_{safe_name2}_Subsidy_Report.pdf"
    tex_filename = f"{safe_name}_{safe_name1}_{safe_name2}_Subsidy_Report.tex"

    tex_path = os.path.join(output_dir, tex_filename)
    pdf_path = os.path.join(output_dir, filename)

    tex_content = f"""
\\documentclass[11pt]{{article}}
\\usepackage{{geometry}}
\\geometry{{a4paper, margin=1in}}
\\usepackage{{array}}
\\usepackage{{longtable}}
\\usepackage{{enumitem}}
\\setlist[itemize]{{leftmargin=1.5em}}
\\usepackage{{graphicx}}

\\begin{{document}}

\\begin{{flushright}}
\\includegraphics[width=3cm]{{S4I_logo.png}}
\\end{{flushright}}

\\begin{{center}}
\\Huge\\textbf{{Subsidy4India, a venture of SCPL}}\\\\[0.5em]
\\large 305, Regent Chambers, Nariman Point, Mumbai 400021 (INDIA)\\\\
Offices in New Delhi \\& New York \\\\
\\end{{center}}

\\textbf{{Date: {pd.Timestamp.now().strftime('%d-%m-%Y')}}}

\\vspace{{1em}}

\\begin{{itemize}}
  \\item {latex_escape(user_data['Organization Name'])}
  \\item {latex_escape(user_data['District'])}, {latex_escape(user_data['State'])}
  \\item \\textbf{{Attn.:}} {latex_escape(user_data['Name'])}
\\end{{itemize}}

\\section*{{Overview}}
Subsidy4India has identified various subsidies available for your Organization for your manufacturing unit in {latex_escape(user_data['District'])}, {latex_escape(user_data['State'])}.

\\begin{{itemize}}
  \\item \\textbf{{Name of Scheme:}} Punjab Industrial and Business Development Policy 2022
  \\item \\textbf{{Base of subsidy:}} Subsidy schemes applicable to your company as a MSME / Large / Mega entity
  \\item \\textbf{{Estimated subsidy value:}} Each subsidy has been mentioned in detail in the proposal.
  \\item \\textbf{{Date of start of commercial production:}} Within the policy period.
\\end{{itemize}}

\\section*{{Subsidy Breakdown}}
\\begin{{itemize}}
  \\item \\textbf{{Capital investment subsidy (One-time):}} Based on Fixed Capital Investment and scheme parameters.
  \\item \\textbf{{Stamp Duty exemption / reimbursement:}} 100\\% exemption/reimbursement on eligible transactions.
  \\item \\textbf{{Interest subsidy:}} Applicable based on enterprise type and location. For Startups interest subsidy is available at 8\\% interest rate on term loan amount
  \\item \\textbf{{SGST reimbursement:}} Calculated on capital investment made.
\\end{{itemize}}

\\section*{{Subsidy Snapshot}}
\\begin{{longtable}}{{|p{{4cm}}|p{{4cm}}|p{{4cm}}|p{{4cm}}|}}
\\hline
\\textbf{{Subsidy head}} & \\textbf{{Total subsidy}} & \\textbf{{No. of years}} & \\textbf{{Assumption}} \\\\
\\hline
Capital Investment Subsidy & Rs. {latex_escape(result['capital_investment_subsidy'])} & One time & Post production \\\\
\\hline
Interest subsidy & Rs. {latex_escape(result['interest_subsidy'])} & 3 years & With cap of Rs. 10 Lakhs \\\\
\\hline
Stamp Duty Subsidy & Rs. {latex_escape(result['stamp_duty_subsidy'])} & One time & Post production \\\\
\\hline
SGST Reimbursement & Rs. {latex_escape(result['sgst_reimbursement'])} & 5 years & Post production \\\\
\\hline
\\end{{longtable}}

\\textbf{{Total estimated subsidy available is Rs. {latex_escape(result['total_subsidy'])}.}}

\\section*{{Other Key Subsidies and Incentives}}

\\begin{{itemize}}

  \\item \\textbf{{Electricity Duty (ED) Exemption:}} Up to 100\\% exemption for eligible units for 10–15 years based on location and size.

  \\item \\textbf{{Property Tax Exemption:}} Full waiver for 5–10 years. Application via Form-PT on Invest Punjab portal.

  \\item \\textbf{{Employment Generation Subsidy:}} Rs. 36,000/year per male, Rs. 48,000/year per female/SC/BC/OBC employee for up to 5 years.

  \\item \\textbf{{Marketing and Vendor Development Support:}} 50\\% (up to Rs.10L) for international, 25\\% (up to Rs.3L) for domestic fairs; Rs. 5Cr support for MSME cluster events.

  \\item \\textbf{{Non-Fiscal Incentives:}} PAPRA exemption, liberal FAR, flatted factories for MSMEs.

  \\item \\textbf{{Sector-Specific Incentives:}} e.g., 100\\% tax reimbursement for food processing units, Rs.10Cr top-up under M-SIPS for electronics.

\\end{{itemize}}

\\section*{{Estimated Disbursement Timeline}}
\\begin{{itemize}}
  \\item There will be a sanction provided for each of the subsidy 
  application made which is sanctioned in upto 90 days and then disbursed as per funds 
  availability with the Govt. Department and ranges from 3 months to 6 months from the 
  date of sanction of the subsidy application.
  \\item In the case of SGST reimbursement, the company needs to file for the same every 
  year post filing of annual GST return i.e. GSTR9 after which the SGST reimbursement 
  is made ranging from 3 months to 6 months from the date of filing SGST 
  reimbursement application. 
\\end{{itemize}}

\\section*{{How SCPL Helps}}

\\begin{{itemize}}
  \\item SCPL will work with the client to ensure that the last rupee of subsidy is received in your 
    bank account and the contract is valid till we achieve the same.  
  \\item If there is a delay in receipt of the subsidy amount due to operational reasons or budget 
    allocation delay with the respective Govt. Department, SCPL will keep the client informed at every step.
\\end{{itemize}}

\\section*{{Value Added Services}}
\\begin{{itemize}}
  \\item DPR preparation
  \\item Market research
  \\item DSIR (R\\&D certification) grant support
  \\item IP protection: patents, trademarks, copyrights
\\end{{itemize}}

\\section*{{Not Sure?}}
\\begin{{itemize}}
  \\item Ask for references from our happy customers.
\\end{{itemize}}

\\section*{{Disclosure}}
\\begin{{itemize}}
  \\item SCPL (parent company of Subsidy4India) Team has calculated the subsidy based on 
    details provided by the client and the same can vary depending on the capital investment 
    made by the client, exact location of the land where the manufacturing unit is being 
    setup, documents provided for registering the subsidy application and any follow up 
    documents required by the Central or State Government authorities and will not be liable 
    for any reduction in subsidy amount applicable to the client including the client being 
    determined as non-eligible to avail the subsidy due to lack of documentation, change of 
    policy and non-cooperation by client.
\\end{{itemize}}

\\end{{document}}
"""

    with open(tex_path, "w", encoding="utf-8") as f:
        f.write(tex_content)

    result = subprocess.run(
        ["pdflatex", "-interaction=nonstopmode", "-output-directory", output_dir, tex_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if result.returncode != 0:
        log_file = os.path.join(output_dir, "pdflatex_error.log")
        with open(log_file, "w") as f:
            f.write("STDOUT:\n" + result.stdout + "\n\nSTDERR:\n" + result.stderr)
        raise Exception(f"PDF generation failed. Details saved to {log_file}")

    return pdf_path
