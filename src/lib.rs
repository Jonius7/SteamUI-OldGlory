use std::fs;
use prettify_js::*;
use pyo3::prelude::*;

#[pyfunction]
fn beautify(filename: &str) {
    //let filename = "./chunk~2dcc5aaf7.js";
    let contents = fs::read_to_string(filename)
        .expect("Something went wrong reading the file");
    
    println!("Writing file...");
    let (pretty, _mappings) = prettyprint(&contents);
    
    let beaut_filename = get_beaut_filename(filename);
    fs::write(beaut_filename, pretty).expect("Invalid file!");
    //println!("{}", get_beaut_filename("chunk~2dcc5aaf7.js"));
    println!("File written"); 
}

fn get_beaut_filename(filename: &str) -> String{
    let beaut_filename = filename.split(".");
    let mut index = 0;
    let mut beaut_pre = "";
    let mut beaut_suf = "";
    for name_part in beaut_filename {
        //println!("{}", name_part);
        if index == 0 {
            beaut_pre = name_part;
        } else if index == 1 {
            beaut_suf = name_part;
        }
        index +=1;
    }
    return [beaut_pre, ".beaut.", beaut_suf].join("")
}

#[pymodule]
fn js_beautify(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(beautify, m)?)?;
    Ok(())
}
