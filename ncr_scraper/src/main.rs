use rayon::prelude::*;
use serde::Deserialize;
use std::sync::Mutex;
use std::time::Duration;
use ureq::Agent;

#[derive(Debug, Deserialize, Clone)]
struct CreditProvider {
    #[serde(rename = "NCR Registration No")]
    ncr_number: String,
    #[serde(rename = "Full Name")]
    full_name: String,
    #[serde(rename = "Trading Name")]
    trading_name: String,
    #[serde(rename = "Legal Registration No")]
    legal_number: String,
    #[serde(rename = "Phone")]
    phone: String,
    #[serde(rename = "Fax")]
    fax: String,
    #[serde(rename = "Physical Address")]
    address: String,
    #[serde(rename = "Town")]
    town: String,
    #[serde(rename = "Final Registration Date")]
    reg_date: String,
    #[serde(rename = "Status")]
    status: String,
}

fn fetch_page(agent: &Agent, base_url: &str, page: usize) -> Vec<CreditProvider> {
    let url = format!("{}?page={}", base_url, page);
    
    match agent.get(&url).call() {
        Ok(response) => {
            let mut records = Vec::new();
            let html = response.into_string().unwrap_or_default();
            
            for line in html.lines() {
                if line.contains("NCRCP") {
                    if let Some(start) = line.find("NCRCP") {
                        let remaining = &line[start..];
                        if let Some(end) = remaining.find('<') {
                            let ncr = format!("NCRCP{}", &remaining[5..end]);
                            
                            let fields: Vec<&str> = line.split('<')
                                .filter(|s| !s.is_empty())
                                .collect();
                            
                            if fields.len() >= 10 {
                                records.push(CreditProvider {
                                    ncr_number: ncr,
                                    full_name: extract_td(&fields, 1),
                                    trading_name: extract_td(&fields, 2),
                                    legal_number: extract_td(&fields, 3),
                                    phone: extract_td(&fields, 4),
                                    fax: extract_td(&fields, 5),
                                    address: extract_td(&fields, 6),
                                    town: extract_td(&fields, 7),
                                    reg_date: extract_td(&fields, 8),
                                    status: extract_td(&fields, 9),
                                });
                            }
                        }
                    }
                }
            }
            records
        }
        Err(e) => {
            eprintln!("Error fetching page {}: {}", page, e);
            Vec::new()
        }
    }
}

fn extract_td(fields: &[&str], index: usize) -> String {
    let mut count = 0;
    for field in fields {
        if field.contains("<td") {
            if count == index {
                if let Some(start) = field.find('>') {
                    if let Some(end) = field[start+1..].find('<') {
                        return field[start+1..start+1+end].to_string();
                    }
                }
            }
            count += 1;
        }
    }
    String::new()
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    
    let (base_url, output_file, total_records) = match args.get(1).map(|s| s.as_str()) {
        Some("voluntary") => (
            "https://www.ncr.org.za/register_of_registrants/voluntary_cancel_cp.php",
            "ncr_voluntary_cp.csv",
            2510,
        ),
        Some("cancelled") => (
            "https://www.ncr.org.za/register_of_registrants/cancelled_by_tribunal_cp.php", 
            "ncr_cancelled_cp.csv",
            100,
        ),
        _ => (
            "https://www.ncr.org.za/register_of_registrants/registered_cp.php/registered_cp.php",
            "ncr_registered_cp.csv",
            9682,
        ),
    };
    
    println!("Scraping NCR Credit Providers: {}", base_url);
    
    let agent = ureq::AgentBuilder::new()
        .timeout(Duration::from_secs(30))
        .build();
    
    let pages_needed = (total_records / 10) + 1;
    
    println!("Fetching {} pages...", pages_needed);
    
    let all_records: Mutex<Vec<CreditProvider>> = Mutex::new(Vec::new());
    
    let pages: Vec<usize> = (1..=pages_needed).collect();
    
    pages.into_par_iter().for_each_with(agent, |agent, page| {
        std::thread::sleep(Duration::from_millis(50));
        
        let records = fetch_page(agent, base_url, page);
        
        if !records.is_empty() {
            let mut all = all_records.lock().unwrap();
            all.extend(records);
            
            if page % 100 == 0 {
                println!("Progress: {}/{}", page, pages_needed);
            }
        }
    });
    
    let mut unique: Vec<CreditProvider> = Vec::new();
    let mut seen = std::collections::HashSet::new();
    
    for cp in all_records.lock().unwrap().iter() {
        if seen.insert(cp.ncr_number.clone()) {
            unique.push(cp.clone());
        }
    }
    
    let mut wtr = csv::Writer::from_path(output_file).unwrap();
    wtr.write_record(&[
        "NCR Registration No", "Full Name", "Trading Name", 
        "Legal Registration No", "Phone", "Fax",
        "Physical Address", "Town", "Final Registration Date", "Status"
    ]).unwrap();
    
    for cp in &unique {
        wtr.serialize(cp).unwrap();
    }
    
    println!("\nTotal unique records: {}", unique.len());
    println!("Done! Output: {}", output_file);
}