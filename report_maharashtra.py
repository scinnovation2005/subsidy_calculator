# report_generator file
import pandas as pd
import os
import subprocess

def latex_escape(text):
    if text is None:
        return ""
    return str(text).replace('&', '\\&').replace('%', '\\%').replace('_', '\\_').replace('#', '\\#').replace('{', '\\{').replace('}', '\\}').replace('$', '\\$')

def generate_report_maharashtra(user_data, result, zone):
    output_dir = "reports"
    os.makedirs(output_dir, exist_ok=True)

    # A safe filename based on user's information
    safe_name = user_data.get("Organisation Name", "user").replace(" ", "_")
    safe_name1 = user_data.get("State", "user").replace(" ", "_")
    safe_name2 = user_data.get("Enterprise Size", "user").replace(" ", "_")
    filename = f"{safe_name}_{safe_name1}_{safe_name2}_Subsidy_Report.pdf"
    tex_filename = f"{safe_name}_{safe_name1}_{safe_name2}_Subsidy_Report.tex"

    tex_path = os.path.join(output_dir, tex_filename)
    pdf_path = os.path.join(output_dir, filename)

    tex_content = f"""
\\documentclass[11pt]{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage[T1]{{fontenc}}
\\usepackage{{geometry}}
\\geometry{{a4paper, margin=1in}}
\\usepackage{{array}}
\\usepackage{{longtable}}
\\usepackage{{enumitem}}
\\setlist[itemize]{{leftmargin=1.5em}}
\\usepackage{{graphicx}}

\\begin{{document}}

\\begin{{center}}
\\Huge\\textbf{{Subsidy4India, a venture of SCPL}}\\\\[0.5em]
\\large 305, Regent Chambers, Nariman Point, Mumbai 400021 (INDIA)\\\\
Offices in New Delhi \\& New York\\\\
\\end{{center}}

\\textbf{{Date: {pd.Timestamp.now().strftime('%d-%m-%Y')}}}

\\vspace{{1em}}
\\begin{{itemize}}
    \\textbf{{Organization:}} {latex_escape(user_data['Organization Name'])} \\\\
    \\textbf{{Location:}} {latex_escape(user_data['Subdistrict'])}, {latex_escape(user_data['District'])}, {latex_escape(user_data['State'])} \\\\
    \\textbf{{Attn.:}} {latex_escape(user_data['Name'])}
\\end{{itemize}}

\\section*{{Overview}}
Subsidy4India has identified various subsidies available for your organisation for your manufacturing unit in {latex_escape(user_data['District'])}, {latex_escape(user_data['Subdistrict'])} \\& {latex_escape(user_data['State'])} and sharing the evaluation report for your perusal which is located in Zone \\textbf{{{latex_escape(zone)}}}.
\\begin{{itemize}}

  \\item \\textbf{{Name of Scheme:}} Maharashtra Industrial Policy 2019
  \\item \\textbf{{Base of subsidy:}} Subsidy schemes applicable to your company as a MSME / Large / Mega entity
  \\item \\textbf{{Estimated subsidy value:}} Each subsidy has been mentioned in detail in the proposal.
  \\item \\textbf{{Date of start of commercial production:}} This framework aims to attract Rs. 5.4–5.9 lakh crore in industrial investment by 2028–29 while generating 20 lakh jobs. 
\\end{{itemize}}

\\section*{{Subsidy Breakdown}} 
\\begin{{itemize}}

    \\item \\textbf{{(a) Capital investment subsidy (One-time):}} Based on the Maharashtra Industrial Policy 2019 and Package Scheme of Incentives (PSI-2019), the Investment Promotion Subsidy (IPS) is the primary capital subsidy mechanism designed to reimburse State Goods and Services Tax (SGST) paid by eligible industrial units on their first sale of products within Maharashtra. \\\\
    \\item \\textbf{{(b) Stamp Duty Subsidy:}} The stamp duty exemption operates as a 100\\% waiver rather than a reimbursement, meaning eligible units are completely exempt from paying stamp duty during their investment period for specific transactions. \\\\
    \\item Exemption available only during the designated investment period (typically 3-5 years). \\\\
    \\item Exemption applies to initial transactions only, not subsequent transfers. \\\\
\\item \\textbf{{(c) Interest Subsidy (applicable only when a term loan is availed for the project):}} The Interest Subsidy under the Package Scheme of Incentives 2019 (PSI-2019) provides financial support by subsidizing interest paid on term loans for eligible industrial units with cap amount of electricity bills paid. \\\\
\\end{{itemize}}

\\section*{{Subsidy Snapshot}}

\\begin{{longtable}}{{|p{{4cm}}|p{{4cm}}|p{{4cm}}|p{{4cm}}|}}
\\hline
\\textbf{{Subsidy head}} & \\textbf{{Total subsidy}} & \\textbf{{No. of years}} & \\textbf{{Assumption}} \\\\
\\hline
Capital Investment Subsidy & Rs. {latex_escape(result['capital_investment_subsidy'])} & Disbursed over 7 years & One-time post production \\\\
\\hline
Interest subsidy & Rs. {latex_escape(result['interest_subsidy'])} & 7 years & Post production \\\\
\\hline
Stamp Duty Waiver & Rs. {latex_escape(result['stamp_duty_waive_off'])} & Waiver is not available for Zone A \\& B  & \\\\
\\hline 
SGST Reimbursement & Rs. {latex_escape(result['sgst_reimbursement'])} & Equally reimburse over 10 years & \\\\
\\hline
\\end{{longtable}}

\\textbf{{Total estimated subsidy available is Rs. {latex_escape(result['total_subsidy'])}.}}

\\section*{{Other Subsidies \\& Incentives}}
\\begin{{itemize}}
    \\item \\textbf{{1. Power Tariff Subsidy:}} Direct reduction in per-unit electricity charges for eligible manufacturing units.
        \\begin{{itemize}}
            \\item New MSME and LSI units (except those in category A areas)
            \\item Commencement of commercial production within the policy period
        \\end{{itemize}}

        \\textbf{{Type \\& Quantum of Benefit:}} 
        \\begin{{itemize}}
            \\item Rs.1/unit for 3 years in Vidarbha, Marathwada, North Maharashtra, Raigad, Ratnagiri, Sindhudurg
            \\item Rs. 0.50/unit for 3 years in other eligible areas (except A areas)
            \\item For certain sectors, benefit may extend up to 5 years
        \\end{{itemize}}

    \\item \\textbf{{2. Electricity Duty Exemption:}} Exemption from payment of electricity duty for eligible units.
        \\begin{{itemize}}
            \\item MSME and LSI units in all zones except A (with limited exceptions for A/B: only 100\\% EOUs, IT/BT manufacturing)
            \\item New units and eligible expansion/diversification projects
        \\end{{itemize}}

        \\textbf{{Type \\& Quantum of Benefit:}} 
        \\begin{{itemize}}
            \\item 100\\% exemption for 10-15 years (zone and sector dependent)
            \\item For A/B zones, 7 years for 100\\% EOUs, IT/BT manufacturing
        \\end{{itemize}}

    \\item \\textbf{{3. Green Industrialization Assistance:}} Financial support for investments in water, energy, and environmental conservation.
        \\begin{{itemize}}
            \\item MSME units undertaking projects for waste management, pollution control, health \\& safety, water harvesting, or captive renewable energy
        \\end{{itemize}}

        \\textbf{{Type \\& Quantum of Benefit:}} 
        \\begin{{itemize}}
            \\item Assistance for setting up ETPs, pollution control, water harvesting, and renewable energy systems
            \\item Budgetary support as per MPCB guidelines
        \\end{{itemize}}

    \\item \\textbf{{4. Employment Generation Incentives:}} Special incentives for projects generating direct employment, especially for local persons.
        \\begin{{itemize}}
            \\item New and expansion projects meeting minimum employment thresholds
            \\item CMEGP: Unemployed youth aged 18--45, setting up micro-enterprises
        \\end{{itemize}}

        \\textbf{{Type \\& Quantum of Benefit:}} 
        \\begin{{itemize}}
            \\item Grant-in-aid: 15--35\\% of project cost (CMEGP)
            \\item Priority in land allotment for projects with high local employment
            \\item Customized incentives for Mega/Ultra-Mega projects based on employment
        \\end{{itemize}}

    \\item \\textbf{{5. R\\&D and Incubation Support (Sector-Specific):}} Support for R\\&D, incubation, and innovation, especially in ESDM, biotechnology, and IT/BT sectors.
        \\begin{{itemize}}
            \\item Startups, R\\&D units, and incubators in notified sectors
        \\end{{itemize}}

        \\textbf{{Type \\& Quantum of Benefit:}} 
        \\begin{{itemize}}
            \\item Grants for R\\&D, incubation, and patent creation
            \\item Support for setting up incubation centers and innovation hubs
        \\end{{itemize}}
\\end{{itemize}}

\\section*{{Estimated Date of receipt:}} 
There will be a sanction provided for each of the subsidy 
application made which is sanctioned in upto 90 days and then disbursed as per funds 
availability with the Govt. Department and ranges from 3 months to 6 months from the 
date of sanction of the subsidy application. \\\\
In the case of SGST reimbursement, the company needs to file for the same every 
year post filing of annual GST return i.e. GSTR9 after which the SGST reimbursement 
is made ranging from 3 months to 6 months from the date of filing SGST 
reimbursement application.

\\section*{{How will SCPL ensure the subsidy gets into your bank account?}}
\\begin{{itemize}}
\\item SCPL will work with the client to ensure that the last rupee of subsidy is received in your 
bank account and the contract is valid till we achieve the same  
\\item If there is a delay in receipt of the subsidy amount due to operational reasons or budget 
allocation delay with the respective Govt. Department, SCPL will keep the client informed at 
every step
\\end{{itemize}}

\\section*{{Value Added Services}} 
\\begin{{itemize}}
\\item Preparation of Detailed Project Report (DPR)
\\item Market Research to plan your Go To Market Strategy
\\item DSIR (R\\&D certification) project for accessing R\\&D funding including grants from Govt. agencies
\\item Intellectual Property protection by filing patent, design registration, trademark and copyright in India and global jurisdictions
\\end{{itemize}}

\\section*{{Not sure?}} 
\\begin{{itemize}}
\\item Conduct a referral check by asking to get in touch with our happy customers
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
policy and non-cooperation by client
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
        print("PDF generation failed!")
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
        raise Exception("PDF generation error")

    return pdf_path
