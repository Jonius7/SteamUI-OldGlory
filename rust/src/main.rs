use std::fs;
use prettify_js::*;
use pyo3::prelude::*;

#[pyfunction]
fn beautify(filename) {
    let filename = "./chunk~2dcc5aaf7.js";
    let contents = fs::read_to_string(filename)
        .expect("Something went wrong reading the file");
    
    println!("Writing file...");
    let (pretty, _mappings) = prettyprint(&contents);
    
    fs::write("chunk~2dcc5aaf7.beaut.js", pretty).expect("Invalid file!");
    println!("File written"); 
}

#[pymodule]
fn js_beautify(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(beautify, m)?)?;
    Ok(())
}
